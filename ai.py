"""
This module contains the various algorithms that power the Chess agent.

Methods include:
- Monte Carlo Tree Search with UCB
- Minimax with alpha-beta pruning

Functions:
- mcts(num_iterations, board, tree, is_white)
- ucb(board, tree)
- minimax(depth, board, is_maximize, alpha, beta)
- determine_move(depth, board, is_maximize)
"""

import chess
import evaluation
import random
import math

def ucb(board, tree):
    """Given board, return the move with the optimal UCB depending on player"""
    t = tree[str(board)][1] # node's total visits
    best_ucb = None
    best_move = None
    ucb = 0
    is_white = board.turn
    if is_white:
        best_ucb = -float('inf')
    else:
        best_ucb = float('inf')
    for move in board.legal_moves:
        board.push(move)
        r_j = tree[str(board)][0] / tree[str(board)][1] # child node's win percentage
        n_j = tree[str(board)][1] # child node's total
        if is_white:
            ucb = r_j + math.sqrt( (2 * math.log(t)) / n_j)
            if ucb >= best_ucb:
                best_ucb = ucb
                best_move = move
        else:
            ucb = r_j - math.sqrt( (2 * math.log(t)) / n_j)
            if ucb <= best_ucb:
                best_ucb = ucb
                best_move = move
        board.pop()
    return best_move

def mcts(num_iterations, board, tree, is_white):
    """Given current board, player, and number of iterations, returns the optimal move by MCTS"""
    for i in range(num_iterations):
        moves_not_made = []
        traversed_nodes = []
        final_score = 0

        # Generate all moves that have not been made at root
        for move in board.legal_moves:
            board.push(move)
            if str(board) not in tree:
                moves_not_made.append(move)
            board.pop()

        # If all of current node's children have been visited, use UCB to pick best move
        new_pos = board.copy()
        while len(moves_not_made) == 0 and not new_pos.is_game_over():
            traversed_nodes.append(str(new_pos))
            move_to_make = ucb(new_pos, tree)
            new_pos.push(move_to_make)
            for move in new_pos.legal_moves:
                new_pos.push(move)
                if str(new_pos) not in tree:
                    moves_not_made.append(move)
                new_pos.pop()

        # Reached node with moves that have not been made
        # Keep track of latest node and randomly play until end.
        if not new_pos.is_game_over():
            traversed_nodes.append(str(new_pos))
            move_to_make = random.choice(moves_not_made)
            new_pos.push(move_to_make)
        traversed_nodes.append(str(new_pos))

        while not new_pos.is_game_over():
            simulated_moves = new_pos.legal_moves
            new_pos.push(random.choice(list(simulated_moves)))

        # Back-propagate stats with current iteration results: (#wins, #total)
        final_score = new_pos.result()
        if(final_score == "1/2-1/2"):
            final_score = 0.5
        else:
            final_score = int(final_score[0])
        
        while traversed_nodes:
            node = traversed_nodes.pop()
            if node not in tree:
                tree[node] = (final_score, 1)
            else:
                tree[node] = (tree[node][0] + final_score, tree[node][1] + 1)

    # Based on populated game tree, determine final move from win percentages
    final_selection = []
    final_index = 0

    for move in board.legal_moves:
        board.push(move)
        stats = tree[str(board)]
        final_selection.append((stats[0] / stats[1], move))
        board.pop()

    # Determine optimal win percentage based on player
    for i in range(len(final_selection)):
        choice = final_selection[i]
        if is_white:
            if(choice[0] < final_selection[final_index][0]):
                final_index = i
        else:
            if(choice[0] > final_selection[final_index][0]):
                final_index = i
    return final_selection[final_index][1] # return move with optimal win percentage


def minimax(depth, board, is_maximize, alpha, beta):
    """Minimax with alpha-beta pruning"""
    if depth == 0 or not board.legal_moves: # depth limit reached or no moves left
        return evaluation.evaluate_board(board)

    if is_maximize: # White
        best_score = -float('inf')
    else: # Black
        best_score = float('inf')

    # Find move that leads to optimal value
    for move in board.legal_moves:
        board.push(move)
        move_val = minimax(depth - 1, board, not is_maximize, alpha, beta)
        if is_maximize: 
            best_score = max(best_score, move_val)
            alpha = max(alpha, best_score)
        else:
            best_score = min(best_score, move_val)
            beta = min(beta, best_score)
        board.pop() 

        # Prune children that don't need to be looked at
        if(alpha >= beta):
            return best_score

    return best_score

def determine_move(depth, board, is_maximize):
    """
    Given depth, current board, and current player, return the optimal move
    from minimax.
    """
    if is_maximize:
        best_score = -float('inf')
    else:
        best_score = float('inf')
    best_move = None
    
    for move in board.legal_moves:
        board.push(move)
        child_score = minimax(depth - 1, board, not is_maximize, -float('inf'), float('inf'))
        if is_maximize: # White's turn
            if child_score > best_score:
                best_score = child_score
                best_move = move
        else: # Black's turn
            if child_score < best_score:
                best_score = child_score
                best_move = move
        board.pop()
    return best_move