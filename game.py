from copy import deepcopy

from utils import get_available_spaces


def initialize_board():
    # Inicializa o tabuleiro como uma matriz 3x3 vazia
    return [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]


def make_move(board, move, symbol):
    # Calcula a linha e a coluna correspondentes ao movimento
    row = (move - 1) // 3
    col = (move - 1) % 3

    # Cria uma cópia do tabuleiro para não alterar o original
    new_board = deepcopy(board)
    
    # Insere o símbolo do jogador na posição especificada
    new_board[row][col] = symbol
    return new_board


def check_game(board):
    # Verifica cada linha para uma condição de vitória
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            winner = board[row][0]
            winner_positions = (row * 3 + 1, row * 3 + 2, row * 3 + 3)

            return winner, winner_positions

    # Verifica cada coluna para uma condição de vitória
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            winner = board[0][col]
            winner_positions = (col + 1, col + 4, col + 7)

            return winner, winner_positions
        
    # Verifica a diagonal principal para uma condição de vitória
    if board[0][0] == board[1][1] == board[2][2] != "":
        winner = board[0][0]
        winner_positions = (1, 5, 9)

        return winner, winner_positions
    
    # Verifica a diagonal secundária para uma condição de vitória
    if board[0][2] == board[1][1] == board[2][0] != "":
        winner = board[0][2]
        winner_positions = (3, 5, 7)

        return winner, winner_positions

    # Verifica se o jogo terminou em empate
    if not get_available_spaces(board): 
        return "draw", ()

    # Retorna que o jogo ainda está em andamento
    return "game in process", ()
