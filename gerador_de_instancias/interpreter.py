import pickle
import sys
import random

cols = 10
filename = sys.argv[1]

def print_board(board):
    for row in board:
        aux = "|"
        for elem in row:
            aux += elem
        print(aux, "|")
    aux = ""
    for _ in range(cols+2):
        aux += "-"
    print(aux)

def print_play(play):
    print_board(play["board"])
    print("Piece: ", play["piece"])
    print("Next Piece: ", play["next_piece"])
    print("Action: ", play["action"])
    print("Lines Cleared: ", play["lines_cleared"])

f = open(filename, "rb")
games = pickle.load(f)

game = random.choice(games)
for play in game:
    print_play(play)

#play = random.choice(game)
#print("random play selected from file:")
#print_play(play)



#print("Route: ", game[i]["route"])

