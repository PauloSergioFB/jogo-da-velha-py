import os
import sys
from time import sleep, perf_counter
from concurrent.futures import ThreadPoolExecutor

import text as t
from config import LATENCY, SCREEN_WIDTH, ROBOT_THINKING_MIN_DURATION
from minimax import get_best_move
from utils import get_available_spaces


def clear_screen():
    # Limpa a tela do terminal, dependendo do sistema operacional
    os.system("cls" if os.name == "nt" else "clear")


def clear_row(width):
    # Limpa uma linha específica no terminal
    print("\r".ljust(width + 1), end="", flush=True)


def hide_cursor():
    # Oculta o cursor no terminal
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    # Mostra o cursor no terminal
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def centralize(content, fill=" "):
    # Centraliza o conteúdo baseado na largura da tela
    return content.center(SCREEN_WIDTH, fill)


def centralize_prompt(prompt, fill=" "):
    # Centraliza um prompt de entrada
    n = len(prompt)
    return prompt.rjust((SCREEN_WIDTH - n) // 2 + n, fill)


def display_content(content, centralize=False, fill=" "):
    # Exibe conteúdo na tela com opção de centralização
    sleep(LATENCY)  # Simula latência na exibição

    if centralize: content = centralize(content, fill)
    print(content)


def display_game_screen(players, board, player, game_status="game in process", winning_positions=()):
    # Exibe a tela principal do jogo
    clear_screen()  # Limpa a tela antes de exibir o novo estado
    print(format_scoreboard(players))  # Exibe o placar atualizado
    print(format_board(board, winning_positions))  # Exibe o tabuleiro com possíveis posições vencedoras destacadas

    if game_status == "game in process":
        # Se o jogo está em andamento, mostra de quem é a vez
        print(centralize(format_player_turn(player)))
        return
    
    if game_status == "draw":
        # Se o jogo terminou em empate, exibe a mensagem correspondente
        print(centralize(t.draw_feedback))
        return
    
    if game_status != "draw":
        # Se há um vencedor, exibe a mensagem de vitória
        print(centralize(t.win_feedback.format(player["name"], player["symbol"])))
        return


def calculate_ellipses_animation_stage(content, stage_i):
    # Calcula o estágio atual da animação de reticências
    n = len(content)
    max_stage_i = (n - 3) + stage_i % 4
    return f"\r{content[:max_stage_i]}"


def ellipses_animation(content, final_content, duration):
    # Exibe uma animação de reticências por um determinado tempo
    n = len(content)
    for i in range(duration * 5):
        clear_row(n + 1)

        stage = calculate_ellipses_animation_stage(content, i)
        print(f"\r{stage}", end="", flush=True)
        sleep(0.2)

    clear_row(n + 1)
    # Exibe o conteúdo final após a animação
    print(f"\r{final_content}", end="" if final_content == "" else "\n")


def get_game_mode():
    # Solicita ao usuário que escolha o modo de jogo
    game_modes = {
        "1": "Jogador 1 vs Jogador 2",
        "2": "Jogador 1 vs Computador",
        "0": "Encerrar Programa"
    }

    while True:
        display_content(t.game_mode_options)

        game_mode = input(t.game_mode_prompt)

        if game_modes.get(game_mode) is not None:
            # Se a opção é válida, confirma e retorna o modo escolhido
            display_content(t.game_mode_feedback.format(game_modes.get(game_mode)))
            return int(game_mode)

        display_content(t.invalid_input)

def get_players(game_mode):
    # Configura os jogadores com base no modo de jogo selecionado
    player_1, player_2 = {}, {}

    # Solicita os nomes dos jogadores ou do computador
    player_name_1 = input(t.player_name_prompt.format("Jogador 1"))
    player_name_2 = input(t.player_name_prompt.format(f"{"Jogador 2" if game_mode == 1 else "Computador"}"))

    # Define atributos do Jogador 1
    player_1["name"] = player_name_1 if player_name_1 else "Jogador 1"
    player_1["type"] = "human"
    player_1["symbol"] = "X"
    player_1["wins"] = 0

    # Define atributos do Jogador 2 ou Computador
    player_2["name"] = player_name_2 if player_name_2 else "Jogador 2" if game_mode == 1 else "Computador"
    player_2["type"] = "human" if game_mode == 1 else "robot"
    player_2["symbol"] = "O"
    player_2["wins"] = 0

    return {"player_1": player_1, "player_2": player_2}


def get_human_move(board):
    # Solicita ao jogador humano que insira sua jogada
    while True:
        move = input(centralize_prompt(t.player_move_prompt))
        if not move in get_available_spaces(board):
            # Se a jogada não é válida, informa o usuário e volta à origem do loop
            print(centralize(t.invalid_input))
            continue

        return int(move)


def get_robot_move(board, player):
    # Calcula a jogada do computador usando o algoritmo Minimax
    with ThreadPoolExecutor() as executor:
        future = executor.submit(get_best_move, board, player["symbol"])  # Executa em um thread separado

        robot_move_prompt = centralize_prompt(t.robot_move_prompt)
        n = len(robot_move_prompt)
        stage_i = 0

        start, duration = perf_counter(), 0
        while duration < ROBOT_THINKING_MIN_DURATION or not future.done():
            # Exibe uma animação enquanto o computador calcula a melhor jogada
            clear_row(n + 1)

            stage = calculate_ellipses_animation_stage(robot_move_prompt, stage_i)
            print(f"\r{stage}", end="", flush=True)
            sleep(0.2)

            end = perf_counter()
            duration = (end - start)

            stage_i += 1

        clear_row(n + 1)
        return int(future.result())  # Retorna a jogada calculada


def get_move(player, board):
    # Obtém a jogada, seja de um jogador humano ou do computador
    if player["type"] == "human":
        return get_human_move(board)

    return get_robot_move(board, player)


def format_scoreboard(players):
    # Formata o placar para exibição na tela
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


def format_board(board, highlight_pos=[]):
    # Formata o tabuleiro de jogo para exibição
    values = {}

    i = 1
    for line in board:
        for pos in line:
            # Define o índice ou o símbolo em cada posição do tabuleiro
            values[f"index_{i}"] = str(i) if not pos else " "
            values[f"pos_{i}"] = f" {pos} " if pos else "   "

            # Destaca as posições vencedoras, se houver
            if i in highlight_pos:
                values[f"pos_{i}"] = f"[{pos}]"

            i += 1

    board = t.board.format(**values)
    # Centraliza o tabuleiro com base na largura da tela
    board = "\n".join(line.center(SCREEN_WIDTH) for line in board.splitlines()) + "\n"

    return board


def format_player_turn(player):
    # Formata a mensagem indicando a vez do jogador atual
    return t.player_turn.format(player["name"], player["symbol"])
