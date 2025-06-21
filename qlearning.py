import tetris_interface

class qlearning():
    def __init__(self, player, n_episodes):
        self.player = player
        self.n_episodes = n_episodes
    def play_games(self, n_games):
        for i in range(n_games):
            game = tetris_interface.Tetris()


