import pickle
import sys
import tetris_dataset
import player
import mlp
import qlearning

filename = sys.argv[1]
f = open(filename, "rb")
games_data = pickle.load(f)

reward_function = 'q'
penalty_function = 'q'

db_manager = tetris_dataset.dataset_manager(reward_function, penalty_function, 10000)
db_manager.gen_train_db(games_data)

init_epsilon = 0.3
n_episodes = 100

ql = qlearning.qlearning(
        player = player.player(
            model = mlp.MLP(),
            epsilon = init_epsilon,
            epsilon_decay = (init_epsilon - 0.01)/n_episodes,
        ),
        n_episodes = n_episodes,
        n_games = 50,
        max_plays = 100,
        dataset_manager = db_manager,
        gamma = 0.99,
        epochs = 10,
        batch_size = 128,
        lr = 0.00001,
    )
ql.main_loop()
