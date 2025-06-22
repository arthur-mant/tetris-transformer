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
        return [idx]


    def gen_db(self, play_db):
        states = []
        actions = []
        rews = []

        for play in play_db:
            s, r = self.get_play(play)
            states += s
            rews += r

        self.db = 


    def get_play(self, play):
        state = tetris_parser.encode_state(play["board"], play["piece"], play["next_piece"], play["action"])

        rew= self.rewards_object.total_reward(
                play["lines_cleared"],
                play["action"][0],
                play["gameover"]
                )

        return state, rew


if __name__ == '__main__':
    pass
