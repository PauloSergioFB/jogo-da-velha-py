from copy import deepcopy


def get_available_spaces(board):
    available_spaces = []

    i = 1
    for line in board:
        for pos in line:
            if pos == "":
                available_spaces.append(str(i))

            i += 1

    return available_spaces


def make_move(board, move, symbol):
    new_board = deepcopy(board)

    move_row = (move - 1) // 3
    move_col = (move - 1) % 3

    new_board[move_row][move_col] = symbol
    return new_board


def check_game_status(board):
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] != "":
            pos_1 = i * 3 + 1
            pos_2 = i * 3 + 2
            pos_3 = i * 3 + 3

            return board[i][0], (pos_1, pos_2, pos_3)

    for i in range(len(board)):
        if board[0][i] == board[1][i] == board[2][i] != "":
            pos_1 = i + 1
            pos_2 = i + 4
            pos_3 = i + 7
            
            return board[0][i], (pos_1, pos_2, pos_3)
        
    if board[0][0] == board[1][1] == board[2][2] != "": 
        pos_1 = 1
        pos_2 = 5
        pos_3 = 9

        return board[0][0], (pos_1, pos_2, pos_3)
    
    if board[0][2] == board[1][1] == board[2][0] != "":
        pos_1 = 3
        pos_2 = 5
        pos_3 = 7
        
        return board[0][2], (pos_1, pos_2, pos_3)

    if get_available_spaces(board) == []: return "draw", ()

    
    return "game in progress", ()


def swap_symbol(symbol):
    return "X" if symbol == "O" else "O"
