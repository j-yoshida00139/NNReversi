"""
nnhandler.py

Handler method to learn based on Neural Network learning process
"""
import move_loader
import network
import sys, os, math
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
#sys.path.append(os.path.dirname(os.path.abspath(__file__).pardir))


import network2

class NNHandler(object):
	print(os.path.join(os.path.dirname(__file__), os.pardir))
	def __init__(self):
		self.n_input = 192 #366
		self.n_neutral_neuron = 100
		self.n_output = 64 #12
		self.size = [self.n_input, self.n_neutral_neuron, self.n_output]
		print("loaded")

	def learn(self):
		import game
		game = game.Game(8, 8)
		maxFileNo = game.getLastFileNo()

		n_epoch = 100
		n_batch_size = math.floor(maxFileNo/200)*100
		print("batch size is :")
		print(n_batch_size)
		coe_learn = 0.1
		print("started")

		for x in range(10):
			print("cycle number : {0:03d}".format(x+1))
			training_data, validation_data, test_data = move_loader.load_data(n_batch_size)
			print("training_data : ")
			print(len(training_data))
			print("validation_data : ")
			print(len(validation_data))
			print("test_data : ")
			print(len(test_data))
			"""network.py"""
			#net = network.Network(self.size)
			#net.SGD(training_data, n_epoch, n_batch_size, coe_learn, test_data=test_data)
			"""network2.py"""
			#net = network2.load('properties.txt')
			net = network2.Network(self.size, cost=network2.CrossEntropyCost())
			net.SGD(training_data, n_epoch, n_batch_size, 10.0, lmbda = 1.0, evaluation_data=validation_data, monitor_evaluation_accuracy=True, monitor_evaluation_cost=True, monitor_training_accuracy=True, monitor_training_cost=True)

			#net.save('properties.txt')

