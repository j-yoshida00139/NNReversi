import pytest

from ...utils.dbmanager import *

pytestmark = pytest.mark.django_db


def test_decode_db_arrange():
	first_int = 66032381159471
	last_int = 3939357278671015
	game_arrange = [
		0, 1, 2, 0, 1, 2, 0, 1,
		2, 0, 1, 2, 0, 1, 2, 0,
		1, 2, 0, 1, 2, 0, 1, 2,
		0, 1, 2, 0, 1, 2, 0, 1,
		2, 0, 1, 2, 0, 1, 2, 0,
		1, 2, 0, 1, 2, 0, 1, 2,
		0, 1, 2, 0, 1, 2, 0, 1,
		2, 0, 1, 2, 0, 1, 2, 0
	]
	assert decode_db_arrange(first_int, last_int) == game_arrange


def test_flip_two_dim_list():
	sample = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	assert flip_2dim_list(sample, "Horizontal") == [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
	sample = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	assert flip_2dim_list(sample, "Vertical") == [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
	with pytest.raises(BaseException):
		flip_2dim_list(sample, "Other")


def test_rotate_2dim_list_90deg():
	sample = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	assert rotate_2dim_list_90deg(sample) == [[3, 6, 9], [2, 5, 8], [1, 4, 7]]


def test_rotate_2dim_list_degree():
	sample = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	assert rotate_2dim_list(sample, 0) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	assert rotate_2dim_list(sample, 90) == [[3, 6, 9], [2, 5, 8], [1, 4, 7]]
	assert rotate_2dim_list(sample, 180) == [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
	assert rotate_2dim_list(sample, 270) == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
	assert rotate_2dim_list(sample, 360) == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def test_flip_arrange_int():
	arrange_int = 660323811594713939357278671015
	flipped_int_hor = 1452430613618011145185326950141
	assert flip_arrange_int(arrange_int, "Horizontal") == flipped_int_hor
	flipped_int_ver = 2509029184243533849258951963655
	assert flip_arrange_int(arrange_int, "Vertical") == flipped_int_ver
	with pytest.raises(BaseException):
		flip_arrange_int(arrange_int, "Other")


def test_flip_move_int():
	samples_hor = [[0, 7], [1, 6], [9, 14], [17, 22]]
	samples_ver = [[0, 56], [1, 57], [9, 49], [17, 41]]
	for sample, correct in samples_hor:
		assert flip_move_int(sample, "Horizontal") == correct
	for sample, correct in samples_ver:
		assert flip_move_int(sample, "Vertical") == correct
	with pytest.raises(BaseException):
		flip_move_int(-1, "Horizontal")
	with pytest.raises(BaseException):
		flip_move_int(64, "Vertical")
	with pytest.raises(BaseException):
		flip_move_int(1, "Other")
	with pytest.raises(BaseException):
		flip_move_int(64, "Other")


def test_extract_list_by_indices():
	n_list = [1, 3, 6]
	target_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	extracted_list = extract_list_by_indices(target_list, n_list)
	assert extracted_list == ['b', 'd', 'g']


def test_extract_nn_data_by_indices():
	BestMove(first_half_arrangement=66032381159471, last_half_arrangement=3939357278671015, move_index=5).save()
	BestMove(first_half_arrangement=145243061361801, last_half_arrangement=1145185326950141, move_index=10).save()
	BestMove(first_half_arrangement=250902918424353, last_half_arrangement=3849258951963655, move_index=25).save()
	n_list = [2, 1, 0]
	correct_nn_arrange_list = [
		BestMove.encode_to_nn_arrange([
			2, 0, 1, 2, 0, 1, 2, 0,
			0, 1, 2, 0, 1, 2, 0, 1,
			1, 2, 0, 1, 2, 0, 1, 2,
			2, 0, 1, 2, 0, 1, 2, 0,
			0, 1, 2, 0, 1, 2, 0, 1,
			1, 2, 0, 1, 2, 0, 1, 2,
			2, 0, 1, 2, 0, 1, 2, 0,
			0, 1, 2, 0, 1, 2, 0, 1
		], 1),
		BestMove.encode_to_nn_arrange([
			1, 0, 2, 1, 0, 2, 1, 0,
			0, 2, 1, 0, 2, 1, 0, 2,
			2, 1, 0, 2, 1, 0, 2, 1,
			1, 0, 2, 1, 0, 2, 1, 0,
			0, 2, 1, 0, 2, 1, 0, 2,
			2, 1, 0, 2, 1, 0, 2, 1,
			1, 0, 2, 1, 0, 2, 1, 0,
			0, 2, 1, 0, 2, 1, 0, 2
		], 1),
		BestMove.encode_to_nn_arrange([
			0, 1, 2, 0, 1, 2, 0, 1,
			2, 0, 1, 2, 0, 1, 2, 0,
			1, 2, 0, 1, 2, 0, 1, 2,
			0, 1, 2, 0, 1, 2, 0, 1,
			2, 0, 1, 2, 0, 1, 2, 0,
			1, 2, 0, 1, 2, 0, 1, 2,
			0, 1, 2, 0, 1, 2, 0, 1,
			2, 0, 1, 2, 0, 1, 2, 0
		], 1)
	]
	correct_nn_move_list = [
		[
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 1, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0
		], [
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 1, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0
		], [
			0, 0, 0, 0, 0, 1, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 0, 0, 0, 0, 0, 0, 0
		]
	]
	np_arrange_list, np_move_list = extract_nn_data_by_indices(n_list)
	correct_np_arrange_list = np.array([np.reshape(correctNNArrange, 192) for correctNNArrange in correct_nn_arrange_list])
	assert np_arrange_list.all() == correct_np_arrange_list.all()
	correct_np_move_list = np.array([np.reshape(correctNNMove, 64) for correctNNMove in correct_nn_move_list])
	assert np_move_list.all() == correct_np_move_list.all()
