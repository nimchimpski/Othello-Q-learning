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
        print(f'---db_row found= {db_row}')
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

    size = 4
        
   
    return render_template('index.html', size=size)

# @app.route('/play', methods=['POST', 'GET'])
# def play():
#     print('>>>PLAY ROUTE GET')

#     BLACK = 'BLACK'
#     WHITE = 'WHITE'
#     human = BLACK

#     ####      GET SESSION ID
#     sessionid = session.get('sessionid')

#     ####      CREATE GAME INSTANCE
#     game = othello.Othello(4)
#     size = game.size
#     print(f'---size = {size}')

#     ####      CREATE INITIAL BOARD
#     board = game.create_board()
#     print(f'---board initialised--{board}-')

#     player = BLACK

#     ####            iIF NO DB ROW CREATE ONE
#     db_row = Gamedb.query.filter_by(dbsessionid=sessionid).first()
#     if db_row == None:
#         print(f'---no db_row= {db_row}')
#         ####    CREATE NEW ROW IN DB
#         db_row = Gamedb(dbsessionid=sessionid, boardstate=json.dumps(board), player=json.dumps(player), human=json.dumps(human))
#         db.session.add(db_row)
#     #### SAVE BOARD IN DB
#     db_row.saveboard(sessionid, board, player)

#     ####    RENDER TEMPLATE AND SEND BOARD AS JINJA VARIABLE
#     return render_template('index.html', board=board, player=player, size=size)

    



    # #########      POST     #########
    # if request.method == 'POST':
    #     print('>>>PLAY ROUTE POST')

    #     ####    print all json
    #     # print(f"\n--- request.json= {request.json} ---") 

    #     ####     CHECK IF NEW GAME + INITIALISE
    #     if request.json.get('newgame') == True:
    #         print('--- NEW GAME ---')

    #         ####   RESET BOARD
    #         board = othello.create_board()
    #         print(f'---board initialised--{board}-')
    #         #### iF NO ROW IN DB FOR THIS SESSIONID, CREATE ONE
    #         print('---queried db_row---')
    #         print(f'---existing db_row= {db_row}')
    #         if not db_row:
    #             print('---MAKING NEW db_row---')
    #             ####.   CREATE NEW ROW IN DB    
    #             db_row = Gamedb(dbsessionid=sessionid, boardstate=json.dumps(board), player=json.dumps(player))
    #             db.session.add(db_row)
    #         # INITIALISE BOARD IN DATABASE
    #         db_row.saveboard(sessionid, board, player)
    #         print(f'---db_row= {db_row}')
    #         print(f'---initialised board saved---{db_row}')

    #     ####     HUMAN MOVE
    #     humanmove = request.json.get('humanmove')
    #     if humanmove != None:
    #         humanmove = request.json.get('humanmove')
    #         human = request.json.get('human')
    #         # print(f"--- humanMove received: {humanmove}{type(humanmove)}---")
    #         humanmovetuple = tuple(int(char) for char in humanmove)
    #         # print(f"--- movetuple= {humanmovetuple} ---")
    #         #### GET BOARD FROM DB
    #         board = db_row.getboard(sessionid)
    #         # print(f"+++ board retrieved hm= {board} ---")

    #         ####  UPDATE BOARD WITH HUMAN MOVE  ####
    #         availactions = game.available_actions()
    #         board = game.move(move, availactions)
    #         # print(f"--- board after human mv= {board} ---")

    #         ####   CHECK FOR GAME OVER
    #         if game.gameover():
    #             gameover = True
    #             winner = game.calc_winner()
    #             ####  SEND RESPONSE WITH WINNER 
    #         return jsonify({'gameover': gameover, 'winner': winner, 'aimove': aimovestr})

    #         #### STORE BOARD IN DB
    #         db_row.saveboard(sessionid, board)
    #         ####    DETERMINE WHOSE TURN
    #         game.update_player()

    #     ####     AI  MOVE
    #     print(f"--- AI MOVE")
    #     ####    GET BOARD FROM DB
    #     board = db_row.getboard(sessionid)
    #     print(f">>>> player b4 ai mv= {player} ---")
    #     print(f"board retrieved b4 ai mv= {board} ---")
    #     #### ai makes move
    #     aimove = ai.choose_action(board)
    #     # print(f"\n---aimove={aimove}")

    #     ####        UPDATE BOARD
    #     availactions = game.available_actions()
    #     board = game.move(move, availactions)
    #     print(f"--- board after ai mv= {board} ---")
    #     ####   CHECK FOR GAME OVER
    #     if game.gameover():
    #         gameover = True
    #         winner = game.calc_winner()
    #     if winner is not None: # test line
    #         print(f"--- Ai is winner={winner} ---")

    #     ####    PREPARE RESPONSE
    #         aimovestr = ''.join(str(e) for e in aimove)
    #         # print(f"---aimovestr={aimove}{type(aimove)}")
    #         return jsonify({'gameover': gameover, 'winner': winner, 'aimove': aimovestr})
    #     #### STORE BOARD IN DB
    #     db_row.saveboard(sessionid, board)
    #     #### prepare response
    #     # print(f"---aimovestr={aimove}{type(aimove)}")
    #     # print(f"---aimove={aimove}{type(aimove)}")

    #     return jsonify({'aimove': aimovestr})
    

if __name__ == '__main__':
    app.run()