class Rewards:
    crl = 
    crq = 
    cphl =
    cphq = 
    
    def reward_linear(l):
        return self.crl*l
    def reward_quadratic(l):
        return self.crq*l*l
    def penalty_height_linear(h):
        return cphl*h
    def penalty_height_linear(h):
        return cphq*h*h
    def penalty_overlap(overlap):
        return overlap
