import tetris_interface


class qlearning():
    def __init__(self, player, n_episodes, max_plays):
        self.player = player
        self.n_episodes = n_episodes
        self.max_plays = max_plays
    def gen_plays_db(self, n_games):
        plays_db = []
        for i in range(n_games):
            game = tetris_interface.Tetris()

            for play in range(self.max_plays)
                if game.gameover:
                    break
                board, piece, next_piece = game.get_state()
                action, route = player.act(board, piece, next_piece)
                lines_cleared = game.play_route(route)
                self.plays_db.append({
                    'board': board,
                    'piece': piece,
                    'next_piece': next_piece,
                    'action': action,
                    'lines_cleared': lines_cleared,
                    'done', game.gameover
                })
        return plays_db
