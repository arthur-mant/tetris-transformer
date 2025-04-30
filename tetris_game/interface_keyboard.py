class Keyboard:
    def get_event_from_keyboard(self, pygame, game, pressing_down):
        command = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, False, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    command = game.rotate
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    command = game.go_left
                if event.key == pygame.K_RIGHT:
                    command = game.go_right
                #if event.key == pygame.K_SPACE:
                #    game.hard_drop()
                if event.key == pygame.K_ESCAPE and game.gameover:
                    return True, False, None

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False
        return False, pressing_down, command
