import gamelogic
import ai1
import numpy as np

test_board = np.array([[0, 0, 0, 0],
                       [0, 2, 0, 0],
                       [1, 0, 1, 1],
                       [0, 2, 2, 0]])

print(gamelogic.board)
# print(ai1.actions_available(gamelogic.board))

# test_state = ai1.State(gamelogic.board, gamelogic.player_no)

# print("minimax result: " + str(ai1.minimax_search(test_state)))


def make_ai1_move(board, player):
    if board[board.shape[0] / 2, board.shape[0] / 2] == 0:
        gamelogic.make_actual_move((board.shape[0] / 2, board.shape[0] / 2))
        return
    # move = ai1.pick_action_most_wins(ai1.State(board, player))
    move = ai1.minimax_search(ai1.State(board, player))
    if move is None:
        move = ai1.pick_action_most_wins(ai1.State(board, player))
    gamelogic.make_actual_move(move)


# def recursive_factorial(n):
#     if n == 0:
#         return 1
#     else:
#         return n*recursive_factorial(n-1)
#
#
# print(test_board)
# l1 = ai1.shortest_path(test_board, 1)
# print(l1)
# print(ai1.identify_tiles_on_path(test_board, l1, 1))
#
# l2 = ai1.shortest_path(test_board, 2)
# print(l2)
# print(ai1.identify_tiles_on_path(test_board, l2, 2))


# print(gamelogic.board)

#
while not (gamelogic.has_player_won(1, gamelogic.board) or gamelogic.has_player_won(2, gamelogic.board)):
    if gamelogic.player_no == 1:
        make_ai1_move(gamelogic.board, gamelogic.player_no)
        print(gamelogic.board)
    else:
        string_move = raw_input('Make a move (in the format x, y):')
        res = tuple(map(int, string_move.split(', ')))
        gamelogic.make_actual_move(res)



