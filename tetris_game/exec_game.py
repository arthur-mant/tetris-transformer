from tetris_game import screen
import pygame
import time

class GameRun:

    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen_i = screen.Screen(pygame, 500, 500, 100, 60, 20)

    def run_frame(self, command):

        if command == "R":
            self.game.piece.rotate()
        elif command == "B":
            self.game.piece.go_down()
        elif command == "E":
            self.game.piece.go_side(-1)
        elif command == "D":
            self.game.piece.go_side(1)

        self.screen_i.update_screen(self.game)

    def run_game(self, route):
        self.screen_i.update_screen(self.game)
        #time.sleep(0.02)
        for elem in route:
            self.run_frame(elem)
            #time.sleep(0.02)
        return self.game.freeze()
