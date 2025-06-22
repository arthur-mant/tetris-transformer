import random
import requests
import pickle
import sys
sys.path.insert(0, '..')
from tetris_game import definitions
from datetime import datetime


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
                aux += elem
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

    def generate_player_db(self, n, n_plays):
        print("Number of games: ", n)
        print("Size of each game: ", n_plays)
        print("Total plays: ", n*n_plays)
        for n in range(n):
            self.new_game()
            i = 0
            lost = False
            while ((i < n_plays) and (not lost)):
                nxt_board, path = self.treat_response(self.make_request(url))
                if (nxt_board == -1):
                    lost = True
                    self.history[-1]['gameover'] = True
                    break

                piece_coordinates, lines_cleared = self.board_to_coordinate(nxt_board)
                self.history.append({
                    'board': self.convert_to_int(self.board),
                    'piece': self.piece,
                    'next_piece': self.next_piece,
                    'action': piece_coordinates,
                    'lines_cleared': lines_cleared,
                    'gameover': False
                })
                self.update_game(nxt_board)
                i = i+1
            if n % 10 == 10-1:
                self.save_player_data()
        self.save_player_data()

    def get_coordinates(self, piece_board):
        for i in range(-2, rows):
            for j in range(-2, cols):
                m = []
                for k in range(4):
                    for l in range(4):
                        if  (i+k >= 0) and (j+l >= 0) and \
                            (i+k < len(self.board)) and \
                            (j+l < len(self.board[0])) and \
                            (piece_board[i+k][j+l] == '1'):

                            m.append(k*4+l)

                if (len(m) == 4):
                    for k in range(len(pieces[self.piece])):
                        if vector_equal(m, pieces[self.piece][k]):
                            return i, j, k
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

            if aux_board[pos[0]+i][pos[1]+j] == '0':
                aux_board[pos[0]+i][pos[1]+j] = '1'
            else:
                print("ERROR: Wrong position when decoding line board")


        for i in range(rows):
            complete = True
            for j in range(cols):
                if aux_board[i][j] == '0':
                    complete = False
            if complete:
                for k in range(i, 0, -1):
                    for l in range(cols):
                        aux_board[k][l] = aux_board[k-1][l]



        for i in range(rows):
            for j in range(cols):
                if aux_board[i][j] != new_board[i][j]:
                    return False
        return True

    def board_to_coordinate(self, new_board):

        piece_board = matrix_sub(new_board, self.board)

        cleared_lines = False
        for i in range(rows):
            for j in range(cols):
                if piece_board[i][j] == '-1':
                    cleared_lines = True
        if not cleared_lines:
            return self.get_coordinates(piece_board), 0

        lines_cleared = 0
        deepest_line_cleared = 0
        for j in range(len(piece_board[0])):
            depth_count = 0
            for i in range(len(piece_board)):
                if piece_board[i][j] == '-1':
                    depth_count += 1
                    deepest_line_cleared = max(deepest_line_cleared, i)
            lines_cleared = max(lines_cleared, depth_count)

        filled = []
        for j in range(cols):
            if self.board[deepest_line_cleared][j] == '0':
                filled.append(j)


        possible_pos = []

        for i in range(4):
            for j in range(4):
                for r in range(len(pieces[self.piece])):
                    pos_v = []
                    for e in pieces[self.piece][r]:
                        k = e // 4
                        l = e % 4

                        line_index = deepest_line_cleared -3+i +k
                        column_index = filled[0]-3+j +l

                        if line_index < rows and column_index < cols and self.board[line_index][column_index] == '0':
                            pos_v.append([line_index, column_index, r])

                    if (len(pos_v) == 4):
                        num_bottom = 0
                        for e in pos_v:
                            if (e[0] == deepest_line_cleared):
                                num_bottom += 1
                        if num_bottom == len(filled):
                            shift_down = -1
                            end = False

                            while not end:
                                shift_down += 1

                                for e in pieces[self.piece][r]:
                                    k = e // 4
                                    l = e % 4

                                    line_index = deepest_line_cleared -3+i +k +shift_down+1
                                    column_index = filled[0]-3+j +l

                                    if not (line_index < rows and column_index < cols and self.board[line_index][column_index] == '0'):
                                        end = True

                            possible_pos.append((deepest_line_cleared-3+i+shift_down, filled[0]-3+j, r))
        for pos in possible_pos:
            if self.simulate_and_check(pos, new_board):
                return pos, lines_cleared
        return None, None

    def gen_route(self, path):

        #L = translacao pra esquerda
        #R = translacao pra direita
        #A = rotacao horaria ("normal")
        #B = rotacao anti-horaria ("invertida")


        route = ""
        desvio = 0
        for i in range(len(path)):
            if path[i] in [".", "E", "F", "L", "I", "G", "R", "A", "B", "D"]:
                if path[i] in ["E", "F", "L"]:
                    route += "L"
                if path[i] in ["I", "G", "R"]:
                    route += "R"
                if path[i] in ["E", "I", "A"]:
                    route += "A"
                if path[i] in ["F", "G", "B"]:
                    route += "B"

                if path[i] == "D":
                    route += "D"
                    desvio = ((i % 2) + 1) % 2
                    print("Found a D, expect weird untested behaviour")
                    break

                if ((i % 2) + desvio % 2) == 1:
                    route += "D"
        return route

    #debugging methods

    def find_tuck_path(self, path):
        for i in range(1, len(path)):
            if path[i-1] == '.' and path[i] != '*' and path[i] != '^' and path[i] != '.':
                return True
        return False

    def fall_length(self, path):
        length = 0
        for i in range(len(path)):
            if path[i] == "D":
                print("Down is being used PANIC")
                sys.exit(0)
                return 0
            if path[i] != "*" and path[i] != "^" and path[i] != ".":
                aux = i

        return aux+1

    def get_router_data(self):

        for i in range(3):
            found = False
            while not found:

                nxt_board, path = self.treat_response(self.make_request(url))
                found = self.find_tuck_path(path)

                aux_board = self.board

                aux_coordinate = self.board_to_coordinate(nxt_board)
                self.update_game(nxt_board)


            print(aux_coordinate)
            print("Fall: ", aux_coordinate[0]+2)

            print(path)

            print("Route: ", self.gen_route(path))

            print("Fall length: ", self.fall_length(path))

            self.print_board(aux_board)
            self.print_board(nxt_board)
            piece_board = matrix_sub(nxt_board, aux_board)
            self.print_board(piece_board)

    def test_get_data(self):
        for i in range(50):
            nxt_board, path = self.treat_response(self.make_request(url))

            piece_board = matrix_sub(nxt_board, self.board)

            self.print_piece()
            self.print_board(piece_board)

            self.update_game(nxt_board)




x = game()

x.generate_player_db(n_games, number_of_plays)
#x.get_router_data()
#x.test_get_data()

#print(piecev_to_matrix(0,0))
