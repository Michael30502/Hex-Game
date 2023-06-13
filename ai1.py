import gamelogic
import numpy as np
import sys
from collections import deque
import random


cut_off_depth = 2

state_counter = 0


class State:
    def __init__(self, board_config, player_turn):
        self.board_config = board_config
        self.player_turn = player_turn

    def is_terminal_state(self):
        return gamelogic.has_any_won(self.board_config)

    def __str__(self):
        return "board in state: \n" + str(self.board_config)


# generate the list of actions possible on the board
def actions_to_explore(board):
    # actions available
    moves_list = []
    for i in range(0, gamelogic.board_size):
        for j in range(0, gamelogic.board_size):
            if board[i, j] == 0:
                moves_list.append((i, j))

    tiles_on_1_shortest_path = identify_tiles_on_path(board, 1)
    tiles_on_2_shortest_path = identify_tiles_on_path(board, 2)
    tiles_on_both_paths = tiles_on_1_shortest_path.intersection(tiles_on_2_shortest_path)
    candidate_moves = set(moves_list).intersection(tiles_on_both_paths)
    # while len(candidate_moves) > 7:
    #     candidate_moves.remove(max(candidate_moves))
    #     candidate_moves.remove(min(candidate_moves))
    return candidate_moves


def result_state(state, action):
    # global state_counter
    # state_counter += 1
    # print(state_counter)
    next_player = gamelogic.opponent(state.player_turn)
    new_board = gamelogic.make_sim_move(action, state.board_config, next_player)
    return State(new_board, next_player)


# currently assumes that AI is player 1
# def victory_counter(state, sum_so_far):
#     if gamelogic.has_player_won(1, state.board_config):
#         return 1
#     elif gamelogic.has_player_won(2, state.board_config):
#         return -1
#     res_list = []
#
#     print("actions_to_explore within victory counter: " + str(actions_to_explore(state)))
#     for a in actions_to_explore(state):
#         new_state = result_state(state, a)
#         res = victory_counter(new_state, sum_so_far)
#         res_list.append(res)
#     victories_found = sum(res_list)
#     return victories_found


# def pick_action_most_wins(state):
#     res_list = []
#     print("actions to explore in pick most wins: " + str(actions_to_explore(state)))
#     for a in actions_to_explore(state):
#         new_state = result_state(state, a)
#         if new_state.is_terminal_state():
#             return a
#         res_list.append((victory_counter(new_state, 0), a))
#     print(res_list)
#     return max(res_list, key=lambda item: item[0])[1]


# how do we measure how good a board is? Suggestion: Length of shortest path from one side to the other
# Note that player 1 is always horizontal and player 2 always vertical
def shortest_path(board, player):
    # initialise the matrix containing all lenghts found so far
    lengths_found = np.full(board.shape, float('inf'))
    # make sets to keep track of what is already explored and what is next to explore
    frontier = deque()
    visited = set()
    # the first column can be immediatly set
    # Empty tiles have cost 1, own tiles are free and enemy tiles are obstacles
    if player == 1:
        for i in range(0, board.shape[0]):
            lengths_found[i, 0] = weight(board[i, 0], player)
            if board[i, 0] != gamelogic.opponent(player):
                frontier.append((i, 0))
    elif player == 2:
        for i in range(0, board.shape[0]):
            lengths_found[0, i] = weight(board[0, i], player)
            if board[0, i] != gamelogic.opponent(player):
                frontier.append((0, i))

    # while there are still tiles to explore:
    while len(frontier) > 0:
        pos = frontier.popleft()
        visited.add(pos)
        if board[pos] == gamelogic.opponent(player):
            continue
        neighs = gamelogic.find_neighbours(pos, board, skipping=visited)
        for n in neighs:
            frontier.append(n)
            if lengths_found[n] > lengths_found[pos] + weight(board[n], player):
                lengths_found[n] = lengths_found[pos] + weight(board[n], player)
    return lengths_found


# returns a tuple with the minimal path length found for each player
def minimal_length_values(board, player):
    board_size = board.shape[0]
    if player == 1:
        lengths_found = shortest_path(board, 1)
        return min(lengths_found[:, board_size - 1])
    else:
        lengths_found = shortest_path(board, 2)
        return min(lengths_found[board_size - 1, :])


def weight(elem, player):
    if elem == 0:
        return 1
    elif elem == player:
        return 0
    else:
        return float('inf')


# function for finding the tiles that are actually involved in the shortest path
# hopefully this can save a lot of computation time
def identify_tiles_on_path(board, player):
    lengths_found = shortest_path(board, player)
    min_length_1 = minimal_length_values(board, 1)
    min_length_2 = minimal_length_values(board, 2)
    board_size = board.shape[0]
    path_found = set()
    visited = set()
    if player == 1:
        for i in range(0, board_size):
            if lengths_found[i, board_size - 1] == min_length_1:
                path_found.add((i, board_size - 1))
    elif player == 2:
        for i in range(0, board_size):
            if lengths_found[board_size - 1, i] == min_length_2:
                path_found.add((board_size - 1, i))

    while len(path_found - visited) > 0:
        for elem in path_found - visited:
            neighbours = gamelogic.find_neighbours(elem, board)
            for nb in neighbours:
                if lengths_found[elem] - weight(board[elem], player) == lengths_found[nb]:
                    path_found.add(nb)
            visited.add(elem)
    return path_found


# IDEA shamelessly stolen from
# https://gsurma.medium.com/hex-creating-intelligent-adversaries-part-2-heuristics-dijkstras-algorithm-597e4dcacf93
# the heuristic should be: heuristic_score = remaining_opponent_hexes - remaining_cpu_hexes
# currently assumes that AI is player 1
def heuristic(state):
    min_for_player_1 = minimal_length_values(state.board_config, 2)
    min_for_player_2 = minimal_length_values(state.board_config, 2)
    return min_for_player_1 - min_for_player_2


def max_value(state, depth, alpha, beta):
    if depth > min(cut_off_depth, state.board_config.shape[0] - 1) or state.is_terminal_state():
        return heuristic(state), None
    v = float('-inf')
    move = None

    for a in actions_to_explore(state.board_config):
        new_state = result_state(state, a)
        if new_state.is_terminal_state():
            return v, a
        v2, a2 = min_value(new_state, depth + 1, alpha, beta)
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v >= beta:
            return v, move
    return v, move


def min_value(state, depth, alpha, beta):
    if depth > min(cut_off_depth, state.board_config.shape[0] - 1) or state.is_terminal_state():
        return heuristic(state), None
    v = float('inf')
    move = None

    for a in actions_to_explore(state.board_config):
        new_state = result_state(state, a)
        if new_state.is_terminal_state():
            return v, a
        v2, a2 = max_value(new_state, depth + 1, alpha, beta)
        if v2 < v:
            v, move = v2, a
            beta = min(beta, v)
        if v <= alpha:
            return v, move
    return v, move


def minimax_search(state):
    value, move = max_value(state, 0, float('-inf'), float('inf'))
    if move is None:
        print("minimax found no move. None returned")
    return move


# very simple function to build bridges for initial gameplay
def bridge_builder(state):
    suggested_moves = []
    for i in range(0, gamelogic.board_size):
        for j in range(0, gamelogic.board_size):
            if state.board_config[i, j] == state.player_turn:
                candidates = [(i-1, j-1), (i-1, j+2), (i+1, j-2), (i+1, j+1)]
                print("candidates: " + str(candidates))
                for c in candidates:
                    if c[0] < 0 or c[1] < 0 or c[0] >= gamelogic.board_size or c[1] >= gamelogic.board_size:
                        print("candidate discarded as out of bounds: " + str(c))
                        continue
                    if state.board_config[c] != 0:
                        print("candidate discarded as not empty: " + str(c))
                        continue
                    if has_opponent_neighbour(c, state):
                        print("candidate discarded due to opponent neighbour: " + str(c))
                        continue
                    if c in identify_tiles_on_path(state.board_config, state.player_turn):
                        return c
                    suggested_moves.append(c)
    suggested_moves = list(set(suggested_moves).intersection(identify_tiles_on_path(state.board_config, state.player_turn)))
    print("suggested moves in bridge builder: " + str(suggested_moves))
    if len(suggested_moves) == 0:
        print("no moves found via bridge builder")
        return None
    return random.choice(suggested_moves)


# the bridge builder takes too little concern in the position of the opponent.
# what about a strategy that just tries to block as much as possible?

def has_opponent_neighbour(pos, state):
    r, c = pos
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == j:
                continue

            if r + i < 0 or r + i >= state.board_config.shape[0] or c + j < 0 or c + j >= state.board_config.shape[0]:
                continue

            if state.board_config[r + i, c + j] == gamelogic.opponent(state.player_turn):
                return True
    return False
