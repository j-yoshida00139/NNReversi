import sys, os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir) + '/utils')
import mathFunc

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
		out = mathFunc.sigmoid(x)
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
		self.y = mathFunc.softmax(x)
		self.loss = mathFunc.crossEntropyLoss(self.y, self.t)
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