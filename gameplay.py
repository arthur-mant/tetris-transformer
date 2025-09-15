import player
import rewards
import sys
import torch
from tetris_game import tetris_interface
from tetris_game import exec_game
import numpy as np

#inicializando a rede

if len(sys.argv) <= 1:
    print("please inform neural network weights file")
    sys.exit(0)

use_screen = "-s" in sys.argv or "--screen" in sys.argv

if use_screen:
    print("Using screen")
else:
    print("Not showing games on screen, to do it use the flag -s")

nn_file = sys.argv[-1]
nn_name = nn_file.split("/")[1]
nn_name = nn_name.split("_episode")[0]
nn_name = nn_name.split("_most_recent")[0]

if "cnn" in nn_name:
    import cnn
    model = cnn.CNN()
else:
    import mlp
    model = mlp.MLP(False)
model.load_state_dict(torch.load(nn_file, weights_only=True))

rewards_object = rewards.Rewards('q', 'q')

p1 = player.player(model, 0, 0, False, rewards_object, nn_name, 0.99)

#jogando os jogos

n_games = 10
max_plays = 1000
lines = [4*[0] for i in range(n_games)]

game_length = []

for i in range(n_games):
    game = tetris_interface.Tetris()
    if use_screen:
        game_exec = exec_game.GameRun(game)

    for play in range(max_plays):
        if game.gameover:
            break
        board, piece, next_piece = game.get_state()
        action, route = p1.act(board, piece, next_piece)

        if use_screen:
            lines_cleared = game_exec.run_game(route)
        else:
            lines_cleared = game.play_route(route)

        if lines_cleared > 0:
            lines[i][lines_cleared-1] += 1
    print("game ", i, " score: ", game.score, " number of pieces: ", game.pieces)
    print("lines_cleared: ")
    for j in range(4):
        print(j+1, ": ", lines[i][j])
    game_length.append(game.pieces)
print("mean length: ", np.mean(game_length))
