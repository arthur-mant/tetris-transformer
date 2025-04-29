Este repositório se refere ao gerador de instâncias de jogos para o treinamento inicial do agente. É dependente do StackRabbit, disponível em https://github.com/GregoryCannon/StackRabbit, que deve estar neste diretório.

Será necessário abrir o servidor do StackRabbit em outro terminal antes de rodar qualquer programa, executando, dentro do diretório StackRabbit:

node built/src/server/app.js

Para gerar a base de dados, informe a quantidade de jogos e a quantidade de jogadas por jogo:

python request_data.py NUM_JOGOS NUM_JOGADAS

Os dados serão guardados no diretório data/, sendo referidos pela quantidade de jogos e jogadas
