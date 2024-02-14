from othello import Othello





def test_move2():
    game=Othello()
    game.size = 3
    board = [[-1,1,-1],
            [1,-1,-1],
             [0,0,-1]]
   
    assert game.move(board, (2,0), -1) == [[-1,1,-1],
    [-1,-1,-1],
    [-1,0,-1]]

def test_direction_checker()
    board = 


   