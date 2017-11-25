import numpy as np
from personal.models import BestMove


def decode_db_arrange(first_int, last_int):
	arrange_int = BestMove.get_whole_arrange_int(first_int, last_int)
	game_arrange = []
	for i in range(64):
		arrange_int, mod = divmod(arrange_int, 3)
		game_arrange.append(mod)
	game_arrange.reverse()
	return game_arrange


def flip_two_dim_list(two_dim_arrange, way):
	if way == "Horizontal":
		axis = 1
	elif way == "Vertical":
		axis = 0
	else:
		raise BaseException("2nd argument should be 'Horizontal' or 'Vertical'")
	np_arrange = np.array(two_dim_arrange)
	flipped = np.flip(np_arrange, axis).tolist()
	return flipped


def flip_arrange_int(arrange_int, way):
	if not way == "Horizontal" and not way == "Vertical":
		raise BaseException("2nd argument should be 'Horizontal' or 'Vertical'")
	first_half, last_half = BestMove.get_first_last_arrange_int(arrange_int)
	game_arrange = decode_db_arrange(first_half, last_half)
	two_dim_arrange = np.array(game_arrange).reshape(8, 8).tolist()
	flipped_arrange = np.array(flip_two_dim_list(two_dim_arrange, way)).reshape(64).tolist()
	new_arrange_int = 0
	for val in flipped_arrange:
		new_arrange_int = new_arrange_int * 3 + int(val)
	return new_arrange_int


def flip_move_int(move_int, way):
	if not move_int >= 0 or not move_int < 64:
		raise BaseException(
			"Argument should be between 0 and 63, but it's {0}".format(move_int))
	if not way == "Horizontal" and not way == "Vertical":
		raise BaseException("2nd argument should be 'Horizontal' or 'Vertical'")
	two_dim_move = np.array(decode_db_move(move_int)).reshape(8, 8)
	symm_move_64 = flip_two_dim_list(two_dim_move, way)
	np_move_array = np.array(symm_move_64).reshape(64)
	converted_move_int = np.argmax(np_move_array)
	return converted_move_int


def decode_db_move(move_index):
	move_list = [0.0] * 64
	move_list[move_index] = 1.0
	return move_list


def extract_nn_data_by_indices(n_list):
	all_best_move = BestMove.objects.all()
	best_move_list = extract_list_by_indices(all_best_move, n_list)
	arrange_list = extract_arrange_from_best_move(best_move_list)
	move_list = extract_move_from_best_move(best_move_list)
	np_arrange_list = np.array([np.reshape(x, 192) for x in arrange_list])
	np_move_list = np.array([np.reshape(x, 64) for x in move_list])
	return np_arrange_list, np_move_list


def extract_list_by_indices(target_list, n_list):
	extracted_list = []
	for i in n_list:
		extracted_list.append(target_list[i])
	return extracted_list


def extract_arrange_from_best_move(best_move_list):
	arrange_list = []
	for bestMove in best_move_list:
		game_arrange = decode_db_arrange(bestMove.first_half_arrangement, bestMove.last_half_arrangement)
		nn_arrange = BestMove.encode_to_nn_arrange(game_arrange, 1)
		arrange_list.append(nn_arrange)
	return arrange_list


def extract_move_from_best_move(best_move_list):
	move_list = []
	for bestMove in best_move_list:
		move_list.append(decode_db_move(bestMove.move_index))
	return move_list
