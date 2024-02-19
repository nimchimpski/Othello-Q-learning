from othello import *

####   Q TABLED AUTOMATICALLY SAVED IF NEW, 
####  AND LOADED IF EXISTS


# ai = train(10000, 0.4, 0.1)

with open('qtables/qtable.pickle', 'rb') as f:
    qtable = pickle.load(f)

print_q_table(qtable)
# print(f'---len(ai.q)={len(ai.q)}')


# evaluate(2,'qtables/single_player_qtable' , None)


