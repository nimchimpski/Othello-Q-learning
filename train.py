from othello import *
qfile = 'qtable'
ai = train(50, alpha=0.3, maxeps=0.5, mineps=0.1, decay_rate=0.001)
# 
# print_q_table(ai.q)
#  
print('>>>size of = ', qfile , len(ai.q))

# x = OthelloAI.load_data('testing')
# print(f'>>>testing= {x}')


# create blanc q  table

# ai = OthelloAI()

# ai.save_data(qfile)

    



