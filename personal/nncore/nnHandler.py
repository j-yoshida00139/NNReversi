"""
nnhandler.py

Handler method to learn based on Neural Network learning process
"""
import move_loader
import network
import sys, os, math
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir) + '/utils')
import basicFunc
#sys.path.append(os.path.dirname(os.path.abspath(__file__).pardir))
from mnist import load_mnist

import network2_edit

class NNHandler(object):
	print(os.path.join(os.path.dirname(__file__), os.pardir))
	def __init__(self):
		#self.n_input = 192 #366
		#self.n_neutral_neuron = 100
		#self.n_output = 64 #12
		self.n_input = 784 #366
		self.n_neutral_neuron = 50
		self.n_output = 10 #12
		self.size = [self.n_input, self.n_neutral_neuron, self.n_output]
		print("loaded")

	def learn(self):
		maxFileNo = 1800
		#maxFileNo = basicFunc.getLastFileNo()

		n_epoch = 10000
		n_batch_size = 100
		#n_batch_size = math.floor(maxFileNo/200)*200
		print("batch size is :")
		print(n_batch_size)
		#coe_learn = 10.0
		coe_learn = 0.1
		lmbda = 0.0
		#lmbda = 0.001
		print("started")

		for x in range(1):
			print("cycle number : {0:03d}".format(x+1))
			training_data2, validation_data2, test_data2 = move_loader.load_data(n_batch_size)
			(x_train, t_train), (x_eva, t_eva) = load_mnist(normalize=True, one_hot_label=True)
			#training_data, validation_data = [], []
			#for x, t in zip(training_data_tmp[0], training_data_tmp[1]):
			#	training_data.append([x, t])
			#for x, t in zip(validation_data_tmp[0], validation_data_tmp[1]):
			#	validation_data.append([x, t])
			#print("training_data : ")
			#print(len(training_data))
			#print("validation_data : ")
			#print(len(validation_data))
			"""network.py"""
			#net = network.Network(self.size)
			#net.SGD(training_data, n_epoch, n_batch_size, coe_learn, test_data=test_data)
			"""network2.py"""
			#net = network2.load('properties.txt')
			net = network2_edit.Network(self.size, cost=network2_edit.QuadraticCost())
			#net = network2_edit.Network(self.size, cost=network2_edit.CrossEntropyCost())
			#net.SGD(training_data, n_epoch, n_batch_size, coe_learn, lmbda, evaluation_data=validation_data,
			#        monitor_evaluation_accuracy=True, monitor_evaluation_cost=True, monitor_training_accuracy=True,
			#        monitor_training_cost=True)
			net.SGD(x_train, t_train, n_epoch, n_batch_size, coe_learn, x_eva, t_eva)

	#net.save('properties.txt')

