import pickle
import sys
import tetris_dataset
import player
import mlp
import qlearning

load_from_file = not "-n" in sys.argv
if load_from_file:
    print("loading weights from file")
else:
    print("starting weights from scratch")

filename = sys.argv[-1]
f = open(filename, "rb")
games_data = pickle.load(f)

reward_function = 'q'
penalty_function = 'q'

#mexer no tamannho
db_manager = tetris_dataset.dataset_manager(reward_function, penalty_function, 10000)
db_manager.gen_train_db(games_data)

init_epsilon = 0.1
n_episodes = 1000

ql = qlearning.qlearning(
        player = player.player(
            model = mlp.MLP(),
            epsilon = init_epsilon,
            epsilon_decay = (init_epsilon - 0.01)/n_episodes,
            load_from_file = load_from_file
        ),
        n_episodes = n_episodes,
        n_games = 100,
        max_plays = 100,
        dataset_manager = db_manager,
        gamma = 0.99,
        epochs = 1,
        batch_size = 128,
        lr = 0.0001,
    )
ql.main_loop()
