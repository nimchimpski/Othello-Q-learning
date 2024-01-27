from othello import *

newgame = Othello(3)

####   TEST BOARD
def create_test_board():
    # board = [[BLACK,WHITE,EMPTY],
    #          [WHITE,WHITE,EMPTY],
    #          [BLACK,EMPTY,EMPTY]]
    
    board = [[WHITE,WHITE, WHITE],
             [EMPTY,WHITE,BLACK],
             [WHITE,WHITE,BLACK]]
    return board

testboard = create_test_board()
# print(f'testboard={testboard}')
newgame.board = testboard
# print(f'newgame board={newgame.board}')

# print(f'///newgame.player={newgame.player}')
# print(f'///newgame.enemy={newgame.enemy}')
# print(f'///newgame.turnsplayed={newgame.turnsplayed}')

#### TEST DIRECTION_CHECKER (cell,dir,player,enemy)

# validmoves = newgame.direction_checker((0,2),(0,-1))
# print(f'validmoves player={validmoves}')
# validmoves = newgame.direction_checker((0,2),(0,-1),player=WHITE,enemy=BLACK)
# print(f'validmoves enemy={validmoves}')


#### TEST AVAILABLE_ACTIONS  (player,enemy)

# testactions = newgame.available_actions()
# print(f'\n///testactions player={testactions}\n')
# testactions = newgame.available_actions(WHITE,BLACK)
# print(f'\n///testactions enemy={testactions}\n')

#### TEST WHOSE TURN

def test_whose_turn():
    assert newgame.whose_turn(2) == (BLACK, WHITE)
    assert newgame.whose_turn(3) == (WHITE, BLACK)
    assert newgame.whose_turn(0) == (BLACK, WHITE)

#### TEST MOVE
# newgame.move((0,2))

####   TEST PRINTBOARD

# newgame.printboard()

#### TEST SCORES
# blackwins =  [[WHITE,BLACK, BLACK],
#              [WHITE,WHITE,BLACK],
#              [BLACK,BLACK,BLACK]]
# print(f'///scores={newgame.scores(blackwins)}')


#### TEST TERMINAL

# print(f'///terminal={newgame.terminal()}')

#### TEST WINNER

# print(f'///winner={newgame.calc_winner()}')

#### TEST PLAY

# play()

