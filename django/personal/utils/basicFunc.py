import numpy as np

from personal.utils import game


def unshared_copy(in_list):
	if isinstance(in_list, list):
		return list(map(unshared_copy, in_list))
	return in_list


def conv_input(input_array):
	input_tmp_array = []
	for input_data in input_array:
		input_tmp_array.append(input_data[0])
	input_array = input_tmp_array
	input_nparray = np.array([])

	tmp = np.array([])
	tmp = np.append(tmp, np.array([input_array[x] for x in range(0, 192, 3)]).reshape(8, 8))
	tmp = np.append(tmp, np.array([input_array[x] for x in range(1, 192, 3)]).reshape(8, 8))
	tmp = np.append(tmp, np.array([input_array[x] for x in range(2, 192, 3)]).reshape(8, 8))
	input_nparray = np.append(input_nparray, tmp)
	input_nparray = input_nparray.reshape(1, 3, 8, 8)
	return input_nparray


def calc_win_ratio(arrange_list, next_color, your_color):
	num_game, win, games = 100, 0, 0
	for i in range(num_game):
		tmp_game = game.Game(8, 8, unshared_copy(arrange_list), next_color)
		while not tmp_game.is_ended():
			tmp_game.go_next_with_auto_move()
		games += 1 if not tmp_game.get_winners_color() == 0 else 0  # Not even score
		win += 1 if tmp_game.get_winners_color() == your_color else 0
	win_ratio = win / games * 100.0 if games != 0 else 0.0
	return win_ratio
