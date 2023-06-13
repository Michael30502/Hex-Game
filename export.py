import numpy as np
import string

#this splits a board into 2 lists containing moves from player 1 and 2 respectively
def split_board(board):
    #TODO this is gonna be hard without some way
    alphabet = list(string.ascii_uppercase)
    p1_list = []
    p2_list = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                p1_list.append(str(alphabet[i]) + str(j+1)+" ")
                
            elif board[i][j] == 2:
                p2_list.append(str(alphabet[i]) + str(j+1)+" ")
    return p1_list, p2_list

    #TODO i also include the color and then i can switch between blue and red moves for the final print
    print("player1 list")
    print(p1_list)
    print("player 2 list")
    print(p2_list)

#this then makes a combined list
def combine_lists(player1_list, player2_list):
    export_list = [None]*(len(player1_list)+len(player2_list))
    if len(player1_list) > (len(player2_list)):
        export_list[0::2]= player1_list
        export_list[1::2]= player2_list
    else:
        export_list[0::2]= player2_list
        export_list[1::2]= player1_list
    
    return export_list



#this makes a txt file called export.txt where we store the board as a string which can be opened in other hex games
def export_to_file(combined_list):

    export_string = ""
    for elem in combined_list:
        export_string += (elem)

    with open('export.txt', 'w') as f:
        f.write(export_string)
    return export_string

def export_board(board):
    p1_list,p2_list = split_board(board)
    combined_lists = combine_lists(p1_list, p2_list)
    export_to_file(combined_lists)




    



