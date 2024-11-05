import os
import sys
from time import sleep, perf_counter
from concurrent.futures import ThreadPoolExecutor

from constants import *
from game import *
from ai import best_move

import text as t


# Função para limpar a tela, usa "cls" para Windows e "clear" para outros sistemas operacionais
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Funções para esconder e mostrar o cursor no terminal
def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


# Função para exibir conteúdo na tela, com opção de centralizar e usar um caractere de preenchimento
def display_content(content, centralize=False, fill=" "):
    sleep(LATENCY)

    if centralize: content = centralize(content, fill)
    print(content)


# Função que centraliza o conteúdo com um caractere de preenchimento opcional
def centralize(content, fill=" "):
    return content.center(SCREEN_WIDTH, fill)


# Centraliza o prompt (ex: pergunta ao usuário), alinhando-o horizontalmente
def centralize_prompt(prompt, fill=" "):
    n = len(prompt)

    return prompt.rjust((SCREEN_WIDTH - n) // 2 + n, fill)


# Animação com reticências durante uma espera, atualiza o conteúdo em ciclos
def animate_ellipses(content, final_content, duration):
    n = len(content)

    for i in range(duration * 5):
        print("\r".ljust(n + 1), end="", flush=True)

        stage = content[:(n - 3) + i % 4]
        print(f"\r{stage}", end="", flush=True)

        sleep(0.2)

    print("\r".ljust(n + 1), end="", flush=True)
    print(f"\r{final_content}", end="" if final_content == "" else "\n")


# Formata o placar de pontuação dos jogadores, usando um dicionário para preencher o layout
def format_scoreboard(players):
    fill = "#"
    values = {
        "p1": players["player_1"]["name"],
        "p1_symbol": players["player_1"]["symbol"],
        "p1_score": players["player_1"]["wins"],
        "p2": players["player_2"]["name"],
        "p2_symbol": players["player_2"]["symbol"],
        "p2_score": players["player_2"]["wins"],
    }

    scoreboard = "".ljust(SCREEN_WIDTH, fill) + "\n"
    scoreboard += f" {t.scoreboard.format(**values)} ".center(SCREEN_WIDTH, fill) + "\n"
    scoreboard += "".ljust(SCREEN_WIDTH, fill) + "\n"

    return scoreboard


# Formata o tabuleiro do jogo e permite destacar posições específicas
def format_board(board, highlight_pos=[]):
    values = {}

    i = 1
    for line in board:
        for pos in line:
            values[f"index_{i}"] = str(i) if not pos else " "
            values[f"pos_{i}"] = f" {pos} " if pos else "   "

            if i in highlight_pos: values[f"pos_{i}"] = f"[{pos}]"

            i += 1

    board = t.board.format(**values)

    board = "\n".join(line.center(SCREEN_WIDTH) for line in board.splitlines()) + "\n"

    return board


# Formata o turno do jogador exibindo seu nome e símbolo
def format_player_turn(player):
    return t.player_turn.format(player["name"], player["symbol"])


# Exibe as opções de modo de jogo e permite ao usuário escolher uma opção válida
def get_game_mode():
    game_modes = {
        "1": "Jogador 1 vs Jogador 2",
        "2": "Jogador 1 vs Computador",
        "0": "Encerrar Programa"
    }

    while True:
        display_content(t.game_mode_options)

        game_mode = input(t.game_mode_prompt)

        if game_modes.get(game_mode) is not None:
            display_content(t.game_mode_feedback.format(game_modes.get(game_mode)))
            return int(game_mode)

        display_content(t.invalid_input)


# Inicializa os jogadores de acordo com o modo de jogo selecionado
def get_players(game_mode):
    player_1, player_2 = {}, {}

    player_name_1 = input(t.player_name_prompt.format("Jogador 1"))
    player_name_2 = input(t.player_name_prompt.format(f"{'Jogador 2' if game_mode == 1 else "Computador"}"))

    player_1["name"] = player_name_1 if player_name_1 else "Jogador 1"
    player_1["type"] = "human"
    player_1["symbol"] = "X"
    player_1["wins"] = 0

    player_2["name"] = player_name_2 if player_name_2 else "Jogador 2" if game_mode == 1 else "Computador"
    player_2["type"] = "human" if game_mode == 1 else "robot"
    player_2["symbol"] = "O"
    player_2["wins"] = 0

    return {"player_1": player_1, "player_2": player_2}


# Alterna o turno entre os jogadores com base no número da rodada
def get_player_turn(players, n_round):
    symbol = "X" if n_round % 2 else "O"

    if players["player_1"]["symbol"] == symbol: return players["player_1"]
    if players["player_2"]["symbol"] == symbol: return players["player_2"]


# Recebe a jogada do jogador humano e valida se é um espaço disponível
def get_human_move(board):
    while True:
        move = input(centralize_prompt(t.player_move_prompt))

        if not move in get_available_spaces(board):
            print(centralize(t.invalid_input))
            continue

        return move


# Gera a jogada do computador usando uma função assíncrona para pensar por um tempo
def get_robot_move(board, player):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(best_move, board, player)

        min_duration = ROBOT_THINKING_DELAY
        start = perf_counter()
        duration = 0

        i = 0
        content = centralize_prompt(t.robot_move_prompt)
        n = len(content)

        while duration <= min_duration or not future.done():
            print("\r".ljust(n + 1), end="", flush=True)

            stage = content[:(n - 3) + i % 4]
            print(f"\r{stage}", end="", flush=True)

            sleep(0.2)

            end = perf_counter()
            duration = (end - start)

            i += 1

        print("\r".ljust(n + 1), end="", flush=True)
        print("\r", end="")

        move = future.result()

    print(centralize(t.robot_move_feedback.format(move)))

    hide_cursor()
    sleep(ROBOT_FEEDBACK_PLAY_DURATION)
    show_cursor()

    return move


# Função principal do jogo, controla o fluxo de rodadas e exibe o placar
def game(players):
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    n_round = 1

    while True:
        player = get_player_turn(players, n_round)

        clear_screen()

        print(format_scoreboard(players))
        print(format_board(board))
        print(centralize(format_player_turn(player)))

        move = get_human_move(board) if player["type"] == "human" else get_robot_move(board, player)
        board = make_move(board, int(move), player["symbol"])
        game_status, winning_pos = check_game_status(board)

        if game_status == "game in progress":
            n_round += 1
            continue

        clear_screen()

        print(format_scoreboard(players))
        print(format_board(board, winning_pos))

        if game_status == "draw": print(centralize(t.draw_feedback))

        if game_status in ["X", "O"]:
            print(centralize(t.win_feedback.format(player["name"], player["symbol"])))

            if players["player_1"]["symbol"] == game_status: players["player_1"]["wins"] += 1
            if players["player_2"]["symbol"] == game_status: players["player_2"]["wins"] += 1

        players["player_1"]["symbol"], players["player_2"]["symbol"] = players["player_2"]["symbol"], players["player_1"]["symbol"]
        return players


# Pergunta ao usuário se ele deseja uma revanche após o término do jogo
def rematch():
    while True:
        user_input = input(centralize_prompt(t.rematch_prompt)).upper()

        if not user_input in ["S", "N"]:
            print(centralize(t.invalid_input))
            continue

        return bool(user_input == "S")


# Função principal do programa, inicia e controla o fluxo de seleção de modos e partidas
def main():
    animate_ellipses(t.starting_program, t.started_program, STARTING_PROGRAM_DELAY)

    while True:
        game_mode = get_game_mode()
        if game_mode == 0: break

        players = get_players(game_mode)

        while True:
            players = game(players)
            if not rematch():
                clear_screen()
                break

    display_content(t.end_program)


# Executa o programa principal e restaura o cursor em caso de erro inesperado
if __name__ == "__main__":
    try:
        main()
    except:
        show_cursor()
        raise
