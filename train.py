from othello import *

ai = train(10000)

# SAVE THE MODEL
ai.save_data('qtable')  
print('--size of qtable=', len(ai.q))




    



