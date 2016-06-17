import sys, os
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
import json
from django.http import Http404, HttpResponse
#import network

def test(request):
    if request.is_ajax() and request.method == 'POST':
        arrange = request.POST.get('arrange')
        arrangeArray = json.loads(arrange)
        color = request.POST.get('color')
        colorInt = int(color)
        arrangeList = [];

        for cols in arrangeArray:
        	for value in cols:
        		print (value)
        		print (color)
        		if value == 0:
	        		arrangeList.append(0)
        		elif value == colorInt:
	        		arrangeList.append(1)
	        	else:
	        		arrangeList.append(2)
        print (arrangeList)


        return HttpResponse(color, content_type='application/json')
    else:
        raise Http404


def add_todo(request):
    if request.is_ajax() and request.POST:
        data = {'message': "%s added" % request.POST.get('item')}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404
