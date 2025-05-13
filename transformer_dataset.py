import rewards
import torch

#TESTAR

class dataset_manager:

    def __init__(self, reward_function, penalty_function):
        self.rewards_object = rewards.Rewards(reward_function, penalty_function)

    def set_db(self, game_db):
        self.game_db = game_db

    def get_highest_reward_sum(self):
        out = 0
        for game in self.game_db:
            aux = 0
            for play in game:
                aux += self.rewards_object.total_reward(
                        play["lines_cleared"],
                        play["action"][0], 
                        play["is_illegal"]
                    )
            out = max(out, aux)
            print("max reward sum: ", out)
        return out


    def gen_db(self, initial_rtg):
        states = []
        actions = []
        rtgs = []
        timesteps = []
        for game in self.game_db:
            s, a, r, t = self.get_game(game, initial_rtg)
            states += s
            actions += a
            rtgs += r
            timesteps += t

        return (torch.tensor(states), torch.tensor(actions), torch.tensor(rtgs), torch.tensor(timesteps))

    def get_game(self, game_data, initial_rtg):
        states = []
        actions = []
        rtgs = []
        timesteps = []
        aux_rtg = initial_rtg
        for play in game_data:
            state, action, rtg, timestep = self.get_play(play, aux_rtg)
            aux_rtg = rtg

            states.append(state)
            actions.append(action)
            rtgs.append(rtg)
            timesteps.append(timestep)

        return states, actions, rtgs, timesteps
            

    def get_play(self, play, rtg):
        rtg -= self.rewards_object.total_reward(
                play["lines_cleared"],
                play["action"][0], 
                play["is_illegal"]
                )

        aux = []
        for i in play["board"]:
            for j in i:
                aux.append(j)
        aux.append(play["piece"])
        aux.append(play["next_piece"])
        state = aux
        action = play["action"]
        rtg = rtg
        timestep = play["timestep"]
        return state, action, rtg, timestep

if __name__ == '__main__':
    pass
