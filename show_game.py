import pickle
import sys
import random
from tetris_game import tetris_interface

filename = sys.argv[1]
f = open(filename, "rb")
games = pickle.load(f)
game = games[0]

actions = []
pieces = []

for play in game:
    actions.append(play["coordinate"])
    pieces.append(play["piece"])

#print(actions)
#print(pieces)

game_exec = tetris_interface.GameRun(
            tetris_interface.Tetris(piece_list=pieces)
        )
game_exec.run_game(actions)
