from othello import *

####   Q TABLED AUTOMATICALLY SAVED IF NEW, 
####  AND LOADED IF EXISTS


ai = train(100000, 0.1, 0.1, '6x6')

# print_q_table(ai.q)


# with open('qtables/qtable.pickle', 'rb') as f:
#     qtable = pickle.load(f)

# print_q_table(qtable)
# print(f'---len(ai.q)={len(ai.q)}')


# evaluate(2,'qtables/single_player_qtable' , None)


