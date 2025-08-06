import pickle
import sys
from tetris_game import exec_game
from tetris_game import tetris_interface
import tetris_parser
import time

filename = sys.argv[1]
f = open(filename, "rb")
game = pickle.load(f)

actions = []
pieces = []

for play in game:
    actions.append(play["action"])
    pieces.append(play["piece"])

tetris_game = tetris_interface.Tetris(piece_list=pieces)
game_exec = exec_game.GameRun(tetris_game)

for action in actions:
    board = tetris_game.translate_board(tetris_game.field)
    route = tetris_parser.get_route(board, tetris_game.piece.type, action[0], action[1], action[2], [], [])
    game_exec.run_game(route)
    tetris_game.freeze()

time.sleep(10)
