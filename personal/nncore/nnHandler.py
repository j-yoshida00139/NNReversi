"""
nnhandler.py

Handler method to learn based on Neural Network learning process
"""
from personal.nncore import move_loader
from personal.nncore import network
from personal.utils.trainer import Trainer


class NNHandler(object):
	def __init__(self):
		self.n_input = 192
		self.n_neutral_neuron = 100
		self.n_output = 64
		self.size = [self.n_input, self.n_neutral_neuron, self.n_output]
		print("loaded")

	@staticmethod
	def learn():
		maxFileNo = 32000

		n_epoch = 1
		n_batch_size = 100
		# n_batch_size = math.floor(maxFileNo/200)*200
		print("batch size is :")
		print(n_batch_size)
		# coe_learn = 0.1
		# lmbda = 0.0
		# lmbda = 0.001
		print("started")

		for x in range(n_epoch):
			print("cycle number : {0:03d}".format(x+1))
			x_train, t_train, x_eva, t_eva, x_test, t_test = move_loader.load_data(maxFileNo, flatten=False)

			net = network.Network()
			trainer = Trainer(
				net, x_train, t_train, x_test, t_test,
				epochs=20, mini_batch_size=100,
				optimizer='Adam', optimizer_param={'lr': 0.001},
				evaluate_sample_num_per_epoch=1000)
			trainer.train()
