import pytest
from mixer.backend.django import mixer

from personal.models import BestMove
from personal.utils import dbmanager

pytestmark = pytest.mark.django_db


class TestBestMove:
	def test_create(self):
		obj = mixer.blend('personal.BestMove')
		assert obj.pk == 1, 'Should create a BestMove instance'

	def test_save_or_update(self):
		first_half_arrangement, last_half_arrangement, move_index = 66032381159471, 3939357278671015, 5
		best_move = BestMove(
			first_half_arrangement=first_half_arrangement,
			last_half_arrangement=last_half_arrangement,
			move_index=move_index)
		game_arrange = dbmanager.decode_db_arrange(first_int=first_half_arrangement, last_int=last_half_arrangement)
		assert BestMove.has_move_data(game_arrange) is False
		best_move.save_or_update()
		assert BestMove.has_move_data(game_arrange) is True
		pk = best_move.pk
		best_move.move_index = move_index + 1
		best_move.save_or_update()
		assert best_move.pk == pk
		assert BestMove.has_move_data(game_arrange) is True
		assert best_move.move_index != move_index

	def test_has_move_data(self):
		first_half_arrangement, last_half_arrangement, move_index = 66032381159471, 3939357278671015, 5
		BestMove(
			first_half_arrangement=first_half_arrangement,
			last_half_arrangement=last_half_arrangement,
			move_index=move_index).save()
		game_arrange = dbmanager.decode_db_arrange(first_int=first_half_arrangement, last_int=last_half_arrangement)
		assert BestMove.has_move_data(game_arrange) is True
		game_arrange = dbmanager.decode_db_arrange(first_int=last_half_arrangement, last_int=first_half_arrangement)
		assert BestMove.has_move_data(game_arrange) is False

	def test_encode_to_nn_arrange(self):
		game_arrange = [
			[0, 1, 2, 0, 1, 2, 0, 1],
			[2, 0, 1, 2, 0, 1, 2, 0],
			[1, 2, 0, 1, 2, 0, 1, 2],
			[0, 1, 2, 0, 1, 2, 0, 1],
			[2, 0, 1, 2, 0, 1, 2, 0],
			[1, 2, 0, 1, 2, 0, 1, 2],
			[0, 1, 2, 0, 1, 2, 0, 1],
			[2, 0, 1, 2, 0, 1, 2, 0],
		]
		nn_arrange_1 = [
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0],
			[1.0], [0.0], [0.0]
		]
		nn_arrange_2 = [
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0], [0.0],
			[1.0], [0.0], [0.0]
		]
		assert BestMove.encode_to_nn_arrange(game_arrange, player_color=1) == nn_arrange_1
		assert BestMove.encode_to_nn_arrange(game_arrange, player_color=2) == nn_arrange_2

	def test_encode_db_arrange(self):
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
		correct_first_int = 66032381159471
		correct_last_int = 3939357278671015
		first_int, last_int = BestMove.encode_to_db_arrange(game_arrange=game_arrange)
		assert first_int == correct_first_int
		assert last_int == correct_last_int

	def test_conv_to_game_arrange(self):
		color_arrange = [[0, 1, 2], [1, 0, 2], [1, 1, 0]]
		player_color = 2
		assert BestMove.conv_to_game_arrange(
			color_arrange=color_arrange, player_color=player_color) == [2, 0, 1, 0, 2, 1, 0, 0, 2]

	def test_encode_to_db_move(self):
		assert BestMove.encode_to_db_move(1, 2) == 10
		assert BestMove.encode_to_db_move(5, 7) == 47

	def test_store_best_move(self):
		winners_move = dict()
		winners_move["arrange"] = [
			[2, 1, 0, 2, 1, 0, 2, 1],
			[0, 2, 1, 0, 2, 1, 0, 2],
			[1, 0, 2, 1, 0, 2, 1, 0],
			[2, 1, 0, 2, 1, 0, 2, 1],
			[0, 2, 1, 0, 2, 1, 0, 2],
			[1, 0, 2, 1, 0, 2, 1, 0],
			[2, 1, 0, 2, 1, 0, 2, 1],
			[0, 2, 1, 0, 2, 1, 0, 2]
		]
		winners_move["color"] = 1
		winners_move["row"] = 2
		winners_move["col"] = 4
		BestMove.store_best_move(winners_move=winners_move)
		best_move = BestMove.objects.get()
		assert best_move.first_half_arrangement == 66032381159471
		assert best_move.last_half_arrangement == 3939357278671015
		assert best_move.move_index == BestMove.encode_to_db_move(2, 4)
