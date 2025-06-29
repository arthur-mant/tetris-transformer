from tetris-dataset import dataset_manager
import tetris_parser
import numpy as np
import random
from copy import deepcopy

db_file = 

class player():
    def __init__(self, model):
        self.model = model
        self.stable_model = deepcopy(model)

    def update_stable_model(self)
       self.stable_model.load_state_dict(self.model.state_dict()) 

    def set_epsilon(self, num_episode)
        self.epsilon = epsilon

    def best_action(self, board, piece, next_piece, model):
        actions, afterstate_encodings = tetris_parser.get_all_afterstates_encodings(board, piece, next_piece)
        afterstate_values = model(afterstate_encodings)
        
        while len(actions) > 0:
            idx_best_action = np.argmax(afterstate_values) 
            best_action = actions[idx_best_play]
            route = tetris_parser.get_route(board, piece, best_action[0], best_action[1], best_action[2], [])
            if route != None:
                return play, route, afterstate_values[idx_best_action]
            print("removed unviable action")
            idx = actions.index(play)
            actions.remove(idx)
            afterstate_values.remove(idx)

    def random_action(self, board, piece):
        possible_actions = tetris_parser.get_possible_actions(board, piece)
        while len(possible_actions) > 0:
            play = random.choice(possible_actions)
            route = tetris_parser.get_route(board, piece, play[0], play[1], play[2], [])
            if route != None:
                return play, route
            print("removed unviable action")
            possible_actions.remove(play)


    def act(self, board, piece, next_piece):
        if random.random() < epsilon:
            return self.random_action(board, piece)
        else:
            action, route, _ = self.best_action(board, piece, next_piece, self.model)
            return action, route


