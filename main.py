import pickle
import sys
import tetris_dataset
import player
import mlp
import cnn
import qlearning
import rewards
import random
import torch

torch.set_num_threads(4)
random.seed(1)      #change seeds later

load_from_file = not "-n" in sys.argv
if load_from_file:
    print("loading weights from file")
else:
    print("starting weights from scratch")

#filename = sys.argv[-1]
#f = open(filename, "rb")
#games_data = pickle.load(f)

reward_exp = 4
penalty_exp = 2
penalty_multiplier = 0.1

rewards_object = rewards.Rewards(reward_exp, penalty_exp, penalty_multiplier)

#mexer no tamannho
db_manager = tetris_dataset.dataset_manager(rewards_object)
#db_manager.gen_game_db(games_data)

init_epsilon = 1
n_episodes = 2000
lr = 0.00001
epochs = 10
update_interval = 10
gamma = 0.99
delta = 0.1

name = "cnn_"
name += "lr"+str(lr)+"_epochs"+str(epochs)+"_update_interval"+str(update_interval)+"_gamma"+str(gamma)+"_delta"+str(delta)+"_rew_exp"+str(reward_exp)+"_pen_exp"+str(penalty_exp)+"_pen_mult"+str(penalty_multiplier)
print("Name: ", name)

ql = qlearning.qlearning(
        player = player.player(
            model = cnn.CNN(),
            init_epsilon = init_epsilon,
            min_epsilon = 0.01,
            load_from_file = load_from_file,
            rewards_object = rewards_object,
            name = name,
            gamma = gamma,
            delta = delta
        ),
        n_episodes = n_episodes,
        n_games = 100,
        max_plays = 300,
        dataset_manager = db_manager,
        epochs = epochs,
        batch_size = 128,
        lr = lr,
        name = name,
        update_interval = update_interval,
        gamma = gamma,
        delta = delta,
        rewards_object = rewards_object
    )
#ql.main_loop(not load_from_file)
ql.main_loop(False)

