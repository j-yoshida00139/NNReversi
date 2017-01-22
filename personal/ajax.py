import sys, os
#from os import listdir
#from os.path import isfile, join
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
import json
from django.http import Http404, HttpResponse
import network
import csv
#import numpy as np
import game

n_input = 192 #366
n_neutral_neuron = 100
n_output = 64 #12
NONE = 0
ROWS = 8
COLS = 8

game = game.Game(ROWS, COLS)


def nextMove(request):
	if request.is_ajax() and request.method == 'POST':
		arrange = request.POST.get('arrange')
		colorInt = int(request.POST.get('color'))
		canPut = request.POST.get('canPutList')

		arrangeArray = json.loads(arrange)
		canPutList = json.loads(canPut)

		arrangeList = game.returnNnInputList(arrangeArray, colorInt)

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
		cellJson = json.dumps({"row": row,"col": col})

		return HttpResponse(cellJson, content_type='application/json')
	else:
		raise Http404


def storeWinnersData(request):
	if request.is_ajax() and request.method == 'POST':
		winnersData = request.POST.get('winnersData')
		winnersDataArray = json.loads(winnersData)
		print (winnersDataArray)
		lastFileNo = game.getLastFileNo()

		for i in range(len(winnersDataArray)):
			winnersMove = winnersDataArray[i]
			inputList = game.returnNnInputList(winnersMove["arrange"], winnersMove["color"])
			fileNo = lastFileNo + i
			fileNameInput  = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/input_{0:08d}".format(fileNo+1)
			fileNameOutput = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/output_{0:08d}".format(fileNo+1)
			fIn  = open(fileNameInput  + '.csv', 'w')
			fOut = open(fileNameOutput + '.csv', 'w')

			row = winnersMove["row"]
			col = winnersMove["col"]
			moveList = game.returnMoveList(row, col)

			dataWriterIn = csv.writer(fIn)
			dataWriterIn.writerow(game.returnNnInputStoreList(inputList))
			fIn.close()
			dataWriterOut = csv.writer(fOut)
			dataWriterOut.writerow(moveList)
			fOut.close()

		return HttpResponse(winnersDataArray, content_type='application/json')
	else:
		raise Http404
