echo "The script will run the games played by the following agents:
1) Minimax with depth 3 vs. Random player (5 Games, ~60 seconds)
2) Minimax with depth 3 vs. MCTS with 500 iterations (1 Game, ~300 seconds)
3) MCTS with 500 iterations vs. Random player (1 Game, ~ 2500 seconds)

The result of a game is displayed in the format of [White_score]-[Black_score].

MCTS against Random player takes so long because MCTS is not very good given
the number of iterations we are allowing it, so it takes a long time to play
against a player with random moves. MCTS seems to be not performing well under areasonable time limit because Chess is a complex game with many states, so the 
timeframe may not be enough to have enough iterations. Usually, MCTS performs slightly better than the Random player.

Running test script for Chess AI...."
python game.py
