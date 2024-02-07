import math
import random
import time
from copy import deepcopy

EMPTY = 0
BLACK = 1
WHITE = -1
VALID = '*'

class Othello():

    def __init__(self, size=4):
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
    def boardwithavails(self, board,  player):  
        print('# ++++boardforresponse')
    
        # print(f'player={player}')
        for cell in self.available_actions( board, player):
            # print(f'cell={cell}')
            board[cell[0]][cell[1]] = '*'
        print(f"response() board=")
        self.printboard(board)
        return board
       
    def switchplayer(self, player):
        # print(f'+++switchplayer()')
        # print(f'player={player}')
        assert player in [BLACK, WHITE]
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
        Make the move `action` for the current player.
        `action` must be a tuple `(i,j)`.
        return the updated board
        """
        # print(f'\n++++move(), ')
        # print(f'board={board}')
        # print(f'action={action}')
        # print(f'player={player}')
        if board is None:
            print("Board is None")
        availactions = self.available_actions(board, player)
        # print(f'availactions={availactions}')
     
        # print(f'player={self.player}')


        #####      IS ACTION VALID
         # Check if the action is valid
        assert action in availactions, f"Action {action} not in available actions {availactions}"
        if action not in availactions:
            print("\n>>>>Error: Action not in available_actions.")
            return board  # Or handle the error differently
        # else:
            # print(f'Action is valid')

        ####     GET BITS TO FLIP
      
        bitstoflip = availactions[action]
    

        ####  MARK BOARD WITH FLIPPED PIECES
        if bitstoflip:
            for bit in bitstoflip:
                board[bit[0]][bit[1]] = player
        # print(f'board with just  flips')
        
          #####     MARK BOARD WITH ACTUAL MOVE
        board[action[0]][action[1]] = player
        # print(f'board with flips and move= {board}')

      
        # print('END OF MOVE()')

        return board

    def direction_checker(self, cell, direction, player, board):

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

        # print(f'+++++direction from {cell} in direction { compass}')
        
        ####      CHECK FOR TEST CONDITIONS


        ####       SET UP VARIABLES
        captured = set()
        nextcell = cell

        def calcnextcell():
            # print(f'+++calcnextcell ')
            result = tuple(c + d for c,d in zip(nextcell, direction)) 
            ####       IS THE NEW CELL ON THE BOARD?
            if result[0] < 0 or result[0] >= self.size or result[1] < 0 or result[1] >= self.size:
                # print(f'OUT OF BOUNDS')
                return None
            # print(f'result={result}')
            return result
        
        ####   RUN LOOP TO CHECK DIRECTION
        while True:
            ####       CALCULATE NEXT CELL
            nextcell = calcnextcell()
            if nextcell is None:
                return None
            # print(f'first nextcell calc={nextcell}')

            ### CALCULATE opponent
            opponent = self.switchplayer(player)

            ####       IF NEXTCELL IS NOT opponent, ABORT?
            if not board[nextcell[0]][nextcell[1]] == opponent:
                # print(f'NOT opponent NEIGHBOUR')
                return None

            ####       FOUND ENENY
            # print(f'opponent at {nextcell} in direction {compass},')
            captured.add(nextcell)
            # print(f'captured={captured}')

        
            ####       LOOK FOR A PLAYER PIECE IN THAT DIRECTION TO VALIDATE MOVE
            further = calcnextcell()
            # print(f'calc2 for player piece at end ={further}')
            if further and (board[further[0]][further[1]] == player):
                # print(f'FOUND PLAYER AT END! {nextcell}')
                # print(f'captured in this direction={captured}')
                return captured
            else:
            ####       NO PLAYER PIECE IN THAT DIRECTION, INVALID MOVE
                # print(f'----NO PLAYER PIECE AT END :(')
                # captured = set()
                return None
          
    def available_actions(self, board, player):
        """
        returns a list of tuples,  with all of the available actions `(i, j)` in that state, plus the captued pieces for each move, as a set.
        """
        
        
        # print(f'+++availale_actions for {player}')
        # self.printboard(board)
        actions = {}
        ####       CREATE THE DIRECTIONS
        directions = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == dj == 0)]
        # directions = [(0,-1), (-1,-1)]
        # print(f'directions={directions}')

        ####        FOR EACH BOARD cell
        for i, row in enumerate(board):
            for j, content in enumerate(row):
                cell = (i,j)
                # print(f'content={content}')

                # print(f'\n >>>CHECKING THIS = {cell}')
                if (content == 1) or (content == -1) :
                    # print(f'content is not EMPTY nor *, so continue')
                    continue
                
                # print(f'cell={cell}, type={type(cell[0])}')
                alldirscaptured = set()
                ####       FOR EACH DIRECTION
                for direction in directions:
                    
                    ####        IF VALID , ADD MOVE TO SET, ADD CAPTURED PIECES TO SET
                    onedircaptured = self.direction_checker(cell, direction, player, board )
                    # print(f'onedir_captured={onedircaptured}')
                    ####    IF THERE IS ANY ADD TO TOAL CAPTURED FOR THIS cell
                    if onedircaptured:
                        # print(f'onedir_captured=true')
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
        # print(f'>>>>>actions={actions}')
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
                if cell == BLACK:
                    black_score += 1
                elif cell == WHITE:
                    white_score += 1
        # print(f'black_score={black_score}')
        # print(f'white_score={white_score}')
        return (black_score, white_score)

    def calc_winner(self, board):
        black, white = self.scores(board)
        if black > white:
            self.winner = BLACK
            return BLACK
        elif white > black:
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
            # print(f'+++gameover: board is full')
            return True

        ####   CHECK IF NEITHER PLAYER HAS ANY VALID MOVES
        if (not self.available_actions(  board, -1) and not self.available_actions(board, 1)):
            return True
        # print(f'----end of gameover()')
        return False
        
    def evaluateboard(self,captures):
        """
        Returns a number representing the value of the current game state to the player.
        """
        # print(f'+++evaluateboard()')
        if captures == 0:
            return 0

        result = 1 - 1 / (captures + 1)
        return result
       

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
        """
        if state is None or action is None:
            print(f"---!!!!!state or action is None")
            return

        if old_q is None:
            old_q = 0
   
        statetuple = self.statetotuple(state)
     
        newvalest = reward + future_rewards
 
        result = old_q + (self.alpha * (newvalest - old_q))
        result = round(result, 2)
        self.q[player, statetuple, action] = result
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
            n = self.get_q_value(game_instance.player, state, action)
            if n is None:
                n = 0
            qlist.append(n)
        # print(f"---qlist={qlist} len={len(qlist)}")
        best = max(qlist)
        # print(f"---best={best}")
        # gamma = (1 - self.epsilon)
        gamma = 1
        result =  gamma * best
        # print(f"---result={result}")
        # print(f">>>best={best}")
        return result
        
    

        # get max of the q values

    def choose_q_action(self, state, player, game_instance, epsilon=False):
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
        actions = game_instance.available_actions(state, player)
        # print(f"---actions={actions}")
        ####  IF ONLY ONE ACTION RETURN IT
        # if len(actions) == 1:
        #     return list(actions)[0]

        ####  

        # WITH EPSILON TRUE: CHOOSE RANDOM ACTION WITH EPSILON PROB
        if epsilon == True:
            # print(f"---epsilon = {epsilon}")
            x = random.random()
            print(f"---random x = {x}")
            if x < self.epsilon:
                action = random.choice(list(actions))
                # print(f">>>EPs=True : random action= {action}")
                return action

        ####     IF NO Q VALUES, CHOOSE ACTION WITH MOST CAPTURES/BITSTOFLIP
        # calculate longest tuple in actions
        # print(f"---actions={actions}")
   

        ####    CHOOSE  ACTION WITH BEST Q VALUE
        maxq = 0
        bestaction_q = None
        # print(f'---CHOOING Q ACTION HERE:')
        for action in actions:
            q = self.get_q_value(player, state, action)
            if q is None:
                q = 0
            # print(f"---q={q}")
            if q >= maxq:
                maxq = q
                bestaction_q = action
            # print(f"---bestcaction={bestaction_q}")
        # bestaction could be none
        # get the captured pieces
        captured = actions[bestaction_q]
        # print(f"---captured={captured}")
        # print(f'+--end of choose_q_action()')
        return bestaction_q, captured
    


def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    ai = OthelloAI()
    # ai0wins = 0
    completed = 0
    ####      PLAY N GAMES
    for i in range(n):
        
        print(f"Playing training game {i + 1}")
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

            ####      KEEP TRACK OF CURRENT STATE AND ACTION
            new_state = deepcopy(game.state)
            # print(f"^^^GAME.STATE=")
            # game.printboard(game.state)
            print(f"^^^ STATECOPY=")
            game.printboard(new_state)

            ####      CHOOSE ACTION FROM Q TABLE
            actions = ai.choose_q_action(new_state, game.player, game)
            action = actions[0]
            print(f"^^^ q action just chosen ={action}")
            
            ####      KEEP TRACK OF LAST STATE AND ACTION
            last[game.player]["state"] = new_state
            last[game.player]["action"] = action

            ####      MAKE MOVE
            new_state = game.move(new_state, action, game.player)
            print(f"/^^^AFTER MOVE:")
            game.printboard(new_state)

            ####     EVALUATE NEW STATE
            # number of captures?
            captures = len(actions[1])
            print(f"^^^captures={captures}")
            evaluation = game.evaluateboard(captures)
            print(f"^^^evaluation={evaluation}")

            ####     UPADTE Q VALUES
            ai.update(game.state, action, new_state, evaluation, game)

            ####      WHEN GAME IS OVER, UPDATE Q VALUES WITH REWARDS
            if game.gameover(new_state):
                print(f"^^^gameover={game.gameover(new_state)}")
                game.winner = game.calc_winner(new_state)
                # print(f"^^^game.calc_winner= {game.calc_winner(new_state)}")
                print(f"^^^game.winner= {game.winner}")
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
        # print(f"^^^q table at end of game = {ai.q}")
    print(f"Done training {completed} games")
    print(f"^^^q table = {ai.q}")
    ####      RETURN THE TRAINED AI
    return ai


if __name__ == "__main__":
        app.run(debug=True)
