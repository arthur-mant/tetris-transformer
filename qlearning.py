import tetris_interface


class qlearning():
    def __init__(self, player, n_episodes, n_games, max_plays, dataset_manager, gamma):
        self.player = player
        self.n_episodes = n_episodes
        self.n_games = n_games      #per episode
        self.max_plays = max_plays  #per game
        self.dataset_manager = dataset_manager
        self.gamma = gamma          #future reward discount

    def gen_games_db(self):
        games_db = []
        for i in range(self.n_games):
            game = tetris_interface.Tetris()
            game_history = []

            for play in range(self.max_plays)
                if game.gameover:
                    break
                board, piece, next_piece = game.get_state()
                action, route = player.act(board, piece, next_piece)
                lines_cleared = game.play_route(route)
                game_history.append({
                    'board': board,
                    'piece': piece,
                    'next_piece': next_piece,
                    'action': action,
                    'lines_cleared': lines_cleared,
                    'gameover': game.gameover
                })
            games_db.append(game_history)

        return games_db
    def calculate_target_q(self, reward, next_state):
        _, _, max_next_state_value = self.player.best_action(next_state[0], next_state[1], next_state[2], self.player.stable_model)
        return reward+self.gamma*(max_next_state_value)

    def training_loop(self):
        for i in n_episodes:
            self.dataset_manager.gen_train_db(self.gen_plays_db(), self.bellman_equation)

