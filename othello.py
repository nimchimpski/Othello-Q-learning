import math
import random
import time

EMPTY = ' '
BLACK = 'X'
WHITE = 'O'

class Othello():

    def __init__(self, size=4, human=BLACK):
        """
        Initialize game board.
        Each game board has
            - size: defined by user
        """
        # (print('\n+++init'))
        self.size = size
        self.board = self.create_board()
        # self.board = [[WHITE,WHITE, WHITE],
        #               [EMPTY,WHITE,WHITE],
        #               [WHITE,WHITE,BLACK]]
        self.turnsplayed = 0
        self.player = BLACK
        self.enemy = WHITE
        # print(f'player={self.player}')
        self.human = human
        # print(f'human={human}')
        self.winner = None
        # print(f'----end of init')
        # self.availactions = self.available_actions()
    
    def printboard(self):
        # print('\n+++printboard')
        # print(f'player={self.player}')
        # print(f'enemy={self.enemy}')
        # print(f'turnsplayed={self.turnsplayed}')
        avacts = self.available_actions()
        # print(f'avacts={avacts}'    )
        print('\n***OTHELLO***\n')
        
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if self.board[i][j] == BLACK:
                    print("X", end="")
                elif self.board[i][j]== WHITE:
                    print("O", end="")
                elif (i,j) in avacts:
                    print("*", end="")
                elif self.board[i][j]== EMPTY:
                    print(".", end="")
            print()
        print()
       
    def switchplayer(self, player):
        if player == BLACK:
            if available_moves(player):
                return WHITE
        else:
            return BLACK

    def calculate_opponent(self, player):
        if player == BLACK:
            return WHITE
        else:   
            return BLACK

    def update_player(self, turnsplayed=None):
        if turnsplayed is None:
            turnsplayed = self.turnsplayed
        # print('\n+++update_player')
        # print(f'turnsplayed={self.turnsplayed}')
        if turnsplayed %2 == 0:
            self.player = BLACK
            self.enemy = WHITE
            # print(f'player now black?={self.player}')
        else:
            self.player = WHITE
            self.enemy = BLACK
            # print(f'player now white?={self.player}')
        # print(f'end of update_player')
        return self.player, self.enemy

    def create_board(self):
        # print('+++create_board')
        board = []
        for i in range (self.size):
            row = []
            for j in range (self.size):
                row.append(EMPTY)
            board.append(row)
        center = int((self.size/2)-1)
        board[center][center] = WHITE
        board[center][center+1] = BLACK
        board[center+1][center] = BLACK
        board[center+1][center+1] = WHITE
        return board

    def move(self, action, availactions=None):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i,j)`.
        return the updated board
        """
        # print(f'\n++++++++++++++++++++++++++++move()')
        if availactions is None:
            availactions = self.available_actions()
        print(f'availactions={availactions}')
        # print(f'turnsplayed={self.turnsplayed}')
        # print(f'player={self.player}')

        ####       Check for errors
        if self.winner is not None:
            raise Exception("Game already won")

        #####      IS ACTION VALID
        try:
            availactions.get(action)
        except ValueError:
            print(f"\n>>>>Error:  not in available_actions, or availactions is problematic")

        ####       FLIP CAPTURED PIECES
        # print(f'action={action}'    )
        # print(f'availactions={availactions}')
        try:
            bitstoflip = availactions.get(action)
        except AttributeError:
            print("ERROR! no bitstoflip in available_actions")
        # print(f'bitstoflip={bitstoflip}')
        if bitstoflip:
            for bit in bitstoflip:
                self.board[bit[0]][bit[1]] = self.player
        
          #####     MARK BOARD WITH MOVE
        self.board[action[0]][action[1]] = self.player
        self.printboard()
        # print(f'board after flip')
        # print(f'{self.player} just moved at {action}')

        ####       CHECK IF GAME OVER
        if self.gameover():
            self.winner = self.calc_winner()
            # print(f'GAME OVER! winner={self.winner}')
            return 
      
        ####       Update turnsplayed   
        self.turnsplayed += 1
        # print(f'turnsplayed={self.turnsplayed}')
        self.update_player()
        # print(f'----ENF OF MOVE()')
        return self.board

    def direction_checker(self, cell, direction, player=None):

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
        if player is None:
            player = self.player

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

            ### CALCULATE ENEMY
            enemy = self.calculate_opponent(player)

            ####       IF NEXTCELL IS NOT ENEMY, ABORT?
            if not self.board[nextcell[0]][nextcell[1]] == enemy:
                # print(f'NOT ENEMY NEIGHBOUR')
                return None

            ####       FOUND ENENY
            # print(f'enemy at {nextcell} in direction {compass},')
            captured.add(nextcell)
            # print(f'captured={captured}')

        
            ####       LOOK FOR A PLAYER PIECE IN THAT DIRECTION TO VALIDATE MOVE
            further = calcnextcell()
            # print(f'calc2 for player piece at end ={further}')
            if further and (self.board[further[0]][further[1]] == player):
                # print(f'FOUND PLAYER AT END! {nextcell}')
                # print(f'captured in this direction={captured}')
                return captured
            else:
            ####       NO PLAYER PIECE IN THAT DIRECTION, INVALID MOVE
                # print(f'----NO PLAYER PIECE AT END :(')
                # captured = set()
                return None
          
    def available_actions(self, player=None):
        """
        returns a list of tuples,  with all of the available actions `(i, j)` in that state, plus the captued pieces for each move, as a set.
        """
        # print('+++availale_actions()')
        if player is None:
            player = self.player
        actions = {}
        ####       CREATE THE DIRECTIONS
        directions = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == dj == 0)]
        # directions = [(0,-1), (-1,-1)]
        # print(f'directions={directions}')

        ####        FOR EACH BOARD cell
        for i, row in enumerate(self.board):
            # print(f' x= {x}')
            for j, content in enumerate(row):
                cell = (i,j)

                # print(f'\n >>>CHECKING THIS = {cell}')
                if content != EMPTY:
                    continue
                
                # cell = (int(cell[0]), int(cell[1]))
                # print(f'cell={cell}, type={type(cell[0])}')
                alldirscaptured = set()
                ####       FOR EACH DIRECTION
                for direction in directions:
                    
                    ####        IF VALID , ADD MOVE TO SET, ADD CAPTURED PIECES TO SET
                    onedircaptured = self.direction_checker(cell, direction, player )
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
        # print(f'actions={actions}')
        self.availactions = actions
        return actions
   
    def scores(self, board=None):
        """
        Returns a tuple (black_score, white_score) for the current game state.
        """
        # print(f'+++scores()')
        if board is None:
            board = self.board
        black_score = 0
        white_score = 0
        for row in self.board:
            for cell in row:
                if cell == BLACK:
                    black_score += 1
                elif cell == WHITE:
                    white_score += 1
        # print(f'black_score={black_score}')
        # print(f'white_score={white_score}')
        return (black_score, white_score)

    def calc_winner(self):
        black, white = self.scores()
        if black > white:
            self.winner = BLACK
            return BLACK
        elif white > black:
            self.winner = WHITE
            return WHITE
        else:
            return None

    def gameover(self):
        """
        Returns True if game is over, False otherwise.
        """
        # print(f'+++gameover()')
        if self.winner is not None:
            return True
        ####    CHECK IF BOARD IS FULL
        if not any(cell == EMPTY for row in self.board for cell in row):
            return True

        ####   CHECK IF NEITHER PLAYER HAS ANY VALID MOVES
        if (not self.available_actions() and not self.available_actions(self.enemy, self.player)):
            return True
        # print(f'----end of gameover()')
        return False
        


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        # print(f"+++update")
        # print(f"---old_state={old_state}, action={action}, new_state={new_state}, reward={reward}")
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)
        # print(f"+++>>>update: self.q={self.q}")

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        # self.q = ((0, 0, 0, 2), (3, 2): -1,
        # print
        if not state or not action:
            return 0   
        # print(f"---state type= {type(state)}")
        statetuple = tuple(state)
        # print(f"---state type= {type(statetuple)}")

        
        q =  self.q.get((statetuple, action), 0)
        # print(f"+++>>>get_q_value: {state}, {action} = q {q}")
        return q 

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        if state is None or action is None:
            # print(f"---!!!!!state or action is None")
            return
   
        statetuple=tuple(state)
     
        newvalest = reward + future_rewards
 
        result = old_q + (self.alpha * (newvalest - old_q))
        result = round(result, 2)
        self.q[statetuple, action] = result
        # print(f"---updateq self.q = {self.q[statetuple, action]}")
        

    def best_future_reward(self, state):
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
        actions =  Nim.available_actions(state)
        # print(f"+++best_future: actions={actions} len={len(actions)})") 
        if not actions:
            # print(f"---no actions")
            return 0
        # get q value for actions
        qlist = []
        for action in actions:
            # print(f"---action={action}")
            # print(f"---q = {self.get_q_value(state, action)})")
            qlist.append(self.get_q_value(state, action))
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

    def choose_action(self, state, epsilon=True):
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
        actions = Nim.available_actions(state)
        # print(f"---actions = {actions}")
        if len(actions) == 1:
            return list(actions)[0]
        # print(f"+++choose_action: {actions}")
        if epsilon == True:
        # With Epsilon True: choose random action with epsilon prob
            # print(f"---epsilon = {epsilon}")
            x = random.random()
            # print(f"---random x = {x}")
            if x < self.epsilon:
                action = random.choice(list(actions))
                # print(f">>>EPs=True : random action= {action}")
                return action

        # else choose best action
        max = 0
        bestaction = None
        for action in actions:
            if not bestaction:
                bestaction = action
            # print(f"---action in loop={action}")
            q = self.get_q_value(state, action)
            # print(f"---q={q}")
            if q >= max:
                max = q
                bestaction = action
        # print(f">>>chooseaction={bestaction}")
        return bestaction

    # def printq(self,x):
    #     for key,val in self.q.items():
    #         # print(f"///{key[0][1]}")
    #         if key[0] == x:  # enter state you want to inspect

    #             print(f"result = {key,':',val}")
    #             print(f"result = {key} : {val}")

def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = NimAI()
    # player0wins = 0

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()
        # print(f"---q dict={player.q}")

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:
            # print(f"\n---player = {game.player}")

            # Keep track of current state and action
            state = game.piles.copy()
            # print(f"---state={state}")
            action = player.choose_action(game.piles)
            # print(f"---action={action}")

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # print(f"---{game.player}'s last = {last[game.player]}")

            # Make move
            game.move(action)
            new_state = game.piles.copy()
            # print(f"---new_state={new_state}")

            # When game is over, update Q values with rewards
            if game.winner is not None:
                # print(f"\n***winner = {game.winner} so update q")
                # if game.winner == 0:
                #     player0wins += 1 
                player.update(state, action, new_state, -1)
                # print(f"---state action = {state, action}")
                # print(f"---{state}{action} = {player.q[(tuple(state), action)]}")
                

                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                # print(f"---q table size = {len(player.q)}")
                # print(f"---q table: {player.q}")
                # player.printq((1,3,5,7))
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                # print(f"---continue game")
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )
            # print(f">>>endloop Tain")
        # firstplayerwins = player0wins/n
        # secondplayerwins = 1 - firstplayerwins
        # print(f"\n---{n} games played")
        # print(f"first player wins {firstplayerwins}")
        # print(f"second player wins {secondplayerwins}\n")

    print("Done training")

    # Return the trained AI
    return player


def playterminal(player0=0, player1=1):
    """
    Play game between 2 humans or human game against the AI.
    `player0 = AI, human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """
    # Create new game
    game = Othello()

    # If no player order set, choose human's order randomly
    if game.human is None:
        game.human = random.randint(0, 1)



    # Game loop
    while True:

        # Print board
        game.printboard()
        print('. is empty')
        print('* is available move')
        print(f'00 is top left, 0{game.size-1} is top right')
        if game.turnsplayed == 0:
            print(f'X plays first')
        print()
        ####     CHECK FOR GAME OVER

        if game.gameover():
            game.calc_winner()
            print(f'GAME OVER! winner={game.winner}')
            playagain = input("Play again? (y/n): ")
            if playagain == 'y':
                game = Othello()
                continue
            else:
                return

            # CHECK IF AVAILABLE ACTIONS FOR BLACK
        if not game.available_actions():
                print(f"no available moves for {game.player}")
                print(f"{game.enemy} to play")
                game.turnsplayed += 1
                game.update_player()
                
        inputmove = input(f"enter a move for {game.player}...")
        # print(f'TERM inputmove={inputmove}')

        ####      CHECK FOR VALID INPUT
        if len(inputmove) != 2 and not inputmove.isdigit() :
            print(f"\nInvalid move, try again.")
            continue
        else:
            inputmove = tuple(int(i) for i in inputmove)

        ####      CHECK FOR VALID MOVE
        availactions = game.available_actions()   
        # print(f'TERM availactions={availactions}') 
        if inputmove not in availactions:
            print(f"\nInvalid move, try again.")
            continue
        else:
            game.move(inputmove, availactions)
        
    if __name__ == "__main__":
        app.run(debug=True)
