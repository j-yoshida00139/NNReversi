import numpy as np
from personal.utils import mathFunc
from personal.utils.util import im2col, col2im


class AffineLayer(object):
	def __init__(self):
		self.w = None
		self.b = None
		self.x = None
		self.original_x_shape = None
		self.dw = None
		self.db = None
		self.dW = None

	def set_params(self, w, b):
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

		out = np.dot(self.x, self.w) + self.b
		return out

	def backward(self, d_out):
		dx = np.dot(d_out, self.w.T)
		self.dW = np.dot(self.x.T, d_out)
		self.db = np.sum(d_out, axis=0)

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

	def backward(self, d_out):
		d_out[self.mask] = 0
		dx = d_out

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
		self.loss = mathFunc.cross_entropy_loss(self.y, self.t)
		return self.loss

	def backward(self, d_out=1):
		batch_size = self.t.shape[0]
		if self.t.size == self.y.size:
			dx = (self.y - self.t) / batch_size
		else:
			dx = self.y.copy()
			dx[np.arange(batch_size), self.t] -= 1
			dx = dx / batch_size

		return dx


class Dropout:
	"""
	http://arxiv.org/abs/1207.0580
	"""

	def __init__(self, dropout_ratio=0.5):
		self.dropout_ratio = dropout_ratio
		self.mask = None

	def forward(self, x, train_flg=True):
		if train_flg:
			self.mask = np.random.rand(*x.shape) > self.dropout_ratio
			return x * self.mask
		else:
			return x * (1.0 - self.dropout_ratio)

	def backward(self, dout):
		return dout * self.mask


class BatchNormalization:
	"""
	http://arxiv.org/abs/1502.03167
	"""

	def __init__(self, gamma, beta, momentum=0.9, running_mean=None, running_var=None):
		self.gamma = gamma
		self.beta = beta
		self.momentum = momentum
		self.input_shape = None  # Conv層の場合は4次元、全結合層の場合は2次元

		# テスト時に使用する平均と分散
		self.running_mean = running_mean
		self.running_var = running_var

		# backward時に使用する中間データ
		self.batch_size = None
		self.xc = None
		self.std = None
		self.d_gamma = None
		self.d_beta = None

	def forward(self, x, train_flg=True):
		self.input_shape = x.shape
		if x.ndim != 2:
			N, C, H, W = x.shape
			x = x.reshape(N, -1)

		out = self.__forward(x, train_flg)

		return out.reshape(*self.input_shape)

	def __forward(self, x, train_flg):
		if self.running_mean is None:
			N, D = x.shape
			self.running_mean = np.zeros(D)
			self.running_var = np.zeros(D)

		if train_flg:
			mu = x.mean(axis=0)
			xc = x - mu
			var = np.mean(xc ** 2, axis=0)
			std = np.sqrt(var + 10e-7)
			xn = xc / std

			self.batch_size = x.shape[0]
			self.xc = xc
			self.xn = xn
			self.std = std
			self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * mu
			self.running_var = self.momentum * self.running_var + (1 - self.momentum) * var
		else:
			xc = x - self.running_mean
			xn = xc / (np.sqrt(self.running_var + 10e-7))

		out = self.gamma * xn + self.beta
		return out

	def backward(self, d_out):
		if d_out.ndim != 2:
			N, C, H, W = d_out.shape
			d_out = d_out.reshape(N, -1)

		dx = self.__backward(d_out)

		dx = dx.reshape(*self.input_shape)
		return dx

	def __backward(self, d_out):
		d_beta = d_out.sum(axis=0)
		d_gamma = np.sum(self.xn * d_out, axis=0)
		dxn = self.gamma * d_out
		dxc = dxn / self.std
		d_std = -np.sum((dxn * self.xc) / (self.std * self.std), axis=0)
		d_var = 0.5 * d_std / self.std
		dxc += (2.0 / self.batch_size) * self.xc * d_var
		dmu = np.sum(dxc, axis=0)
		dx = dxc - dmu / self.batch_size

		self.d_gamma = d_gamma
		self.d_beta = d_beta

		return dx


class Convolution:
	def __init__(self):
		self.W = None
		self.b = None
		self.stride = None
		self.pad = None
		self.x = None
		self.col = None
		self.col_W = None
		self.dW = None
		self.db = None

	def set_params(self, W, b, stride=1, pad=0):
		self.W = W
		self.b = b
		self.stride = stride
		self.pad = pad

		# 中間データ（backward時に使用）
		self.x = None
		self.col = None
		self.col_W = None

		# 重み・バイアスパラメータの勾配
		self.dW = None
		self.db = None

	def forward(self, x):
		FN, C, FH, FW = self.W.shape
		N, C, H, W = x.shape
		out_h = 1 + int((H + 2 * self.pad - FH) / self.stride)
		out_w = 1 + int((W + 2 * self.pad - FW) / self.stride)

		col = im2col(x, FH, FW, self.stride, self.pad)
		col_W = self.W.reshape(FN, -1).T

		out = np.dot(col, col_W) + self.b
		out = out.reshape(N, out_h, out_w, -1).transpose(0, 3, 1, 2)

		self.x = x
		self.col = col
		self.col_W = col_W

		return out

	def backward(self, d_out):
		FN, C, FH, FW = self.W.shape
		d_out = d_out.transpose(0, 2, 3, 1).reshape(-1, FN)

		self.db = np.sum(d_out, axis=0)
		self.dW = np.dot(self.col.T, d_out)
		self.dW = self.dW.transpose(1, 0).reshape(FN, C, FH, FW)

		d_col = np.dot(d_out, self.col_W.T)
		dx = col2im(d_col, self.x.shape, FH, FW, self.stride, self.pad)

		return dx


class Pooling:
	def __init__(self):
		self.pool_h = None
		self.pool_w = None
		self.stride = None
		self.pad = None
		self.x = None
		self.arg_max = None

	def set_params(self, pool_h, pool_w, stride=1, pad=0):
		self.pool_h = pool_h
		self.pool_w = pool_w
		self.stride = stride
		self.pad = pad

		self.x = None
		self.arg_max = None

	def forward(self, x):
		N, C, H, W = x.shape
		out_h = int(1 + (H - self.pool_h) / self.stride)
		out_w = int(1 + (W - self.pool_w) / self.stride)

		col = im2col(x, self.pool_h, self.pool_w, self.stride, self.pad)
		col = col.reshape(-1, self.pool_h * self.pool_w)

		arg_max = np.argmax(col, axis=1)
		out = np.max(col, axis=1)
		out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)

		self.x = x
		self.arg_max = arg_max

		return out

	def backward(self, d_out):
		d_out = d_out.transpose(0, 2, 3, 1)

		pool_size = self.pool_h * self.pool_w
		d_max = np.zeros((d_out.size, pool_size))
		d_max[np.arange(self.arg_max.size), self.arg_max.flatten()] = d_out.flatten()
		d_max = d_max.reshape(d_out.shape + (pool_size,))

		d_col = d_max.reshape(d_max.shape[0] * d_max.shape[1] * d_max.shape[2], -1)
		dx = col2im(d_col, self.x.shape, self.pool_h, self.pool_w, self.stride, self.pad)

		return dx
