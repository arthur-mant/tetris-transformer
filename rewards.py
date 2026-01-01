import sys
from tetris_game import definitions

line_score = [0]+definitions.line_score
def total_reward(lines, height, gameover):
    if gameover:
        return -1
    return (line_score[lines]+height)/(line_score[4]+20)

