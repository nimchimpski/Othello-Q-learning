from othello import *

ai = train(5, filename= 'testing')
# 
# print_q_table(ai.q)
#  
print('>>>size of qtable=', len(ai.q))

x = OthelloAI.load_data('testing')
# print(f'>>>testing= {x}')




    



