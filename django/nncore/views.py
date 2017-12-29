from .src import network
from .utils import mathFunc
from django.http import Http404, HttpResponse
from .utils.trainer import Trainer
import numpy as np
import json
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


def train(request):
	if request.method == 'POST':
		nn_input_str = request.body.decode('utf-8')
		nn_input_list = json.loads(nn_input_str)
		x_train, t_train, x_test, t_test = \
			nn_input_list["x_train"], \
			nn_input_list["t_train"], \
			nn_input_list["x_test"], \
			nn_input_list["y_test"]
		trainer = Trainer(
			net, x_train, t_train, x_test, t_test,
			epochs=20, mini_batch_size=100,
			optimizer='Adam', optimizer_param={'lr': 0.001},
			evaluate_sample_num_per_epoch=1000)
		trainer.train()
		result_json = json.dumps({"status": "OK"})

		return HttpResponse(result_json, content_type='application/json')
	else:
		raise Http404
