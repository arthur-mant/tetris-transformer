import tetris_parser
import random
from collections import deque
import torch

class dataset_manager():

    def __init__(self, rewards_object, db_size):
        self.rewards_object = rewards_object
        self.db = deque(maxlen=db_size)
        self.shuffled_idx = []

    def __len__(self):
        return len(self.db)
    def __getitem(self, idx):
        return self.db[idx]
    def sample(self, batch_size):
        afterstates_out = []
        next_pieces_out = []
        target_q_out = []
        for _ in range(batch_size):
            idx = self.shuffled_idx[self.iterator]
            afterstates_out.append(self.afterstates[self.shuffled_idx[self.iterator]])
            next_pieces_out.append(self.next_pieces[self.shuffled_idx[self.iterator]])
            target_q_out.append(self.target_q[self.shuffled_idx[self.iterator]])
            self.iterator += 1
            if self.iterator == len(self.target_q):
                self.shuffle()
        return torch.stack(afterstates_out), torch.cat(next_pieces_out, 0), torch.stack(target_q_out)

    def gen_game_db(self, game_db):
        for game in game_db:
            for i in range(len(game)):
                #se não perdeu mas acabou o episodio (chego no max de jogadas)
                if i == len(game)-1:
                    break
                state = (game[i]["board"], game[i]["piece"], game[i]["next_piece"])
                action = game[i]["action"]
                next_state = (game[i+1]["board"], game[i+1]["piece"], game[i+1]["next_piece"])
                self.db.append((state, action, next_state))

    def gen_train_db(self, model, calculate_target_q):
        self.afterstates = []
        self.next_pieces = []
        self.target_q = []
        with torch.no_grad():
            for s, a, ns in self.db:
                afterstate, next_piece, lines, gameover = tetris_parser.generate_afterstate(s[0], s[1], s[2], a) 
                self.afterstates.append(afterstate)
                self.next_pieces.append(next_piece)
                self.target_q.append(torch.tensor(calculate_target_q(ns), dtype=torch.float))

        if len(self.shuffled_idx) != len(self.target_q):
            self.shuffled_idx = list(range(len(self.target_q)))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.shuffled_idx)
        self.iterator = 0

if __name__ == '__main__':
    pass
