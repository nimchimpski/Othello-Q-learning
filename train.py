from othello import *
qfile = '66_move_eval'
ai = train(50000, alpha=0.3, maxeps=0.5, mineps=0.1, decay_rate=0.001, filename= qfile)
# 
# print_q_table(ai.q)
#  
print('>>>size of = ', qfile , len(ai.q))

# x = OthelloAI.load_data('testing')
# print(f'>>>testing= {x}')




    



