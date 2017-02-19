"""
nnhandler.py

Handler method to learn based on Neural Network learning process
"""
import move_loader
import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir) + '/utils')
import network
from utils.trainer import Trainer
from mnist import load_mnist

class NNHandler(object):
	def __init__(self):
		self.n_input = 192 #366
		self.n_neutral_neuron = 100
		self.n_output = 64 #12
		self.size = [self.n_input, self.n_neutral_neuron, self.n_output]
		print("loaded")

	def learn(self):
		maxFileNo = 18000

		n_epoch = 10000
		n_batch_size = 100
		#n_batch_size = math.floor(maxFileNo/200)*200
		print("batch size is :")
		print(n_batch_size)
		coe_learn = 0.1
		lmbda = 0.0
		#lmbda = 0.001
		print("started")

		for x in range(1):
			print("cycle number : {0:03d}".format(x+1))
			x_train, t_train, x_eva, t_eva, x_test, t_test = move_loader.load_data(maxFileNo, flatten=False)

			#(x_train, t_train), (x_test, t_test) = load_mnist(flatten=False)
			net = network.Network()
			trainer = Trainer(net, x_train, t_train, x_test, t_test,
			                  epochs=20, mini_batch_size=100,
			                  optimizer='Adam', optimizer_param={'lr':0.001},
			                  evaluate_sample_num_per_epoch=1000)
			trainer.train()
			#net = network2_edit.Network(self.size)
			#net.SGD(x_train, t_train, n_epoch, n_batch_size, coe_learn, x_eva, t_eva)


