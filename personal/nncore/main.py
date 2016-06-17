"""
main.py

main method to run the neural network calculation
"""
import stock_loader
import network
import network2


n_input = 192 #366
n_neutral_neuron = 100
n_output = 64 #12

def nextPiece(arrange):
	size = [n_input, n_neutral_neuron, n_output]
	net = network.Network(size)
	
	return net.feedforward(arrange)

#n_input = 366
#n_neutral_neuron = 100
#n_output = 12
#n_epoch = 100
#n_batch_size = 500
#coe_learn = 0.1
#size = [n_input, n_neutral_neuron, n_output]

#for x in range(10):
	#print "cycle number : {0:03d}".format(x+1)
	#training_data, validation_data, test_data = stock_loader.load_data()
	"""network.py"""
	#net = network.Network(size)
	#net.SGD(training_data, n_epoch, n_batch_size, coe_learn, test_data=test_data)
	"""network2.py"""
	#net = network2.load('properties.txt')
	#net = network2.Network(size, cost=network2.CrossEntropyCost())
	#net.SGD(training_data, 30, 10, 0.5, lmbda = 5.0, evaluation_data=validation_data, monitor_evaluation_accuracy=True, monitor_evaluation_cost=True, monitor_training_accuracy=True, monitor_training_cost=True)
	#net.save('properties.txt')