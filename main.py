import pickle
import sys
import transformer_dataset

filename = sys.argv[1]
f = open(filename, "rb")
games_data = pickle.load(f)

reward_function = 'q'
penalty_function = 'q'

db_manager = transformer_dataset.dataset_manager(reward_function, penalty_function)
db_manager.set_db(games_data)

train_dataset = db_manager.gen_db(db_manager.get_highest_reward_sum())

#print(train_dataset)
#print(train_dataset[0][0], train_dataset[1][0], train_dataset[2][0], train_dataset[3][0])

