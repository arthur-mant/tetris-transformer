import pygame
import random
import screen
import copy

pieces = [
    [[8, 9, 10, 11], [2, 6, 10,14]],    #I
    [[8, 9, 10, 14], [5, 9, 12, 13], [4, 8, 9, 10], [5, 6, 9, 13]],      #J
    [[8, 9, 10, 12], [4, 5, 9, 13], [6, 8, 9, 10], [5, 9, 13, 14]],      #L
    [[8, 9, 10, 13], [5, 8, 9, 13], [5, 8, 9, 10], [5, 9, 10, 13]],       #T
    [[9, 10, 13, 14]],                    #O
    [[8, 9, 13, 14], [6, 9, 10, 13]],      #Z
    [[9, 10, 12, 13], [5, 9, 10, 14]]       #S
]
class Piece:

    def __init__(self, x, y, rot):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(pieces) - 1)
        self.rotation = rot

    def image(self):
        return pieces[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation+1) % len(pieces[self.type])



class Tetris:
    score = 0
    lines = 0
    pieces = 0
    field = []
    width = 10
    height = 20
    level = 1
    fps = "?"

    gameover = False
    line_score = [400, 1000, 3000, 12000]

    def __init__(self, field=None):      #should be at least 4x4
        if bool(field):
            self.field = field
        else:
            self.field = [ [ -1 for i in range(self.width) ] for j in range(self.height) ]

        self.piece = Piece((self.width//2)-2, -2, 0)
        self.next_piece = Piece((self.width//2)-2, -2, 0)

    def new_piece(self):
        self.piece = self.next_piece
        self.next_piece = Piece((self.width//2)-2, -2, 0)
        self.pieces += 1

    def intersects(self):
        intersection = False

        for block in self.piece.image():
            i = block//4
            j = block%4

            if  i+self.piece.y >= -2 and \
                (i+self.piece.y > self.height-1 or \
                j+self.piece.x > self.width-1 or \
                j+self.piece.x < 0 or \
                self.field[i+self.piece.y][j+self.piece.x] > -1):
                    intersection = True

        return intersection

    def freeze(self):
        #self.score += self.piece.y+2
        for block in self.piece.image():
            i = block//4
            j = block%4
            if i+self.piece.y < self.height and i+self.piece.y >= 0 and \
                j+self.piece.x < self.width and j+self.piece.x >= 0:
                self.field[i+self.piece.y][j+self.piece.x] = self.piece.type
        lines = self.break_lines()
        self.new_piece()
        if self.intersects():
            self.gameover = True
            return 0
        return lines

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            holes = 0
            for j in range(self.width):
                if self.field[i][j] == -1:
                    holes += 1
            if holes == 0:
                lines += 1
                for k in range(i, 1, -1):
                    for l in range(self.width):
                        self.field[k][l] = self.field[k-1][l]
        if lines > 0:
            self.score += self.line_score[lines-1]
            self.lines += lines
            print(lines, " cleared!!!!!!!!!!!!")
        return lines

    #retorna is_illegal, lines_cleared
    def act(self, action):
        self.piece.x = action[0]
        self.piece.y = action[1]
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

        self.piece.y -= 1
        return False, self.freeze()


class GameRun:
    game = None
    screen_i = None

    def __init__(self, game, use_screen=True):
        pygame.init()
        self.game = game

        if bool(use_screen):
            self.screen_i = screen.Screen(pygame, 500, 500, 100, 60, 20)

    def run_frame(self, action):
        if self.game.piece is None:
            print("ERROR: No piece")
            #self.game.new_piece()

        if bool(action):
            self.game.act(action)

        if bool(self.screen_i):
            self.screen_i.update_screen(self.game)

        return True

    def close_game(self):
        pygame.quit()


if __name__ == '__main__':

    game_run = GameRun(Tetris(), use_screen=True)
    action = None
    while game_run.run_frame(action):
        action = [int(i) for i in input().split()]
        
