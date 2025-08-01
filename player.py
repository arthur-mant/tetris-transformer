from tetris_dataset import dataset_manager
import tetris_parser
import numpy as np
import random
import torch
from copy import deepcopy

class player():
    def __init__(self, model, epsilon, epsilon_decay, load_from_file, use_encoding, rewards_object, name):
        self.model = model
        if load_from_file:
            torch.load(name+"most_recent.h5")
        self.stable_model = deepcopy(model)
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.use_encoding = use_encoding
        self.rewards_object = rewards_object

    def update_stable_model(self):
       self.stable_model.load_state_dict(self.model.state_dict()) 

    def update_epsilon(self):
        if self.epsilon > self.epsilon_decay:
            self.epsilon -= self.epsilon_decay

    def save_model(self, path):
        torch.save(self.model.state_dict(), path)

    def best_action(self, board, piece, next_piece, model):
        actions, afterstates, lines, gameover = tetris_parser.get_all_afterstates(board, piece, next_piece, self.use_encoding)
        afterstate_values = list(model(afterstates).detach().numpy())

        for i in range(len(actions)):
            afterstate_values[i] += self.rewards_object.total_reward(
                    lines[i],
                    actions[i][0],
                    gameover[i]
                    )

        while len(actions) > 0:
            idx_best_action = np.argmax(afterstate_values) 
            best_action = actions[idx_best_action]
            #print("board: ", board)
            #print("piece: ", piece)
            #print("best_action: ", best_action)
            route = tetris_parser.get_route(board, piece, best_action[0], best_action[1], best_action[2], [], [])
            if route != None:
                return best_action, route, afterstate_values[idx_best_action][0]
            #print("removed unviable action: ", best_action)
            idx = actions.index(best_action)
            del actions[idx]
            del afterstate_values[idx]
            #print("actions left: ", actions)

    def random_action(self, board, piece):
        possible_actions = tetris_parser.get_possible_actions(board, piece)
        while len(possible_actions) > 0:
            play = random.choice(possible_actions)
            route = tetris_parser.get_route(board, piece, play[0], play[1], play[2], [], [])
            if route != None:
                return play, route
            #print("removed unviable action")
            possible_actions.remove(play)


    def act(self, board, piece, next_piece):
        if random.random() < self.epsilon:
            return self.random_action(board, piece)
        else:
            action, route, _ = self.best_action(board, piece, next_piece, self.model)
            return action, route


