import random
import requests
import pickle
import sys
sys.path.insert(0, '..')
from tetris_game import definitions
from datetime import datetime
import numpy as np

sys.path.append("/home/lann/mestrado/tetris-transformer/")
import tetris_parser


if len(sys.argv) < 3 or not sys.argv[1].isnumeric() or not sys.argv[1].isnumeric():
    print("Informe o número de jogos e o número de jogadas")
    print("python request_data.py NUM_JOGOS NUM_JOGADAS")
    sys.exit(0)
n_games = int(sys.argv[1])
number_of_plays = int(sys.argv[2])

cols = 10
rows = 20
url = "http://localhost:3000"
recording_dir = "./data/"

piece_vector = definitions.piece_vector
pieces = definitions.pieces

def get_piece():
    return random.randrange(7)

def matrix_sub(A, B):
    C = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            C[i][j] = str(int(A[i][j]) - int(B[i][j]))
    return C

def vector_equal(V, U):
    for i in range(len(V)):
        if(V[i] != U[i]):
            return False
    return True


class game:

    piece = get_piece()
    next_piece = get_piece()
    history = []
    board = [[str(0) for _ in range(cols)] for _ in range(rows)]
    completed_games = []
    scores = []
    length = []

    archive_filename = recording_dir+"n_games"+str(n_games)+"n_plays"+str(number_of_plays)+".pkl"

    def new_game(self):
        self.piece = get_piece()
        self.next_piece = get_piece()
        self.board = [[str(0) for _ in range(cols)] for _ in range(rows)]

    def print_board(self, board):
        for row in range(len(board)):
            aux = ""
            if row < 10:
                aux += "0"
            aux += str(row)+" |"
            for elem in board[row]:
                aux += str(elem)
            print(aux, "|")
        aux = ""
        for _ in range(cols+2+4):
            aux += "-"
        print(aux)

    def print_game(self):
        print("Piece: ", self.piece, "  Next Piece: ", self.next_piece)
        self.print_board(self.board)
        print(self.history)

    def make_request(self, url):

        req = url + "/get-move?board="

        for row in self.board:
            for elem in row:
                req += elem

        req += "&currentPiece="\
                +piece_vector[self.piece]\
                +"&nextPiece="\
                +piece_vector[self.next_piece]\
                +"&level=25&lines=0&inputFrameTimeline=X"


        response = requests.get(req)

        if response.status_code != 200:
            raise Exception(f"request received error {response.status_code}. Is the server okay?")

        return response.text


    def treat_response(self, text):

        if ("No legal moves" in text):
            return -1, -1

        aux = text.split("|")       #[:-2]

        #rotacao, translacao, altura = list(map(int, aux[0].split(',')))
        #print(rotacao, translacao, altura)

        path = aux[1]

        board = [ aux[2][i:i+cols] for i in range (0, len(aux[2]), cols) ]

        return board, path

    def convert_to_int(self, board):
        out = []
        for line in board:
            aux = []
            for elem in line:
                aux.append(int(elem))
            out.append(aux)
        return out

    def update_game(self, board):
        self.board = board
        self.piece = self.next_piece
        self.next_piece = get_piece()

    def save_player_data(self):

        print("Saved ", len(self.history), " completed games to ", self.archive_filename)
        fileObj = open(self.archive_filename, 'wb')
        pickle.dump(self.history, fileObj)
        fileObj.close()

        #fileObj = open(self.route_archive_filename, 'wb')
        #pickle.dump(self.route_history, fileObj)
        #fileObj.close()

    def generate_player_db(self, n_games, n_plays):
        print("Number of games: ", n_games)
        print("Size of each game: ", n_plays)
        print("Total plays: ", n_games*n_plays)
        line_score = [400, 1000, 3000, 12000]
        for n in range(n_games):
            self.new_game()
            game_data = []
            i = 0
            lost = False
            score = 0
            while ((i < n_plays) and (not lost)):
                nxt_board, path = self.treat_response(self.make_request(url))
                if (nxt_board == -1):
                    lost = True
                    game_data[-1]['gameover'] = True
                    break

                piece_coordinates, lines_cleared = self.board_to_coordinate(nxt_board)
                if piece_coordinates == None:
                    print("ERROR: NULL ACTION")
                    #self.print_board(self.board)
                    #self.print_board(nxt_board)
                if lines_cleared > 4:
                    print(lines_cleared)
                    self.print_board(self.board)
                    self.print_board(nxt_board)
                game_data.append({
                    'board': self.convert_to_int(self.board),
                    'piece': self.piece,
                    'next_piece': self.next_piece,
                    'action': piece_coordinates,
                    'lines_cleared': lines_cleared,
                    'gameover': False
                })
                self.update_game(nxt_board)
                i = i+1

                if lines_cleared > 0:
                    #print(lines_cleared)
                    score += line_score[lines_cleared-1]

                if ('1' in nxt_board[0]) or ('1' in nxt_board[1]):
                    lost = True
                    game_data[-1]['gameover'] = True
                    break

            print("game ", n, ", score ", score, " length " , len(game_data))
            self.scores.append(score)
            self.length.append(len(game_data))
            self.history.append(game_data)
            if n % 10 == 10-1:
                self.save_player_data()
        self.save_player_data()

        print("mean length: ", np.mean(self.length))
        print("mean score: ", np.mean(self.scores))
        print("score std deviation: ", np.std(self.scores))

    def get_coordinates(self, piece_board):

        blocks = 0
        for i in piece_board:
            for j in i:
                blocks += int(j)
        for i in range(-2, rows):
            for j in range(-2, cols):
                for r in range(len(pieces[self.piece])):
                    viable = True
                    new_blocks = 0
                    for elem in pieces[self.piece][r]:
                        k = elem // 4
                        l = elem % 4
                        if i+k < -2 or (i+k) >= len(self.board) or j+l < 0 or j+l >= len(self.board[0]) or (i+k >=0 and piece_board[i+k][j+l] == '0'):
                            viable = False
                            break
                        if (i+k >=0 and piece_board[i+k][j+l] == '1'):
                            new_blocks += 1
                    if blocks == new_blocks and viable:
                        return i, j, r
        return None

    def simulate_and_check(self, pos, new_board):
        aux_board = []
        for i in range(rows):
            aux_row = []
            for j in range(cols):
                aux_row.append(self.board[i][j])
            aux_board.append(aux_row)

        for e in pieces[self.piece][pos[2]]:
            i = e // 4
            j = e % 4

            if pos[0]+i == -1 or pos[0]+i == -2:
                pass
            elif aux_board[pos[0]+i][pos[1]+j] == '0':
                aux_board[pos[0]+i][pos[1]+j] = '1'
            else:
                print(pos)
                print("ERROR: Wrong position when decoding line board")
                return False

        for i in range(rows):
            complete = True
            for j in range(cols):
                if aux_board[i][j] == '0':
                    complete = False
            if complete:
                for k in range(i, 0, -1):
                    for l in range(cols):
                        aux_board[k][l] = aux_board[k-1][l]
                for l in range(cols):
                    aux_board[0][l] = '0'

        for i in range(rows):
            for j in range(cols):
                if aux_board[i][j] != new_board[i][j]:
                    return False
        return True

    def board_to_coordinate(self, new_board):

        piece_board = matrix_sub(new_board, self.board)
        #self.print_board(piece_board)

        cleared_lines = False
        for i in range(rows):
            for j in range(cols):
                if piece_board[i][j] == '-1':
                    cleared_lines = True
        if not cleared_lines:
            pos = self.get_coordinates(piece_board)
            if self.simulate_and_check(pos, new_board):
                return pos, 0
            else:
                print("ERROR: simulation failed")
                print(pos)
                print(self.board)
                print(new_board)
                print("Piece: ", self.piece)


        lines_cleared = 0
        for j in range(len(piece_board[0])):
            depth_count = 0
            for i in range(len(piece_board)):
                if piece_board[i][j] == '-1':
                    depth_count += 1
                if depth_count > 0 and piece_board[i][j] == '0':
                    break
            lines_cleared = max(lines_cleared, depth_count)

        for pos in tetris_parser.get_possible_actions(self.convert_to_int(self.board), self.piece):
            if self.simulate_and_check(pos, new_board):
                return pos, lines_cleared
        print("something is wrong....")
        print(self.board)
        print(new_board)
        print("Piece: ", self.piece)
        return None, None

x = game()
x.generate_player_db(n_games, number_of_plays)
