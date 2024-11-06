from ui import *
from game import *
from config import STARTING_PROGRAM_DELAY, ROBOT_FEEDBACK_PLAY_DURATION
from utils import get_player_turn, swap_symbol


def new_game(players):
    # Inicializa o tabuleiro e o contador de rodadas
    board, n_round = initialize_board(), 1
    while True:
        # Obtém o jogador atual com base na rodada
        player = get_player_turn(players, n_round)

        # Exibe o estado atual do jogo
        display_game_screen(players, board, player)

        # Obtém a jogada do jogador atual
        move = get_move(player, board)
        # Atualiza o tabuleiro com a jogada realizada
        board = make_move(board, move, player["symbol"])

        if player["type"] == "robot":
            # Se o jogador for o computador, oculta o cursor e exibe feedback
            hide_cursor()

            clear_screen()
            display_game_screen(players, board, player)
            print(centralize(t.robot_move_feedback.format(move)))

            # Pausa para exibir a jogada do robô
            sleep(ROBOT_FEEDBACK_PLAY_DURATION)
            show_cursor()

        # Verifica o status atual do jogo
        game_status, winning_positions = check_game(board)
        if game_status == "game in process":
            # Se o jogo ainda está em andamento, incrementa a rodada e continua
            n_round += 1
            continue

        if game_status != "draw":
            # Se houve um vencedor, incrementa a pontuação do jogador
            player["wins"] += 1

        # Alterna os símbolos dos jogadores para a próxima partida
        players["player_1"]["symbol"] = swap_symbol(players["player_1"]["symbol"])
        players["player_2"]["symbol"] = swap_symbol(players["player_2"]["symbol"])

        # Exibe a tela final do jogo com o resultado
        display_game_screen(players, board, player, game_status, winning_positions)
        break


def rematch():
    # Pergunta ao usuário se deseja jogar novamente
    while True:
        user_input = input(centralize_prompt(t.rematch_prompt)).upper()

        if not user_input in ["S", "N"]:
            # Se a entrada não é válida informa o usuário e volta à origem do loop
            print(centralize(t.invalid_input))
            continue

        # Retorna True se o usuário quiser jogar novamente
        return bool(user_input == "S")


def main():
    # Exibe uma animação de inicialização do programa
    ellipses_animation(t.starting_program, t.started_program, STARTING_PROGRAM_DELAY)
    while True:
        # Solicita o modo de jogo ao usuário
        game_mode = get_game_mode()
        if game_mode == 0:
            # Encerra o programa se o usuário escolher o modo de jogo 0
            break

        # Configura os jogadores de acordo com o modo selecionado
        players = get_players(game_mode)
        while True:
            # Inicia uma nova partida
            new_game(players)
            if not rematch():
                # Limpa a tela se o usuário não quiser jogar novamente
                clear_screen()
                break

    # Exibe a mensagem de encerramento do programa
    display_content(t.end_program)


if __name__ == "__main__":
    try:
        main()
    except:
        # Garante que o cursor será mostrado novamente em caso de erro
        show_cursor()
        raise
