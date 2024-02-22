from othello import *

qtable = '66_boardeval'
ai = train(1, filename= qtable)
# 
# print_q_table(ai.q)
#  
print('>>>size of = ', qtable , len(ai.q))

# x = OthelloAI.load_data('testing')
# print(f'>>>testing= {x}')




    



