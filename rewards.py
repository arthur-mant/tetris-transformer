import sys

class Rewards:
    #definição das constantes
    #valores provisórios
    crl = 1
    crq = 1
    cphl = -10*1/20     #fração de quanto a penalidade vale em relação à recompensa
    cphq = -1*1/100
    cpi = -2
    
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
            self.pen = self.penalty_height_linear
        else:
            print("invalid penalty function")
            sys.exit(1)

    def reward_linear(self, l):
        return self.crl*l
    def reward_quadratic(self, l):
        return self.crq*l*l
    def penalty_height_linear(self, h):
        return self.cphl*(20-h)
    def penalty_height_linear(self, h):
        return self.cphq*(20-h)*(20-h)
    def total_reward(self, lines, height):
        return self.rew(lines)+self.pen(height)

