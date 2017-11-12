import json
from django.http import Http404, HttpResponse
from personal.nncore import network
import numpy as np
from personal import game
from personal.utils import basicFunc, mathFunc
from personal.models import BestMove

n_input = 192
n_neutral_neuron = 100
n_output = 64
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
		arrangeList = BestMove.conv64ListToNnInputList(arrangeArray, colorInt)
		arrangeList = basicFunc.convInput(arrangeList)

		net = network.Network()
		result = net.feedforward(arrangeList)
		resultList = []
		for resultValue in result[0]:
			resultList.append(float(resultValue))
		resultList = mathFunc.softmax(np.array(resultList))

		outputList = []
		for i in range(0, len(resultList)-1):
			outputList.append(float(resultList[i]*canPutList[i]))

		index = outputList.index(max(outputList))
		row, col = divmod(index, 8)

		cellJson = json.dumps({"row": row, "col": col})

		return HttpResponse(cellJson, content_type='application/json')
	else:
		raise Http404


def storeWinnersData(request):
	if request.is_ajax() and request.method == 'POST':
		winnersData = request.POST.get('winnersData')
		winnersDataArray = json.loads(winnersData)
		print(winnersDataArray)

		for winnersData in winnersDataArray:
			if not BestMove.hasMoveData(winnersData["arrange"], winnersData["color"]):
				BestMove.storeBestMove(winnersData)

		return HttpResponse(winnersDataArray, content_type='application/json')
	else:
		raise Http404
