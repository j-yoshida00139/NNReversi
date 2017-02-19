from collections import OrderedDict
import layer
import numpy as np
import last_result_loader as lr_loader


class Network(object):

	def __init__(self, sizes):
		self.sizes = sizes
		self.sizes, self.weights, self.biases = lr_loader.load_data(sizes)

		self.layers = OrderedDict()
		self.layers['Affine1'] = layer.AffineLayer(self.weights[0], self.biases[0])
		self.layers['Relu1'] = layer.Relu()
		self.layers['Affine2'] = layer.AffineLayer(self.weights[1], self.biases[1])
		self.lastLayer = layer.SoftmaxCrossEntropyLayer()

	def feedforward(self, x):
		for layer in self.layers.values():
			x = layer.forward(x)
		return x

	def loss(self, x, t):
		y = self.feedforward(x)
		return self.lastLayer.forward(y, t)

	def accuracy(self, x, t):
		y = self.feedforward(x)
		y = np.argmax(y, axis=1)
		if t.ndim != 1: t = np.argmax(t, axis=1)

		accuracy = np.sum(y == t) / float(x.shape[0])
		return accuracy

	def gradient(self, x, t):
		self.loss(x, t)

		dout = 1
		dout = self.lastLayer.backward(dout)

		layers = list(self.layers.values())
		layers.reverse()
		for layer in layers:
			dout = layer.backward(dout)

		grads = {}
		grads['W1'], grads['b1'] = self.layers['Affine1'].dW, self.layers['Affine1'].db
		grads['W2'], grads['b2'] = self.layers['Affine2'].dW, self.layers['Affine2'].db
		return grads

	def SGD(self, x_train, t_train, epochs, mini_batch_size, eta,
			x_eva = None, t_eva = None):

		for j in range(epochs):
			batch_mask = np.random.choice(x_train.shape[0], mini_batch_size)
			x_batch = x_train[batch_mask]
			t_batch = t_train[batch_mask]

			grad = self.gradient(x_batch, t_batch)

			self.weights[0] -= eta * grad['W1']
			self.weights[1] -= eta * grad['W2']
			self.biases[0] -= eta * grad['b1']
			self.biases[1] -= eta * grad['b2']

			if j % 600 == 0:
				accuracy = self.accuracy(x_train, t_train)
				print("Accuracy on training data  : {0:8f}".format(
					accuracy))
				accuracy = self.accuracy(x_eva, t_eva)
				print("Accuracy on evaluation data: {0:8f}".format(
					accuracy))
		lr_loader.store_result(self.sizes, self.weights, self.biases)
