#### Libraries
# Standard library
import json
import random
from collections import OrderedDict

# Third-party libraries
import numpy as np
# import bigfloat

import last_result_loader as lr_loader

#### Define the quadratic and cross-entropy cost functions

class QuadraticCost(object):

	@staticmethod
	def fn(a, y):
		return 0.5*np.linalg.norm(a-y)**2

	@staticmethod
	def delta(z, a, y):
		return (a-y) * sigmoid_prime(z)


class CrossEntropyCost(object):

	@staticmethod
	def fn(a, y):
		return np.sum(np.nan_to_num(-y*np.log(a)-(1-y)*np.log(1-a)))

	@staticmethod
	def delta(_z, a, y):
		return (a-y)


class AffineLayer(object):
	def __init__(self, w, b):
		self.w = w
		self.b = b

		self.x = None
		self.original_x_shape = None
		self.dw = None
		self.db = None

	def forward(self, x):
		self.original_x_shape = x.shape
		x = x.reshape(x.shape[0], -1)
		self.x = x

		out_temp = np.dot(self.x, self.w)
		out = np.dot(self.x, self.w) + self.b
		return out

	def backward(self, dout):
		dx = np.dot(dout, self.w.T)
		self.dW = np.dot(self.x.T, dout)
		self.db = np.sum(dout, axis=0)

		dx = dx.reshape(*self.original_x_shape)
		return dx


class Relu:
	def __init__(self):
		self.mask = None

	def forward(self, x):
		self.mask = (x <= 0)
		out = x.copy()
		out[self.mask] = 0

		return out

	def backward(self, dout):
		dout[self.mask] = 0
		dx = dout

		return dx

class SigmoidLayer(object):
	def __init__(self):
		self.out = None

	def forward(self, x):
		out = sigmoid(x)
		self.out = out
		return out

	def backward(self, dout):
		dx = dout * (1.0 - self.out) * self.out
		return dx

class SoftmaxCrossEntropyLayer(object):
	def __init__(self):
		self.loss = None
		self.y = None
		self.t = None

	def forward(self, x, t):
		self.t = t
		self.y = softmax(x)
		self.loss = crossEntropyLoss(self.y, self.t)
		return self.loss

	def backward(self, dout=1):
		batch_size = self.t.shape[0]
		if self.t.size == self.y.size:
			dx = (self.y - self.t) / batch_size
		else:
			dx = self.y.copy()
			dx[np.arange(batch_size), self.t] -= 1
			dx = dx / batch_size

		return dx




#### Main Network class
class Network(object):

	def __init__(self, sizes, cost=CrossEntropyCost):
		self.sizes = sizes
		self.sizes, self.weights, self.biases = lr_loader.load_data(sizes)

		self.layers = OrderedDict()
		self.layers['Affine1'] = AffineLayer(self.weights[0], self.biases[0])
		self.layers['Relu1'] = Relu()
		self.layers['Affine2'] = AffineLayer(self.weights[1], self.biases[1])
		self.lastLayer = SoftmaxCrossEntropyLayer()

	def feedforward(self, x):
		for layer in self.layers.values():
			x = layer.forward(x)
		return x

	def loss(self, x, t):
		y = self.feedforward(x)
		return self.lastLayer.forward(y, t)

	def accuracy(self, data, convert=False):
		results = [(self.feedforward(x.reshape(1, len(x))), y) for (x, y) in data]
		sum_correct = 0
		for result in results:
			i_idx, o_idx = np.argmax(result[0]), np.argmax(result[1])
			sum_correct += 1 if i_idx == o_idx else 0
		return sum_correct * 100.0 / len(results)

	def accuracy_new(self, x, t):
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

			#print("Epoch %s training complete" % j)
			grad = self.gradient(x_batch, t_batch)

			self.weights[0] -= eta * grad['W1']
			self.weights[1] -= eta * grad['W2']
			self.biases[0] -= eta * grad['b1']
			self.biases[1] -= eta * grad['b2']
			if j % 600 == 0:
				accuracy = self.accuracy_new(x_train, t_train)
				print("Accuracy on training data  : {0:8f}".format(
					accuracy))
				accuracy = self.accuracy_new(x_eva, t_eva)
				print("Accuracy on evaluation data: {0:8f}".format(
					accuracy))
		lr_loader.store_result(self.sizes, self.weights, self.biases)

	def update_mini_batch(self, mini_batch, eta, lmbda, n):
		x_batch, t_batch = [], []
		for n in mini_batch:
			x_batch.append(np.array(n[0]))
		for n in mini_batch:
			t_batch.append(np.array(n[1]))
		grad = self.gradient(x_batch, t_batch)

		self.weights[0] -= eta * grad['W1']
		self.weights[1] -= eta * grad['W2']
		self.biases[0] -= eta * grad['b1']
		self.biases[1] -= eta * grad['b2']
		self.layers['Affine1'] = AffineLayer(self.weights[0], self.biases[0])
		self.layers['Affine2'] = AffineLayer(self.weights[1], self.biases[1])

	def softmax(self, x):
		if x.ndim == 2:
			x = x.T
			x -= np.max(x, axis=0)
			y = np.exp(x) / np.sum(np.exp(x), axis=0)
			return y.T

		x -= np.max(x)
		return np.exp(x) / np.sum(np.exp(x))

# Miscellaneous functions
def sigmoid(z):
	#a = np.where(z < -500.0, -500.0, z)

	#b = []
	#for x in a:
	#	b.append(np.exp(-x))
	#a = np.where(a<-10.0, 0.0, np.exp(-a))
	#a = 1.0/(1.0+a)
	#a = np.where(a<-10.0, 0.0, 1.0/(1.0+np.exp(-a)))

	#return np.where(z<-10.0, 0.0, 1.0/(1.0+np.exp(-z)))
	return 1.0/(1.0+np.exp(-z))


def sigmoid_prime(z):
	return sigmoid(z)*(1-sigmoid(z))


def crossEntropyLoss(y, t):
	if y.ndim == 1:
		t = t.reshape(1, t.size)
		y = y.reshape(1, y.size)

	if t.size == y.size:
		t = t.argmax(axis=1)

	batch_size = y.shape[0]
	return -np.sum(np.log(y[np.arange(batch_size), t])) / batch_size


def softmax(x):
	if x.ndim == 2:
		x = x.T
		x -= np.max(x, axis=0)
		y = np.exp(x) / np.sum(np.exp(x), axis=0)
		return y.T

	x -= np.max(x)
	return np.exp(x) / np.sum(np.exp(x))