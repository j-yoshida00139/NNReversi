import json
import numpy as np
from django.http import Http404, HttpResponse
from .models import BestMove
from .nncore import network
from .utils import basicFunc, mathFunc, game

n_input = 192
n_neutral_neuron = 100
n_output = 64
NONE = 0
ROWS = 8
COLS = 8
mainGame = game.Game(ROWS, COLS)


def next_move(request):
	if request.is_ajax() and request.method == 'POST':
		arrange = request.POST.get('arrange')
		color_int = int(request.POST.get('color'))
		can_put = request.POST.get('canPutList')

		arrange_array = json.loads(arrange)
		can_put_list = json.loads(can_put)
		arrange_list = BestMove.encode_to_nn_arrange(arrange_array, color_int)
		arrange_list = basicFunc.conv_input(arrange_list)

		net = network.Network()
		result = net.feed_forward(arrange_list)
		result_list = []
		for resultValue in result[0]:
			result_list.append(float(resultValue))
		result_list = mathFunc.softmax(np.array(result_list))

		output_list = []
		for i in range(0, len(result_list)-1):
			output_list.append(float(result_list[i]*can_put_list[i]))

		index = output_list.index(max(output_list))
		row, col = divmod(index, 8)

		cell_json = json.dumps({"row": row, "col": col})

		return HttpResponse(cell_json, content_type='application/json')
	else:
		raise Http404


def store_winners_data(request):
	if request.is_ajax() and request.method == 'POST':
		winners_data = request.POST.get('winnersData')
		winners_data_array = json.loads(winners_data)
		print(winners_data_array)

		for winners_data in winners_data_array:
			game_arrange = BestMove.conv_to_game_arrange(winners_data["arrange"], winners_data["color"])
			if not BestMove.has_move_data(game_arrange):
				BestMove.store_best_move(winners_data)

		return HttpResponse(winners_data_array, content_type='application/json')
	else:
		raise Http404
