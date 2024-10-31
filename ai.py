from game import *


def minimax(board, symbol, my_symbol):
    game_status, _ = check_game_status(board)

    if game_status == "draw": return 0
    if game_status == my_symbol: return 1
    if game_status == swap_symbol(my_symbol): return -1

    available_spaces = get_available_spaces(board)

    move_scores = []
    for move in available_spaces:
        new_board = make_move(board, int(move), symbol)
        move_score = minimax(new_board, swap_symbol(symbol), my_symbol)
        move_scores.append(move_score)

    if symbol == my_symbol: return max(move_scores)
    if symbol != my_symbol: return min(move_scores)


def best_move(board, player):
    my_symbol = player["symbol"]
    available_spaces = get_available_spaces(board)
    best_move_score = None

    for move in available_spaces:
        new_board = make_move(board, int(move), my_symbol)
        move_score = minimax(new_board, swap_symbol(my_symbol), my_symbol)

        if best_move_score is None or move_score > best_move_score:
            best_move_score = move_score
            best_move = move
        
    return best_move
