import sys

class Rewards:
    
    def __init__(self, rew_exp, pen_exp, pen_multiplier):
        self.rew_exp = rew_exp
        self.pen_exp = pen_exp
        self.pen_multiplier = pen_multiplier

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

