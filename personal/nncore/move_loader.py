"""
move_loader
~~~~~~~~~~~~
A library to load the move data of reversi.
"""

#### Libraries
import random
import math
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import dbmanager

def load_data(batch_size):
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
    x_train, t_train, x_eva, t_eva, x_test, t_test = get_random_data(n_training, n_validation, n_test, n_total)
    return (x_train, t_train, x_eva, t_eva, x_test, t_test)

def get_random_data(n_training, n_validation, n_test, n_total):
    num_list = list(range(n_total))
    random.shuffle(num_list)
    num_training_list   = num_list[0                       : n_training                    ]
    num_validation_list = num_list[n_training              : n_training+n_validation       ]
    num_test_list       = num_list[n_training+n_validation : n_training+n_validation+n_test]

    x_train, t_train = dbmanager.get_data_by_list(num_training_list)
    x_eva, t_eva     = dbmanager.get_data_by_list(num_validation_list)
    x_test, t_test   = dbmanager.get_data_by_list(num_test_list)

    return (x_train, t_train, x_eva, t_eva, x_test, t_test)

