import sys, os
#from os import listdir
#from os.path import isfile, join
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/utils')
import json
from django.http import Http404, HttpResponse
import network
import network2_edit
import csv
import numpy as np
import game
import basicFunc

n_input = 192 #366
n_neutral_neuron = 100
n_output = 64 #12
NONE = 0
ROWS = 8
COLS = 8

mainGame = game.Game(ROWS, COLS)

def nextMove(request):
	if request.is_ajax() and request.method == 'POST':
		arrange = request.POST.get('arrange')
		colorInt = int(request.POST.get('color'))
		canPut = request.POST.get('canPutList')

		arrangeArray = json.loads(arrange)
		canPutList = json.loads(canPut)
		arrangeList = mainGame.returnNnInputList(arrangeArray, colorInt)

		size = [n_input, n_neutral_neuron, n_output]
		#net = network.Network(size)
		net = network2_edit.Network(size)

		arrangeList = np.array(arrangeList).T
		result = net.feedforward(arrangeList)
		resultList = []
		for resultValue in result[0]:
			print(resultValue)
			resultList.append(float(resultValue))
		resultList = net.softmax(np.array(resultList))

		outputList = []
		for i in range(0, len(resultList)-1):
			outputList.append(float(resultList[i]*canPutList[i]))

		index = outputList.index(max(outputList))
		row, col = divmod(index, 8)

		#tmp
		#tmpGame = game.Game(8, 8, basicFunc.unsharedCopy(arrangeArray), colorInt)
		#row, col, winRatio = tmpGame.findBestMove()
		#tmp

		cellJson = json.dumps({"row": row,"col": col})

		return HttpResponse(cellJson, content_type='application/json')
	else:
		raise Http404


def storeWinnersData(request):
	if request.is_ajax() and request.method == 'POST':
		winnersData = request.POST.get('winnersData')
		winnersDataArray = json.loads(winnersData)
		print (winnersDataArray)
		lastFileNo = basicFunc.getLastFileNo()

		for i in range(len(winnersDataArray)):
			winnersMove = winnersDataArray[i]
			inputList = mainGame.returnNnInputList(winnersMove["arrange"], winnersMove["color"])
			fileNo = lastFileNo + i
			fileNameInput  = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/input_{0:08d}".format(fileNo+1)
			fileNameOutput = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/output_{0:08d}".format(fileNo+1)
			fIn  = open(fileNameInput  + '.csv', 'w')
			fOut = open(fileNameOutput + '.csv', 'w')

			row = winnersMove["row"]
			col = winnersMove["col"]
			moveList = mainGame.returnMoveList(row, col)

			dataWriterIn = csv.writer(fIn)
			dataWriterIn.writerow(mainGame.returnNnInputStoreList(inputList))
			fIn.close()
			dataWriterOut = csv.writer(fOut)
			dataWriterOut.writerow(moveList)
			fOut.close()

		return HttpResponse(winnersDataArray, content_type='application/json')
	else:
		raise Http404

