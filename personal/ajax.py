import sys, os
from os import listdir
from os.path import isfile, join
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
import json
from django.http import Http404, HttpResponse
import network
import csv
import numpy as np

n_input = 192 #366
n_neutral_neuron = 100
n_output = 64 #12
NONE = 0
ROWS = 8
COLS = 8


def nextMove(request):
	if request.is_ajax() and request.method == 'POST':
		arrange = request.POST.get('arrange')
		arrangeArray = json.loads(arrange)
		color = request.POST.get('color')
		colorInt = int(color)

		canPut = request.POST.get('canPutList')
		canPutList = json.loads(canPut)

		arrangeList = returnNnInputList(arrangeArray, colorInt)

		size = [n_input, n_neutral_neuron, n_output]
		net = network.Network(size)

		result = net.feedforward(arrangeList)
		resultList = []
		for resultValue in result:
			resultList.append(float(resultValue))

		outputList = []
		for i in range(0, len(resultList)-1):
			outputList.append(float(resultList[i]*canPutList[i]))

		index = outputList.index(max(outputList))
		row, col = divmod(index, 8)

		cell = {
			"row":row,
			"col":col
		}
		cellJson = json.dumps(cell)

		return HttpResponse(cellJson, content_type='application/json')
	else:
		raise Http404

def storeWinnersData(request):
	if request.is_ajax() and request.method == 'POST':
		winnersData = request.POST.get('winnersData')
		winnersDataArray = json.loads(winnersData)
		print (winnersDataArray)
		lastFileNo = getLastFileNo()

		for i in range(len(winnersDataArray)):
			winnersMove = winnersDataArray[i]
			# winnersMove = json.loads(winnersDataArray[i])
			inputList = returnNnInputList(winnersMove["arrange"], winnersMove["color"])
			fileNo = lastFileNo + i
			fileNameInput  = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/input_{0:08d}".format(fileNo+1)
			fileNameOutput = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/output_{0:08d}".format(fileNo+1)
			fIn  = open(fileNameInput  + '.csv', 'w')
			fOut = open(fileNameOutput + '.csv', 'w')

			row = winnersMove["row"]
			col = winnersMove["col"]
			moveList = returnMoveList(row, col)

			dataWriterIn = csv.writer(fIn)
			# for i in range(0, len(inputList)):
			dataWriterIn.writerow(returnNnInputStoreList(inputList))
			fIn.close()
			dataWriterOut = csv.writer(fOut)
			# for i in range(0, len(moveList)):
			dataWriterOut.writerow(moveList)
			fOut.close()



		return HttpResponse(winnersDataArray, content_type='application/json')
	else:
		raise Http404

def getLastFileNo():
	path = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/"
	fileNoList = [retrieveFileNo(f) for f in listdir(path) if isfile(join(path, f))]
	return np.max(fileNoList)

def retrieveFileNo(filename):
	print(filename)
	if filename.count(".csv"):
		tmpFileName = filename.replace("input_","")
		tmpFileName = tmpFileName.replace("output_","")
		tmpFileName = tmpFileName.replace(".csv","")
		return int(tmpFileName)
	else:
		return 0

def returnNnInputList(rawArray, color):
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
	return arrangeList;

def returnNnInputStoreList(rawArray):
	arrangeList = []
	for value in rawArray:
		arrangeList.append(value[0])
	print(arrangeList)
	return arrangeList

def returnMoveList(row, col):
	moveList = []
	for y in range(0, ROWS):
		for x in range(0, COLS):
			if y==row and x==col:
				moveList.append(float(1))
			else:
				moveList.append(float(0))
	return moveList
