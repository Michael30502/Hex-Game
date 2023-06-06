import random

import numpy as np

board_size = 11



board = np.zeros((board_size, board_size), dtype=int)

player_no = 1


def is_empty(pos):
    return board[pos] == 0


def opponent(player):
    if player == 1:
        return 2
    return 1


def make_actual_move(pos):
    global player_no
    # print(board[pos])
    if is_empty(pos):
        # print(pos)
        board[pos] = player_no + 1
        # print find_neighbours(pos)
        if has_player_won(player_no+1, board):
            print("Player {p} won!".format(p=player_no+1))
        player_no = (player_no + 1) % 2
    # else:
    #     print("Illegal move")


def make_cpu_move():
    global player_no
    random_number = get_random_empty_pos()
    if random_number != -1:
        board[random_number] = player_no + 1
    player_no = (player_no + 1) % 2


def get_random_empty_pos():
    random_pos = -1
    x = 0
    y = 0
    pos_list = []
    # Makes a list of all empty positions on the board
    for hex in board:
        for hex2 in hex:
            if hex2 == 0:
                pos_list.append((y, x))
            x += 1
        x = 0
        y += 1
    # Chooses a random position from the list, if there is any
    if len(pos_list) >= 1:
        random_pos = pos_list[random.randrange(0, len(pos_list))]

    return random_pos


# if a nonnegative value is specified when calling, only neighbours of that value are returned
def find_neighbours(pos, value=-1):
    (r, c) = pos
    nset = set()
    # this loop will pass through all 8 neighbours of the array, plus the element itself ...
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            # ... however, a hexagon has at most 6 neighbours. The surplus elements are skipped by:
            if i == j:
                continue
            # this handles the edge cases:
            if r + i < 0 or r + i >= board_size or c + j < 0 or c + j >= board_size:
                continue
            # here we only extract neighbours of a specific value, if a nonnegative value is specified
            if value >= 0:
                if value == board[r + i, c + j]:
                    nset.add((r + i, c + j))
            else:
                nset.add((r + i, c + j))
    return nset


# assumes that player is either number 1 or 2.
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
        if board[r, c] == playerno:
            # any tile found is added to the set containing the possible path
            possible_path.add((r, c))
            # In this loop, the neighbours of our path candidates are included into the possible path.
            # We also keep track of already explored candidates, so we won't end in an infinite loop.
            while len(possible_path - visited_set) > 0:
                for elem in possible_path - visited_set:
                    (x, y) = elem
                    possible_path = possible_path | find_neighbours(
                        (x, y), value=playerno
                    )
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
