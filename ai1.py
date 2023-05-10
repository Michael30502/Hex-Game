import gamelogic


# first challenge. Generating the state space

class State:
    def __init__(self, board_config, player_turn):
        self.board_config = board_config
        self.player_turn = player_turn

    def is_terminal_state(self):
        return gamelogic.has_player_won(self.player_turn + 1, self.board_config)

    def __str__(self):
        return "board in state: \n" + str(self.board_config)


# generate the list of actions possible on the board
def actions_available(board):
    moves_list = []
    for i in range(0, gamelogic.board_size):
        for j in range(0, gamelogic.board_size):
            if board[i, j] == 0:
                moves_list.append((i, j))
    return moves_list


# currently assumes that AI is player 1
def victory_counter(state, sum_so_far):
    if gamelogic.has_player_won(2, state.board_config):
        return 1
    elif gamelogic.has_player_won(1, state.board_config):
        return -1
    res_list = []
    for a in actions_available(state.board_config):
        next_player = (state.player_turn + 1) % 2
        new_board = gamelogic.make_sim_move(a, state.board_config, next_player)
        new_state = State(new_board, next_player)
        res = victory_counter(new_state, sum_so_far)
        res_list.append(res)
    victories_found = sum(res_list)
    return victories_found


def pick_action_most_wins(state):
    res_list = []
    for a in actions_available(state.board_config):
        next_player = (state.player_turn + 1) % 2
        new_board = gamelogic.make_sim_move(a, state.board_config, next_player)
        new_state = State(new_board, next_player)
        if new_state.is_terminal_state():
            return a
        res_list.append((victory_counter(new_state, 0), a))
    print(res_list)
    return max(res_list, key=lambda item: item[0])[1]


def max_value(state):
    if state.is_terminal_state():
        return 1, None
    v = float('-inf')
    move = (-1, -1)
    v_sum = 0
    for a in actions_available(state.board_config):
        next_player = (state.player_turn + 1) % 2
        new_board = gamelogic.make_sim_move(a, state.board_config, next_player)
        new_state = State(new_board, next_player)
        v2, a2 = min_value(new_state)
#        print("v2 found in max_value:" + str(v2))
        v_sum = v_sum + v2
        if v2 > v:
            v, move = v2, a
    return v_sum, move


def min_value(state):
    if state.is_terminal_state():
        return -1, None
    v = float('inf')
    move = (-1, -1)
    v_sum = 0
    for a in actions_available(state.board_config):
        next_player = (state.player_turn + 1) % 2
        new_board = gamelogic.make_sim_move(a, state.board_config, next_player)
        new_state = State(new_board, next_player)
        v2, a2 = max_value(new_state)
        v_sum = v_sum + v2
        if v2 < v:
            v, move = v2, a
    return v_sum, move


def minimax_search(state):
    value, move = max_value(state)
    return move


def expand_state(state):
    new_states = []
    for action in actions_available(state.board_config):
        new_board = gamelogic.make_sim_move(action, state.board_config, state.player_turn)
        next_player = (state.player_turn + 1) % 2
        new_states.append(State(new_board, next_player))
    return new_states


# bfs as described in Russel & Norvig section "Uninformed search strategies"
def breadth_first_search(initial_state):
    state = initial_state
    if gamelogic.has_player_won(state.player_turn, state.board_config):
        return state
    frontier = [state]
    reached = {initial_state}
    while frontier.len() > 0:
        state = frontier.pop()
        for child in expand_state(state):
            s = child
            if gamelogic.has_player_won(child.player_turn, child.board_config):
                return child
            if s not in reached:
                reached.add(s)
                frontier.append(child)
    return [-1]


