#definições de variáveis

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

colors = [          #adicionar cores
    (0, 0, 204),
    (0, 204, 0),
    (204, 0, 0),
    (102, 0, 204),
    (255, 153, 0),
    (255, 0, 255),
    (0, 204, 255),
    (190, 190, 190)
]


class Screen:

    pygame = None
    display = None
    game_pos_x = 0
    game_pos_y = 0
    zoom = 1
    width = 500
    lenght = 500

    text_font_size = 1
    text_font = None
    title_font = None

    def __init__(self, pygame, width, lenght, x, y, zoom):

        self.pygame = pygame
        self.display = self.pygame.display.set_mode((width, lenght))
        self.pygame.display.set_caption("Tetris")

        self.game_pos_x = x
        self.game_pos_y = y
        self.zoom = zoom
        self.width = width
        self.lenght = lenght

        self.text_font_size = 19
        self.text_font = self.pygame.font.SysFont('Calibri', self.text_font_size, True, False)
        self.title_font = self.pygame.font.SysFont('Calibri', 55, True, False)


    def update_screen(self, game):
        self.display.fill(WHITE)

        for i in range(game.height):
            for j in range(game.width):
                self.pygame.draw.rect(self.display, GRAY, [self.game_pos_x + self.zoom * j, self.game_pos_y + self.zoom * i, self.zoom, self.zoom], 1)
                if game.field[i][j] > -1:
                    self.pygame.draw.rect(self.display, colors[game.field[i][j]], [self.game_pos_x + self.zoom * j + 1, self.game_pos_y + self.zoom * i + 1, self.zoom - 2, self.zoom - 1])

        if game.piece is not None:
            for block in game.piece.image():
                i = block//4
                j = block%4
                if i+game.piece.y >= 0:
                    self.pygame.draw.rect(self.display, colors[game.piece.type],
                        [self.game_pos_x + self.zoom*(j+game.piece.x)+1,
                        self.game_pos_y + self.zoom*(i+game.piece.y)+1,
                        self.zoom-2, self.zoom-2])

        self.pygame.draw.rect(self.display, GRAY, [self.game_pos_x + self.zoom*(game.width+0.5), self.game_pos_y, self.zoom*6, self.zoom*6], 1)
        text_next = self.text_font.render("Next", True, BLACK)
        self.display.blit(text_next, [self.game_pos_x + self.zoom*(game.width+2.5), self.game_pos_y])

        for i in range(4):
            for j in range(4):
                self.pygame.draw.rect(self.display, GRAY, [self.game_pos_x + self.zoom*(j+game.width+1.5), self.game_pos_y+self.zoom*(i+1), self.zoom, self.zoom], 1)
        if game.next_piece is not None:
            for block in game.next_piece.image():
                i = block//4
                j = block%4
                self.pygame.draw.rect(self.display, colors[game.next_piece.type],
                    [self.game_pos_x + self.zoom*(j+game.width+1.5)+1,
                     self.game_pos_y + self.zoom*(i+1)+1,
                     self.zoom-2, self.zoom-2])

        self.pygame.draw.rect(self.display, GRAY, [self.game_pos_x + self.zoom*(game.width+0.5), self.game_pos_y+self.zoom*(7), self.zoom*6, self.zoom*8], 1)

        text_score = self.text_font.render("Score: " + str(game.score), True, BLACK)
        text_lines = self.text_font.render("Lines: " + str(game.lines), True, BLACK)
        text_pieces = self.text_font.render("Pieces: " + str(game.pieces), True, BLACK)
        text_level = self.text_font.render("Level: " + str(game.level), True, BLACK)
        text_fps = self.text_font.render("FPS: " + str(game.fps), True, BLACK)

        text_game_over = self.title_font.render("GAME OVER", True, (0, 0, 0))
        #text_reset = self.title_font.render("Press ESC", True, (255, 215, 0))

        self.display.blit(text_score, [self.game_pos_x + self.zoom*(game.width+1), self.game_pos_y+self.zoom*(7)+self.text_font_size*0.5])
        self.display.blit(text_lines, [self.game_pos_x + self.zoom*(game.width+1), self.game_pos_y+self.zoom*(7)+self.text_font_size*2])
        self.display.blit(text_pieces, [self.game_pos_x + self.zoom*(game.width+1), self.game_pos_y+self.zoom*(7)+self.text_font_size*3.5])
        self.display.blit(text_level, [self.game_pos_x + self.zoom*(game.width+1), self.game_pos_y+self.zoom*(7)+self.text_font_size*5])
        self.display.blit(text_fps, [self.game_pos_x + self.zoom*(game.width+1), self.game_pos_y+self.zoom*(7)+self.text_font_size*6.5])
        if game.gameover:
            self.display.blit(text_game_over, [100, 0])
            #self.display.blit(text_reset, [25, 265])

        self.pygame.display.flip()

