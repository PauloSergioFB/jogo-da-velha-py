from utils import get_available_spaces, swap_symbol
from game import make_move, check_game


def get_best_move(board, my_symbol):
    best_move_score = None  # Inicializa a melhor pontuação como None

    available_spaces = get_available_spaces(board)
    for space in available_spaces:
        move = int(space)
        new_board = make_move(board, move, my_symbol)  # Simula a jogada no novo tabuleiro
        move_score = minimax(new_board, swap_symbol(my_symbol), my_symbol)  # Avalia a jogada usando o algoritmo Minimax

        # Atualiza a melhor pontuação e a melhor jogada se a pontuação atual for maior
        if best_move_score is None or move_score > best_move_score:
            best_move_score = move_score
            best_move = move

    return best_move    


def minimax(board, symbol, my_symbol):
    game_status, _ = check_game(board)  # Verifica o estado atual do jogo

    # Verifica as condições de término do jogo e atribui pontuações
    if game_status == "draw": return 0  # Empate
    if game_status == my_symbol: return 1  # Vitória do jogador
    if game_status == swap_symbol(my_symbol): return -1  # Derrota do jogador

    move_scores, available_spaces = [], get_available_spaces(board)
    for space in available_spaces:
        move = int(space)

        new_board = make_move(board, move, symbol)  # Simula a jogada no novo tabuleiro
        move_score = minimax(new_board, swap_symbol(symbol), my_symbol)  # Chamada recursiva do algoritmo Minimax
        move_scores.append(move_score)  # Armazena a pontuação da jogada

    # Retorna a melhor pontuação dependendo de quem é a vez de jogar
    if symbol == my_symbol:
        return max(move_scores)  # Maximiza a pontuação se for o jogador
    else:
        return min(move_scores)  # Minimiza a pontuação se for o adversário
