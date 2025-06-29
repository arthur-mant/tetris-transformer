import tetris_interface
import tetris_parser
from torch.utils.data import Dataloader
from torch import nn
from torch import optim

class qlearning():
    def __init__(self, player, n_episodes, n_games, max_plays, dataset_manager, gamma, epochs, batch_size, lr):
        self.player = player
        self.n_episodes = n_episodes
        self.n_games = n_games      #per episode
        self.max_plays = max_plays  #per game
        self.dataset_manager = dataset_manager
        self.gamma = gamma          #future reward discount
        self.epochs = epochs
        self.batch_size = batch_size
        self.loss_f = nn.SmoothL1Loss()
        self.optimizer = optim.AdamW(self.player.model.parameters(), lr=lr) 

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
        if len(self.dataset_manager) > self.batch_size
            return
        #state, action, reward, next_state
        batch = self.dataset_manager.sample(self.batch_size)

        q = []
        target_q = []

        with torch.no_grad():
            for s, a, r, ns in batch:
                q.append(self.player.model(tetris_parser.encode_state(s[0], s[1], s[2], a)))
                if ns == None:
                    target_q.append(r)
                else:
                    target_q.append(self.calculate_target_q(r, ns))
        loss = self.loss_f(q, target_q)

        self.optimizer.zero_grad()
        loss.backward()

        torch.nn.utils.clip_grad_value_(self.player.model.parameters(), 10)
        self.optimizer.step()

    def main_loop(self):
        for i in n_episodes:
            self.dataset_manager.gen_train_db(
                self.gen_games_db()
            )
            for _ in range(self.epochs*(len(self.dataset_manager)//(2*self.batch_size))):
                self.training_loop()
            self.player.update_stable_model()
            

