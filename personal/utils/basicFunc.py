# Basic functions
import sys, os
import numpy as np
import csv
from os import listdir
from os.path import isfile, join

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir) + '/nncore')
import game


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


def storeWinnersData(winnersData):
	tmpGame = game.Game(8, 8)
	lastFileNo = getLastFileNo()
	for i, winnersMove in list(enumerate(winnersData)):
		inputList = game.Game.returnNnInputList(winnersMove["arrange"], winnersMove["color"])
		fileNo = lastFileNo + i
		fileNameInput = os.path.join(os.path.dirname(__file__), os.pardir) + "/nncore/winnersData/input_{0:08d}".format(
			fileNo + 1)
		fileNameOutput = os.path.join(os.path.dirname(__file__), os.pardir) + "/nncore/winnersData/output_{0:08d}".format(fileNo + 1)
		fIn = open(fileNameInput + '.csv', 'w')
		fOut = open(fileNameOutput + '.csv', 'w')

		moveList = tmpGame.returnMoveList(winnersMove["row"], winnersMove["col"])

		dataWriterIn = csv.writer(fIn)
		dataWriterIn.writerow(game.Game.returnNnInputStoreList(inputList))
		fIn.close()
		dataWriterOut = csv.writer(fOut)
		dataWriterOut.writerow(moveList)
		fOut.close()
	return True


def unsharedCopy(inList):
	if isinstance(inList, list):
		return list(map(unsharedCopy, inList))
	return inList