from othello import *

ai = OthelloAI()
game = Othello()
board = [[1,0,0,0],
        [0,-1,1,0],
        [0,1,-1,0],
        [0,0,0,0]]

canon_board, transformations = ai.canonical_board(board)
print("---canon=", (canon
_board, transformations))
