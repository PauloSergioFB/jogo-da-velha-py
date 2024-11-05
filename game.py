from copy import deepcopy


# Retorna uma lista com as posições disponíveis no tabuleiro
def get_available_spaces(board):
    available_spaces = []

    i = 1
    for line in board:
        for pos in line:
            if pos == "":
                available_spaces.append(str(i))

            i += 1

    return available_spaces


# Cria uma nova cópia do tabuleiro com a jogada realizada em uma posição específica
def make_move(board, move, symbol):
    new_board = deepcopy(board)  # Cria uma cópia para evitar alterar o tabuleiro original

    move_row = (move - 1) // 3  # Calcula a linha da jogada
    move_col = (move - 1) % 3   # Calcula a coluna da jogada

    new_board[move_row][move_col] = symbol  # Atribui o símbolo na posição desejada
    return new_board


# Verifica o estado atual do jogo e identifica um ganhador, empate ou se o jogo continua
def check_game_status(board):
    # Verifica linhas para identificar vitória
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] != "":
            pos_1 = i * 3 + 1
            pos_2 = i * 3 + 2
            pos_3 = i * 3 + 3
            return board[i][0], (pos_1, pos_2, pos_3)  # Retorna o símbolo vencedor e as posições

    # Verifica colunas para identificar vitória
    for i in range(len(board)):
        if board[0][i] == board[1][i] == board[2][i] != "":
            pos_1 = i + 1
            pos_2 = i + 4
            pos_3 = i + 7
            
            return board[0][i], (pos_1, pos_2, pos_3)
        
    # Verifica a diagonal principal para identificar vitória
    if board[0][0] == board[1][1] == board[2][2] != "": 
        pos_1 = 1
        pos_2 = 5
        pos_3 = 9

        return board[0][0], (pos_1, pos_2, pos_3)
    
    # Verifica a diagonal secundária para identificar vitória
    if board[0][2] == board[1][1] == board[2][0] != "":
        pos_1 = 3
        pos_2 = 5
        pos_3 = 7
        
        return board[0][2], (pos_1, pos_2, pos_3)

    # Se não houver espaços disponíveis, o jogo termina em empate
    if get_available_spaces(board) == []:
        return "draw", ()

    # Caso contrário, o jogo ainda está em andamento
    return "game in progress", ()


# Troca o símbolo de "X" para "O" ou vice-versa
def swap_symbol(symbol):
    return "X" if symbol == "O" else "O"
