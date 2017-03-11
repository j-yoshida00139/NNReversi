from layer import *
import numpy as np
import pickle
import math, os

class Network(object):
	def __init__(self, input_dim=(3, 8, 8),
				convParams = ({'filter_num':16, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':16, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':32, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':32, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':64, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':64, 'filter_size':2, 'pad':1, 'stride':1}),
				affineParams = (100, 64)):  #hidden_size=100, output_size=100

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

		if os.path.exists("params.pkl"):
			self.load_params()
		else:
			self.initParams(input_dim, convParams, affineParams)

		prmIdx = 0
		conv_iter = iter(convParams)
		for layer in self.layers:
			if isinstance(layer, Convolution):
				convParam = next(conv_iter)
				layer.setParams(self.params['W' + str(prmIdx + 1)], self.params['b' + str(prmIdx + 1)], convParam['stride'], convParam['pad'])
				prmIdx += 1
			elif isinstance(layer, Pooling):
				layer.setParams(pool_h=2, pool_w=2, stride=2)
			elif isinstance(layer, AffineLayer):
				layer.setParams(self.params['W' + str(prmIdx + 1)], self.params['b' + str(prmIdx + 1)])
				prmIdx += 1

	def feedforward(self, x, train_flg=False):
		for layer in self.layers:
			if isinstance(layer, Dropout):
				x = layer.forward(x, train_flg)
			else:
				x = layer.forward(x)
		return x

	def loss(self, x, t):
		y = self.feedforward(x, train_flg=True)
		return self.last_layer.forward(y, t)

	def accuracy(self, x, t, batch_size=100):
		if t.ndim != 1 : t = np.argmax(t, axis=1)

		acc = 0.0

		for i in range(int(x.shape[0] / batch_size)):
			tx = x[i*batch_size:(i+1)*batch_size]
			tt = t[i*batch_size:(i+1)*batch_size]
			y = self.feedforward(tx, train_flg=False)
			y = np.argmax(y, axis=1)
			acc += np.sum(y == tt)

		return acc / x.shape[0]

	def gradient(self, x, t):
		# forward
		self.loss(x, t)

		# backward
		dout = 1
		dout = self.last_layer.backward(dout)

		tmp_layers = self.layers.copy()
		tmp_layers.reverse()
		for layer in tmp_layers:
			dout = layer.backward(dout)

		# 設定
		grads = {}
		i = 1
		for layer in self.layers:
			if isinstance(layer, Convolution) or isinstance(layer, AffineLayer):
				grads['W' + str(i)] = layer.dW
				grads['b' + str(i)] = layer.db
				i += 1

		return grads

	def initParams(self, input_dim, convParams, affineParams):
		self.params = {}
		prmIdx = 0
		pre_channel, pre_height, pre_width = input_dim
		affine_iter, conv_iter = iter(affineParams), iter(convParams)
		for layer in self.layers:
			if isinstance(layer, Relu) or isinstance(layer, Dropout):
				continue

			if isinstance(layer, Convolution):
				convParam = next(conv_iter)
				conn_to_pre_layer = pre_channel * (convParam['filter_size'] ** 2)
				weight_init_scale = math.sqrt(2.0 / conn_to_pre_layer)
				self.params['W' + str(prmIdx + 1)] = weight_init_scale * \
								np.random.randn(convParam['filter_num'], pre_channel,
												convParam['filter_size'], convParam['filter_size'])
				self.params['b' + str(prmIdx + 1)] = np.zeros(convParam['filter_num'])
				FN, _C, FH, FW = self.params['W' + str(prmIdx + 1)].shape
				height = int((pre_height + 2 * convParam['pad'] - (FH - 1)) / convParam['stride'])
				width  = int((pre_width  + 2 * convParam['pad'] - (FW - 1)) / convParam['stride'])
				pre_channel, pre_height, pre_width = FN, height, width

			elif isinstance(layer, Pooling): # no parameter
				height = int((pre_height + self.pad * 2) / self.stride)
				width  = int((pre_width  + self.pad * 2) / self.stride)
				pre_channel, pre_height, pre_width = pre_channel, height, width

			elif isinstance(layer, AffineLayer):
				affineParam = next(affine_iter)
				conn_to_pre_layer = pre_channel * pre_height * pre_width
				weight_init_scale = math.sqrt(2.0 / conn_to_pre_layer)

				self.params['W' + str(prmIdx + 1)] = weight_init_scale * np.random.randn(pre_channel * pre_height * pre_width, affineParam)
				self.params['b' + str(prmIdx + 1)] = np.zeros(affineParam)
				FN = self.params['b' + str(prmIdx + 1)].shape[0]
				height, width = 1, 1
				pre_channel, pre_height, pre_width = FN, height, width

			prmIdx = prmIdx + 1 if not(isinstance(layer, Pooling)) else prmIdx


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

