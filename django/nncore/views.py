from django.shortcuts import render
from .src import network
from .utils import mathFunc
from django.http import Http404, HttpResponse
from django.middleware.csrf import get_token
import numpy as np
import json
ROWS = 8
COLS = 8

net = network.Network()


def forward(request):
	# csrf_token = get_token(request)
	if request.method == 'POST':
		nn_input_str = request.body.decode('utf-8')
		# nn_input_str = request.POST.get('nn_input')
		nn_input_list = json.loads(nn_input_str)
		nn_input_nparray = np.array(nn_input_list["nn_input"])
		nn_input = nn_input_nparray.reshape(1, 3, 8, 8)
		nn_output = net.feed_forward(nn_input)
		move = mathFunc.softmax(nn_output)
		move_list = move.tolist()
		move_json = json.dumps({"nn_output": move_list})

		return HttpResponse(move_json, content_type='application/json')
	else:
		raise Http404
