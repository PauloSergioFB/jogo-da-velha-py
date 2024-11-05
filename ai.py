from game import *


# Função Minimax para avaliar as jogadas possíveis e determinar o melhor resultado
# Recebe o tabuleiro atual, o símbolo do jogador da vez e o símbolo do "jogador principal"
def minimax(board, symbol, my_symbol):
    game_status, _ = check_game_status(board)  # Verifica o status atual do jogo

    # Retorna 0 para empate, 1 para vitória do "jogador principal" e -1 para derrota
    if game_status == "draw": return 0
    if game_status == my_symbol: return 1
    if game_status == swap_symbol(my_symbol): return -1

    available_spaces = get_available_spaces(board)  # Obtém as posições disponíveis no tabuleiro

    move_scores = []  # Armazena os escores de cada jogada
    for move in available_spaces:
        # Realiza uma jogada na posição disponível e alterna o símbolo para o próximo jogador
        new_board = make_move(board, int(move), symbol)
        move_score = minimax(new_board, swap_symbol(symbol), my_symbol)  # Avalia o resultado da jogada recursivamente
        move_scores.append(move_score)

    # Se o símbolo atual pertence ao "jogador principal", busca o valor máximo (melhor resultado para ele)
    if symbol == my_symbol: return max(move_scores)
    # Caso contrário, busca o valor mínimo (pior resultado para o oponente)
    if symbol != my_symbol: return min(move_scores)


# Função que determina a melhor jogada usando o algoritmo Minimax
def best_move(board, player):
    my_symbol = player["symbol"]  # Define o símbolo do "jogador principal"
    available_spaces = get_available_spaces(board)  # Obtém as posições disponíveis no tabuleiro
    best_move_score = None  # Inicializa o melhor escore com "None" para comparação futura

    # Avalia cada jogada possível e calcula o escore com o Minimax
    for move in available_spaces:
        new_board = make_move(board, int(move), my_symbol)  # Cria um novo tabuleiro com a jogada
        move_score = minimax(new_board, swap_symbol(my_symbol), my_symbol)  # Calcula o escore com Minimax

        # Atualiza a jogada com o maior escore
        if best_move_score is None or move_score > best_move_score:
            best_move_score = move_score
            best_move = move
        
    return best_move  # Retorna a melhor jogada encontrada
