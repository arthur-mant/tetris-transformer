import pickle

cols = 10
filename = "./data/player/plays_games100size1000.pkl"
i = 567


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




f = open(filename, "rb")
game = pickle.load(f)

print(game[i])

print_board(game[i]["board"])
print("Piece: ", game[i]["piece"])
print("Next Piece: ", game[i]["next_piece"])
print("Coordinate: ", game[i]["coordinate"])

#print("Route: ", game[i]["route"])

