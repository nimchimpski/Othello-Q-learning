from othello import *

ai = train(1, filename= 'testing')
# print_q_table(ai.q)
# SAVE THE MODEL
# ai.save_data('qtable')  
print('--size of qtable=', len(ai.q))




    



