from othello import OthelloAI, Othello

def test_invertboard():
    game = Othello()
    ai = OthelloAI()
    board = [[0,0,0,0],
             [0,-1,1,0],
             [0,1,-1,0],
             [0,0,0,0]]
    print(f'///len(board)={len(board)}')
    game.size = len(board)
    print(f'///game.size={game.size}===')
    game.printboard(board)


    assert ai.invertboard(board) == [[0,0,0,0],
                                       [0,1,-1,0],
                                       [0,-1,1,0],
                                       [0,0,0,0]]

# def test_choose_q_action():
#     ai = OthelloAI()
#     q_table = {((0,0), (1,0)): 0.5, ((0,0), (0,1)): 0.3}

    
#     assert ai.choose_q_action(q_table, (0,0)) == (1,0)