import numpy as np


def sigmoid(z):
	return 1.0/(1.0+np.exp(-z))


def sigmoid_prime(z):
	return sigmoid(z)*(1-sigmoid(z))


def cross_entropy_loss(y, t):
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


def base_10_to_n_str(x, n):
	if int(x / n):
		return base_10_to_n_str(int(x / n), n) + str(x % n)
	return str(x % n)


def base_10_to_n(x, n):
	return int(base_10_to_n_str(x, n))
