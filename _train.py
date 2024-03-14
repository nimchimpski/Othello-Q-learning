from othello import *

# ai = train(40000, filename="masterq")
ai = OthelloAI()
tuples = ai.generate_tuple_list(4)
print('tuples= ', tuples)

# print_q_table(ai.q)


