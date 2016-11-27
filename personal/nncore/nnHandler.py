"""
nnhandler.py

Handler method to learn based on Neural Network learning process
"""
import move_loader
import network
#import network2

class NNHandler(object):

	def __init__(self):
		self.n_input = 192 #366
		self.n_neutral_neuron = 100
		self.n_output = 64 #12
		self.size = [self.n_input, self.n_neutral_neuron, self.n_output]
		print("loaded")

	def learn(self):
		n_epoch = 100
		n_batch_size = 200
		coe_learn = 0.1
		print("started")

		for x in range(10):
			print("cycle number : {0:03d}".format(x+1))
			training_data, validation_data, test_data = move_loader.load_data()
			print("training_data : ")
			print(len(training_data))
			print("validation_data : ")
			print(len(validation_data))
			print("test_data : ")
			print(len(test_data))
			"""network.py"""
			net = network.Network(self.size)
			net.SGD(training_data, n_epoch, n_batch_size, coe_learn, test_data=test_data)
			"""network2.py"""
		#net = network2.load('properties.txt')
		#net = network2.Network(size, cost=network2.CrossEntropyCost())
		#net.SGD(training_data, 30, 10, 0.5, lmbda = 5.0, evaluation_data=validation_data, monitor_evaluation_accuracy=True, monitor_evaluation_cost=True, monitor_training_accuracy=True, monitor_training_cost=True)

		#net.save('properties.txt')

