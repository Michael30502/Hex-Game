# Authored by William (s184471)
import numpy as np


def array_to_string(array):
    # return a string with all the elements in the array sepperated by a " "
    # input = an array
    return " ".join(str(elem) for elem in array.flat)


def string_to_square_numpy_array(input_string):
    # returns array by splitting the string into integers and convert them to a numpy array
    # input an import string
    flat_array = np.array([int(elem) for elem in input_string.split()])
    print("flat array is")
    print(flat_array)
    array_size = int(np.sqrt(flat_array.size))

    # Reshape the flat array into a square array
    array = flat_array.reshape((array_size, array_size))
    print("new array is")
    print(array)
    return array


# Checking the elements in arr are either 0,1,2 and that ther is only a difference of 1 in the ammount of player
# elements
def is_board_legal(board):
    # returns boolean value depending on the validity of the board
    # in = the board array

    # for player tile checking
    values, counts = np.unique(board, return_counts=True)
    # we start by determining if the size is a perfect square
    # check if other values than 0,1,2 is in the array
    if np.amax(board) > 2:
        print(" wrong values in array, entries cant be larger than 2")
        return False
    elif np.amin(board) < 0:
        print(" wrong values in array, entries cant be smaller than 0")
        return False
    # checks if the boards only contains 0's
    elif len(values) < 2:
        print("board is empty but legal")
        return True
    # if player 1 has more or equal 2 tiles while player 2 has 0 board is illegal
    elif len(values) < 3 and (0 in values and 1 in values):
        if counts[1] >= 2:
            print("player 1 has too many tiles")
            return False
        else:
            # this is when the only move made is player 1
            return True
    # same with player 2 but this time since player 1 always starts the number cant exceed 1
    elif len(values) < 3 and (0 in values and 2 in values):
        if counts[1] >= 1:
            print("player 2 has too many tiles")
            return False
        else:
            print("this should not be possible to reach 2")
            return True

    elif len(values) < 3 and (1 in values and 2 in values):
        # this is a case where the board we are trying to import is full
        print("player has won")
        return False
    # checking if the difference between player tiles is larger than 1
    elif abs(counts[1] - counts[2]) >= 2:
        print("difference in player tiles is too big")
        return False

    else:
        print("board is legal")
        return True


def calculate_player_turn(board):
    # returns an integer to determine which players turn it is
    # takes a board to calculate what player should play next by chekcing the ammount of 1 and 2 values on the board.
    values = np.unique(board)
    # absolute difference between player tiles (must not exceed 1)

    # if there is only 1 element in values assuming the only element present is 0 #TODO
    if len(values) < 2:
        return 1
    # if there are 2 elements present in our array and 1 of them is 1 assuming rest is 0 then it must be player 2's turn
    elif len(values) < 3 and (1 in values):
        return 2
    elif len(values) < 3 and (2 in values):
        return 1
    elif values[1] <= values[2]:
        return 1
    elif values[2] < values[1]:
        return 2
    else:
        print("calculate_player_turn ERROR")
        return 0
