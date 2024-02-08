from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
import sys
import time
import json
import uuid
import os

import othello as othello

app = Flask(__name__, static_folder='../sharedstatic')
app.secret_key = "supermofustrongpword"

aiplayer = othello.OthelloAI()

####      CONFIGURE PROXYFIX WITH THE CORRECT PARAMETERS
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

####      CONFIG DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_ECHO'] = True

####      SET THE APP TO DEBUG MODE
environment = os.environ.get('FLASK_ENV', 'production')
app.config['ENV'] = environment
if environment == 'development':
    app.config['DEBUG'] = True
else:
    app.config['DEBUG'] = False
# app.debug = False

####      GAMEDB IS ACTUALLY A ROW IN THE DATABASE ? TODO CHANGE NAME
class Gamedb(db.Model):
    dbid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dbsessionid = db.Column(db.String, nullable=False)
    boardstate = db.Column(db.String, nullable=False)
    player = db.Column(db.String, nullable=False)
    human = db.Column(db.String, nullable=False)

    def saveboard(self, sessionid, board, player, human):
        # print(f'+++SAVEBOARD---')
        self.dbsessionid = sessionid
        self.boardstate = json.dumps(board)  ####      STORE BOARD AS A STRING
        self.player = json.dumps(player)
        self.human = json.dumps(human)
        ####      COMMIT THE CHANGES TO THE DATABASE
        db.session.commit()
        # print(f'---db_row saved= {self}')
        return board


    def getboard(self, sessionid):
        # print(f'+++GETBOARD---')
        db_row = Gamedb.query.filter_by(dbsessionid=sessionid).first()
        if db_row:
            # print(f'---db_row found= {db_row}')
            return json.loads(db_row.boardstate)
        else:
            # print('+++getboard: no db_row in db---')
            return None

    def __repr__(self):

        return f"<Gamedb(dbid={self.dbid}, dbsessionid={self.dbsessionid}, boardstate={self.boardstate}, player={self.player}, human={self.human})>"

with app.app_context():
    db.create_all()

def checkfordbrow(sessionid):
    db_row = Gamedb.query.filter_by(dbsessionid=sessionid).first()
    if db_row:
        # print(f'+++db_row found= {db_row}')
        return True
    else:
        print('+++checkfordbrow: no db_row in db---')
        return False

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


    ######  ROUTES  ######

@app.route('/', methods=['GET'])
def index():
    print('>>>INDEX ROUTE GET')
    ####       IF NO SESSIONID, CREATE ONE
    sessionid = session.get('sessionid')
    if not sessionid:
        print('---no sessionid in session---')
        session['sessionid'] = str(uuid.uuid4())
        sessionid = session['sessionid']
    # print(f'---sessionid={sessionid}')
    game = othello.Othello()
    size = game.size
    # render page with size of board variable
    return render_template('index.html', size=size)



@app.route('/play', methods=['POST', 'GET'])
def play():
    print('>>>PLAY ROUTE GET')

    EMPTY = 0
    BLACK = 1
    WHITE = -1
    winner = None
    print(f'winner= {winner}')

    ####      GET SESSION ID
    sessionid = session.get('sessionid')
    print(f'---sessionid={sessionid}')

    ####      CREATE GAME INSTANCE
    game = othello.Othello()
    
    ####      GET THE DB ROW
    db_row = Gamedb.query.filter_by(dbsessionid=sessionid).first()
    if not db_row:
        print('---no db_row in db---')
    # else:
        # print(f'---db_row found= ')
       
   
    #########      POST     #########
    if request.method == 'POST':
        # print('>>>PLAY ROUTE POST')

        ####    PRINT ALL JSON
        print(f"\n--- request.json= {request.json} ---") 

        ####    GET VARIABLES FROM JSON
        player = request.json.get('player')
        if player:
            player = int(player)
        human = request.json.get('human')
        if human:
            human = int(human)
        humanmove = request.json.get('humanmove')
        if human == 1:
            ai = -1
        else:
            ai = 1
        print(f"---human= {human}, ai= {ai}---")

        ####     CHECK IF NEW GAME + INITIALISE
        if request.json.get('newgame') == True:
            assert request.json.get('humanmove') != True

            ####   RESET BOARD
            board = game.create_board()
            # print(f'---board initialised--{board}-')
            # print(f'---player= {human}---')
            # print(f'\n*******player= {player}---')

            ####    CREATE NEW ROW INSTANCE
            if not db_row:
                # print('---making new db_row--- ')
                db_row = Gamedb(
                        dbsessionid=sessionid,
                        boardstate=json.dumps(board),
                        player=json.dumps(player),
                        human=json.dumps(human)
                    )
                db.session.add(db_row)

            ####    SAVE INIT BOARD TO DB
            print(f'---board to be saved= {board}')
            db_row.saveboard(sessionid, board, player, human)
            # print(f'---new db_row saved= {db_row}')

            ####  IF HUMAN IS BLACK RETURN VALID MOVES
            print(f'---human= {human}, type= {type(human)}---')
            print(f'---human == 1? {human == 1}---')
            if human == 1:
                print(f'---HUMAN IS BLACK SO GET AVAIL BOARD:',{human})
                board = game.boardwithavails(board, human)
                # print(f'---response board board={board}')
                player = 1 # DELET THIS?
        
            if human != -1:
            #### IF HUMAN IS NULL JUST SEND INITIAL BOARD
                responsevars = {'newgame': True, 'player': player, 'board': board}
                print(f'---First responsevars= {responsevars}')
                return jsonify({'newgame': True,'board': board, 'player': player})

        #    NOT A NEW GAME

        print('||| AFTER NEWGAME CONDITION')
        #### GET BOARD FROM DB
        board = db_row.getboard(sessionid)
        print(f"board retrieved1 = {board}")
    
        humanmove = request.json.get('humanmove')
        
        if humanmove: # ONLY SENT ONCE AFTER MOVE TO GET UPDATED BOARD
            print(f'---IN "IF HUMANMOVE"---')
            #### MEANS WE ONLY WANT BOARD WITH FLIPS
            humanmovetuple = tuple(int(char) for char in humanmove)

            ####    UPDATE BOARD WITH HUMAN MOVE
            board = game.move(board, humanmovetuple,  player)
            
            print(f"--- board with human move flips = {board} ")
            #### NOW JUST SEND THE BOARD - GOTO RESPONSE
            player = game.switchplayer(player)
        
        else :
            ####             AI MOVE

            print(f'----GET AI MOVE. NO HUMANMOVE...HUMANMOVE WAS SAVED IN LAST REQUEST---')
            print(f"---player AI? {player}---")
            ####  CHECK FOR MOVES AVAILABLE FOR AI
            if  game.available_actions(board, player):
                print(f'---AI MOVES AVAILABLE---')
                print(f'---ai avail actions= {game.available_actions(board, player)}')  

                '''
                AI MOVE

                aimove = AI.choose_action(board, player, epsilon=False)
                '''
                # inputmove = input('enter ai move: ')
                # aimove = tuple(int(char) for char in inputmove)
                aimove = aiplayer.choose_q_action(board, player, game, epsilon=False)
                print(f'---ai move= {aimove}')


                #### MAKE AI MOVE
                game.move( board, aimove[0], player )

                ####  SAVE BOARD    
                print(f'---board + ai move TO SAVE={board}---')
                db_row.saveboard(sessionid, board, player, human)

            else:
                print(f'---NO VALID MOVES FOR AI, SO CHECK HUMAN---')
                player = human
                board = game.boardwithavails(board, human)
                # CHECK HUMAN HAS MOVES - IF NOT GAME OVER 
                humanavails = game.available_actions(board, player)
                print(f'---avail moves hum={humanavails}')  
                if not   game.available_actions(board, player):
                    print(f'no human avails?={humanavails}. GAMEOVER')
                    winner = game.calc_winner(board)
                print(f'---response vars no ai moves: gameover={winner},player={player}, board={board}')
                return jsonify({'gameover':winner, 'player': player, 'board': board})
            # print(f'---board after ai move {board}---')
            #### NOW ITS HUMANS TURN: SWITCH PLAYER
            player = human

            ####    CHECK IF GAME OVER
            
            if game.gameover(board):
                print('---GAME OVER---')
                winner = game.calc_winner(board) 
                print(f'---winner= {winner}')
        
        print(f'---player to be returned= {player}')

        ###   SAVE BOARD

        print(f'---board to be saved= {board}')
        db_row.saveboard(sessionid, board, player, human)

        if player == human:

            ####   ADD VALID MOVES

            # Ai HAS MOVED - CHECK IF HUMAN CAN MOVE.
            print(f'----avail moves={game.available_actions(board, player)}')
            if not game.available_actions(board, player):
                print(f'---NO VALID MOVES FOR HUMAN---')
                # IF NOT, PLAYER = AI
                player = ai
            else:
                print(f'---adding valid moves to board')
                board = game.boardwithavails(board, human)
        if winner:
            print(f'---q table = {aiplayer.q}')
        ####  PREPARE RESPONSE
        responsedict = {'gameover': winner, 'player': player, 'board': board}
        print(f'---response normal  {responsedict}')
        # return json with board
        return jsonify({'gameover': winner, 'player': player, 'board': board})
    
 

if __name__ == '__main__':
    app.run()