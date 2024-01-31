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

    def saveboard(self, sessionid, board, player=None):
        # print(f'+++SAVEBOARD---')
        self.dbsessionid = sessionid
        self.boardstate = json.dumps(board)  ####      STORE BOARD AS A STRING
        if player is not None:
            self.player = json.dumps(player)
        ####      COMMIT THE CHANGES TO THE DATABASE
        db.session.commit()
        return board


    def getboard(self, sessionid):
        # print(f'+++GETBOARD---')
        db_row = Gamedb.query.filter_by(dbsessionid=sessionid).first()
        if db_row:
            print(f'---db_row found= {db_row}')
            return json.loads(db_row.boardstate)
        else:
            print('+++getboard: no db_row in db---')
            return None

    def __repr__(self):

        return f"<Gamedb(dbid={self.dbid}, dbsessionid={self.dbsessionid}, boardstate={self.boardstate}, player={self.player})>"

with app.app_context():
    db.create_all()

def checkfordbrow(sessionid):
    db_row = Gamedb.query.filter_by(dbsessionid=sessionid).first()
    if db_row:
        print(f'+++db_row found= {db_row}')
        return True
    else:
        print('+++getboard: no db_row in db---')
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
    print(f'---sessionid={sessionid}')
    # render page with size of board variable
    return render_template('index.html')

@app.route('/play', methods=['POST', 'GET'])
def play():
    print('>>>PLAY ROUTE GET')

    EMPTY = '*'
    BLACK = 'BLACK'
    WHITE = 'WHITE'
    human = BLACK

    ####      GET SESSION ID
    sessionid = session.get('sessionid')

    ####      CREATE GAME INSTANCE
    game = othello.Othello(4)
     ####    CREATE NEW ROW INSTANCE
    db_row = Gamedb(dbsessionid=sessionid, boardstate=json.dumps(board), player=json.dumps(player), human=json.dumps(human))
    db.session.add(db_row)
    #########      POST     #########
    if request.method == 'POST':
        print('>>>PLAY ROUTE POST')

        ####    print all json
        print(f"\n--- request.json= {request.json} ---") 

        ####     CHECK IF NEW GAME + INITIALISE
        if request.json.get('newgame') == True:
            print('--- NEW GAME ---')
            ####   RESET BOARD
            board = game.create_board()
            print(f'---board initialised--{board}-')
            human = request.json.get('human')    
            print(f'---player= {human}---')
            player = human # always black 1st move
            


            #  if human is black send blacks valid moves
            if human == BLACK:
                print('---human = BLACK')
                board = game.boardforresponse(board)
                print(f'---board={board}')
                player = BLACK
           
        
            if human == None: # just for print!!!
                print('---sending init board')
                player = None
            else :
                #  return the initialised board
                print(f'---returning board full= {board}--')
            print(f'---player={player}')

            return jsonify({'newgame': True,'board': board, 'player': player})

        #   IF NOT A NEW GAME
        else :
            #### GET BOARD FROM DB
            board = db_row.getboard(sessionid)
            print(f"+++ board retrieved hm= {board}")
            ####     HUMAN MOVE
        
            humanmove = request.json.get('humanmove')
            print(f"--- humanMove received: {humanmove}{type(humanmove)}---")
            humanmovetuple = tuple(int(char) for char in humanmove)
            print(f"--- movetuple= {humanmovetuple} ")

            # update board with human move
            player = human
            board = move(humanmove, board, player)
            aimove = False
            # if messgae is getaimove
            if request.json.get('message') == "getaimove":
                player = ai
                aimovecalc = ai.getmove(board)
                board = move(aimove, board, player )
                # update board with ai move
                aimove = True
            saveboard(sessionid, board, player)
                # if not  win
            if not game.gameover():
                 # add valid moves
                board = game.boardforresponse(board)
            else:
                winner = game.calc_winner()
            
            # return json with board
            return jsonify({'gameover': winner, 'aimove': aimove, 'board': board})
        
 

if __name__ == '__main__':
    app.run()