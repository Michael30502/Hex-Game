import gamelogic
import ai1
import numpy as np

test_board = np.array([[0, 1, 0],
                       [1, 0, 2],
                       [1, 2, 2]])

# print(gamelogic.board)
# print(ai1.actions_available(gamelogic.board))

# test_state = ai1.State(gamelogic.board, gamelogic.player_no)

# print("minimax result: " + str(ai1.minimax_search(test_state)))


def make_ai1_move(board, player):
    move = ai1.pick_action_most_wins(ai1.State(board, player))
    print(move)
    gamelogic.make_actual_move(move)


def recursive_factorial(n):
    if n == 0:
        return 1
    else:
        return n*recursive_factorial(n-1)


print(gamelogic.board)


while not (gamelogic.has_player_won(1, gamelogic.board) or gamelogic.has_player_won(2, gamelogic.board)):
    if gamelogic.player_no == 0:
        make_ai1_move(gamelogic.board, gamelogic.player_no)
        print(gamelogic.board)
    else:
        string_move = raw_input('Make a move (in the format x, y):')
        res = tuple(map(int, string_move.split(', ')))
        gamelogic.make_actual_move(res)



