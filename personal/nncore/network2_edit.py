#### Libraries
# Standard library
import json
import random
from collections import OrderedDict

# Third-party libraries
import numpy as np

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
		self.original_x_shape = np.array(x).shape
		#x = x.reshape(x.shape[0], -1)
		#self.x = x
		self.x = np.array(x).reshape(len(x), len(x[0]))
		#self.w = np.array(self.w).reshape(len(self.w), len(self.w[0]))
		#self.b = np.array(self.b).reshape(1, len(self.b))
		out = np.dot(self.x, self.w) + self.b
		return out

	def backward(self, dout):
		dx = np.dot(dout, self.w.T)
		self.dW = np.dot(self.x.T, dout)
		self.db = np.sum(dout, axis=0)

		dx = dx.reshape(*self.original_x_shape)
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
		self.t = np.array(t)
		self.y = softmax(x)
		self.loss = crossEntropyLoss(self.y, self.t)
		return self.loss

	def backward(self, dout=1):
		batch_size = self.t.shape[0]
		if self.t.size == self.y.size:
			self.t = self.t.reshape(len(self.t), len(self.t[0]))
			self.y = self.y.reshape(len(self.y), len(self.y[0]))
			#dx = (self.y - self.t) / batch_size
			dx = (self.y - self.t)
		else:
			dx = self.y.copy()
			dx[np.arange(batch_size), self.t] -= 1
			#dx = dx / batch_size

		return dx


#### Main Network class
class Network(object):

	def __init__(self, sizes, cost=CrossEntropyCost):
		self.num_layers = len(sizes)
		self.sizes = sizes
		self.default_weight_initializer()
		self.sizes, self.weights, self.biases = lr_loader.load_data(sizes)
		self.weights[0] = self.weights[0].T
		self.weights[1] = self.weights[1].T
		self.biases[0] = np.array(self.biases[0]).reshape(len(self.biases[0]))
		self.biases[1] = np.array(self.biases[1]).reshape(len(self.biases[1]))
		self.cost=cost

		self.layers = OrderedDict()
		self.layers['Affine1'] = AffineLayer(self.weights[0], self.biases[0])
		self.layers['Sigmoid1'] = SigmoidLayer()
		self.layers['Affine2'] = AffineLayer(self.weights[1], self.biases[1])
		self.layers['Sigmoid2'] = SigmoidLayer()
		self.lastLayer = SoftmaxCrossEntropyLayer()

	def loss(self, x, t):
		y = self.feedforward(x)
		return self.lastLayer.forward(y, t)

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

	def default_weight_initializer(self):
		self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
		self.weights = [np.random.randn(y, x)/np.sqrt(x)
						for x, y in zip(self.sizes[:-1], self.sizes[1:])]

	def large_weight_initializer(self):
		self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
		self.weights = [np.random.randn(y, x)
						for x, y in zip(self.sizes[:-1], self.sizes[1:])]

	def feedforward(self, x):
		for layer in self.layers.values():
			x = layer.forward(x)
		return x

	def SGD(self, training_data, epochs, mini_batch_size, eta,
			lmbda = 0.0,
			evaluation_data=None,
			monitor_evaluation_cost=False,
			monitor_evaluation_accuracy=False,
			monitor_training_cost=False,
			monitor_training_accuracy=False):
		if evaluation_data: n_data = len(evaluation_data)
		n = len(training_data)
		evaluation_cost, evaluation_accuracy = [], []
		training_cost, training_accuracy = [], []
		for j in range(epochs):
			random.shuffle(training_data)
			mini_batches = [
				training_data[k:k+mini_batch_size]
				for k in range(0, n, mini_batch_size)]
			for mini_batch in mini_batches:
				self.update_mini_batch(
					mini_batch, eta, lmbda, len(training_data))
			print("Epoch %s training complete" % j)
			if monitor_training_cost:
				cost = self.total_cost(training_data, lmbda)
				training_cost.append(cost)
				print("Cost on training data      : {0:8f}".format(cost))
			if monitor_evaluation_cost:
				cost = self.total_cost(evaluation_data, lmbda)
				evaluation_cost.append(cost)
				print("Cost on evaluation data    : {0:8f}".format(cost))
			if monitor_training_accuracy:
				accuracy = self.accuracy(training_data)
				training_accuracy.append(accuracy)
				print("Accuracy on training data  : {0:8f}".format(
					accuracy))
			if monitor_evaluation_accuracy:
				accuracy = self.accuracy(evaluation_data)
				evaluation_accuracy.append(accuracy)
				print("Accuracy on evaluation data: {0:8f}".format(
					self.accuracy(evaluation_data)))
		lr_loader.store_result(self.sizes, self.weights, self.biases)

	def update_mini_batch(self, mini_batch, eta, lmbda, n):
		#nabla_b = [np.zeros(b.shape) for b in self.biases]
		#nabla_w = [np.zeros(w.shape) for w in self.weights]
		#for x, y in mini_batch:
		#	delta_nabla_b, delta_nabla_w = self.backprop(x, y)
		#	nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
		#	nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
		#self.weights = [(1-eta*(lmbda/n))*w-(eta/len(mini_batch))*nw
		#				for w, nw in zip(self.weights, nabla_w)]
		#self.biases = [b-(eta/len(mini_batch))*nb
		#			   for b, nb in zip(self.biases, nabla_b)]

		x_batch, t_batch = [], []
		for n in mini_batch:
			x_batch.append(np.array(n[0]))
		for n in mini_batch:
			t_batch.append(np.array(n[1]))

		#x_batch = x_batch.reshape(len(x_batch), len(x_batch[0]))
		#t_batch = t_batch.reshape(len(t_batch))

		grad = self.gradient(x_batch, t_batch)

		self.weights[0] -= eta * grad['W1'] / len(mini_batch)
		self.weights[1] -= eta * grad['W2'] / len(mini_batch)
		self.biases[0]  -= eta * grad['b1'] / len(mini_batch)
		self.biases[1]  -= eta * grad['b2'] / len(mini_batch)

	def backprop(self, x, y):
		nabla_b = [np.zeros(b.shape) for b in self.biases]
		nabla_w = [np.zeros(w.shape) for w in self.weights]
		# feedforward
		activation = x
		activations = [x] # list to store all the activations, layer by layer
		zs = [] # list to store all the z vectors, layer by layer
		for b, w in zip(self.biases, self.weights):
			z = np.dot(w, activation)+b
			zs.append(z)
			activation = sigmoid(z)
			activations.append(activation)
		# backward pass
		delta = (self.cost).delta(zs[-1], activations[-1], y)
		nabla_b[-1] = delta
		nabla_w[-1] = np.dot(delta, activations[-2].transpose())
		for l in range(2, self.num_layers):
			z = zs[-l]
			sp = sigmoid_prime(z)
			delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
			nabla_b[-l] = delta
			nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())

		# nabla_b[0] size100, nabla_b[1] size64
		# nabla_w[0] size100x192, nabla_w[1] size64x100
		# y:answer, x:input

		# bnparray =

		return (nabla_b, nabla_w)

	def accuracy(self, data, convert=False):
		results = [(self.feedforward(x.reshape(1, len(x))), y) for (x, y) in data]
		sum_correct = 0
		for result in results:
			i_idx, o_idx = np.argmax(result[0]), np.argmax(result[1])
			sum_correct += 1 if i_idx == o_idx else 0
		return sum_correct * 100.0 / len(results)

	def total_cost(self, data, lmbda, convert=False):
		cost = 0.0
		for x, y in data:
			a = self.feedforward(x.reshape(1, len(x)))
			if convert: y = vectorized_result(y)
			cost += self.cost.fn(a, y)/len(data)
		cost += 0.5*(lmbda/len(data))*sum(
			np.linalg.norm(w)**2 for w in self.weights)
		return cost

	def save(self, filename):
		"""Save the neural network to the file ``filename``."""
		"""data = {"sizes": self.sizes,
				"weights": [w.tolist() for w in self.weights],
				"biases": [b.tolist() for b in self.biases],
				"cost": str(self.cost.__name__)}"""
		data = {"sizes": self.sizes,
				"weights": [w.tolist() for w in self.weights],
				"biases": [b.tolist() for b in self.biases]}
		f = open(filename, "w")
		json.dump(data, f)
		f.close()

#### Loading a Network
def load(filename):
	f = open(filename, "r")
	data = json.load(f)
	f.close()
	net = Network(data["sizes"])
	net.weights = [np.array(w) for w in data["weights"]]
	net.biases = [np.array(b) for b in data["biases"]]
	return net

#### Miscellaneous functions
def vectorized_result(j):
	e = np.zeros((10, 1))
	e[j] = 1.0
	return e

def sigmoid(z):
	return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
	return sigmoid(z)*(1-sigmoid(z))

def crossEntropyLoss(y, t):
	if y.ndim == 1:
		t = t.reshape(1, t.size)
		y = y.reshape(1, y.size)

	t = np.array(t)

	if t.size == y.size:
		t = t.argmax(axis=1)

	batch_size = y.shape[0]
	#return -np.sum(np.log(y[np.arrange(batch_size), t])) / batch_size
	return -np.sum(np.log(y[np.arange(batch_size), t]))


def softmax(x):
	if x.ndim == 2:
		x = x.T
		x = x - np.max(x, axis=0)
		y = np.exp(x) / np.sum(np.exp(x), axis=0)
		return y.T

	x = x - np.max(x)
	return np.exp(x) / np.sum(np.exp(x))