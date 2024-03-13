from othello import *

# ai = train(40000, filename="masterq")
ai = OthelloAI()
tuples = ai.maketuples(8)
print('tuples= ', tuples)

# print_q_table(ai.q)


