"""
move_loader
~~~~~~~~~~~~
A library to load the move data of reversi.
"""

import random
import math
import numpy as np
from personal import dbmanager


def load_data(batch_size, flatten=True):
	"""
	training_data : number of elements is same as the number of sample
					each element has 2 child elements
					1st one is the arrangement of the pieces
					2nd one is the next move for the arrangement
	validation_data, test_data : same structure as training_data
	"""

	n_total = batch_size
	n_training = math.floor(batch_size*0.8)
	n_validation = math.floor(batch_size*0.1)
	n_test = math.floor(batch_size*0.1)
	x_train_tmp, t_train, x_eva_tmp, t_eva, x_test_tmp, t_test = get_random_data(n_training, n_validation, n_test, n_total)
	if flatten is False:
		x_train = np.array([])
		for data in x_train_tmp:
			tmp_data = np.array([])
			tmp_data = np.append(tmp_data, np.array([data[x] for x in range(0, 192, 3)]).reshape(8, 8))
			tmp_data = np.append(tmp_data, np.array([data[x] for x in range(1, 192, 3)]).reshape(8, 8))
			tmp_data = np.append(tmp_data, np.array([data[x] for x in range(2, 192, 3)]).reshape(8, 8))
			x_train = np.append(x_train, tmp_data)
		x_train = x_train.reshape(len(x_train_tmp), 3, 8, 8)
		x_eva = np.array([])
		for data in x_eva_tmp:
			tmp_data = np.array([])
			tmp_data = np.append(tmp_data, np.array([data[x] for x in range(0, 192, 3)]).reshape(8, 8))
			tmp_data = np.append(tmp_data, np.array([data[x] for x in range(1, 192, 3)]).reshape(8, 8))
			tmp_data = np.append(tmp_data, np.array([data[x] for x in range(2, 192, 3)]).reshape(8, 8))
			x_eva = np.append(x_eva, tmp_data)
		x_eva = x_eva.reshape(len(x_eva_tmp), 3, 8, 8)
		x_test = np.array([])
		for data in x_test_tmp:
			tmp_data = np.array([])
			tmp_data = np.append(tmp_data, np.array([data[x] for x in range(0, 192, 3)]).reshape(8, 8))
			tmp_data = np.append(tmp_data, np.array([data[x] for x in range(1, 192, 3)]).reshape(8, 8))
			tmp_data = np.append(tmp_data, np.array([data[x] for x in range(2, 192, 3)]).reshape(8, 8))
			x_test = np.append(x_test, tmp_data)
		x_test = x_test.reshape(len(x_test_tmp), 3, 8, 8)
	else:
		x_train, x_eva, x_test = x_train_tmp, x_eva_tmp, x_test_tmp

	return x_train, t_train, x_eva, t_eva, x_test, t_test


def get_random_data(n_training, n_validation, n_test, n_total):
	num_list = list(range(n_total))
	random.shuffle(num_list)
	num_training_list = num_list[0: n_training]
	num_validation_list = num_list[n_training: n_training+n_validation]
	num_test_list = num_list[n_training+n_validation: n_training+n_validation+n_test]

	x_train, t_train = dbmanager.extract_nn_data_by_indices(num_training_list)
	x_eva, t_eva = dbmanager.extract_nn_data_by_indices(num_validation_list)
	x_test, t_test = dbmanager.extract_nn_data_by_indices(num_test_list)

	return x_train, t_train, x_eva, t_eva, x_test, t_test
