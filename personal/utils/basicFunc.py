# Basic functions
import sys
import os
import numpy as np
from os import listdir
from os.path import isfile,\
	join
from personal import dbmanager
from personal.models import BestMove

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir) + '/nncore')
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir) + '/Model')
#import dbmanager


def getLastFileNo():
	path = os.path.join(os.path.dirname(__file__), os.pardir) + "/nncore/winnersData/"
	fileNoList = [retrieveFileNo(f) for f in listdir(path) if isfile(join(path, f))]
	return np.max(fileNoList)


def retrieveFileNo(filename):
	if filename.count(".csv"):
		tmpFileName = filename.replace("input_", "")
		tmpFileName = tmpFileName.replace("output_", "")
		tmpFileName = tmpFileName.replace(".csv", "")
		return int(tmpFileName)
	else:
		return 0


def conv64ListToNnInputList(rawArray, color):
	arrangeList = []
	for cols in rawArray:
		for value in cols:
			if value == 0:
				arrangeList.append([float(1)])
				arrangeList.append([float(0)])
				arrangeList.append([float(0)])
			elif value == color:
				arrangeList.append([float(0)])
				arrangeList.append([float(1)])
				arrangeList.append([float(0)])
			else:
				arrangeList.append([float(0)])
				arrangeList.append([float(0)])
				arrangeList.append([float(1)])
	return arrangeList


def storeWinnersDataList(winnersData):
	for i, winnersMove in list(enumerate(winnersData)):
		storeBestMove(winnersMove)
	return True


def storeBestMove(winnersMove):
	inputList = conv64ListToNnInputList(winnersMove["arrange"], winnersMove["color"])
	inputInt = dbmanager.encodeArrangement(inputList)
	firstHalf, lastHalf = divmod(inputInt, int(1E16))
	outIndex = winnersMove["row"] * 8 + winnersMove["col"]
	bestMove = BestMove(first_half_arrangement=firstHalf, last_half_arrangement=lastHalf, move_index=outIndex)
	bestMove.save()


def unsharedCopy(inList):
	if isinstance(inList, list):
		return list(map(unsharedCopy, inList))
	return inList


def convInput(input_array):
	input_tmp_array = []
	for input_data in input_array:
		input_tmp_array.append(input_data[0])
	input_array = input_tmp_array
	input_nparray = np.array([])

	# print(input_array)
	tmp = np.array([])
	tmp = np.append(tmp, np.array([input_array[x] for x in range(0, 192, 3)]).reshape(8, 8))
	tmp = np.append(tmp, np.array([input_array[x] for x in range(1, 192, 3)]).reshape(8, 8))
	tmp = np.append(tmp, np.array([input_array[x] for x in range(2, 192, 3)]).reshape(8, 8))
	input_nparray = np.append(input_nparray, tmp)
	input_nparray = input_nparray.reshape(1, 3, 8, 8)
	# print(input_nparray)
	return input_nparray
