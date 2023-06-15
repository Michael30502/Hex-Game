import gamelogic
import numpy as np
from collections import deque


cut_off_depth = 2


# class used for managing states in the state space
class State:
    def __init__(self, board_config, player_turn):
        self.board_config = board_config
        self.player_turn = player_turn

    def is_terminal_state(self):
        return gamelogic.has_any_won(self.board_config)

    def __str__(self):
        return "board in state: \n" + str(self.board_config)


# utility function for generating the next state given a certain action
def result_state(state, action):
    next_player = gamelogic.opponent(state.player_turn)
    new_board = gamelogic.make_sim_move(action, state.board_config, next_player)
    return State(new_board, next_player)


# generate the list of relevant actions to consider, i.e. actions lying on the shortest path for both opponent and AI
def actions_to_explore(board):
    # identify the actions available
    moves_list = []
    for i in range(0, board.shape[0]):
        for j in range(0, board.shape[0]):
            if board[i, j] == 0:
                moves_list.append((i, j))

    # find the actions on the shortest paths in both directions
    tiles_on_1_shortest_path = identify_tiles_on_path(board, 1)
    tiles_on_2_shortest_path = identify_tiles_on_path(board, 2)
    tiles_on_both_paths = tiles_on_1_shortest_path.intersection(tiles_on_2_shortest_path)
    # the moves to explore are those that are both on a shortest path as well as actually legal
    return set(moves_list).intersection(tiles_on_both_paths)


# small utility function for interpreting array elements as nodes with edges in a graph
def weight(elem, player):
    if elem == 0:
        return 1
    elif elem == player:
        return 0
    else:
        return float('inf')


# algorithm based on Dijkstra's shortest path
# note that player 1 is always horizontal and player 2 always vertical
def shortest_path(board, player):
    # initialise the matrix containing all lenghts found so far
    lengths_found = np.full(board.shape, float('inf'))
    # make sets to keep track of what is already explored and what is next to explore
    frontier = deque()
    visited = set()
    # the first column can be immediatly set
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


# function for finding the tiles that are actually involved in some shortest path
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


# simple heuristic function to be used in the MiniMax algorithm with cut-off
def heuristic(state):
    min_for_player_1 = minimal_length_values(state.board_config, 2)
    min_for_player_2 = minimal_length_values(state.board_config, 2)
    return min_for_player_1 - min_for_player_2


# maximises the AI's score in the minimax algorithm
# based upon the algorithms presented in [[[[book reference]]]]
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


# minimises the AI's score in the minimax algorithm
# based upon the algorithms presented in [[[[book reference]]]]
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


# starts the MiniMax search, returning the move to make
def minimax_search(state):
    value, move = max_value(state, 0, float('-inf'), float('inf'))
    if move is None:
        print("minimax found no move. None returned")
    return move
