from othello import *

ai = train(1000)

ai.save_data('qtables/single_player_qtable')
    
# print(ai.q[(1,3,5,7),(0,1)])
# print(ai.q[(1,3,5,7),(3,1)])



# play(ai,0)


