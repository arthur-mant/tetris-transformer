import rewards

#TESTAR

class gen_dataset:

    def __init__(self, reward_function, penalty_function):
        self.rewards_object = rewards.Rewards(reward_function, penalty_function)

    def get_data(self, game_data, initial_rtg)
        out = []
        for game in game_data:
            rtg = initial_rtg
            game_dataset = []
            for play in game:
                game_dataset.append(self.get_play(play, rtg))
                rtg = game_dataset[-1][-2]
            out.append(game_dataset)
        return out

    def get_play(self, play_data, rtg):
        rtg -= self.reward_object(
                play["lines_cleared"],
                play["action"][0], 
                play["is_illegal"]
                )
        #processar a informação como for necessário
        return [play["board"], play["piece"], play["next_piece"], play["action"], rtg, play["done"]]
