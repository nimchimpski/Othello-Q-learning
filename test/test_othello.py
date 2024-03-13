from othello import Othello, OthelloAI





def test_move2():
    game=Othello()
    game.size = 3
    board = [[-1,1,-1],
            [1,-1,-1],
             [0,0,-1]]
   
    assert game.move(board, (2,0), -1) == [[-1,1,-1],
    [-1,-1,-1],
    [-1,0,-1]]



def test_calcnextcell():
    game=Othello()
    game.size = 3
    board = [[-1,1,-1],
            [1,-1,-1],
             [0,0,-1]]
   
    assert game.calcnextcell(board, (2,0), (-1,0)) == (1,0)
    assert game.calcnextcell(board, (1,0), (-1,0)) == (0,0)
    assert game.calcnextcell(board, (0,0), (-1,0)) == None
    assert game.calcnextcell(board, (2,2), (-1,1)) == None

def test_direction_checker():
    game = Othello()
    board = [[0,0,0,0],
             [-1,1,0,0],
             [-1,0,1,0],
             [1,0,0,-1]]
    game.size = len(board)

    assert game.direction_checker(board, (0,0), (1,0), 1) == {(1,0),(2,0)}
    assert game.direction_checker(board, (0,0), (1,1), -1) == {(1,1),(2,2)}
    assert game.direction_checker(board, (0,0), (0,1), -1) == None


def test_available_actions():
    game = Othello()
    board = [[0,0,0,0],
             [0,-1,1,0],
             [0,1,-1,0],
             [0,0,0,0]]
    game.size = len(board)
    print(f'===game.size={game.size}===')

    assert game.available_actions(board, 1) == {(0,1):{(1,1)},(1,0):{(1,1)},(2,3):{(2,2)},(3,2):{(2,2)}}
    # assert game.available_actions(board, -1) == {(0,2),(1,3),(2,0),(3,1)}
    # assert game.available_actions(board, 0) == None
   


def test_canonical_move():
    ai = OthelloAI()
    
    assert ai.canonical_move(['rotate 270'], (1,4), 6) == (1,1)
    # assert ai.retranslate_move(['rotate 270'], (0,1), 6) == (4,0)

    assert ai.canonical_move(['rotate 90'], (1,4), 6) == (4,4)
    # assert ai.retranslate_move(['rotate 90'], (1,4), 6) == (1,1)