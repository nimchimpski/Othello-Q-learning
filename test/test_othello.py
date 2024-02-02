from othello import Othello



board = [['WHITE','BLACK','WHITE'],
        ['BLACK','WHITE','WHITE'],
        ['     ','     ','WHITE']]

# def test_create_board():
#     game=Othello()
#     assert game.create_board() == [
#                                    ['WHITE','BLACK','     '],
#                                    ['BLACK','WHITE','     '],
#                                    ['     ','     ','     ']]

# def test_move_blackfirst():
#     game=Othello()
   
#     assert game.move(board, (2,1), 'BLACK') == [['WHITE','BLACK','     '],['BLACK','BLACK','     '],['     ','BLACK','     ']]
def test_move2():
    game=Othello()
    board = [['WHITE','BLACK','WHITE'],
            ['BLACK','WHITE','WHITE'],
             ['     ','     ','WHITE']]
   
    assert game.move(board, (2,0), 'WHITE') == [['WHITE','BLACK',' WHITE'],
    ['WHITE','BLACK','WHITE'],
    ['WHITE','     ','WHITE']]

def test_available_actions1():
    game=Othello()
    board = [['WHITE','BLACK','     '],
             ['BLACK','WHITE','     '],
             ['     ','     ','     ']]
    assert game.available_actions(board, 'BLACK') == {(2, 1): {(1, 1)}, (1, 2): {(1, 1)}}

def test_available_actions2():
    game=Othello()
    board = [['WHITE','BLACK','WHITE'],
            ['BLACK','WHITE','WHITE'],
            ['     ','     ','WHITE']]
    assert game.available_actions(board, 'WHITE') == {(2,0): {(1,0)}}



# def test_gameover_false():
#     game=Othello()
#     board = [['WHITE','BLACK','     '],
#         ['BLACK','WHITE','     '],
#         ['     ','     ','     ']]
#     assert game.gameover(board) == False

# def test_gameover_full():
#     game=Othello()
#     board = [['WHITE','BLACK','WHITE'],
#         ['BLACK','WHITE','WHITE'],
#         ['WHITE','WHITE','WHITE']]
#     assert game.gameover(board) == True

# def test_winner():
#     game=Othello()
#     board = [['WHITE','WHITE','BLACK'],
#         ['WHITE','WHITE','BLACK'],
#         ['WHITE','WHITE', 'WHITE']]
#     assert game.calc_winner(board) == 'WHITE'

   