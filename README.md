# Batalha Naval P2P (UDP)

Este é um jogo de Batalha Naval multiplayer ponto-a-ponto (P2P) desenvolvido em Python. O jogo utiliza a interface gráfica padrão do Python (`tkinter`) e `sockets` UDP para comunicação, permitindo que dois jogadores se conectem e joguem através da rede.

## 📋 Pré-requisitos

Para rodar este projeto a partir do zero, você precisará apenas do **Python 3.6 ou superior** instalado na sua máquina. O projeto não requer nenhuma instalação de bibliotecas externas (pip install), pois utiliza apenas bibliotecas padrões da linguagem.

*Para verificar se você tem o Python instalado, abra seu terminal/prompt de comando e digite:*
```bash
python --version
```

## 🚀 Como Rodar o Jogo

Se você quiser testar o jogo localmente (simulando dois jogadores na mesma máquina), siga estes passos:

1. **Abra dois Terminais diferentes** (pode ser o Prompt de Comando do Windows, PowerShell ou o terminal integrado da sua IDE) e navegue até a pasta do projeto em ambos:
   ```bash
   cd "caminho/para/pasta/Batalha Naval"
   ```

2. **Inicie o Jogador 1 (Host):** No primeiro terminal, execute:
   ```bash
   python main.py
   ```
   * Na tela inicial, clique em **Host (Criar Partida)**.
   * A Porta Local já estará preenchida com `5000`.
   * Clique em **Iniciar Host** e aguarde.

3. **Inicie o Jogador 2 (Join):** No segundo terminal, execute:
   ```bash
   python main.py
   ```
   * Na tela inicial, clique em **Join (Entrar em Partida)**.
   * As portas e o IP estarão preenchidos automaticamente para testes locais (IP `127.0.0.1`, Porta do Host `5000` e Sua Porta Local `5001`).
   * Clique em **Entrar**.

> Se for jogar em computadores diferentes (em uma rede local ou via Hamachi/Radmin), substitua o IP `127.0.0.1` pelo Endereço IPv4 da rede do outro computador.

## 🎮 Como Jogar

1. **Sorteio:** Assim que ambos se conectarem, a tela do minigame "Pedra, Papel e Tesoura" aparecerá. Façam as escolhas simultaneamente. Quem vencer inicia a partida com o tabuleiro liberado. (Se der empate, escolham novamente).
2. **O Tabuleiro:** O seu tabuleiro é preenchido de forma aleatória com sua frota (os blocos azuis claros). Você enxerga seus barcos no lado esquerdo ("Meu Tabuleiro") e atira no lado direito ("Tabuleiro Alvo").
3. **Regras da Batalha:**
   - Clique no tabuleiro alvo para atirar.
   - **Tiro na água:** Se o quadrante ficar **verde/cinza**, você errou. É a vez do oponente.
   - **Tiro no navio:** Se o quadrante ficar **vermelho**, você acertou parte de uma embarcação e **ganha o direito de atirar novamente**.
4. **Chat:** Durante toda a partida, você pode enviar mensagens de texto utilizando a caixa localizada ao lado direito da tela de jogo.
5. **Fim de jogo:** O jogo encerra automaticamente quando um dos jogadores atingir as 10 partes totais dos navios inimigos (3 Submarinos, 2 Cruzadores, 1 Porta-aviões).
