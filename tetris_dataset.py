import tetris_parser
import random
from collections import deque


class dataset_manager():

    def __init__(self, rewards_object, db_size):
        self.rewards_object = rewards_object
        self.db = deque(maxlen=db_size)

    def __len__(self):
        return len(self.db)
    def __getitem(self, idx):
        return self.db[idx]
    def sample(self, batch_size):
        out = []
        for _ in range(batch_size):
            out.append(self.db[self.shuffled_idx[self.iterator]])
            self.iterator = (self.iterator + 1) % len(self.db)
        return out

    def gen_train_db(self, game_db):

        for game in game_db:
            for i in range(len(game)):
                #se não perdeu mas acabou o episodio (chego no max de jogadas)
                if i == len(game)-1 and not game[i]['gameover']:
                    break
                state = (game[i]["board"], game[i]["piece"], game[i]["next_piece"])
                action = game[i]["action"]
                rew = self.rewards_object.total_reward(
                        game[i]["lines_cleared"],
                        game[i]["action"][0],
                        game[i]["gameover"]
                        )                

                if game[i]['gameover']:
                    next_state = None
                else:
                    next_state = (game[i+1]["board"], game[i+1]["piece"], game[i+1]["next_piece"])
                self.db.append((state, action, rew, next_state))

        self.shuffled_idx = list(range(len(self.db)))
        random.shuffle(self.shuffled_idx)
        self.iterator = 0

if __name__ == '__main__':
    pass
