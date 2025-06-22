from tetris-dataset import dataset_manager
import tetris_parser
import numpy as np
import random

db_file = 
exploration_rate = 

class player():
    def __init__(self, model):
        self.model = model
    def best_action(self, board, piece, next_piece):
        actions, afterstate_encodings = tetris_parser.get_all_afterstates_encodings(board, piece, next_piece)
        afterstate_values = self.model(afterstate_encodings)
        
        while len(actions) > 0:
            play = actions[np.argmax(afterstate_values)]
            route = tetris_parser.get_route(board, piece, play[0], play[1], play[2], [])
            if route != None:
                return play, route
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
        if random.random() < exploration_rate:
            return self.random_action(board, piece)
        else:
            return self.best_action(board, piece, next_piece)


