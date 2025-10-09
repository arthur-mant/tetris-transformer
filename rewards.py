import sys

class Rewards:
    #definição das constantes
    #valores provisórios
    cphl = -10*1/20     #fração de quanto a penalidade vale em relação à recompensa
    cphq = -1*1/(22*22)
    
    def __init__(self, reward_function, penalty_function):
        if reward_function == "l":
            self.rew = self.reward_linear
        elif reward_function == "q":
            self.rew = self.reward_quadratic
        else:
            print("invalid reward function")
            sys.exit(1)

        if penalty_function == "l":
            self.pen = self.penalty_height_linear
        elif penalty_function == "q":
            self.pen = self.penalty_height_quadratic
        else:
            print("invalid penalty function")
            sys.exit(1)

    def reward_linear(self, l):
        return l
    def reward_quadratic(self, l):
        return l*l/(4*4)
    def penalty_height_linear(self, h):
        return self.cphl*(20-h)
    def penalty_height_quadratic(self, h):
        return self.rew(1)/self.rew(4)*(20-h)*(20-h)/(22*22)
    def penalty_gameover(self):
        #penaliza 1 tetris quando perde
        return -1
    def total_reward(self, lines, height, gameover):
        if gameover:
            return self.penalty_gameover()
        return self.rew(lines)-self.pen(height)

