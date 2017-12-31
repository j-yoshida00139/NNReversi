from .src import network
from .utils import mathFunc
from django.http import Http404, HttpResponse
import numpy as np
import json
import pickle
ROWS = 8
COLS = 8

net = network.Network()


def forward(request):
	if request.method == 'POST':
		nn_input_str = request.body.decode('utf-8')
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


def upload_input(request):
	if request.method == 'POST':
		nn_input_str = request.body.decode('utf-8')
		nn_input_list = json.loads(nn_input_str)
		params = dict()
		params["x_train"], params["t_train"], params["x_test"], params["t_test"] = \
			np.array(nn_input_list["x_train"]), \
			np.array(nn_input_list["t_train"]), \
			np.array(nn_input_list["x_test"]), \
			np.array(nn_input_list["t_test"])
		with open("nncore/input_data/learn_input.pkl", 'wb') as f:
			pickle.dump(params, f)
		result_json = json.dumps({"status": "OK"})

		return HttpResponse(result_json, content_type='application/json')
	else:
		raise Http404
