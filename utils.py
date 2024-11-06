def get_available_spaces(board):
    # Inicializa o contador e a lista de espaços disponíveis
    i, available_spaces = 1, []
    
    for row in board:
        for space in row:
            # Se o espaço estiver vazio, adiciona o índice à lista
            if space == "":
                available_spaces.append(str(i))
            
            i += 1

    return available_spaces


def swap_symbol(symbol):
    # Alterna o símbolo entre "X" e "O"
    return "X" if symbol == "O" else "O"


def get_player_turn(players, n_round):
    # Determina o símbolo do jogador atual com base na rodada
    symbol = "X" if n_round % 2 else "O"

    # Retorna o jogador correspondente ao símbolo atual
    if players["player_1"]["symbol"] == symbol: return players["player_1"]
    if players["player_2"]["symbol"] == symbol: return players["player_2"]
