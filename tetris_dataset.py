import rewards
import torch
import tetris_parser

#TESTAR

class dataset_manager:

    def __init__(self, reward_function, penalty_function):
        self.rewards_object = rewards.Rewards(reward_function, penalty_function)

    def __len__(self):
        return len()
    def __getitem(self, idx):
        return self.db[idx]


    def gen_train_db(self, game_db, calculate_target_q):
        self.db = []
        for game in game_db:
            for i in range(len(game)):
                #se não perdeu mas acabou o episodio (chego no max de jogadas)
                if i == len(game)-1 and not game[i]['gameover']:
                    break
                rew = self.rewards_object.total_reward(
                        game[i]["lines_cleared"],
                        game[i]["action"][0],
                        game[i]["gameover"]
                        )
                if game[i]['gameover']:
                    target_q = rew
                else:
                    target_q = calculate_target_q(rew, [game[i+1]["board"], game[i+1]["piece"], game[i+1]["next_piece"]])

                state_encoding = tetris_parser.encode_state(game[i]["board"], game[i]["piece"], game[i]["next_piece"], game[i]["action"])
                self.db.append([state_encoding, target_q])

if __name__ == '__main__':
    pass
