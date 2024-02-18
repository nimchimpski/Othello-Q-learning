from othello import *

####   Q TABLED AUTOMATICALLY SAVED IF NEW, 
####  AND LOADED IF EXISTS


ai = train(10000, 0.2, 0.1, '4x4')
print(f'---len(ai.q)={len(ai.q)}')
    


# evaluate(2,'qtables/single_player_qtable' , None)


