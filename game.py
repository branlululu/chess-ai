"""
This module contains the main interface/game of the program. Evaluates the AI's performance against
other players and returns winning percentages.

Functions:
- simulate_game(depth, tree, random_player)
- simulate_games(N, depth, tree)
"""

import chess
import random
import time
import ai

def simulate_game(depth, tree, num_ierations, minimax_agent=True, random_player=True):
    """
    Lets Agent play against another player and returns the result of the game (1 for White, 0 for Black, and 0.5 for draw)
    Agent is set to play White while the opponent plays Black.
    Agent uses either minimax or MCTS, depending on bool value of minimax_ai.
    Opponent is either random or MCTS, depending on bool value of random_player.
    """

    board = chess.Board()
    turn = 0

    while not board.is_game_over():
        if turn % 2 == 0:
            if minimax_agent:
                ai_move = ai.determine_move(depth, board, True)
            else:
                ai_move = ai.mcts(num_ierations, board, tree, True)
            board.push(ai_move)
        else:
            if random_player:
                opponent_move = random.choice(list(board.legal_moves))
            else:
                opponent_move = ai.mcts(num_ierations, board, tree, False)
            board.push(opponent_move)
        turn += 1

    result = board.result()
    print(result)
    if result == "1/2-1/2":
        return 0.5
    else:
        return int(result[0])

def simulate_games(N, N_mcts, depth, num_iterations, tree):
    """
    Simulate N games using minimax at given depth against another player
    and display results.
    """

    # Minimax against random player
    score = 0
    start_time = time.time()
    print("-----------Running Minimax against Random player-----------")
    for i in range(N):
        print("Game {}: ".format(i + 1), end='')
        score += simulate_game(depth, tree, num_iterations, minimax_agent=True, random_player = True)
    print("# Games: {}\nTime: {} seconds\nDepth: {}\nWin percentage: {}".format(N, time.time()-start_time, depth, score / N * 100))

    # Minimax against MCTS
    score = 0
    start_time = time.time()
    print("-----------Running Minimax against MCTS player-----------")
    for i in range(N_mcts):
        print("Game {}: ".format(i + 1), end='')
        score += simulate_game(depth, tree, num_iterations, minimax_agent = True, random_player = False)
    print("# Games: {}\nTime: {} seconds\nDepth: {}\nIterations: {}\nWin percentage: {}".format(N_mcts, time.time()-start_time, depth, num_iterations, score / N_mcts * 100))

    # MCTS against random player
    score = 0
    start_time = time.time()
    print("-----------Running MCTS against Random player-----------")
    for i in range(N_mcts):
        print("Game {}: ".format(i + 1), end='')
        score += simulate_game(depth, tree, num_iterations, minimax_agent = False, random_player = True)
    print("# Games: {}\nTime: {} seconds\nIterations: {}\nWin percentage: {}".format(N_mcts, time.time()-start_time, num_iterations, score / N_mcts * 100))
    
    return

def main():
    N = 5
    N_mcts = 1
    depth = 3
    num_iterations = 500
    tree = {}
    simulate_games(N, N_mcts, depth, num_iterations, tree)

if __name__ == "__main__":
    main()

# 60 seconds
