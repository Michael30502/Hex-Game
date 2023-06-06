import random
import numpy as np
import ai1

board_size = 11


board = np.zeros((board_size, board_size), dtype=int)

player_no = 0
client_no = 0
player_won = False
multiplayer = False
move_list = list()


board = np.zeros((board_size, board_size), dtype=int)

player_no = 1


def is_empty(pos, board_in):
    return board_in[pos] == 0




def make_move(pos):

# for quickly and conveniently finding the player number of the opponent
def opponent(player):
    if player == 1:
        return 2
    return 1


def make_actual_move(pos):
    global player_no
    # print(board[pos])
    if is_empty(pos) and player_won is False and (multiplayer is False or player_no == client_no):
        #print("multiplayer: {} {}".format(multiplayer, client_no))
        board[pos] = player_no + 1
        if multiplayer:
            move_list.append(pos)
        # print find_neighbours(pos)
        if has_player_won(player_no+1):
            print("Player {p} won!".format(p=player_no+1))
            player_won = True
        player_no = (player_no + 1) % 2
    # else:
    #     print("Illegal move")


def make_sim_move(pos, board_in, player):
    board_out = np.copy(board_in)
    if is_empty(pos, board_in):
        board_out[pos] = player
    return board_out


def make_cpu_move(random_move=False):
    global player_no
    if random_move:
        random_number = get_random_empty_pos()
        if random_number != -1:
            board[random_number] = player_no
    else:
        print(board)
        move = ai1.minimax_search(ai1.State(board, player_no))
        print(board)
        board[move] = player_no
        if has_player_won(player_no, board):
            print("Player {p} won!".format(p=player_no))
    player_no = opponent(player_no)


def make_ai1_move():
    if board[board.shape[0] // 2, board.shape[0] // 2] == 0:
        make_actual_move((board.shape[0] // 2, board.shape[0] // 2))
        return
    # move = ai1.pick_action_most_wins(ai1.State(board, player))
    move = ai1.minimax_search(ai1.State(board, player_no))
    if move is None:
        move = ai1.pick_action_most_wins(ai1.State(board, player_no))
    make_actual_move(move)


def get_random_empty_pos():
    random_pos = -1
    x = 0
    y = 0
    pos_list = []
    # Makes a list of all empty positions on the board
    for hexlist in board:
        for hextile in hexlist:
            if hextile == 0:
                pos_list.append((y, x))
            x += 1
        x = 0
        y += 1

    # Chooses a random position from the list, if there is any
    if len(pos_list) >= 1:
        random_pos = pos_list[random.randrange(0, len(pos_list))]

    return random_pos


# if a nonnegative value is specified when calling, only neighbours of that value are returned
def find_neighbours(pos, board_in, value=-1):
    (r, c) = pos
    nset = set()
    # this loop will pass through all 8 neighbours of the array, plus the element itself ...
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            # ... however, a hexagon has at most 6 neighbours. The surplus elements are skipped by:
            if i == j:
                continue
            # this handles the edge cases:
            if r + i < 0 or r + i >= board_in.shape[0] or c + j < 0 or c + j >= board_in.shape[0]:
                continue
            # here we only extract neighbours of a specific value, if a nonnegative value is specified
            if value >= 0:
                if value == board_in[r + i, c + j]:
                    nset.add((r + i, c + j))
            else:
                nset.add((r + i, c + j))
    return nset


def has_player_won(playerno, board_in):
    path_found = False
    r, c = (0, 0)
    visited_set = set()
    possible_path = set()
    if playerno < 1 or playerno > 2:
        raise Exception(
            "Invalid index for has_player_won: Player must be either 1 or 2"
        )

    while r < board_size and c < board_size and not path_found:
        # first the function looks for one of the player's tiles along an edge (leftmost for player 1, topmost for
        # player 2)
        if board_in[r, c] == playerno:
            # any tile found is added to the set containing the possible path
            possible_path.add((r, c))
            # In this loop, the neighbours of our path candidates are included into the possible path.
            # We also keep track of already explored candidates, so we won't end in an infinite loop.
            while len(possible_path - visited_set) > 0:
                for elem in possible_path - visited_set:
                    (x, y) = elem
                    possible_path = possible_path | find_neighbours((x, y), board_in, value=playerno)
                    visited_set.add(elem)
            # If a tile on the rightmost edge (for player 1) or the bottom edge (for player 2) is in the possible path
            # set, this must mean a path was found. Afterall, it could only have been added if all successive neighbours
            # on the path were added
            for i in range(0, board_size):
                if playerno == 1:
                    if (i, board_size - 1) in possible_path:
                        path_found = True
                        break
                elif playerno == 2:
                    if (board_size - 1, i) in possible_path:
                        path_found = True
                        break
        # this progresses the loop that searches for tiles on the initial edges
        if playerno == 1:
            r = r + 1
        elif playerno == 2:
            c = c + 1
    return path_found


def has_any_won(board_in):
    return has_player_won(1, board_in) or has_player_won(2, board_in)
