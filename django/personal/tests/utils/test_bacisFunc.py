import pytest

from ...utils.basicFunc import *
from ...utils.game import Game

pytestmark = pytest.mark.django_db


def test_unshared_copy():
	sample = ['a', 'b', 'c']
	output = unshared_copy(sample)
	output[0] = 'd'
	assert sample[0] != output[0]
	assert sample[1] == output[1]
	assert sample[2] == output[2]


def test_conv_input():
	sample = [[x % 3] for x in range(192)]
	output = conv_input(sample)
	print(output)
	assert len(output) == 1
	assert len(output[0]) == 3
	assert len(output[0][0] == 8)
	assert len(output[0][0][0] == 8)
	for row in output[0][0]:
		for col in row:
			assert col == 0.0
	for row in output[0][1]:
		for col in row:
			assert col == 1.0
	for row in output[0][2]:
		for col in row:
			assert col == 2.0


def test_calc_win_ratio():
	target_game = Game(8, 8)
	target_game.initialize()
	arrange = [[target_game.BLACK for _y in range(8)] for _x in range(8)]
	assert calc_win_ratio(arrange, target_game.nextColor, target_game.BLACK) == 100.0
	assert calc_win_ratio(arrange, target_game.nextColor, target_game.WHITE) == 0.0
	target_game.initialize()
	for i in range(56):
		target_game.go_next_with_auto_move()
	win_ratio = calc_win_ratio(target_game.arrange, target_game.nextColor, target_game.BLACK)
	assert win_ratio >= 0.0
	assert win_ratio <= 100.0
