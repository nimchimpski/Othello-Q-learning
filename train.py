from othello import *

ai = train(10000, filename= '6x6c')
# print_q_table(ai.q)
# SAVE THE MODEL
# ai.save_data('qtable')  
print('--size of qtable=', len(ai.q))




    



