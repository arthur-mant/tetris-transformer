import rewards

#TESTAR

class gen_dataset:

    def __init__(self, reward_function, penalty_function):
        self.rewards_object = rewards.Rewards(reward_function, penalty_function)

    def load_data(self, game_db, initial_rtg):
        states = []
        actions = []
        rtgs = []
        timesteps = []
        for game in game_db:
            s, a, r, t = self.get_game(game, initial_rtg)
            states += s
            actions += a
            rtgs += r
            timesteps += t
        return torch.tensor(states), torch.tensor(actions), torch.tensor(rtgs), torch.tensor(timesteps)

    def get_game(self, game_data, initial_rtg):
        states = []
        actions = []
        rtgs = []
        timesteps = []
        aux_rtg = initial_rtg
        for play in game:
            state, action, rtg, timestep = self.get_play(play, aux_rtg)
            aux_rtg = rtg

            states.append(state)
            actions.append(action)
            rtgs.append(rtg)
            timesteps.append(timestep)

        return states, actions, rtgs, timesteps
            

    def get_play(self, play_data, rtg):
        rtg -= self.reward_object(
                play["lines_cleared"],
                play["action"][0], 
                play["is_illegal"],
                play["done"]
                )

        aux = []
        for i in play["board"]:
            for j in i:
                aux.append(j)
        aux.append(play["piece"])
        aux.append(play["next_piece"])
        state = aux
        action = play["action"]
        rtg = [rtg]
        timestep = [play["timestep"]]
        return state, action, rtg, timestep

if __name__ == '__main__':
    
