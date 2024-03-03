from othello import *

ai = OthelloAI()
game = Othello()
board = [[1,0,0,0],
        [0,-1,1,0],
        [0,1,-1,0],
        [0,0,0,0]]

canonical_board, transformations = ai.canonical_board_representation(board)
print("---canon=", (canonical_board, transformations))
