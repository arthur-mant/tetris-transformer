import random
from tetris_game import screen
from tetris_game import definitions
import copy
import time

pieces = definitions.pieces
line_score = definitions.line_score

class Piece:

    def __init__(self, x, y, rot, p_type=None):
        self.x = x
        self.y = y
        self.rotation = rot
        
        if p_type == None:
            self.type = random.randint(0, len(pieces) - 1)
        else:
            self.type = p_type


    def image(self):
        return pieces[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation+1) % len(pieces[self.type])

class Tetris:
    score = 0
    lines = 0
    pieces = 0
    field = []
    level = 1
    fps = "?"

    gameover = False

    def __init__(self, field=None, piece_list=None):      #should be at least 4x4
        if bool(field):
            self.field = field
        else:
            self.field = [ [ -1 for i in range(definitions.n_cols) ] for j in range(definitions.n_rows) ]

        self.piece_list = piece_list
        if bool(piece_list):
            self.piece = Piece((definitions.n_cols//2)-2, -2, 0, self.piece_list.pop(0))
            self.next_piece = Piece((definitions.n_cols//2)-2, -2, 0, self.piece_list.pop(0))
        else:
            self.piece = Piece((definitions.n_cols//2)-2, -2, 0)
            self.next_piece = Piece((definitions.n_cols//2)-2, -2, 0)

    def new_piece(self):
        self.piece = self.next_piece
        if bool(self.piece_list):
            self.next_piece = Piece((definitions.n_cols//2)-2, -2, 0, self.piece_list.pop(0))            
        else:
            self.next_piece = Piece((definitions.n_cols//2)-2, -2, 0)
        self.pieces += 1

    def intersects(self):
        for block in self.piece.image():
            i = block//4
            j = block%4
            if i+self.piece.y == -1 or i+self.piece.y == -2:
                break
            if  i+self.piece.y < -2 or \
                i+self.piece.y > definitions.n_rows-1 or \
                j+self.piece.x > definitions.n_cols-1 or \
                j+self.piece.x < 0 or \
                self.field[i+self.piece.y][j+self.piece.x] > -1:
                    #print(i+self.piece.y, j+self.piece.x)
                    return True
        return False

    def freeze(self):
        #self.score += self.piece.y+2
        for block in self.piece.image():
            i = block//4
            j = block%4
            if i+self.piece.y < definitions.n_rows and i+self.piece.y >= 0 and \
                j+self.piece.x < definitions.n_cols and j+self.piece.x >= 0:
                self.field[i+self.piece.y][j+self.piece.x] = self.piece.type
        lines = self.break_lines()
        self.new_piece()
        if self.intersects():
            self.gameover = True
            return 0
        return lines

    def break_lines(self):
        lines = 0
        for i in range(1, definitions.n_rows):
            holes = 0
            for j in range(definitions.n_cols):
                if self.field[i][j] == -1:
                    holes += 1
            if holes == 0:
                lines += 1
                for k in range(i, 1, -1):
                    for l in range(definitions.n_cols):
                        self.field[k][l] = self.field[k-1][l]
        if lines > 0:
            self.score += line_score[lines-1]
            self.lines += lines
            print(lines, " cleared!!!!!!!!!!!!")
        return lines

    #retorna is_illegal, lines_cleared
    def play(self, action):
        self.piece.x = action[1]
        self.piece.y = action[0]
        self.piece.rotation = action[2]

        #checa se da overlap
        if self.intersects():
            self.new_piece()
            #print("intersects")
            return True, 0

        #checa se ta flutuando
        self.piece.y += 1        
        if not self.intersects():
            self.new_piece()
            #print("flutuando")
            return True, 0

        #print("tudo certo")

        self.piece.y -= 1
        return False, self.freeze()

    def play_route(self, route):
        for elem in route:
            if elem == "B":
                self.piece.y += 1
            elif elem == "D":
                self.piece.x += 1
            elif elem == "E":
                self.piece.x -= 1
            elif elem == "R":
                self.piece.rotate()
            if self.intersects():
                print("TRIED FOLLOWING ROUTE BUT SOMETHING WENT WRONG WHEN", elem)
        return self.freeze()

    def translate_board(self, board):
        new_board = []
        for row in board:
            new_row = []
            for i in row:
                if i == -1:
                    new_row.append(0)
                else:
                    new_row.append(1)
            new_board.append(new_row)
        return new_board

    def get_state(self):
        return self.translate_board(self.field), self.piece.type, self.next_piece.type

