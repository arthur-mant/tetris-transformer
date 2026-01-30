import player
import rewards
import sys
import torch
from tetris_game import tetris_interface
import numpy as np
import cnn
import time
import pickle

if len(sys.argv) <= 1:
    print("please inform neural network weights file")
    sys.exit(0)

use_screen = "-s" in sys.argv or "--screen" in sys.argv

if use_screen:
    print("Using screen")
    from tetris_game import exec_game
else:
    print("Not showing games on screen, to do it use the flag -s")

nn_file = sys.argv[-1]
nn_name = nn_file.split("/")[-1]
nn_name = nn_name.split("_episode")[0]
nn_name = nn_name.split("_most_recent")[0]

model = cnn.CNN()
model.load_state_dict(torch.load(nn_file, weights_only=True))

p1 = player.player(model, 0, 0, False, nn_name, 0.99)

#jogando os jogos

n_games = 10000
max_plays = 100000

#lines = [4*[0] for i in range(n_games)]
#game_length = []
#game_score = []

game_data = []

print("max game length: ", max_plays)

for i in range(n_games):
    game = tetris_interface.Tetris()
    if use_screen:
        game_exec = exec_game.GameRun(game)

    time_used = 0
    lines = 4*[0]
    height_list = []

    for play in range(max_plays):
        if game.gameover:
            break
        board, piece, next_piece = game.get_state()
        t = time.time()
        action, route = p1.act(board, piece, next_piece)
        time_used += time.time() - t

        height_list.append(18-action[0])

        if use_screen:
            lines_cleared = game_exec.run_game(route)
        else:
            lines_cleared = game.play_route(route)

        if lines_cleared > 0:
            lines[lines_cleared-1] += 1
    print("game ", i, " score: ", game.score, " number of pieces: ", game.pieces)
    print("lines_cleared: ")
    print("total time: ", time_used)
    for j in range(4):
        print(j+1, ": ", lines[j])
    #game_length.append(game.pieces)
    #game_score.append(game.score)
    game_data.append({
        "height_list": height_list,
        "avg_time": time_used/game.pieces,
        "lines": lines,
        "score": game.score,
        "game_length": game.pieces
    })
    print(game_data[-1])

fileObj = open("test_results/results_"+nn_name+".pkl", 'wb')
pickle.dump(game_data, fileObj)
fileObj.close()

#print("mean length: ", np.mean(game_length))
#print("mean score: ", np.mean(game_score))
#print("score std deviation: ", np.std(game_score))
