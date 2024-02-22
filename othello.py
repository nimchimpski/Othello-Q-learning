import math
import random
import time
import pickle
import os
from copy import deepcopy

EMPTY = 0
BLACK = 1
WHITE = -1
VALID = '*'
PLAYER_COLS = {
    BLACK: "BLACK",
    WHITE: "WHITE",
}

class Othello():

    def __init__(self, size=6):
        """
        Initialize game board.
        Each game board has
            - size: defined by user
        """
        # (print('\n+++init'))
        self.size = size
        self.state = self.create_board()
        self.player = BLACK
        self.winner = None

    @classmethod
    def playercolor(self, player):

        return "BLACK" if player == 1 else "WHITE"

    # BOARD SHOWING AVAILABLE MOVES
    def boardwithavails(self, board,  human, aimove):  
        print(' ++++boardwithavails')
    
        # print(f'player={player}')
        for cell in self.available_actions( board, human):
            print(f'cell={cell}')
            board[cell[0]][cell[1]] = '*'
        # add ai's last move
        if aimove is not None:
            # print(f'---human= {human}')
            if human == 1:
                board[aimove[0]][aimove[1]] = '-'
            elif human == -1:
                board[aimove[0]][aimove[1]] = '+'
        # print(f"for response board= {board}")
        # self.printboard(board)
        return board
       
    def switchplayer(self, player):
        # print(f'+++switchplayer()')
        # print(f'player={player}')
        # print(f'switchplayer player={player}')
        if player == BLACK:
            # if self.available_actions(board, player):
            return WHITE
        else:
            return BLACK

    def printboard(self, board, lastmove=None):
        RED = '\033[91m'
        ENDC = '\033[0m'        
        symbol_map = {1: 'X', -1: 'O', 0: '.'}
        for i, row in enumerate(board):
            row_str = ''
            for j, cell in enumerate(row):
                if lastmove == (i,j):
                    row_str += RED + f' {symbol_map[cell]} ' + ENDC
                else:
                    row_str += f' {symbol_map[cell]} '
            print(row_str)

    def create_board(self):
        # print('+++create_board')
        board = []
        for i in range (self.size):
            row = []
            for j in range (self.size):
                row.append(0)
            board.append(row)
        center = int((self.size/2)-1)
        board[center][center] = -1
        board[center][center+1] = 1
        board[center+1][center] = 1
        board[center+1][center+1] = -1
        return board

    def move(self, board, action, player):
        """
        `action` must be a tuple `(i,j)`.
        return the updated board.
        !!! CHANGES BOARD VAR !!!
        """
        copyboard = deepcopy(board)
        # print(f'\n++++move() for {player}, ')
        # self.printboard(board)
        # print(f'action={action}')
        # print(f'player={player}')
        if board is None:
            print("Board is None")
        availactions = self.available_actions(copyboard, player)
        # print(f'availactions={availactions}')
        # print(f'---action= {action}')
     
        #####      IS ACTION VALID
        if action not in availactions:
            print("\n>>>>Error: Action not in available_actions.")
            return board  # Or handle the error differently
        # else:
            # print(f'Action is valid')

        ####     GET BITS TO FLIP
      
        bitstoflip = availactions[action]
        # print(f'---bitstoflip= {bitstoflip}')
    

        ####  MARK BOARD WITH FLIPPED PIECES
        if bitstoflip:
            for bit in bitstoflip:
                copyboard[bit[0]][bit[1]] = player
        # print(f'board with just  flips')
        
          #####     MARK BOARD WITH ACTUAL MOVE
        copyboard[action[0]][action[1]] = player
        # print(f'board with flips and move')
        # self.printboard(board)

      
        # print('END OF MOVE()')

        return copyboard

    def calcnextcell(self, board, cell, direction):
            #   RETURNS THE NEXT CELL ONLY IF IT IS WITHIN BOUNDS
            # print(f'+++calcnextcell ')
            result = tuple(c + d for c,d in zip(cell, direction)) 
            ####       IS THE NEW CELL ON THE BOARD?
            if result[0] < 0 or result[0] >= self.size or result[1] < 0 or result[1] >= self.size:
                # print(f'OUT OF BOUNDS')
                return None
            # print(f'result={result}')
            return result
    
    def direction_checker(self, board, cell, direction, player):
        """
        Returns a set of captured pieces if possible in that direction, None otherwise.
        """
        #### MAKE PRINTABLE DIRECTIONS
        if direction == (-1, -1):
            compass = 'NW'
        elif direction == (-1, 0):
            compass = 'N'
        elif direction == (-1, 1):  
            compass = 'NE'
        elif direction == (0, -1):
            compass = 'W'
        elif direction == (0, 1):
            compass = 'E'
        elif direction == (1, -1):
            compass = 'SW'
        elif direction == (1, 0):
            compass = 'S'
        elif direction == (1, 1):
            compass = 'SE'

        # print(f'+++++direction_checker().  {compass} from candidate cell{ cell}')
        # self.printboard(board)
        originalcell = cell
        ####       SET UP VARIABLES
        captured = set()
        # nextcell = cell
        opponent = self.switchplayer(player)
        ####   RUN LOOP TO CHECK DIRECTION
        while True:
            # print(f'---START SEARCH LOOP')
            # print(f'---direction={direction}')
            # print(f'opponent={opponent}')

            ####       CALCULATE NEXT CELL
            cell = self.calcnextcell(board, cell, direction)

            # if newcell is not in bounds
            if cell is None:
                # print(f'---cell is None')   
                return None
            # print(f'===new cell= {cell}, original = {originalcell}')

            #### IF THE cell IS EMPTY, RETURN NONE
            if board[cell[0]][cell[1]] == 0:
                # print(f'cell is empty, so returning None')
                return None
            
            
            ####   IF  CELL IS MINE 
            if board[cell[0]][cell[1]]  == player:
                ####    AND  THERE ARE CAPTURED
                if captured:
                    # print(f'{cell} is mine and captured is not empty, so returning = {captured}')
                    return captured
                else:
                    return None

            #### ELSE IF NEXT CELL IS ENEMY, ADD TO CAPTURED
            elif board[cell[0]][cell[1]] == opponent:
                # print(f'opponent at {cell} in direction {compass},')
                captured.add(cell)
                # print(f'captured={captured}')
       
    def available_actions(self, board, player):
        """
        returns a list of tuples,  with all of the available actions `(i, j)` in that state, plus the captued pieces for each move, as a set.
        """
        # print(f'\n+++AVAILABLE_ACTIONS FOR {player}')
        # self.printboard(board)
        actions = {}
        ####       CREATE THE DIRECTIONS
        directions = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == dj == 0)]
        # print(f'directions={directions}')

        ####        FOR EACH BOARD cell
        # print('---GO THROUGH WHOLE BOARD, LOOKING FOR EMPTY CELLS')
        for i, row in enumerate(board):
            for j, content in enumerate(row):
                cell = (i,j)
                # print(f'content={content}')

                # print(f'\n ---CHECKING CELL = {cell}')
                if (content != 0) :
                    # print(f'content is not 0, so continue')
                    continue
                # print(f'---{cell} is empty, so possibly valid: checking directions')
                # print(f'cell={cell}, type={type(cell[0])}')
                alldirscaptured = set()
                ####       FOR EACH DIRECTION
                for direction in directions:
                    # print(f'---checking direction= {direction}')
                    
                    ####        IF VALID , ADD MOVE TO SET, ADD CAPTURED PIECES TO SET
                    onedircaptured = self.direction_checker(board, cell, direction, player )
                    # print(f'onedir_captured={onedircaptured}')
                    ####    IF THERE IS ANY ADD TO TOAL CAPTURED FOR THIS cell
                    if onedircaptured:
                        # print(f'onedir_captured=true, so adding to alldirscaptured')
                        alldirscaptured.update(onedircaptured)
                    else:
                        continue
                        # print(f'onedirc_aptured=false')
                        
                    # print(f'xxxtotalcaptured={alldirscaptured}') 
                # print(f'alldirs_captured={alldirscaptured}') 
                if alldirscaptured:
                    # print(f'alldirs_captured=true')
                    actions[cell]= alldirscaptured 
                else:
                    continue
                    # print(f'alldirs_captured=false') 
        # print(f'>>>>>available actions={actions}')
        self.availactions = actions
        # print(f'+--end of available_actions()')
        return actions
   
    def scores(self, board):
        """
        Returns a tuple (black_score, white_score) for the current game state.
        """
        # print(f'+++scores()')
    
        black_score = 0
        white_score = 0
        for row in board:
            for cell in row:
                if cell == 1:
                    black_score += 1
                elif cell == -1:
                    white_score += 1
        # print(f'black_score={black_score}')
        # print(f'white_score={white_score}')
        return (black_score, white_score)

    def calc_winner(self, board):
        black_score, white_score = self.scores(board)
        # print(f'+++calc_winner()')
        # print(f'black_score, white_score={black_score}{white_score})')
        if black_score > white_score:
            self.winner = BLACK
            return BLACK
        elif white_score > black_score:
            self.winner = WHITE
            return WHITE
        else:
            return None

    def gameover(self, board ):
        """
        Returns True if game is over, False otherwise.
        """
        # print(f'+++gameover()')
        # if self.winner is not None:
        #     print(f'+++gameover: self.winner={self.winner}')
        #     return True
        ####    CHECK IF BOARD IS FULL
        if not any(cell == 0 for row in board for cell in row):
            # print(f'---board is full')
            return True

        ####   CHECK IF NEITHER PLAYER HAS ANY VALID MOVES
        if (not self.available_actions(  board, -1) and not self.available_actions(board, 1)):
            # print(f'---no valid moves for either player')
            # print(f'----end of gameover()')
            return True
        # print(f'----end of gameover()')
        return False
        
    

class OthelloAI():
    ### AI CAN USE CLASS ATTRIBUTES AS IT WILL NOT BE SERVED/SUBJECT TO REQUESTS

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict() # VALUE CAN BE NONE FOR UNEXPLORED STATES
        self.alpha = alpha
        self.epsilon = epsilon
        self.minratio = float('inf')
        self.maxratio = -float('inf')
        

    def update(self, old_state, action, new_state, reward, game_instance, player=None):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
    
        # print(f"+++update")
        # print(f"---old_state={old_state}, action={action}, new_state={new_state}, reward={reward}")
        old = self.get_q_value(player, old_state, action)
        best_future = self.best_future_reward(new_state, game_instance)
        self.update_q_value(player, old_state, action, old, reward, best_future)
        # print(f"+++>>>update: self.q={self.q}")

    def get_q_value(self, player, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        # self.q = ((0, 0, 0, 2), (3, 2): -1)
        # print
        if not state or not action:
            return None  
        # print(f"---state type= {type(state)}")
        statetuple = self.statetotuple(state)
        # print(f"---state type= {type(statetuple)}")

        
        q =  self.q.get((player, statetuple, action), 0)
        # print(f"+++>>>get_q_value: {state}, {action} = q {q}")
        if not q:
            return None
        return q 

    def statetotuple(self, state):
        return tuple(tuple(row) for row in state)

    def update_q_value(self, player, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate + alpha * (new value estimate - old value estimate)

        Q(state, action) = Q(state, action) + α * (reward + γ * max_a Q(next_state, a) - Q(state, action))


        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        # """
      # print(f"+++UPDATEQ FOR {Othello.playercolor(player)}")
        # print(f"---state={state}, action={action}, old_q={old_q}, reward={reward}, future_rewards={future_rewards}")
        if state is None or action is None:
          # print(f"---!!!!!state or action is None")
            return

        if old_q is None:
            old_q = 0
   
        statetuple = self.statetotuple(state)
     
        newvalest = reward + future_rewards
        # print(f"---newvalest={newvalest}")
        ####     IF WINNER = PLAYER, REWARD = 1

        result = old_q + (self.alpha * (newvalest - old_q))
        result = round(result, 2)
        
        
        
        self.q[player, statetuple, action] = result
      # print(f"---updateq self.q = {self.q[player, statetuple, action]}")
        
    def best_future_reward(self, state, game_instance):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.

        =epsilon is the exploration rate (probability of taking a random action))]
        ='Q-table' is a dictionary mapping state-action pairs to Q-values
        """
        actions =  game_instance.available_actions(state, game_instance.player)
        # print(f"+++best_future: actions={actions} len={len(actions)})") 
        if not actions:
            # print(f"---no actions")
            return 0
        # get q value for actions
        qlist = []
        for action in actions:
            # print(f"---action={action}")
            # print(f"---q = {self.get_q_value(state, action)})")
            n = self.get_q_value(game_instance.player, state, action)
            if n is None:
                n = 0
            qlist.append(n)
        # print(f"---qlist={qlist} len={len(qlist)}")
        best = max(qlist)
        # print(f"---best={best}")
        ####   GAMMA=1 MEANS FUTURE REWARDS ARE PRIORITIZED
        gamma = 1 
        result =  gamma * best
        # print(f"---result={result}")
        # print(f">>>best={best}")
        return result
        
    

        # get max of the q values

    def choose_q_action(self, state, player, game_instance, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.
        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).
        If `epsilon` is `True`, return None.
        """
        print(f"+++choose-Q : actions=")
        actions = game_instance.available_actions(state, player)
        # print(f"---actions={actions}")
        if not actions:
            return None
        action = None
        ####  IF ONLY ONE ACTION RETURN IT
        if len(actions) == 1:
            # print(f"---only one action, so returning it")
            key = next(iter(actions))
            action = key
            # print(f'---action 1  = {action}')

        
        # WITH EPSILON TRUE: CHOOSE RANDOM ACTION WITH EPSILON PROB
        elif epsilon == True:
            # print(f"---CHOOSING EPSILON HERE = {epsilon}")
            x = random.random()
            # print(f"---random x = {x}")
            if x < self.epsilon:
                action = random.choice(list(actions))
                # print(f">>>EPs=True : random action= {action}")
            # else:
                # print(f'---a random action was not chosen, so use the q table to choose the best action')

        ### EPSILON FALSE: CHOOSE ACTION WITH HIGHEST Q VALUE
        ####     ALSO RETURN CAPTURES, SO CAN BE USED AS HEURISTIC
        # print(f'---action 2  = {action}')

        # IF RAMDOM ACTION WAS NOT CHOSEN, USE Q TABLE 
        if not action:
            maxq = -float('inf')
            bestaction_q = None
            bestactions = []
            # print(f'---CHOOING Q ACTION HERE:')
            # print(f'---actions={actions}')

            for action in actions:
                assert action is not None
                q = self.get_q_value(player, state, action)
                if q:

                    # print(f"---action {action} q={q}")

                    ###   IS THERE A Q VALUE FOR THIS ACTION? 
                    # if q is None:
                        # q = 0
                    # print(f"---q={q}")
                    if q > maxq:
                        #### TODO THIS COULD PICK AN ACTION WITH EQUAL Q USING A PROBABILITY, OTHERWISE IT WILL ALWAYS PICK THE LAST ACTION WITH THE HIGHEST Q
                        maxq = q
                        bestactions = [action]
                    elif q == maxq:
                        bestactions.append(action)
            if bestactions:
                # print(f"---bestactions= {bestactions}")
                bestaction_q = random.choice(bestactions)
                # print(f"---bestcaction_q= {bestaction_q}")
                action = bestaction_q
            else:
                # print(f"---not in q table")
                return None
        # print(f"---action 3  = {action}")
        # get the captured pieces
        captured = actions[action]
        print(f"---returning={action}, {captured}")
        # print(f'+--end of choose_q_action()')
        return action, captured
    
    def choose_evaluated_action(self, state, player, game_instance):
        print(f"+++choose_evaluation_action()")
        actions = game_instance.available_actions(state, player)
        print(f"---actions={actions}")
        besteval = -float('inf')
        for action in actions:
            print(f"---action={action}")
            eval = self.evaluate_action(state, action, player, game_instance)
            print(f"---eval={eval}")
            if eval > besteval:
                besteval = eval
                bestaction = action
            print(f"---action={action}, besteval={besteval}")
        print(f"---bestaction={bestaction}")
        return bestaction
        
    # def evaluateboard(self, state, action, player, game_instance):
        '''
        frontier pieces
        '''
        print(f'+++evaluateboard()')
        print(f'---action= {action}')
        val = 0
        l = len(state)-1
        # CALCULATE IF ACTION IN CORNER
        if action in [(0,0), (0,l), (l,0), (l,l)]:
            print(f"---action in corner")
            val = 0.5
        # CALCULATE IF ACTION NEXT TO CORNER
        elif action in [(0,1), (1,0), (1,1), (0,l-1), (1,l), (1,l-1), (l,1), (l-1,0), (l-1,1), (l-1,l), (l,l-1), (l-1,l-1)]:
            print(f"--- action next to corner ")
            val = -0.5
        # CALCULATE IF ACTION ON EDGE
        elif action[0] in [0, l] or action[1] in [0, l]:
            if action not in [(0,0), (0,l), (l,0), (l,l)]:
                print(f"---action on edge")
                val = 0.2

        # calculate if player has more available moves than opponent
        playeravails = game_instance.available_actions(state, player)
        opponent = game_instance.switchplayer(player)
        oppavails = game_instance.available_actions(state, opponent)
        if len(playeravails) > len(oppavails):
            print(f"---player has more available moves")
            val += 0.5
        elif len(playeravails) < len(oppavails):
            print(f"---opponent has more available moves")
            val -= 0.5
        # val += min(1, len(avails)/10)

        return val

    # def evaluate_move(board, move, player, captured_pieces):
        val = 0
        size = len(board) - 1

        # Award for corner capture
        corners = [(0, 0), (0, size), (size, 0), (size, size)]
        if move in corners:
            val += 1.0

        # Award for edge moves, especially linking to a corner
        if is_edge(move, size) and not is_corner_adjacent(move, size):
            val += 0.5
            if connects_to_corner(move, board, player):
                val += 0.5

        # Penalize moves adjacent to corners or along the edges
        if is_corner_adjacent(move, size):
            val -= 1.0
        elif is_edge_adjacent(move, size):
            val -= 0.5

        # Mobility and disc ratio evaluation
        mobility_diff, disc_ratio = evaluate_mobility_and_ratio(board, move, player, captured_pieces)
        val += mobility_diff
        val += disc_ratio

        return val

    def is_edge(self,move, last_index):
        return move[0] == 0 or move[0] == last_index or move[1] == 0 or move[1] == last_index

    def is_corner_adjacent(self, move, last_index):
        corner_adjacent_positions = [
            (0, 1), (1, 0), (1, 1),  # Top-left corner adjacent positions
            (last_index, last_index-1), (last_index-1, last_index), (last_index-1, last_index-1),  # Bottom-right corner adjacent positions
            (0, last_index-1), (1, last_index), (1, last_index-1),  # Top-right corner adjacent positions
            (last_index, 1), (last_index-1, 0), (last_index-1, 1)  # Bottom-left corner adjacent positions
            ]
        return move in corner_adjacent_positions


    def is_edge_adjacent(self, board, move, last_index):
        print(f'--move= {move}')
        # Check adjacent to vertical edges and not at corners
        if move[0] in [1, last_index-1] and move[1] not in [0, last_index]:
            if move[0] == 1 and board[0][move[1]] == EMPTY:  # Check upper edge if move is on the second row
                return True
            elif move[0] == last_index-1 and board[last_index-1][move[1]] == EMPTY:  # Corrected index for lower edge check
                return True

        # Check adjacent to horizontal edges and not at corners
        if move[1] in [1, last_index-1] and move[0] not in [0, last_index]:
            if move[1] == 1 and board[move[0]][0] == EMPTY:  # Check left edge if move is in the second column
                return True
            elif move[1] == last_index-1 and board[move[0]][last_index-1] == EMPTY:  # Corrected index for right edge check
                return True

        return False


    def is_corner(self,move, last_index):
        return move in [(0, 0), (0, last_index), (last_index, 0), (last_index, last_index)]
    
    def connects_to_corner(self, move, board, player):
        # Determine if a move is directly connected to a player-occupied corner with a path consisting only of player's pieces
        last_index = len(board) - 1
        corners = [(0, 0), (0, last_index), (last_index, 0), (last_index, last_index)]

        def check_path(start, end):
            # Check if the path between start and end is clear or consists only of player's pieces
            # This function assumes start and end are in a straight line (horizontal, vertical, or diagonal)
            dx = 1 if end[0] > start[0] else -1 if end[0] < start[0] else 0
            dy = 1 if end[1] > start[1] else -1 if end[1] < start[1] else 0

            x, y = start
            while (x, y) != end:
                x += dx
                y += dy
                if (x, y) != end and board[x][y] != player:  # Skip checking the end point itself
                    return False
            return True
    
        for corner in corners:
            if board[corner[0]][corner[1]] == player:
                # Directly connected if on the same row, column, or diagonal
                if corner[0] == move[0] or corner[1] == move[1] or abs(corner[0] - move[0]) == abs(corner[1] - move[1]):
                    # Check the path between the move and the corner
                    if check_path(move, corner):
                        return True
        return False

    def connects_to_corner_2(self, move, board, player):
        # Determine if a move is directly connected to a player-occupied corner with an uninterrupted path
        last_index = len(board) - 1
        corners = [(0, 0), (0, last_index), (last_index, 0), (last_index, last_index)]

        def check_path(corner, move):
            # Check horizontal or vertical paths
            if corner[0] == move[0]:  # Same row
                for col in range(min(corner[1], move[1]) + 1, max(corner[1], move[1])):
                    if board[move[0]][col] != player:
                        return False
            elif corner[1] == move[1]:  # Same column
                for row in range(min(corner[0], move[0]) + 1, max(corner[0], move[0])):
                    if board[row][move[1]] != player:
                        return False
            else:
                # Check diagonal paths
                row_step = 1 if move[0] < corner[0] else -1
                col_step = 1 if move[1] < corner[1] else -1
                row_range = range(move[0] + row_step, corner[0], row_step)
                col_range = range(move[1] + col_step, corner[1], col_step)
                for row, col in zip(row_range, col_range):
                    if board[row][col] != player:
                        return False
            return True

        for corner in corners:
            if board[corner[0]][corner[1]] == player:
                if corner[0] == move[0] or corner[1] == move[1] or abs(corner[0] - move[0]) == abs(corner[1] - move[1]):
                    if check_path(corner, move):
                        return True
        return False



    def evaluate_mobility_and_ratio(self,board, move, player, captured_pieces):
        # This is a placeholder for mobility and disc ratio evaluation
        # Implement your own logic here based on the current state after the move is made and captured pieces are flipped
        mobility_diff = 0.1  # Placeholder value
        disc_ratio = 0.1  # Placeholder value
        return mobility_diff, disc_ratio

        # Example of making a move and evaluating it
        move = (0, 0)  # A corner move
        player = 1  # Assuming 1 is black
        captured_pieces = [(0, 1), (1, 0), (1, 1)]  # Example captured pieces for this move
        # You need to implement the logic for updating the board with the move and captured pieces
        # new_board = make_move(board, move, player, captured_pieces)

        # val = evaluate_move(new_board, move, player, captured_pieces)
        # print(f"Move value: {val}")

    def evaluate_board_2(self, board, player, instance):
        # print(f"+++evaluate_board_2()") 
        val = 0
        size = len(board) - 1
        opponent = -player
        player_pieces = 0
        opponent_pieces = 0
        player_frontier = 0
        opponent_frontier = 0
        player_mobility = 0
        opponent_mobility = 0
        empties = 0

        directions = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == dj == 0)]

        ####    EDGES AND CORNER PIECES
        for i in range(len(board)):
            for j in range(len(board)):
                cell = (i, j)
                if board[i][j] == player:
                    # count pieces
                    player_pieces += 1
                    # IS EDGE?
                    if self.is_edge(cell, size):
                        val += 0.2  
                        # print(f"piece on edge")
                        # CONNECTS TO CORNER?
                        if self.connects_to_corner(cell, board, player):
                            # print(f"connects to corner")
                            val += 0.3
                    # IS CORNER?
                    if self.is_corner(cell, size):
                        # print(f"corner piece")
                        val += 0.5  
                    # is corner adjacent?
                    if self.is_corner_adjacent(cell, size):
                        if not self.connects_to_corner(cell, board, player):
                            # print(f"corner adjacent")
                            val -= 0.5
                    # IS EDGE ADJACENT?
                    if self.is_edge_adjacent(board, cell, size):
                        # but not connects to edge
                        # print(f"edge adjacent")
                        val -= 0.4
                    
                elif board[i][j] == opponent:
                    # print(f"opponent_pieces += 1")
                    opponent_pieces += 1
                elif board[i][j] == 0:
                    empties += 1

                ####    FRONTIER PIECES
                # if a position is filled
                if board[i][j] != 0:
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        # look for an empty position next to it = frontier
                        if 0 <= ni <= size and 0 <= nj <= size and board[ni][nj] == 0:
                            if board[i][j] == player:
                                # print(f"player_frontier += 1")
                                player_frontier += 1
                            else:
                                # print(f"opponent_frontier += 1")
                                opponent_frontier += 1
                            break
        ####   CALCULATE GAME PHASE
        if empties > 20:
            phase = 1
        elif empties <= 20 and empties > 10:
            phase = 2
        else:
            phase = 3
        # print(f"phase= {phase}")

        #####      MOBILITY AND POTENTIAL MOBILITY
        player_mobility = len(instance.available_actions(board, player))
        opponent_mobility = len(instance.available_actions(board, opponent))
        
        # Piece ratio
        # print(f"player_pieces={player_pieces}, opponent_pieces={opponent_pieces}")
        ratio = (player_pieces - opponent_pieces) / (player_pieces + opponent_pieces) 

        # Assuming player_pieces and opponent_pieces are already calculated
        def adjusted_sigmoid(x):
            return 2 / (1 + math.exp(-x)) - 1


        total_pieces = player_pieces + opponent_pieces
        if total_pieces == 0:
            ratio = 0  # Avoid division by zero in an empty or initial board state
        else:
            ratio = (player_pieces - opponent_pieces) / total_pieces
        ratio *= 8
        sigratio = adjusted_sigmoid(ratio)
        # multiply by bias
        
        # print(f'---sigratio= {sigratio}')

        if sigratio < self.minratio:
            self.minratio = sigratio
        if sigratio > self.maxratio:
            self.maxratio = sigratio
        # print(f'--ratio= {round(ratio,2)}\n')
        if phase == 3:
            val += ratio
    
        # Minimize frontier pieces
        val -= (player_frontier - opponent_frontier) / (player_frontier + opponent_frontier + 1) 
        # Mobility 
        val += (player_mobility - opponent_mobility) / (player_mobility + opponent_mobility + 1)  
        # print(f"val={val}")
        val = adjusted_sigmoid(val)
        # print(f"sigmoid val={val}")
        return val
    
    def evaluate_action(self, state, action, player, game_instance):
        print(f"+++evaluate_action()")
        val = 0
        last_index = game_instance.size - 1
        # IF CORNER
        if self.is_corner(action, last_index):
            print(f"---action in corner")
            val = 0.5
        # IF NEXT TO CORNER
        elif self.is_corner_adjacent(action, last_index):
            print(f"--- action next to corner ")
            val = -0.5
        # IF ON EDGE BUT NOT CORNER ADJACENT AND NOT CONNECTED TO CORNER
        elif self.is_edge(action, last_index) and not self.is_corner_adjacent(action, last_index) and not self.connects_to_corner(action, game_instance.state, player):
            print(f"---action on edge")
            val = 0.3
        # IF ON EDGE AND CONNECTED TO CORNER 
        elif self.is_edge(action, last_index) and self.connects_to_corner(action, game_instance.state, player):
            print(f"---action connected to corner")
            val = 0.4
        # IF EDGE ADJACENT
        elif self.is_edge_adjacent(state, action, last_index):
            print(f"---action edge adjacent")
            val = -0.3
        return val

        # calculate if player has more available moves than opponent
        playeravails = game_instance.available_actions(state, player)
        opponent = game_instance.switchplayer(player)
        oppavails = game_instance.available_actions(state, opponent)
        if len(playeravails) > len(oppavails):
            print(f"---player has more available moves")
            val += 0.5
        elif len(playeravails) < len(oppavails):
            print(f"---opponent has more available moves")
            val -= 0.5
        # val += min(1, len(avails)/10)

        return val

    def save_data(self, filename):
        with open(f'qtables/{filename}.pickle', 'wb') as f:
            # print(f"+++saving qtable: {self.q}")
            pickle.dump(self.q, f)

    @classmethod
    def load_data(self, filename ):
        with open(f'qtables/{filename}.pickle', 'rb') as f:
            q = pickle.load(f)
            return q


def print_q_table(q_table):
    for key, value in q_table.items():
        player, state, action = key  # Unpack the key
        # Convert state to a readable format
        state_str = '\n'.join(' '.join('X' if cell == 1 else 'O' if cell == -1 else '.' for cell in row) for row in state)
        
        # Determine player's color for printing
        player_str = 'BLACK' if player == 1 else 'WHITE'
        
        # Format and print the information
        print(f"Player: {player_str}")
        print(f"State:\n{state_str}")
        print(f"Action: {action}")
        print(f"Q-value: {value}")
        print("-" * 40)  # Separator for readability



def train(n, alpha=0.5, epsilon=0.5, filename='testing'):
    """
    Train an AI by playing `n` games against itself.
    """
    ai = OthelloAI(alpha, epsilon)
  # print(f'...filename= {filename}')
    maxeval = -float('inf') 
    mineval = float('inf')
    print(f'---maxeval={maxeval}')

    def epsilon_decay(initial_epsilon, iteration, total_iterations, min_epsilon=0.01, decay_rate=0.01):
        
        # EXPONENTIAL DECAY
        epsilon = min_epsilon + (initial_epsilon - min_epsilon) * math.exp(- decay_rate * iteration)

        return epsilon

    # if file isnt 'testing', check if it exists
    if filename != 'testing':
        if os.path.exists(f'qtables/{filename}.pickle'):
          # print(f"Loading qtable from {filename}")
            #### LOAD IT
            ai.q = ai.load_data(filename)

    # ai0wins = 0
    completed = 0
    ####      PLAY N GAMES
    for i in range(n):
        # print(f'---i= {i}, n= {n}, self.epsilon={ai.epsilon}')
        # LINEAR DECAY
        
        print(f'---EPSILON={round(ai.epsilon, 2)}')
        print(f"\n>>>>>>>>>>Playing training game {i + 1}")
        game = Othello()
        # print(f"...q dict={ai.q}")
        ####      Keep track of last move made by either player
        last = {
            BLACK: {"state": None, "action": None},
            WHITE: {"state": None, "action": None}
        }
        # print(f"...last={last}")
        moves = 0
        ####      GAME LOOP PLAYS 1 GAME
        while True:
            print(f'\n>>>GAME MOVE FOR {game.playercolor(game.player)}')
            moves += 1
            opponent = game.switchplayer(game.player)

            ####      CHOOSE ACTION FROM Q TABLE
            actions = ai.choose_q_action(game.state, game.player, game)
            if  actions is None:
                # print(f"---no actions")
                game.player = game.switchplayer(game.player)
                continue

            action = actions[0]
          # print(f"... q action just chosen ={actions[0]} ")
            
            ####      KEEP TRACK OF LAST STATE (BEFORE MOVE) AND ACTION
            last[game.player]["state"] = game.state
            last[game.player]["action"] = action

            ####      MAKE MOVE
            new_state = game.move(game.state, action, game.player)
            # print(f"/...AFTER MOVEfor player {game.player}")
            # game.printboard(new_state)

            ####      1 CHECK FOR GAME OVER, UPDATE Q VALUES WITH REWARDS
            if game.gameover(new_state):
                print(f"...game over. winner = {game.winner}")
                game.winner = game.calc_winner(new_state)
           
                ####     PLAYER WON
                if game.player == game.winner:
                    # print(f"...winning move for {game.playercolor(game.player)}={last[game.player]['action']}")
                    # print(f"...last[game.player]={last[game.player]}")
                    # game.printboard(last[game.player]['state'])
                    
                    ai.update( last[game.player]["state"],  last[game.player]["action"], new_state,  1, game, game.player)

                    ai.update( last[opponent]["state"],  last[opponent]["action"], new_state, -1, game, opponent )

                #####     PLAYER LOST
                elif game.winner is not game.player:
                    assert game.winner != game.player
                    # print(f"...last[game.player]={last[game.player]}")
                    ai.update( last[game.player]["state"], last[game.player]["action"], new_state, -1, game, game.player)

                    ai.update( last[opponent]["state"],  last[opponent]["action"],  new_state,  1,  game, opponent)

                ####     IT WAS A TIE
                else:
                    assert game.winner == None
                    ai.update(last[BLACK]["state"], last[BLACK]["action"], game.state,  0, game, game.player) 
                    ai.update( last[WHITE]["state"], last[WHITE]["action"], game.state, 0, game, opponent)

                    #### UPDATE DOES NOT NEED PLAYER ARG !!!!!

                break

            ####      2 IF GAME NOT OVER, UPDATE Q VALUES WITH REWARDS

            ####  EVALUATE BOARD
            # print(f"\n---evaluate board")
            evaluation = ai.evaluate_board_2(new_state, game.player, game)
            # print(f"---evaluation= {round(evaluation,2)}")
            if evaluation > maxeval:
                maxeval = evaluation
            if evaluation < mineval:
                mineval = evaluation
            ####     UPDATE Q TABLE
            ai.update(game.state, action, new_state, evaluation, game, game.player)

            game.printboard(new_state, action)

            ####      SAVE THE NEW STATE
            game.state = new_state

            ####      SWITCH PLAYERS . 
            # print(f"...switch player")
            game.player = game.switchplayer( game.player)
            # print(f"...player after switching={game.player}\n")
            # if moves == 100:
            #     break

        completed += 1
        if completed % 100 == 0:
            print(f"played games = {completed}")
            
        # print(f"...q table at end of game = {ai.q}")
    print(f"Done training {completed} games, saved as {filename}.pickle q")
    print(f'---maxratio={round(ai.maxratio,2)}, minratio={round(ai.minratio,2)}')
    print(f'---maxeval= {round(maxeval,2)}, minval = {round(mineval,2)}')
    print(f'--length of qtable = {len(ai.q)}')
    # print(f"...q table = {ai.q}")

    ai.save_data(filename)

    ####      RETURN THE TRAINED AI
    return ai



def evaluate(n, testq, benchmarkq=None):
    """
    Evaluate the performance of `ai` against `benchmarkai` by playing `n` games.
    """
    
       
    testai = OthelloAI()
    
    testai.q = testai.load_data(testq)
    benchmarkai = OthelloAI()
    if benchmarkq:
        benchmarkai.q = benchmarkai.load_data(benchmarkq)
    benchmarkai.color = WHITE

    # print(f'---testai.q={testai.q}')
    # print(f"---benchmark.q={benchmarkai.q}")
    # print(f'---tyoe of benchmarkai.q={type(benchmarkai.q)}')    

    wins = 0
    losses = 0
    ties = 0

    # print(f'---testai.q={testai.q}')
    ####     CALC EVERY OTHER GAME
    for i in range(n):
        game = Othello()
        # every other game, switch starter:
        if i % 2 == 0:
            print(f'---i= {i} is even')
            testai.color = BLACK
            benchmarkai.color = WHITE
        else:
            print(f'---i= {i} is odd')
            testai.color = WHITE
            benchmarkai.color = BLACK
        print(f"\nPLAYING EVALUATION GAME {i + 1}\n")
        # print(f"---testai.color={testai.printcolor}")
        # print(f"---benchmarkai.color={benchmarkai.printcolor}")
        

        while not game.gameover(game.state):
            print(f"\n===MOVE ")

            # print(f'===before move')
            # game.printboard(game.state)

            ####    FOR WHOEVER IS PLAYING, CHOOSE AN ACITON
            if game.player == testai.color:

                ####    MOVE IS FOR TESTAI
                print(f"===TESTAI TO MOVE as {game.playercolor(testai.color)}")
                # print(f"===game.player= {game.playercolor}  ")
                print(f'---CHOOSE Q ACTION')
                action = testai.choose_q_action(game.state, game.player, game, epsilon=False)
                print(f"---ai action={action}")  
                if not action:
                    print(f"---no action")
                    action = testai.choose_evaluated_action(game.state, game.player, game)
                
                # print(f"---ai action={action}")
           
            else:
                ####   MOVE IS BENCHMARKAI
                print(f"=== BENCHMARK TO MOVE as {game.playercolor(benchmarkai.color)} ")
               

                actions = game.available_actions(game.state, game.player)
                # print(f"---actions={actions}")
                action = None
                if actions:
                    randomaction = random.choice(list(actions.items()))
                    # print(f"---random action={randomaction}")
                    action = randomaction
                # print(f"---bench action={action}")
                # action = benchmarkai.choose_q_action(game.state, game.player, game, epsilon=False)
             
            ####    MAKE THE MOVE IF THERE IS ONE
            # print(f"===action={action}")
            if action is not None:
                action = action[0]
                print(f'---action[0]={action}')
                newboard = game.move(game.state, action, game.player)
                print(f"===game state after move")
                game.printboard(newboard, action)
                game.state = newboard
            else:
                print(f"---no action!!!!!!!")
                

            ####     OTHERWISE SEE IF THE OTHER PLAYER CAN MOVE
            if game.gameover(newboard):
                print(f"===game over")
                game.calc_winner(newboard)
                game.printboard(newboard)
                print(f"---game.winner= {game.winner}")
                print(f"---testai.color= {testai.color}")
                if game.winner == testai.color:
                    wins += 1
                    print(f"---END OF GAME {i+1}, \nTESTAI WINS. wins= {wins}||||||||||||\n")
                elif game.winner == benchmarkai.color:
                    losses += 1
                    print(f"---END OF GAME {i+1}. BENCHMARKAI WINS. \nlosses = {losses}||||||||||||\n")
                elif game.winner == None:
                    ties += 1
                    print(f"---END OF GAME {i+1} \nTIE. ties={ties}||||||||||||\n")
                break
            game.player = game.switchplayer(game.player)
        print(f"---END OF GAME {i+1}")
    
    # win/loss ratio
    if losses == 0:
        winlossratio = 1
    else:
        winlossratio= wins/losses
    winrate = wins / n  
        
    print(f"wins: {wins}, losses: {losses}, ties: {ties}")
    print(f"win/loss ratio= {round(winlossratio, 2)}:1")
    print(f"winrate= {winrate}")
    ### print the q table used
    print(f"testq= {testq} len={len(testai.q)}")


if __name__ == "__main__":
        app.run(debug=True)
