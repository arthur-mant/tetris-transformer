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
import math

class qlearning():
    def __init__(self, player, n_episodes, n_games, max_plays, dataset_manager, epochs, batch_size, lr, name, update_interval, gamma, delta, rewards_object):
        self.player = player
        self.n_episodes = n_episodes
        self.n_games = n_games      #per episode
        self.max_plays = max_plays  #per game
        self.dataset_manager = dataset_manager
        self.epochs = epochs
        self.batch_size = batch_size
        self.loss_f = nn.MSELoss()
        self.optimizer = optim.AdamW(self.player.model.parameters(), lr=lr) 
        self.mean_score = []
        self.max_score = []
        self.game_length = []
        self.acc_loss = n_episodes*[0]
        self.total_training_time = 0
        self.total_gen_time = 0
        self.name = name
        self.lines_cleared = [n_episodes*[0] for i in range(4)]
        self.best_game = (0, None)
        self.update_interval = update_interval
        self.gamma = gamma
        self.delta = delta
        self.rewards_object = rewards_object
        torch.set_printoptions(precision=8)


    def gen_games_db(self, episode):
        games_db = []
        scores = []
        total_length = 0
        for i in range(self.n_games):
            game = tetris_interface.Tetris()
            game_history = []

            for play in range(self.max_plays):
                if game.gameover:
                    break
                board, piece, next_piece = game.get_state()
                action, route = self.player.act(board, piece, next_piece)

                lines_cleared = game.play_route(route)
                game_history.append({
                    'board': board,
                    'piece': piece,
                    'next_piece': next_piece,
                    'action': action
                })
                if lines_cleared > 0:
                    self.lines_cleared[lines_cleared-1][episode] += 1
            scores.append(game.score)
            games_db.append(game_history)
            total_length += len(game_history)
            if game.score > self.best_game[0]:
                self.best_game = (game.score, game_history)
            
        self.game_length.append(total_length/self.n_games)
        self.mean_score.append(np.mean(scores))
        self.max_score.append(np.max(scores))
        return games_db

    def calculate_target_q(self, next_state):
        action, _ = self.player.best_action(next_state[0], next_state[1], next_state[2])
        afterstate, next_piece, lines, gameover = tetris_parser.generate_afterstate(next_state[0], next_state[1], next_state[2], action)
        if gameover:
            return [-1]
        else:
            with torch.no_grad():
                return [float(self.rewards_object.total_reward(lines, action[0], gameover) + self.gamma*self.player.stable_model(afterstate, next_piece).detach().numpy()[0])]

    def training_loop(self, episode):
        afterstates, next_pieces, target_q = self.dataset_manager.sample(self.batch_size)
        self.optimizer.zero_grad()

        outputs = self.player.model(afterstates, next_pieces)
        target_q = torch.reshape(target_q, (128, 1))

        loss = torch.sqrt(self.loss_f(outputs, target_q))

        loss.backward()

        self.optimizer.step()
        if episode >= 0:
            self.acc_loss[episode] += loss.item()



    def main_loop(self, initial_training):

        if initial_training:
            print("training on games from file")
            self.dataset_manager.gen_train_db(self.player.model, self.calculate_target_q)
            for _ in range(10*self.epochs*(len(self.dataset_manager)//(self.batch_size))):
                self.training_loop(-1)
            self.player.update_stable_model()

        for i in range(self.n_episodes):
            print("---------------------------------------------------")
            print("Episode ", i)

            
            afst, npc, _, _ = tetris_parser.generate_afterstate([10*[0] for _ in range(20)], 0, 0, (17, 0, 0))
            print("saida exemplo pra tabuleiro vazio: ", self.player.model(afst, npc).item())


            t = time.time()
            self.dataset_manager.gen_game_db(
                self.gen_games_db(i)
            )
            t = time.time() - t
            self.total_gen_time += t
            print("Generating games took ", t, "s this episode, average time is ", self.total_gen_time/(i+1), "s")

            t = time.time()

            self.dataset_manager.gen_train_db(self.player.model, self.calculate_target_q)
            for aux in range(self.epochs*len(self.dataset_manager.target_q)//(self.batch_size)):
                self.training_loop(i)

            if i>0 and i % self.update_interval == 0:
                print("updating stable network!")
                self.player.update_stable_model()
            self.player.update_epsilon()

            self.acc_loss[i] = self.acc_loss[i]/self.epochs
            print("Loss por época (média): ", self.acc_loss[i])
            print("Mean Score: ", self.mean_score[i])
            print("Max Score: ", self.max_score[i])
            print("Mean game length: ", self.game_length[i])

            t = time.time() - t
            self.total_training_time += t
            print("Training took ", t, "s this episode, average time is ", self.total_training_time/(i+1), "s")

            if i>0 and i % 100 == 0:
                print("saving nn")
                self.player.save_model(self.name+"_episode"+str(i)+".h5")

            if i>0 and i % 10 == 0:
                print("plotting graphs...")
                self.player.save_model(self.name+"_most_recent.h5")
                graphs.plot_mean_score(self.mean_score, i, self.name)
                graphs.plot_max_score(self.max_score, i, self.name)
                graphs.plot_accumulated_loss(self.acc_loss, i, self.name)
                graphs.plot_lines_cleared(self.lines_cleared, i, self.name)
                graphs.plot_avg_length(self.game_length, i, self.name)
                #saving best game
                fileObj = open("logs/"+self.name+"_mean_score.pkl", 'wb')
                pickle.dump(self.mean_score, fileObj)
                fileObj.close()
                fileObj = open("logs/"+self.name+"_max_score.pkl", 'wb')
                pickle.dump(self.max_score, fileObj)
                fileObj.close()
                fileObj = open("logs/"+self.name+"_loss.pkl", 'wb')
                pickle.dump(self.acc_loss, fileObj)
                fileObj.close()
                fileObj = open("logs/"+self.name+"_lines_cleared.pkl", 'wb')
                pickle.dump(self.lines_cleared, fileObj)
                fileObj.close()

                fileObj = open("best_games/"+self.name+"_best_game.pkl", 'wb')
                pickle.dump(self.best_game[1], fileObj)
                fileObj.close()

                print("saved as ", self.name)

