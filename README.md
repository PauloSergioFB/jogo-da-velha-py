# Jogo da Velha em Python

Uma implementação do jogo da velha em Python, incluindo um modo de jogo contra o computador utilizando o algoritmo Minimax.

## Sumário

- Configuração e Execução
- Estrutura do Projeto
- Funcionalidades Disponíveis
- Algoritmo Minimax

## Configuração e Execução

Para executar o jogo na sua máquina, siga os passos abaixo:

1. Clone o repositório:

```bash 
git clone https://github.com/PauloSergioFB/jogo-da-velha.git
```

2. Navegue até o diretório do projeto:

```bash
cd jogo-da-velha
```

3. Execute o programa:

```bash
python main.py 
```

Certifique-se de ter o Python 3 instalado na sua máquina.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

- main.py: Ponto de entrada do programa. Gerencia o fluxo principal do jogo.
- game.py: Contém a lógica do jogo da velha, incluindo funções para inicializar o tabuleiro, fazer movimentos e verificar o estado do jogo.
- utils.py: Funções utilitárias usadas em todo o projeto, como alternar símbolos e determinar o jogador atual.
- minimax.py: Implementação do algoritmo Minimax para permitir que o computador jogue de forma ótima contra o jogador humano.
- ui.py: Gerencia a interface do usuário no terminal, incluindo a exibição do tabuleiro, placar e interação com o usuário.
- config.py: Arquivo de configuração contendo constantes usadas no programa, como largura da tela e delays.
- text.py: Armazena todas as mensagens de texto exibidas ao usuário, permitindo fácil modificação e tradução.

## Funcionalidades Disponíveis

- Modos de Jogo:
- Jogador vs Jogador: Dois jogadores humanos jogam um contra o outro.
- Jogador vs Computador: Jogue contra o computador, que usa o algoritmo Minimax para determinar as melhores jogadas.

- Placar: O jogo mantém o placar entre os jogadores durante a sessão.

- Interface Interativa: Interface de linha de comando amigável, com tabuleiro visual e prompts claros.

## Algoritmo Minimax

O algoritmo Minimax é uma abordagem recursiva utilizada em jogos de soma zero para minimizar a perda máxima possível. No contexto do jogo da velha, o algoritmo explora todos os movimentos possíveis do tabuleiro, atribuindo valores a estados de vitória, derrota ou empate, e escolhe a jogada que maximiza a chance de vitória ou minimiza a chance de derrota.

Como funciona no jogo:

- Estado Terminal: O algoritmo verifica se o jogo terminou em vitória, derrota ou empate.
- Recursão: Se o jogo não terminou, o algoritmo simula todos os movimentos possíveis, alternando entre os turnos dos jogadores.
- Avaliação: Cada movimento é avaliado com uma pontuação:
    - Vitória: +1
    - Derrota: -1
    - Empate: 0
- Escolha Ótima: O computador escolhe a jogada com a pontuação máxima possível, garantindo a melhor estratégia possível.

Esse algoritmo assegura que o computador jogue de forma perfeita, tornando-se um oponente desafiador e impossível de vencer se jogar de maneira ideal.

---

Divirta-se jogando!