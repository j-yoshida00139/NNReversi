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

        canPut = request.POST.get('canPutList')
        canPutList = json.loads(canPut)

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

def add_todo(request):
    if request.is_ajax() and request.POST:
        data = {'message': "%s added" % request.POST.get('item')}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404
