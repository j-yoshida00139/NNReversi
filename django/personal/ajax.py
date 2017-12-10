import json
from django.http import Http404, HttpResponse
from .models import BestMove
from .utils import game

ROWS = 8
COLS = 8


def next_move(request):
	if request.is_ajax() and request.method == 'POST':
		arrange = request.POST.get('arrange')
		color_int = int(request.POST.get('color'))
		arrange_array = json.loads(arrange)
		main_game = game.Game(ROWS, COLS, arrange_array, color_int)
		index = main_game.get_next_move_index_by_nn(arrange_array, color_int)
		# index = main_game.get_next_move_index_by_nn(arrange_array, color_int, request.get_host())
		row, col = divmod(index, 8)
		cell_json = json.dumps({"row": int(row), "col": int(col)})

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
