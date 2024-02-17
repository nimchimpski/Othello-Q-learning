import math
import random
import time
import pickle
from copy import deepcopy

EMPTY = 0
BLACK = 1
WHITE = -1
VALID = '*'

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

    # BOARD SHOWING AVAILABLE MOVES
    def boardwithavails(self, board,  human, aimove):  
        print(' ++++boardwithavails')
    
        # print(f'player={player}')
        for cell in self.available_actions( board, human):
            print(f'cell={cell}')
            board[cell[0]][cell[1]] = '*'
        # add ai's last move
        if aimove is not None:
            print(f'---human= {human}')
            if human == 1:
                board[aimove[0]][aimove[1]] = '-'
            elif human == -1:
                board[aimove[0]][aimove[1]] = '+'
        # print(f"for response board= {board}")
        self.printboard(board)
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

    def printboard(self, board):
        for row in board:
            print(row)

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
        return the updated board
        """
        print(f'\n++++move() for {player}, ')
        # self.printboard(board)
        # print(f'action={action}')
        # print(f'player={player}')
        if board is None:
            print("Board is None")
        availactions = self.available_actions(board, player)
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
        print(f'---bitstoflip= {bitstoflip}')
    

        ####  MARK BOARD WITH FLIPPED PIECES
        if bitstoflip:
            for bit in bitstoflip:
                board[bit[0]][bit[1]] = player
        # print(f'board with just  flips')
        
          #####     MARK BOARD WITH ACTUAL MOVE
        board[action[0]][action[1]] = player
        print(f'board with flips and move')
        self.printboard(board)

      
        print('END OF MOVE()')

        return board

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

        print(f'+++++direction_checker().  {compass} from candidate cell{ cell}')
        # self.printboard(board)
        originalcell = cell
        ####       SET UP VARIABLES
        captured = set()
        # nextcell = cell
        opponent = self.switchplayer(player)
        ####   RUN LOOP TO CHECK DIRECTION
        while True:
            print(f'---START SEARCH LOOP')
            # print(f'---direction={direction}')
            # print(f'opponent={opponent}')

            ####       CALCULATE NEXT CELL
            cell = self.calcnextcell(board, cell, direction)

            # if newcell is not in bounds
            if cell is None:
                # print(f'---cell is None')   
                return None
            print(f'===new cell= {cell}, original = {originalcell}')

            #### IF THE cell IS EMPTY, RETURN NONE
            if board[cell[0]][cell[1]] == 0:
                # print(f'cell is empty, so returning None')
                return None
            
            
            ####   IF  CELL IS MINE 
            if board[cell[0]][cell[1]]  == player:
                ####    AND  THERE ARE CAPTURED
                if captured:
                    print(f'{cell} is mine and captured is not empty, so returning = {captured}')
                    return captured
                else:
                    return None

            #### ELSE IF NEXT CELL IS ENEMY, ADD TO CAPTURED
            elif board[cell[0]][cell[1]] == opponent:
                print(f'opponent at {cell} in direction {compass},')
                captured.add(cell)
                print(f'captured={captured}')

    def available_actions(self, board, player):
        """
        returns a list of tuples,  with all of the available actions `(i, j)` in that state, plus the captued pieces for each move, as a set.
        """
        
        
        print(f'\n+++AVAILABLE_ACTIONS FOR {player}')
        self.printboard(board)
        actions = {}
        ####       CREATE THE DIRECTIONS
        directions = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == dj == 0)]
        # print(f'directions={directions}')

        ####        FOR EACH BOARD cell
        print('---GO THROUGH WHOLE BOARD, LOOKING FOR EMPTY CELLS')
        for i, row in enumerate(board):
            for j, content in enumerate(row):
                cell = (i,j)
                # print(f'content={content}')

                # print(f'\n ---CHECKING CELL = {cell}')
                if (content != 0) :
                    # print(f'content is not 0, so continue')
                    continue
                print(f'---{cell} is empty, so possibly valid: checking directions')
                # print(f'cell={cell}, type={type(cell[0])}')
                alldirscaptured = set()
                ####       FOR EACH DIRECTION
                for direction in directions:
                    # print(f'---checking direction= {direction}')
                    
                    ####        IF VALID , ADD MOVE TO SET, ADD CAPTURED PIECES TO SET
                    onedircaptured = self.direction_checker(board, cell, direction, player )
                    print(f'onedir_captured={onedircaptured}')
                    ####    IF THERE IS ANY ADD TO TOAL CAPTURED FOR THIS cell
                    if onedircaptured:
                        print(f'onedir_captured=true, so adding to alldirscaptured')
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
        print(f'>>>>>available actions={actions}')
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

    def update(self, old_state, action, new_state, reward, game_instance):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        player = game_instance.player
        # print(f"+++update")
        # print(f"---old_state={old_state}, action={action}, new_state={new_state}, reward={reward}")
        old = self.get_q_value( old_state, action)
        best_future = self.best_future_reward(new_state, game_instance)
        self.update_q_value( old_state, action, old, reward, best_future)
        # print(f"+++>>>update: self.q={self.q}")

    def get_q_value(self, state, action):
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

        
        q =  self.q.get(( statetuple, action), 0)
        # print(f"+++>>>get_q_value: {state}, {action} = q {q}")
        if not q:
            return None
        return q 

    def statetotuple(self, state):
        return tuple(tuple(row) for row in state)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
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
        """
        # print(f"+++UPDATEQ FOR PLAYER {player}")
        # print(f"---state={state}, action={action}, old_q={old_q}, reward={reward}, future_rewards={future_rewards}")
        if state is None or action is None:
            print(f"---!!!!!state or action is None")
            return

        if old_q is None:
            old_q = 0
   
        statetuple = self.statetotuple(state)
     
        newvalest = reward + future_rewards
        # print(f"---newvalest={newvalest}")
        ####     IF WINNER = PLAYER, REWARD = 1

        result = old_q + (self.alpha * (newvalest - old_q))
        result = round(result, 2)
        # print(f"---result={result}")
        self.q[statetuple, action] = result
        # print(f"---updateq self.q = {self.q[statetuple, action]}")
        
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
            n = self.get_q_value(state, action)
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

    def choose_q_action(self, state, game_instance, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """

        # print(f"+++choose-Q : actions=")
        # print(f"---state={state}")
        ####  convert board to tuple
        for row in state:
            for cell in row:
                if cell == EMPTY:
                    cell = 0
                elif cell == BLACK:
                    cell = 1
                elif cell == WHITE:
                    cell = -1
        # print(f"---state after={state}")

        ####    GET AVAILABLE ACTIONS

        actions = game_instance.available_actions(state, 1)
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
                # print(f"---x < epsilon, so chooseing random action")
                action = random.choice(list(actions))
                # print(f">>>EPs=True : random action= {action}")
            # else:
                # print(f'---a random action was not chosen, so use the q table to choose the best action')
        ### EPSILON FALSE: CHOOSE ACTION WITH HIGHEST Q VALUE
        ####     ALSO RETURN CAPTURES, SO CAN BE USED AS HEURISTIC
        # print(f'---action 2  = {action}')
        if not action:
            maxq = -float('inf')
            bestaction_q = None
            bestactions = []
            # print(f'---CHOOING Q ACTION HERE:')
            # print(f'---actions={actions}')

            for action in actions:
                assert action is not None
                # print(f"---action={action}")
                q = self.get_q_value(state, action)
                # print(f"---q={q}")

                ###    UNSEARCHED STATES/ACTIONS GET AWARDED 0 TODO: ???
                if q is None:
                    q = 0
                # print(f"---q={q}")
                if q > maxq:
                    #### TODO THIS COULD PICK AN ACTION WITH EQUAL Q USING A PROBABILITY, OTHERWISE IT WILL ALWAYS PICK THE LAST ACTION WITH THE HIGHEST Q
                    maxq = q
                    bestactions = [action]
                elif q == maxq:
                    bestactions.append(action)
            # print(f"---bestactions= {bestactions}")
            bestaction_q = random.choice(bestactions)
            # print(f"---bestcaction_q= {bestaction_q}")
            action = bestaction_q
        # print(f"---action 3  = {action}")
      
        # get the captured pieces
        captured = actions[action]
        # print(f"---returning={action}, {captured}")
        # print(f'+--end of choose_q_action()')
        return action, captured
    
    def evaluateboard(self,captures):
        """
        Returns a number representing the value of the current game state to the player.
        """
        # print(f'+++evaluateboard()')
        if captures == 0:
            return 0

        result = 1 - 1 / (captures + 1)
        # print(f'---result={result}')
        result = result * .5
        # print(f'---result={result}')
        # print(f'---captures based evaluation={result}')
        return result
    
    def save_data(self, filename):
        with open(f'{filename}.pickle', 'wb') as f:
            # print(f"+++saving qtable: {self.q}")
            pickle.dump(self.q, f)

    def load_data(self, filename ):
        with open(f'{filename}.pickle', 'rb') as f:
            q = pickle.load(f)
            return q
    
    @staticmethod
    def invertboard(board):
        # print(f'+++invertboard')   
        # Othello().printboard(board)
        
        board = [[-cell for cell in row] for row in board]
        # print()
        # Othello().printboard(board)      
        return board

def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    ai = OthelloAI()
    #### LOAD EXISTING Q TABLE
    # ai.q = ai.load_data('qtable')
    
    # ai0wins = 0
    completed = 0
    ####      PLAY N GAMES
    for i in range(n):
        
        # print(f"Playing training game {i + 1}")
        game = Othello()
        # print(f"^^^q dict={ai.q}")

        ####      Keep track of last move made by either player
        last = {
            BLACK: {"state": None, "action": None},
            WHITE: {"state": None, "action": None}
        }
        # print(f"^^^last={last}")

        ####      GAME LOOP PLAYS 1 GAME
        while True:
            print(f"\n^^^player = {game.player}")
            opponent = game.switchplayer(game.player)
            # print(f"^^^opponent = {opponent}")

            ####      KEEP TRACK OF CURRENT STATE AND ACTION
            new_state = deepcopy(game.state)
            # print(f"^^^GAME.STATE=")
            # game.printboard(game.state)
            # print(f"^^^ STATECOPY=")
            # game.printboard(new_state)

            ####     CHECK IF PLAYEING AS WHITE
            if game.player == WHITE:
                lookup_board = OthelloAI.invertboard(new_state)
            else:
                lookup_board = new_state

            ####      CHOOSE ACTION FROM Q TABLE
            actions = ai.choose_q_action(lookup_board, game)
            if  actions is None:
                # print(f"---no actions")
                game.player = game.switchplayer(game.player)
                continue

            action = actions[0]
            # print(f"^^^ q action just chosen ={actions[0]} ")
            
            ####      KEEP TRACK OF LAST STATE (BEFORE MOVE) AND ACTION
            last[game.player]["state"] = game.state
            last[game.player]["action"] = action

            ####      MAKE MOVE
            new_state = game.move(new_state, action, game.player)
            # print(f"/^^^AFTER MOVEfor player {game.player}")
            # game.printboard(new_state)

            ####     EVALUATE NEW STATE - IF GAME NOT OVER
            # number of captures?
            if not game.gameover(new_state):
                captures = len(actions[1])
                # print(f"^^^captures={captures}")
                evaluation = ai.evaluateboard(captures)
                # print(f"^^^evaluation={evaluation}")

                ####     UPADTE Q VALUES
                ai.update(game.state, action, new_state, evaluation, game)

            ####      WHEN GAME IS OVER, UPDATE Q VALUES WITH REWARDS
            if game.gameover(new_state):
                game.winner = game.calc_winner(new_state)
                # game.printboard(new_state)
                # print(f"---game.winner= {game.winner}")
                # print(f'---game.player= {game.player}')
                # print(f"---last[game.player]['state']={last[game.player]['state']}")
                # print(f"---last[game.player]['action']={last[game.player]['action']}")
                # print(f'---last[game.opponent]["state"]={last[opponent]["state"]}')
                # print(f'---last[game.opponent]["action"]={last[opponent]["action"]}')
                ####     PLAYER WON
                if game.player == game.winner:
                    # print(f"^^^last[game.player]={last[game.player]}")
                    ai.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    game.state,
                    1,
                    game)
                    ai.update(
                    last[opponent]["state"], 
                    last[opponent]["action"],
                    game.state,
                    -1,
                    game
                    )
                #####     PLAYER LOST
                elif game.winner is not game.player:
                    assert game.winner != game.player
                    # print(f"^^^last[game.player]={last[game.player]}")
                    ai.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    game.state,
                    -1,
                    game)
                    ai.update(
                    last[opponent]["state"], 
                    last[opponent]["action"], 
                    game.state, 
                    1, 
                    game)

                ####     IT WAS A TIE
                else:
                    assert game.winner == None
                    ai.update(
                    last[BLACK]["state"],

                    last[BLACK]["action"],
                    game.state, 
                    0.1,
                    game)
                    ai.update(
                    last[WHITE]["state"],
                    last[WHITE]["action"],
                    game.state,
                    0.1,
                    game)

                    #### UPDATE DOES NOT NEED PLAYER ARG !!!!!

                break

            ####      IF GAME IS CONTINUING, NO REWARDS YET
            
            elif last[game.player]["state"] is not None:
                # print(f"^^^continue game - update q values")
                ai.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    game.state,
                    0,
                    game
                ) # FN GETS PLAYER FROM GAME INSTANCE!!!!!!!
            # print(f"^^^q table at end of move = {ai.q}")   

            ####      SAVE THE NEW STATE
            game.state = new_state

            ####      SWITCH PLAYERS . 
            # print(f"^^^switch player")
            game.player = game.switchplayer( game.player)
            # print(f"^^^player after switching={game.player}\n")

        completed += 1
        if completed % 100 == 0:
            print(f"played games = {completed}")
        # print(f"^^^q table at end of game = {ai.q}")
    print(f"Done training {completed} games")
    print(f"^^^q table = {ai.q}")
    ####      RETURN THE TRAINED AI
    return ai


if __name__ == "__main__":
        app.run(debug=True)
