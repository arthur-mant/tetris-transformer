import pygame
import random
import screen
import interface_keyboard
import copy

class Piece:
    x = 0
    y = 0

    pieces = [
        [[8, 9, 10, 11], [2, 6, 10,14]],    #I
        [[8, 9, 10, 14], [5, 9, 12, 13], [4, 8, 9, 10], [5, 6, 9, 13]],      #J
        [[8, 9, 10, 12], [4, 5, 9, 13], [6, 8, 9, 10], [5, 9, 13, 14]],      #L
        [[8, 9, 10, 13], [5, 8, 9, 13], [5, 8, 9, 10], [5, 9, 10, 13]],       #T
        [[9, 10, 13, 14]],                    #O
        [[8, 9, 13, 14], [6, 9, 10, 13]],      #Z
        [[9, 10, 12, 13], [5, 9, 10, 14]]       #S
    ]


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.pieces) - 1)
        self.rotation = 0

    def image(self):
        return self.pieces[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation+1) % len(self.pieces[self.type])


class Tetris:
    level = 1
    score = 0
    lines = 0
    pieces = 0
    field = []
    height = 0
    width = 0
    fps = 0

    gameover = False
    piece = None
    next_piece = None
    line_score = [400, 1000, 3000, 12000]

    def __init__(self, height, width, field=None):      #should be at least 4x4
        self.height = height
        self.width = width
        if bool(field):
            self.field = field
        else:
            self.field = [ [ -1 for i in range(width) ] for j in range(height) ]

        self.piece = Piece((self.width//2)-2, -2)
        self.next_piece = Piece((self.width//2)-2, -2)

    def new_piece(self):
        self.piece = self.next_piece
        self.next_piece = Piece((self.width//2)-2, -2)
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
        self.score += self.piece.y+2
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

    def hard_drop(self):
        while not self.intersects():
            self.piece.y += 1
        self.piece.y -=1
        return self.freeze()

    def go_down(self):
        self.piece.y += 1
        if self.intersects():
            self.piece.y -= 1
            return self.freeze()
        

    def go_side(self, dx):
        old_x = self.piece.x
        self.piece.x += dx
        if self.intersects():
            self.piece.x = old_x

    def go_right(self):
        self.go_side(1)

    def go_left(self):
        self.go_side(-1)

    def rotate(self):
        old_rotation = self.piece.rotation
        self.piece.rotate()
        if self.intersects():
            self.piece.rotation = old_rotation

    def level_up(self):
        self.level += 1

    def num_to_action(self, action):
        switch = {
            0: self.rotate,
            1: self.go_down,
            2: self.go_left,
            3: self.go_right
        }

        return switch.get(action, "Invalid input")

class GameRun:

    done = False
    clock = pygame.time.Clock()
    fps = 60
    game = None
    counter = 1

    keyb = None
    queue_i = None
    screen_i = None
    pressing_down = False
    true_fps = 1

    def __init__(self, game, fps, use_screen=True, use_keyboard=False):
        pygame.init()
        self.game = game
        self.fps = fps

        if bool(use_screen):
            self.screen_i = screen.Screen(pygame, 500, 500, 100, 60, 20)
        if bool(use_keyboard) and bool(use_screen):
            self.keyb = interface_keyboard.Keyboard()

    def run_from_keyboard(self):
        if not bool(self.keyb):
            print("ERROR: Trying to run game using keyboard but no keyboard interface was created")
            return
        self.done, self.pressing_down, command_input = self.keyb.get_event_from_keyboard(pygame, self.game, self.pressing_down)
        return self.run_frame(command_input)[0]

    def run_frame(self, command):
        if self.game.piece is None:
            print("ERROR: No piece")
            #self.game.new_piece()
        self.counter += 1
        if self.counter > 100000:
            self.counter = 0

        if self.keyb and not self.game.gameover and self.fps > 0 and (self.counter % (self.fps // (2*self.game.level)) == 0 or self.pressing_down):
            self.game.go_down()

        aux = None
        if bool(command):
            aux = command()

        if bool(self.screen_i):
            self.screen_i.update_screen(self.game)

        if self.fps > 0:
            self.game.fps = self.true_fps = 1000 // self.clock.tick(self.fps)

#        if self.gameover and bool(self.queue_i):
#            self.done = True

        if self.done:
            self.close_game()
            return False, None

        return True, aux


    def step(self, action):

        #old_piece = copy.deepcopy(self.game.piece)
        reward = self.game.score

        x = (action//4)-1
        rot = (action % 4) % (len(self.game.piece.pieces[self.game.piece.type]))

        for i in range(rot):
            self.run_frame(self.game.rotate)

        init_x = (self.game.width//2 - 2)
        delta_x = x-init_x

        sign = 1 if delta_x > 0 else -1

        for i in range(abs(delta_x)):
            if delta_x > 0:
                self.run_frame(self.game.go_right)
            else:
                self.run_frame(self.game.go_left)

        lines = self.run_frame(self.game.hard_drop)[1]
        #self.run_frame(self.game.num_to_action(action))

        reward = (self.game.score - reward)#*100
        #next_state = self.game.field

        #penalidade para ações q n fazem nada
        #if old_piece == self.game.piece and \
        #    old_piece_count == self.game.pieces:
        #    reward += -10000

        #adiciona um pequeno bonus se a peça se mover para baixo
        #if action == 1:
        #    reward += self.game.piece.y
        #reward += self.game.piece.y+2

        #adiciona penalidade pra rotações pra evitar bumerangue
        #if action == 0:
        #    reward += -1


        #print("reward: ", reward)

        return reward, lines

    def close_game(self):
        pygame.quit()


if __name__ == '__main__':

    game_run = GameRun(Tetris(20,10), 60, use_screen=True, use_keyboard=True)

    while game_run.run_from_keyboard():
        pass
