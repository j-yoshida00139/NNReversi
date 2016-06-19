import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
import json
from django.http import Http404, HttpResponse
import network

n_input = 192 #366
n_neutral_neuron = 100
n_output = 64 #12
NONE = 0

def test(request):
    if request.is_ajax() and request.method == 'POST':
        arrange = request.POST.get('arrange')
        arrangeArray = json.loads(arrange)
        color = request.POST.get('color')
        colorInt = int(color)
        arrangeList = []

        for cols in arrangeArray:
        	for value in cols:
        		if value == 0:
	        		arrangeList.append([float(1)])
	        		arrangeList.append([float(0)])
	        		arrangeList.append([float(0)])
        		elif value == colorInt:
	        		arrangeList.append([float(0)])
	        		arrangeList.append([float(1)])
	        		arrangeList.append([float(0)])
	        	else:
	        		arrangeList.append([float(0)])
	        		arrangeList.append([float(0)])
	        		arrangeList.append([float(1)])

        print (len(arrangeList))
        size = [n_input, n_neutral_neuron, n_output]
        net = network.Network(size)

        result = net.feedforward(arrangeList)
        resultList = []
        for resultValue in result:
            resultList.append(float(resultValue))

        canPutList = []
        for y in range(0, 8):
            for x in range(0, 8):
                if canPutPiece(y, x, colorInt, arrangeArray):
                    canPutList.append(float(1.0))
                else:
                    canPutList.append(float(0.0))

        print ("resultList")
        print (len(resultList))
        print (resultList)
        print ("canPutList")
        print (len(canPutList))
        print (canPutList)

        outputList = []
        for i in range(0, len(resultList)-1):
            outputList.append(float(resultList[i]*canPutList[i]))

        index = outputList.index(max(outputList))
        row, col = divmod(index, 8)

        print ("outputList")
        print (outputList)
        cell = {
            "row":row,
            "col":col
        }
        cellJson = json.dumps(cell)
        print (cell)
        print (cellJson)

        return HttpResponse(cellJson, content_type='application/json')
    else:
        raise Http404

def canPutPiece(row, col, color, arrange):
    if arrange[row][col] != NONE:
        return False

    directions = [
        {"row": 0, "col": 1},
        {"row":-1, "col": 1},
        {"row":-1, "col": 0},
        {"row":-1, "col":-1},
        {"row": 0, "col":-1},
        {"row": 1, "col":-1},
        {"row": 1, "col": 0},
        {"row": 1, "col": 1}
    ]

    for i in range(0, len(directions)-1):
        if canTurnPiece(row, col, color, directions[i]['row'], directions[i]['col'], arrange):
            return True
    return False;

def canTurnPiece(row, col, color, y, x, arrange):
    if isOutOfRange(row+y, col+x):
        return False
    
    # Checking the color of next cell
    if arrange[row+y][col+x] == color or arrange[row+y][col+x] == NONE:
        return False
    
    checkRow = row+2*y
    checkCol = col+2*x

    while not(isOutOfRange(checkRow, checkCol)):
        if arrange[checkRow][checkCol] == color:
            return True
        
        checkRow += y
        checkCol += x

    return False

def isOutOfRange(row, col):
    rows=8
    cols=8
    if row>=rows or col>=cols or row<0 or col<0:
        return True
    else:
        return False


def add_todo(request):
    if request.is_ajax() and request.POST:
        data = {'message': "%s added" % request.POST.get('item')}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404
