from tetris_game import tetris_interface
from tetris_game import definitions
import tetris_parser
import graphs
import numpy as np
from torch import nn
from torch import optim
import torch
import time

#############
#DEBUG TOOL

def print_board(board):
    for i in range(len(board)):
        aux = "|"
        for elem in board[i]:
            aux += "{:>2}".format(elem)
        print("{:>2}".format(i),aux, "|")
    aux = ""
    for _ in range(len(board[0])+2):
        aux += "-"
    print(aux)

##############


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
        self.mean_score = []
        self.max_score = []
        self.acc_loss = [0]*n_episodes
        self.total_training_time = 0
        self.total_gen_time = 0

    def gen_games_db(self):
        games_db = []
        scores = []
        for i in range(self.n_games):
            game = tetris_interface.Tetris()
            game_history = []

            for play in range(self.max_plays):
                if game.gameover:
                    break
                board, piece, next_piece = game.get_state()
                action, route = self.player.act(board, piece, next_piece)
                
                #print("piece: ", definitions.piece_vector[piece])
                #print("route: ", route)
                #print_board(board)


                lines_cleared = game.play_route(route)
                game_history.append({
                    'board': board,
                    'piece': piece,
                    'next_piece': next_piece,
                    'action': action,
                    'lines_cleared': lines_cleared,
                    'gameover': game.gameover
                })
            print("game ", i, " score: ", game.score)
            scores.append(game.score)
            games_db.append(game_history)
            
        self.mean_score.append(np.mean(scores))
        self.max_score.append(np.max(scores))
        return games_db

    def calculate_target_q(self, reward, next_state):
        _, _, max_next_state_value = self.player.best_action(next_state[0], next_state[1], next_state[2], self.player.stable_model)
        return reward+self.gamma*(max_next_state_value)

    def training_loop(self, episode):
        #state, action, reward, next_state
        batch = self.dataset_manager.sample(self.batch_size)
        if batch == None:
            return
        q = []
        target_q = []

        with torch.no_grad():
            for s, a, r, ns in batch:
                q.append(self.player.model(tetris_parser.encode_state(s[0], s[1], s[2], a)).item())
                if ns == None:
                    target_q.append(r)
                else:
                    target_q.append(self.calculate_target_q(r, ns))

        self.optimizer.zero_grad()
        
        loss = self.loss_f(torch.Tensor(q), torch.Tensor(target_q))
        loss.requires_grad = True

        loss.backward()

        #torch.nn.utils.clip_grad_value_(self.player.model.parameters(), 10)
        self.optimizer.step()
        if episode >= 0:
            self.acc_loss[episode] += loss.item()



    def main_loop(self):
        print("training on db")
        #print(len(self.dataset_manager))
        for _ in range(self.epochs*(len(self.dataset_manager)//(self.batch_size))):
            #print(i)
            self.training_loop(-1)
        self.player.update_stable_model()
        for i in range(self.n_episodes):
            t = time.time()
            self.dataset_manager.gen_train_db(
                self.gen_games_db()
            )
            t = time.time() - t
            self.total_gen_time += t
            print("took ", t, " s to generate games this episode")
            print("average time is ", self.total_gen_time/(i+1))

            print("starting training, episode ", i)
            t = time.time()

            for _ in range(self.epochs*(len(self.dataset_manager)//(self.batch_size))):
                self.training_loop(i)

            self.player.update_stable_model()
            self.player.update_epsilon()

            print("Episode: ", i, " Loss: ", self.acc_loss[i], " Mean Score: ", self.mean_score[i], " Max Score: ", self.max_score[i])

            t = time.time() - t
            self.total_training_time += t
            print("took ", t, " s to train this episode")
            print("average time is ", self.total_training_time/(i+1))

            if i>0 and i % 10 == 0:
                self.player.save_model("saved_nns/episode"+str(i)+".h5")
                self.player.save_model("saved_nns/most_recent.h5")
                graphs.plot_mean_score(self.mean_score)
                graphs.plot_max_score(self.max_score)
                graphs.plot_accumulated_loss(self.acc_loss)
