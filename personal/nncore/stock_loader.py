"""
stock_loader
~~~~~~~~~~~~
A library to load the stock price data.
The data from ruby jpstock script.
"""

#### Libraries
# Standard library
import cPickle
import gzip
import zipfile
import random
# Third-party libraries
import numpy as np

def load_data():
    """
    training_data : number of elements is the number of sample
                    each element has 2 child elements
                    1st one is the stock prices for each day
                    2nd one is the stock prices of next year
    validation_data, test_data : same structure as training_data
    """
    n_total = 35000
    n_training = 10000
    n_validation = 1000
    n_test = 1000
    training_data, validation_data, test_data = get_random_data(n_training, n_validation, n_test, n_total)
    return (training_data, validation_data, test_data)

def get_random_data(n_training, n_validation, n_test, n_total):
    zf = zipfile.ZipFile('sample.zip', 'r')
    num_list = range(n_total)
    random.shuffle(num_list)
    num_training_list   = num_list[0                       : n_training                    ]
    num_validation_list = num_list[n_training              : n_training+n_validation       ]
    num_test_list       = num_list[n_training+n_validation : n_training+n_validation+n_test]
    
    training_data   = get_data_by_list(num_training_list, zf)
    validation_data = get_data_by_list(num_validation_list, zf)
    test_data       = get_data_by_list(num_test_list, zf)
    zf.close()

    return (training_data, validation_data, test_data)


def get_data_by_list(n_list, zf):
    inputs  = []
    results = []
    for i in n_list:
        file_no     = "{0:08d}".format(i+1)
        input_data  = load_from_file('sample_output/input_raw_'+file_no+'.csv', zf)
        input_ave   = sum(input_data) / float(len(input_data))
        result_data = load_from_file('sample_output/input_ave_'+file_no+'.csv', zf)
        result_data = [float(x)/(2.0*input_ave) if (float(x)/(2.0*input_ave)<0.95 and float(x)/(2.0*input_ave)>0.05)
                        else (0.95 if float(x)/(2.0*input_ave)>0.95 else 0.05) for x in result_data]
        inputs.append(input_data)
        results.append(result_data)

    inputs = [np.reshape(x, (366, 1)) for x in inputs]
    results = [np.reshape(x, (12, 1)) for x in results]
    return zip(inputs, results)

def load_from_file(fileName, zf):
    outArray = []
    with zf.open(fileName) as sample:
        for line in sample:
            outArray.append(float(line))
    return outArray

