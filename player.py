from tetris_dataset import dataset_manager
import tetris_parser
import numpy as np
import random
import torch
import math
import rewards
from copy import deepcopy


class player():
    def __init__(self, model, init_epsilon, min_epsilon, load_from_file, name, gamma):
        self.model = model
        if load_from_file:
            self.model.load_state_dict(torch.load("saved_nns/"+name+"_most_recent.h5", weights_only=True))
        self.stable_model = deepcopy(model)
        self.init_epsilon = init_epsilon
        self.epsilon = init_epsilon
        self.min_epsilon = min_epsilon
        self.gamma = gamma          #future reward discount

    def update_stable_model(self):
       self.stable_model.load_state_dict(self.model.state_dict()) 

    def update_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon -= (self.init_epsilon-self.min_epsilon)/500
        else:
            self.epsilon = self.min_epsilon

    def save_model(self, name):
        path = "saved_nns/"+name
        torch.save(self.model.state_dict(), path)

    def best_action(self, board, piece, next_piece):
        actions, afterstates, next_pieces, lines, gameover = tetris_parser.get_all_afterstates(board, piece, next_piece)
        with torch.no_grad():
            afterstate_values = list(self.model(afterstates, next_pieces).detach().numpy())

        for i in range(len(actions)):
            if gameover[i]:
                afterstate_values[i] = -1
            else:
                afterstate_values[i] = float(rewards.total_reward(lines[i], actions[i][0], gameover[i])+self.gamma*afterstate_values[i][0])
        while len(actions) > 0:
            idx_best_action = np.argmax(afterstate_values) 
            best_action = actions[idx_best_action]
            route = tetris_parser.get_route(board, piece, best_action[0], best_action[1], best_action[2], [], [])
            if route != None:
                return best_action, route
            idx = actions.index(best_action)
            del actions[idx]
            del afterstate_values[idx]

    def random_action(self, board, piece):
        possible_actions = tetris_parser.get_possible_actions(board, piece)
        while len(possible_actions) > 0:
            play = random.choice(possible_actions)
            route = tetris_parser.get_route(board, piece, play[0], play[1], play[2], [], [])
            if route != None:
                return play, route
            possible_actions.remove(play)


    def act(self, board, piece, next_piece):
        if random.random() < self.epsilon:
            return self.random_action(board, piece)
        else:
            return self.best_action(board, piece, next_piece)


