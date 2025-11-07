import sys

class Rewards:
    
    def __init__(self, min_rew_exp, max_rew_exp, pen_exp, pen_multiplier):
        self.rew_exp = min_rew_exp
        self.min_rew_exp = min_rew_exp
        self.max_rew_exp = max_rew_exp
        self.pen_exp = pen_exp
        self.pen_multiplier = pen_multiplier

    def update_rew_exp(self, episode):
        if self.rew_exp < self.max_rew_exp:
            #no 1500 se chega no final
            self.rew_exp = self.min_rew_exp+((self.max_rew_exp-self.min_rew_exp)*episode/1500)
        print("Novo expoente da recompensa: ", self.rew_exp)

    def reward(self, l):
        return pow(l, self.rew_exp)/pow(4, self.rew_exp)
    def penalty(self, h):
        return self.pen_multiplier*pow(18-h, self.pen_exp)/pow(20, self.pen_exp)
    def penalty_gameover(self):
        #penaliza 1 tetris quando perde
        return -1
    def total_reward(self, lines, height, gameover):
        if gameover:
            return self.penalty_gameover()
        return self.reward(lines)-self.penalty(height)

