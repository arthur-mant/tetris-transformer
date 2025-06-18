import rewards
import torch

#TESTAR

class dataset_manager:

    def __init__(self, reward_function, penalty_function):
        self.rewards_object = rewards.Rewards(reward_function, penalty_function)

    def set_db(self, play_db):
        self.play_db = play_db

    def gen_db(self):
        states = []
        actions = []
        rews = []

        for play in self.play_db:
            s, a, r = self.get_play(play)
            states += s
            actions += a
            rews += r

        return states, actions, rews

    def get_play(self, play):
        state = self.encode_state(play["board"], play["piece"], play["next_piece"])

        action = play["action"]

        rew= self.rewards_object.total_reward(
                play["lines_cleared"],
                play["action"][0]
                )

        return state, action, rew


if __name__ == '__main__':
    pass
