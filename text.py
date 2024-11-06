# Iniciando Programa
starting_program = "Iniciando Jogo da Velha..."  # Mensagem exibida ao iniciar o programa
started_program = "Jogo da Velha Iniciado\n"     # Mensagem exibida após o programa iniciar

# Escolher Modo de Jogo
game_mode_options = """Escolha um modo de jogo:
[1] Jogador 1 vs Jogador 2
[2] Jogador 1 vs Computador
[0] Encerrar Programa\n"""  # Opções de modos de jogo disponíveis

game_mode_prompt = "Sua escolha: "               # Prompt para o usuário selecionar o modo de jogo
game_mode_feedback = "Você escolheu: {}\n"       # Feedback após a escolha do usuário

# Escolher Apelidos para os Jogadores
player_name_prompt = "Digite um apelido para o {}: "  # Solicita o apelido para cada jogador

# Jogo
scoreboard = "{p1}({p1_symbol}) {p1_score} x {p2_score} {p2}({p2_symbol})"  # Formato do placar do jogo

# Representação do tabuleiro do jogo com placeholders
board = """{index_1}      |{index_2}      |{index_3}      
  {pos_1}  |  {pos_2}  |  {pos_3}  
       |       |       
-------|-------|-------
{index_4}      |{index_5}      |{index_6}      
  {pos_4}  |  {pos_5}  |  {pos_6}  
       |       |       
-------|-------|-------
{index_7}      |{index_8}      |{index_9}      
  {pos_7}  |  {pos_8}  |  {pos_9}  
       |       |       """  # Estrutura do tabuleiro com índices e posições

player_turn = "Vez do {}({})\n"  # Mensagem indicando de quem é a vez

# Definir Jogada
player_move_prompt = "Digite a sua jogada: "  # Prompt para o jogador inserir sua jogada
robot_move_prompt = "Pensando..."             # Mensagem exibida enquanto o robô "pensa"
robot_move_feedback = "Jogou em: {}"          # Feedback após o robô realizar sua jogada

# Fim de Jogo
draw_feedback = "Empate!\n"                   # Mensagem de empate
win_feedback = "{}({}) Venceu!\n"             # Mensagem de vitória com nome e símbolo do vencedor

# Jogar Novamente
rematch_prompt = "Jogar Novamente? (S/N): "   # Pergunta se o usuário deseja jogar novamente

# Encerrando Programa
end_program = "Programa Encerrado"            # Mensagem exibida ao encerrar o programa

# Entrada Inválida
invalid_input = "Entrada Inválida!\n"         # Mensagem para entrada inválida do usuário
