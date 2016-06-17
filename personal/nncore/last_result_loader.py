import os.path
import numpy as np
import csv

def load_data():
    fileName = 'sizes.csv'
    sizes = []
    if (os.path.exists(fileName)):
        file = open(fileName)
        for eachLine in file:
            sizes = eachLine.replace('\r\n','').split(',')
            n_size = len(sizes)
            for n in range(0,n_size):
                sizes[n] = int(sizes[n])
        file.close()

    fileName = 'weights.csv'
    weights = []
    if (os.path.exists(fileName)):
        file = open(fileName)
        for n in range(1, n_size):
            lines = []
            for n_line in range(0, sizes[n]):
                line = file.readline().replace('\r\n','').split(',')
                for n_line in range(0, len(line)):
                    line[n_line] = np.float64(line[n_line])
                lines.append(np.array(line))
            weights.append(np.array(lines))
        file.close()

    biases = []
    fileName = 'biases.csv'
    if (os.path.exists(fileName)):
        file = open(fileName)
        for n in range(1, n_size):
            lines = []
            for n_line in range(0, sizes[n]):
                line = file.readline().replace('\r\n','').split(',')
                for n_line in range(0, len(line)):
                    line[n_line] = np.float64(line[n_line])
                lines.append(np.array(line))
            biases.append(np.array(lines))
        file.close()
        
    return (sizes, weights, biases)
    
def store_result(sizes, weights, biases):
    n_weights = len(sizes)-1
    f = open('sizes.csv', 'w')
    dataWriter = csv.writer(f)
    dataWriter.writerow(sizes)
    f.close()
    f = open('weights.csv', 'w')
    dataWriter = csv.writer(f)
    for n in range(0, n_weights):
    	for m in range(0, sizes[n+1]):
    		outStr = []
    		for l in range(0, sizes[n]):
    			outStr.append(weights[n][m][l])
    		dataWriter.writerow(outStr)
    f.close()
    f = open('biases.csv', 'w')
    dataWriter = csv.writer(f)
    for n in range(0, n_weights):
    	for m in range(0, sizes[n+1]):
    		outStr = []
    		outStr.append(biases[n][m][0])
    		dataWriter.writerow(outStr)
    f.close()
