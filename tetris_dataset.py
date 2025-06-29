import rewards
import tetris_parser
import random
from collections import deque

#TESTAR

class dataset_manager():

    def __init__(self, reward_function, penalty_function, db_size):
        self.rewards_object = rewards.Rewards(reward_function, penalty_function)
        self.db = deque(maxlen=db_size)

    def __len__(self):
        return len(self.db)
    def __getitem(self, idx):
        return self.db[idx]
    def sample(self, batch_size):
        return random.sample(selb.db, batch_size)

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
                db.append((state, action, rew, next_state))

if __name__ == '__main__':
    pass
