from collections import OrderedDict
from layer import *
import numpy as np
import pickle
import math

class Network(object):
	def __init__(self, input_dim=(3, 8, 8),
				convParams = [{'filter_num':16, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':16, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':32, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':32, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':64, 'filter_size':4, 'pad':2, 'stride':1},
								{'filter_num':64, 'filter_size':2, 'pad':1, 'stride':1}],
				affineParams = [100, 64]):  #hidden_size=100, output_size=100

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
		prmIdx = 0
		pre_channel, pre_height, pre_width = input_dim
		affine_iter, conv_iter = iter(affineParams), iter(convParams)
		for layer in self.layers:
			if isinstance(layer, Relu):
				continue

			if isinstance(layer, Convolution):
				convParam = next(conv_iter)
				conn_to_pre_layer = pre_channel * (convParam['filter_size'] ** 2)
				weight_init_scale = math.sqrt(2.0 / conn_to_pre_layer)
				self.params['W' + str(prmIdx + 1)] = weight_init_scale * \
								np.random.randn(convParam['filter_num'], pre_channel,
								                convParam['filter_size'], convParam['filter_size'])
				self.params['b' + str(prmIdx + 1)] = np.zeros(convParam['filter_num'])
				layer.setParams(self.params['W' + str(prmIdx + 1)], self.params['b' + str(prmIdx + 1)], convParam['stride'], convParam['pad'], pre_height, pre_width)

			elif isinstance(layer, Pooling): # no parameter
				layer.setParams(pool_h=2, pool_w=2, stride=2, C=pre_channel, pre_height=pre_height, pre_width=pre_width)

			elif isinstance(layer, AffineLayer):
				affineParam = next(affine_iter)
				conn_to_pre_layer = pre_channel * pre_height * pre_width
				weight_init_scale = math.sqrt(2.0 / conn_to_pre_layer)
				self.params['W' + str(prmIdx + 1)] = weight_init_scale * np.random.randn(pre_channel * pre_height * pre_width, affineParam)
				self.params['b' + str(prmIdx + 1)] = np.zeros(affineParam)
				layer.setParams(self.params['W' + str(prmIdx + 1)], self.params['b' + str(prmIdx + 1)])

			pre_channel, pre_height, pre_width = layer.FN, layer.height, layer.width
			prmIdx = prmIdx + 1 if not(isinstance(layer, Pooling)) else prmIdx

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

	def save_params(self, file_name="params.pkl"):
		params = {}
		for key, val in self.params.items():
			params[key] = val
		with open(file_name, 'wb') as f:
			pickle.dump(params, f)

	def load_params(self, file_name="params.pkl"):
		with open(file_name, 'rb') as f:
			params = pickle.load(f)
		for key, val in params.items():
			self.params[key] = val

		for i, layer_idx in enumerate((0, 2, 5, 7, 10, 12, 15, 18)):
			self.layers[layer_idx].W = self.params['W' + str(i+1)]
			self.layers[layer_idx].b = self.params['b' + str(i+1)]

