import tetris_parser
import random
from collections import deque
import torch

class dataset_manager():

    def __init__(self, rewards_object, db_size):
        self.rewards_object = rewards_object
        self.db = deque(maxlen=db_size)
        self.shuffled_idx = list(range(db_size))

    def __len__(self):
        return len(self.db)
    def __getitem(self, idx):
        return self.db[idx]
    def sample(self, batch_size):
        q_out = []
        target_q_out = []
        for _ in range(batch_size):
            idx = self.shuffled_idx[self.iterator]
            q_out.append(idx)
            target_q_out.append(self.target_q[self.shuffled_idx[self.iterator]])
            self.iterator += 1
            if self.iterator == len(self.q):
                self.shuffle()
        return torch.tensor(q_out, dtype=torch.float), torch.tensor(target_q_out, dtype=torch.float)

    def gen_game_db(self, game_db):

        for game in game_db:
            for i in range(len(game)):
                #se não perdeu mas acabou o episodio (chego no max de jogadas)
                if i == len(game)-1:
                    break
                state = (game[i]["board"], game[i]["piece"], game[i]["next_piece"])
                action = game[i]["action"]
                next_rew = self.rewards_object.total_reward(
                        game[i+1]["lines_cleared"],
                        game[i+1]["action"][0],
                        game[i+1]["gameover"]
                        )                
                next_state = (game[i+1]["board"], game[i+1]["piece"], game[i+1]["next_piece"])
                self.db.append((state, action, next_rew, next_state))

    def gen_train_db(self, model, calculate_target_q, use_encoding):
        self.q = []
        self.target_q = []
        with torch.no_grad():
            for s, a, nr, ns in self.db:
                afterstate, lines, gameover = tetris_parser.generate_afterstate(s[0], s[1], s[2], a, use_encoding) 
                self.q.append(model(afterstate).item())
                self.target_q.append(calculate_target_q(nr, ns))
                #if self.target_q[-1] > 30:
                #    print(s, a, nr, ns, self.q[-1], self.target_q[-1])
        #print("q: ", self.q[:100])
        #print("target_q: ", self.target_q[:100])
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.shuffled_idx)
        self.iterator = 0

if __name__ == '__main__':
    pass
