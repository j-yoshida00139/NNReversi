from .layer import *
import numpy as np
import pickle
import math
import os


class Network(object):
	def __init__(
			self,
			input_dim=(3, 8, 8),
			conv_params=(
					{'filter_num': 16, 'filter_size': 4, 'pad': 2, 'stride': 1},
					{'filter_num': 16, 'filter_size': 4, 'pad': 2, 'stride': 1},
					{'filter_num': 32, 'filter_size': 4, 'pad': 2, 'stride': 1},
					{'filter_num': 32, 'filter_size': 4, 'pad': 2, 'stride': 1},
					{'filter_num': 64, 'filter_size': 4, 'pad': 2, 'stride': 1},
					{'filter_num': 64, 'filter_size': 2, 'pad': 1, 'stride': 1}),
			affine_params=(100, 64)):  # hidden_size=100, output_size=100

		# declare layers ===========
		self.layers = []
		self.layers.append(Convolution())
		self.layers.append(Relu())
		self.layers.append(Convolution())
		self.layers.append(Relu())
		self.layers.append(Convolution())
		self.layers.append(Relu())
		self.layers.append(Convolution())
		self.layers.append(Relu())
		self.layers.append(Convolution())
		self.layers.append(Relu())
		self.layers.append(Convolution())
		self.layers.append(Relu())
		self.layers.append(AffineLayer())
		self.layers.append(Relu())
		self.layers.append(AffineLayer())
		self.last_layer = SoftmaxCrossEntropyLayer()
		self.params = {}

		if os.path.exists("params.pkl"):
			self.load_params()
		else:
			self.init_params(input_dim, conv_params, affine_params)
			raise BaseException("No params.pkl")

		prm_idx = 0
		conv_iter = iter(conv_params)
		for layer in self.layers:
			if isinstance(layer, Convolution):
				conv_param = next(conv_iter)
				layer.set_params(
					self.params['W' + str(prm_idx + 1)], self.params['b' + str(prm_idx + 1)], conv_param['stride'], conv_param['pad'])
				prm_idx += 1
			elif isinstance(layer, Pooling):
				layer.set_params(pool_h=2, pool_w=2, stride=2)
			elif isinstance(layer, AffineLayer):
				layer.set_params(self.params['W' + str(prm_idx + 1)], self.params['b' + str(prm_idx + 1)])
				prm_idx += 1

	def feed_forward(self, x, train_flg=False):
		for layer in self.layers:
			if isinstance(layer, Dropout):
				x = layer.forward(x, train_flg)
			else:
				x = layer.forward(x)
		return x

	def loss(self, x, t):
		y = self.feed_forward(x, train_flg=True)
		return self.last_layer.forward(y, t)

	def accuracy(self, x, t, batch_size=100):
		if t.ndim != 1:
			t = np.argmax(t, axis=1)
		acc = 0.0

		for i in range(int(x.shape[0] / batch_size)):
			tx = x[i*batch_size:(i+1)*batch_size]
			tt = t[i*batch_size:(i+1)*batch_size]
			y = self.feed_forward(tx, train_flg=False)
			y = np.argmax(y, axis=1)
			acc += np.sum(y == tt)

		return acc / x.shape[0]

	def gradient(self, x, t):
		# forward
		self.loss(x, t)

		# backward
		d_out = 1
		d_out = self.last_layer.backward(d_out)

		tmp_layers = self.layers.copy()
		tmp_layers.reverse()
		for layer in tmp_layers:
			d_out = layer.backward(d_out)

		# 設定
		grads = {}
		i = 1
		for layer in self.layers:
			if isinstance(layer, Convolution) or isinstance(layer, AffineLayer):
				grads['W' + str(i)] = layer.dW
				grads['b' + str(i)] = layer.db
				i += 1

		return grads

	def init_params(self, input_dim, conv_params, affine_params):
		self.params = {}
		prm_idx = 0
		pre_channel, pre_height, pre_width = input_dim
		affine_iter, conv_iter = iter(affine_params), iter(conv_params)
		for layer in self.layers:
			if isinstance(layer, Relu) or isinstance(layer, Dropout):
				continue

			if isinstance(layer, Convolution):
				conv_param = next(conv_iter)
				conn_to_pre_layer = pre_channel * (conv_param['filter_size'] ** 2)
				weight_init_scale = math.sqrt(2.0 / conn_to_pre_layer)
				self.params['W' + str(prm_idx + 1)] =\
					weight_init_scale * np.random.randn(
						conv_param['filter_num'],
						pre_channel,
						conv_param['filter_size'],
						conv_param['filter_size']
					)
				self.params['b' + str(prm_idx + 1)] = np.zeros(conv_param['filter_num'])
				FN, _C, FH, FW = self.params['W' + str(prm_idx + 1)].shape
				height = int((pre_height + 2 * conv_param['pad'] - (FH - 1)) / conv_param['stride'])
				width = int((pre_width + 2 * conv_param['pad'] - (FW - 1)) / conv_param['stride'])
				pre_channel, pre_height, pre_width = FN, height, width

			elif isinstance(layer, Pooling):  # no parameter
				height = int((pre_height + self.pad * 2) / self.stride)
				width = int((pre_width + self.pad * 2) / self.stride)
				pre_channel, pre_height, pre_width = pre_channel, height, width

			elif isinstance(layer, AffineLayer):
				affine_param = next(affine_iter)
				conn_to_pre_layer = pre_channel * pre_height * pre_width
				weight_init_scale = math.sqrt(2.0 / conn_to_pre_layer)

				self.params['W' + str(prm_idx + 1)] = weight_init_scale * np.random.randn(
					pre_channel * pre_height * pre_width, affine_param)
				self.params['b' + str(prm_idx + 1)] = np.zeros(affine_param)
				FN = self.params['b' + str(prm_idx + 1)].shape[0]
				height, width = 1, 1
				pre_channel, pre_height, pre_width = FN, height, width

			prm_idx = prm_idx + 1 if not(isinstance(layer, Pooling)) else prm_idx

	def save_params(self, file_name="params.pkl"):
		params = {}
		for key, val in self.params.items():
			params[key] = val
		with open(file_name, 'wb') as f:
			pickle.dump(params, f)

	def load_params(self, file_name="params.pkl"):
		self.params = {}
		with open(file_name, 'rb') as f:
			params = pickle.load(f)
		for key, val in params.items():
			self.params[key] = val

		idx = 0
		for layer in self.layers:
			if isinstance(layer, Convolution) or isinstance(layer, AffineLayer):
				layer.W = self.params['W' + str(idx + 1)]
				layer.b = self.params['b' + str(idx + 1)]
				idx += 1
