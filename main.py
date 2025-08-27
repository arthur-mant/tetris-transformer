import pickle
import sys
import tetris_dataset
import player
import mlp
import qlearning
import rewards
import random

random.seed(1)      #change seeds later

load_from_file = not "-n" in sys.argv
if load_from_file:
    print("loading weights from file")
else:
    print("starting weights from scratch")

use_encoding = "-ue" in sys.argv or "--use-encoding" in sys.argv
if use_encoding:
    print("using encoding")
else:
    print("not using encoding")

#filename = sys.argv[-1]
#f = open(filename, "rb")
#games_data = pickle.load(f)

reward_function = 'q'
penalty_function = 'q'

rewards_object = rewards.Rewards(reward_function, penalty_function)

#mexer no tamannho
db_manager = tetris_dataset.dataset_manager(rewards_object, 10000)
#db_manager.gen_game_db(games_data)

init_epsilon = 0.1
n_episodes = 10000
lr = 0.00001
epochs = 100
update_interval = 8
gamma = 0.99

name = "lr"+str(lr)+"_epochs"+str(epochs)+"_update_interval"+str(update_interval)+"_use_encoding"+str(use_encoding)+"_rew"+reward_function+"_pen"+penalty_function

ql = qlearning.qlearning(
        player = player.player(
            model = mlp.MLP(use_encoding),
            init_epsilon = init_epsilon,
            min_epsilon = 0.001,
            load_from_file = load_from_file,
            use_encoding = use_encoding,
            rewards_object = rewards_object,
            name = name,
            gamma = gamma,
        ),
        n_episodes = n_episodes,
        n_games = 100,
        max_plays = 100,
        dataset_manager = db_manager,
        epochs = epochs,
        batch_size = 128,
        lr = lr,
        name = name,
        use_encoding = use_encoding,
        update_interval = update_interval,
        gamma = gamma,
        rewards_object = rewards_object
    )
#ql.main_loop(not load_from_file)
ql.main_loop(False)

