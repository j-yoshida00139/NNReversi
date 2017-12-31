from django.core.management.base import BaseCommand
from ...utils.trainer import Trainer
from ...src import network
import pickle
import os

net = network.Network()


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		file_name = 'nncore/input_data/learn_input.pkl'
		if not os.path.exists(file_name):
			print('Input data does not exist.')
			raise BaseException
		with open(file_name, 'rb') as f:
			params = pickle.load(f)

		n_epoch = 1
		print("started")
		for x in range(n_epoch):
			print("cycle number : {0:03d}".format(x + 1))
			x_train, t_train, x_test, t_test = params["x_train"], params["t_train"], params["x_test"], params["t_test"]
			trainer = Trainer(
				net, x_train, t_train, x_test, t_test,
				epochs=20, mini_batch_size=100,
				optimizer='Adam', optimizer_param={'lr': 0.001},
				evaluate_sample_num_per_epoch=1000)
			trainer.train()

		print("Finished.")
