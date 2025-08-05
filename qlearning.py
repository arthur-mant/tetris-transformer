from tetris_game import tetris_interface
from tetris_game import definitions
import tetris_parser
import graphs
import numpy as np
from torch import nn
from torch import optim
import torch
import time
import pickle

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
    def __init__(self, player, n_episodes, n_games, max_plays, dataset_manager, gamma, epochs, batch_size, lr, name, use_encoding):
        self.player = player
        self.n_episodes = n_episodes
        self.n_games = n_games      #per episode
        self.max_plays = max_plays  #per game
        self.dataset_manager = dataset_manager
        self.gamma = gamma          #future reward discount
        self.epochs = epochs
        self.batch_size = batch_size
        self.use_encoding = use_encoding
        self.loss_f = nn.SmoothL1Loss()
        self.optimizer = optim.AdamW(self.player.model.parameters(), lr=lr) 
        self.mean_score = []
        self.max_score = []
        self.acc_loss = n_episodes*[0]
        self.total_training_time = 0
        self.total_gen_time = 0
        self.name = name
        self.lines_cleared = [n_episodes*[0] for i in range(4)]
        self.best_game = (0, None)


    def gen_games_db(self, episode):
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
                if lines_cleared > 0:
                    self.lines_cleared[lines_cleared-1][episode] += 1
            #print("game ", i, " score: ", game.score)
            scores.append(game.score)
            games_db.append(game_history)
            if game.score > self.best_game[0]:
                self.best_game = (game.score, game_history)
            
        self.mean_score.append(np.mean(scores))
        self.max_score.append(np.max(scores))
        return games_db

    def calculate_target_q(self, next_reward, next_state):
        _, _, max_next_state_value = self.player.best_action(next_state[0], next_state[1], next_state[2], self.player.stable_model)
        #print(max_next_state_value)
        return self.gamma*(next_reward + max_next_state_value)

    def training_loop(self, episode):
        q, target_q = self.dataset_manager.sample(self.batch_size)

        self.optimizer.zero_grad()

        loss = self.loss_f(q, target_q)
        loss.requires_grad = True

        loss.backward()

        #torch.nn.utils.clip_grad_value_(self.player.model.parameters(), 10)
        self.optimizer.step()
        if episode >= 0:
            self.acc_loss[episode] += loss.item()



    def main_loop(self, initial_training):

        if initial_training:
            print("training on games from file")
            self.dataset_manager.gen_train_db(self.player.model, self.calculate_target_q, self.use_encoding)
            for _ in range(10*self.epochs*(len(self.dataset_manager)//(self.batch_size))):
                self.training_loop(-1)
            self.player.update_stable_model()

        for i in range(self.n_episodes):
            print("---------------------------------------------------")
            print("Episode ", i)

            
            print(self.player.model(torch.tensor([0 for _ in range(201)], dtype=torch.float)).item())

            t = time.time()
            self.dataset_manager.gen_game_db(
                self.gen_games_db(i)
            )
            t = time.time() - t
            self.total_gen_time += t
            print("Generating games took ", t, "s this episode, average time is ", self.total_gen_time/(i+1), "s")

            t = time.time()

            self.dataset_manager.gen_train_db(self.player.model, self.calculate_target_q, self.use_encoding)
            for _ in range(self.epochs*(len(self.dataset_manager.q)//(self.batch_size))):
                self.training_loop(i)

            self.player.update_stable_model()
            self.player.update_epsilon()

            self.acc_loss[i] = self.acc_loss[i]/self.epochs
            print("Loss por época (média): ", self.acc_loss[i])
            print("Mean Score: ", self.mean_score[i])
            print("Max Score: ", self.max_score[i])

            t = time.time() - t
            self.total_training_time += t
            print("Training took ", t, "s this episode, average time is ", self.total_training_time/(i+1), "s")

            if i>0 and i % 10 == 0:
                print("saving data, plotting graphs...")
                self.player.save_model(self.name+"episode"+str(i)+".h5")
                self.player.save_model(self.name+"most_recent.h5")
                graph_name = self.name.split('/')[1]
                graphs.plot_mean_score(self.mean_score, i, graph_name)
                graphs.plot_max_score(self.max_score, i, graph_name)
                graphs.plot_accumulated_loss(self.acc_loss, i, graph_name)
                graphs.plot_lines_cleared(self.lines_cleared, i, graph_name)
                #saving best game
                fileObj = open("best_games/"+graph_name[:-1]+".pkl", 'wb')
                pickle.dump(self.best_game[1], fileObj)
                fileObj.close()

