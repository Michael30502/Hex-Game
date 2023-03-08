import numpy as np

board_size = 11

board = np.zeros((board_size, board_size), dtype=int)

player_no = 0


def is_empty(pos):
    return board[pos] == 0


def make_move(pos):
    global player_no
    if is_empty(pos):
        board[pos] = player_no + 1
        # print find_neighbours(pos)
        if has_player_won(player_no+1):
            print "Player {p} won!".format(p=player_no+1)
        player_no = (player_no + 1) % 2
    else:
        print("Illegal move")


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
                if value == board[r+i, c+j]:
                    nset.add((r + i, c + j))
            else:
                nset.add((r + i, c + j))
    return nset


# assumes that player is either number 1 or 2
def has_player_won(playerno):
    path_found = False
    r, c = (0, 0)
    visited_set = set()
    possible_path = set()
    if playerno < 1 or playerno > 2:
        raise Exception("Invalid index for has_player_won: Player must be either 1 or 2")

    while r < board_size and c < board_size and not path_found:
        if board[r, c] == playerno:
            possible_path.add((r, c))
            while len(possible_path - visited_set) > 0:
                for elem in possible_path - visited_set:
                    (x, y) = elem
                    possible_path = possible_path | find_neighbours((x, y), value=playerno)
                    visited_set.add(elem)
            for i in range(0, board_size):
                if playerno == 1:
                    if (i, 10) in possible_path:
                        path_found = True
                        break
                elif playerno == 2:
                    if (10, i) in possible_path:
                        path_found = True
                        break
        if playerno == 1:
            r = r + 1
        elif playerno == 2:
            c = c + 1
    return path_found



