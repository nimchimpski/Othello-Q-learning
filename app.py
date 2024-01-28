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
app.config['ENV'] = 'environment'
if environment == 'development':
    app.config['DESBUG'] = True
else:
    app.config['DEBUG'] = False
# app.debug = False

####      GAMEDB IS ACTUALLY A ROW IN THE DATABASE ? TODO CHANGE NAME
class Gamedb(db.Model):
    dbid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dbsessionid = db.Column(db.String, nullable=False)
    boardstate = db.Column(db.String, nullable=False)
    player = db.Column(db.String, nullable=False)  ####      STORE player AS A STRING

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
    if checkfordbrow(sessionid):
        
    game =Othello()
    return render_template('index.html')

@app.route('/play', methods=['POST', 'GET'])
def play():
    print('>>>PLAY ROUTE GET')

     ####     PRINT THE BOARD

     ####   CHECK FOR GAME OVER

    ####      GET SESSION ID
    sessionid = session.get('sessionid')

    #### CHECK IF SESSION ROW EXISTS
    db_row = Gamedb.query.filter_by(dbsessionid=sessionid).first()
    if db_row == None:
        print(f'---no db_row= {db_row}')


    

    #########      POST     #########
    if request.method == 'POST':
        print('>>>PLAY ROUTE POST')

        ####    print all json
        # print(f"\n--- request.json= {request.json} ---") 

        ####     CHECK IF NEW GAME + INITIALISE
        if request.json.get('newgame') == True:
            print('--- NEW GAME ---')

            ####   RESET BOARD
            board = othello.create_board()
            print(f'---board initialised--{board}-')
            #### iF NO ROW IN DB FOR THIS SESSIONID, CREATE ONE
            print('---queried db_row---')
            print(f'---existing db_row= {db_row}')
            if not db_row:
                print('---MAKING NEW db_row---')
                ####.   CREATE NEW ROW IN DB    
                db_row = Gamedb(dbsessionid=sessionid, boardstate=json.dumps(board), player=json.dumps(player))
                db.session.add(db_row)
            # INITIALISE BOARD IN DATABASE
            db_row.saveboard(sessionid, board, player)
            print(f'---db_row= {db_row}')
            print(f'---initialised board saved---{db_row}')

        ####     HUMAN MOVE
        humanmove = request.json.get('humanmove')
        if humanmove != None:
            humanmove = request.json.get('humanmove')
            human = request.json.get('human')
            # print(f"--- humanMove received: {humanmove}{type(humanmove)}---")
            humanmovetuple = tuple(int(char) for char in humanmove)
            # print(f"--- movetuple= {humanmovetuple} ---")
            #### GET BOARD FROM DB
            board = db_row.getboard(sessionid)
            # print(f"+++ board retrieved hm= {board} ---")
            ####  UPDATE BOARD WITH HUMAN MOVE  ####
            board = game.result(board, humanmovetuple)
            # print(f"--- board after human mv= {board} ---")
            ####   CHECK FOR GAME OVER
            winner = gameovercheck(human, board)
            if winner is not None:
                # print(f"--- GAMEOVER frm humanmove ={winner} ---")
                return jsonify({'winner': winner})
            #### STORE BOARD IN DB
            db_row.saveboard(sessionid, board)
            ####    DETERMINE WHOSE TURN
            player = ttt.player(board)
            # print(f">>>player after human mv= {player} ---")

        ####  AI  MOVE
        print(f"--- AI MOVE")
        # time.sleep(0.5)
        #### GET BOARD FROM DB
        board = db_row.getboard(sessionid)
        player = ttt.player(board)
        print(f">>>> player b4 ai mv= {player} ---")
        print(f"board retrieved b4 ai mv= {board} ---")
        #### ai makes move
        aimove = ttt.minimax(board)
        # print(f"\n---aimove={aimove}")
        #### update board
        board = ttt.result(board, aimove)
        print(f"--- board after ai mv= {board} ---")
        ####   CHECK FOR GAME OVER
        winner = gameovercheck('AI', board)
        if winner is not None:
            print(f"--- Ai is winner={winner} ---")
            aimovestr = ''.join(str(e) for e in aimove)
            # print(f"---aimovestr={aimove}{type(aimove)}")
            return jsonify({'winner': winner, 'aimove': aimovestr})
        #### STORE BOARD IN DB
        db_row.saveboard(sessionid, board)
        #### prepare response
        aimovestr = ''.join(str(e) for e in aimove)
        # print(f"---aimovestr={aimove}{type(aimove)}")
        # print(f"---aimove={aimove}{type(aimove)}")

        return jsonify({'aimove': aimovestr})
    




if __name__ == '__main__':
    app.run()