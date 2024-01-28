from othello import Othello



def test_update_player():
    game=Othello()

    assert game.update_player(0) == ('X', 'O')
    assert game.update_player(1) == ('O', 'X')
    assert game.update_player(2) == ('X', 'O')
    assert game.update_player(20) == ('X', 'O')
    assert game.update_player(31) == ('O', 'X')

def test_create_board():
    game=Othello()
    assert game.create_board() == [[' ',' ',' ',' '],
                                   [' ','O','X',' '],
                                   [' ','X','O',' '],
                                   [' ',' ',' ',' ']]

def test_move_blackfirst():
    game=Othello()
    
    assert game.move((0,1)) == [[' ','X',' ',' '],
                                              [' ','X','X',' '],
                                              [' ','X','O',' '],
                                              [' ',' ',' ',' ']]

def test_availabale_actions():
    game=Othello()
    assert game.available_actions() == {(0, 1): {(1, 1)}, (1, 0): {(1, 1)}, (2, 3): {(2, 2)}, (3, 2): {(2, 2)}}

def test_available_actions_whitefirst():
    game=Othello()
    
    assert game.available_actions('O','X') == {(0, 2): {(1, 2)}, (1,3):{(1,2)},(2,0):{(2,1)},(3,1):{(2,1)}}

   