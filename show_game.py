import pickle
import sys
import random
from tetris_game import tetris_show
import tetris_parser

filename = sys.argv[1]
f = open(filename, "rb")
game = pickle.load(f)

actions = []
pieces = []

for play in game:
    actions.append(play["action"])
    pieces.append(play["piece"])

game = tetris_interface.Tetris(piece_list=pieces)
for action in actions:
    route = tetris_parser.get_route(game.field, game.piece.type, action[0], action[1], action[2], [], [])
game_exec.run_game(actions)
