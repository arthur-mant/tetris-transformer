Este repositório implementa um jogador de Tetris baseado em deep Q-learning

Para treinar uma nova rede, basta executar:

python main.py

Para testar as redes já treinadas, basta executar:

python gameplay.py rede

Onde "rede" é o arquivo de pesos da rede neural, com as já treinadas estando no diretório trained\_nns
Para visualizar o agente jogando, basta adicionar a flag -s

Há 4 diferentes redes, com cada uma sendo treinada utilizando uma função de recompensa diferente. Cada uma deve ser utilizada somente na sua respectiva branch:

A branch main (e a branch original-continuous, da qual a main é uma cópia) se refere ao agente treinado com uma função de recompensa variável que se altera de forma contínua, com a sua rede neural treinada sendo chamada de "continuous.h5"

A branch original-discrete se refere ao agente treinado com uma função de recompensa variável que se altera de forma discreta, com sua rede neural sendo chamada de "discret.h5"

A branch test-original se refere ao agente treinado com uma função de recompensa fixa, com sua rede neural sendo chamada de "fixo.h5"

A branch score-real se refere ao agente treinado com a função de recompensa igual à pontuação do jogo (normalizada), com sua rede neural sendo chamada de "real.h5"
