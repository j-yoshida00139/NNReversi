import os.path
import numpy as np
import pickle


def load_data(sizesArg):
	fileName = 'sizes.dump'
	if (os.path.exists(fileName)):
		with open(fileName, "rb") as f:
			sizes = pickle.load(f)
	else:
		sizes = sizesArg

	fileName = 'weights.dump'
	if os.path.exists(fileName):
		with open(fileName, "rb") as f:
			weights = pickle.load(f)
			#isSamesize = True
			#for x, y, i in zip(sizes[:-1], sizes[1:], range(len(sizes)-1)):
			#	if (len(weights[i]) != x) or (len(weights[i+1]) != y):
			#		isSamesize = False
			#if isSamesize == False:
			#	weights = [np.random.randn(x, y) for x, y in zip(sizes[:-1], sizes[1:])]
	else:
		weights = [0.01 * np.random.randn(x, y) for x, y in zip(sizes[:-1], sizes[1:])]

	fileName = 'biases.dump'
	if os.path.exists(fileName):
		with open(fileName, "rb") as f:
			biases = pickle.load(f)
			#isSamesize = True
			#for x, y, i in zip(sizes[:-1], sizes[1:], range(len(sizes)-1)):
			#	if (len(weights[i]) != x) or (len(weights[i+1]) != y):
			#		isSamesize = False
			#if isSamesize == False:
			#	biases = [np.random.randn(y, 1) for y in sizes[1:]]
	else:
		#biases = [np.random.randn(y, 1) for y in sizes[1:]]
		biases = [np.zeros(sizes[1])]
		biases.append(np.zeros(sizes[2]))

	return (sizes, weights, biases)


def store_result(sizes, weights, biases):
	with open("sizes.dump", "wb") as f:
		pickle.dump(sizes, f)
	with open("weights.dump", "wb") as f:
		pickle.dump(weights, f)
	with open("biases.dump", "wb") as f:
		pickle.dump(biases, f)
