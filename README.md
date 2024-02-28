# Othello Player. Reinforcement learning with q-Table #

*[CLICK TO PLAY!](http://217.174.244.37:5003/)*

### In Train function: ### 
A model playes itself, (always as black using state inversion).
Epsilon Greedy with a decay function ensures sufficient exploration outside the previously learnt policy.
A Heuristic evaluation function is used after every move to update the q-table.

### In Evaluate function: ### 
The model, using a specified q-table, playes against a random player.\
Win rate and win/loss ratio are recorded.

### Flask ###
A flask app presents a web page game where the user can play a model, using a predetermined Q-table.
The baord is updated with AJAX.

