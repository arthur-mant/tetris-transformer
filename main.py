import pickle
import sys
import tetris_dataset
import player
import mlp
import cnn
import qlearning
import random
import torch

torch.set_num_threads(4)
random.seed(1)      #change seeds later

load_from_file = not "-n" in sys.argv
if load_from_file:
    print("loading weights from file")
else:
    print("starting weights from scratch")


db_manager = tetris_dataset.dataset_manager()

init_epsilon = 1
n_episodes = 2500
lr = 0.00001
epochs = 10
update_interval = 10
gamma = 0.99

name = "real_score_"
name += "lr"+str(lr)+"_epochs"+str(epochs)+"_update_interval"+str(update_interval)+"_gamma"+str(gamma)
print("Name: ", name)

ql = qlearning.qlearning(
        player = player.player(
            model = cnn.CNN(),
            init_epsilon = init_epsilon,
            min_epsilon = 0.01,
            load_from_file = load_from_file,
            name = name,
            gamma = gamma
        ),
        n_episodes = n_episodes,
        n_games = 100,
        max_plays = 500,
        dataset_manager = db_manager,
        epochs = epochs,
        batch_size = 128,
        lr = lr,
        name = name,
        update_interval = update_interval,
        gamma = gamma,
    )
#ql.main_loop(not load_from_file)
ql.main_loop(False)

