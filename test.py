from othello import *

newgame = Game()

####   TEST BOARD
def create_test_board():
    board = [[BLACK,WHITE,EMPTY],
             [WHITE,WHITE,EMPTY],
             [BLACK,EMPTY,EMPTY]]

    return board

testboard = create_test_board()
# print(f'testboard={testboard}')
newgame.board = testboard
# print(f'newgame board={newgame.board}')

print(f'newgame.player={newgame.player}')
print(f'newgame.enemy={newgame.enemy}')
print(f'newgame.turnsplayed={newgame.turnsplayed}')

# newgame.printboard()

#### TEST DIRECTION_CHECKER
# newgame.direction_checker(1,2,(-1,-1))


#### TEST AVAILABLE_ACTIONS
print(f'newgame.available_actions={newgame.available_actions()}')

#### TEST WHOSE TURN

#### TEST MOVE





#### TEST SCORES

#### TEST WINNER

#### TEST TERMINAL


