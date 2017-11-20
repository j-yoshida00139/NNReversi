import pytest
from mixer.backend.django import mixer
from personal.models import BestMove
from personal import dbmanager

pytestmark = pytest.mark.django_db


class Test_BestMove:
	def test_create(self):
		obj = mixer.blend('personal.BestMove')
		assert obj.pk == 1, 'Should create a BestMove instance'

	def test_save_or_update(self):
		first_half_arrangement, last_half_arrangement, move_index = 66032381159471, 3939357278671015, 5
		bestMove = BestMove(
			first_half_arrangement=first_half_arrangement,
			last_half_arrangement=last_half_arrangement,
			move_index=move_index)
		gameArrange = dbmanager.decodeDBArrange(firstInt=first_half_arrangement, lastInt=last_half_arrangement)
		assert BestMove.hasMoveData(gameArrange) is False
		bestMove.save_or_update()
		assert BestMove.hasMoveData(gameArrange) is True
		pk = bestMove.pk
		bestMove.move_index = move_index + 1
		bestMove.save_or_update()
		assert bestMove.pk == pk
		assert BestMove.hasMoveData(gameArrange) is True
		assert bestMove.move_index != move_index

	def test_hasMoveData(self):
		first_half_arrangement, last_half_arrangement, move_index = 66032381159471, 3939357278671015, 5
		BestMove(
			first_half_arrangement=first_half_arrangement,
			last_half_arrangement=last_half_arrangement,
			move_index=move_index).save()
		gameArrange = dbmanager.decodeDBArrange(firstInt=first_half_arrangement, lastInt=last_half_arrangement)
		assert BestMove.hasMoveData(gameArrange) is True
		gameArrange = dbmanager.decodeDBArrange(firstInt=last_half_arrangement, lastInt=first_half_arrangement)
		assert BestMove.hasMoveData(gameArrange) is False

	def test_encodeToNNArrange(self):
		gameArrange = [
			[0, 1, 2, 0, 1, 2, 0, 1],
			[2, 0, 1, 2, 0, 1, 2, 0],
			[1, 2, 0, 1, 2, 0, 1, 2],
			[0, 1, 2, 0, 1, 2, 0, 1],
			[2, 0, 1, 2, 0, 1, 2, 0],
			[1, 2, 0, 1, 2, 0, 1, 2],
			[0, 1, 2, 0, 1, 2, 0, 1],
			[2, 0, 1, 2, 0, 1, 2, 0],
		]
		nnArrange_1 = [
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
		nnArrange_2 = [
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
		assert BestMove.encodeToNNArrange(gameArrange, playerColor=1) == nnArrange_1
		assert BestMove.encodeToNNArrange(gameArrange, playerColor=2) == nnArrange_2

	def test_encodeDBArrange(self):
		gameArrange = [
			0, 1, 2, 0, 1, 2, 0, 1,
			2, 0, 1, 2, 0, 1, 2, 0,
			1, 2, 0, 1, 2, 0, 1, 2,
			0, 1, 2, 0, 1, 2, 0, 1,
			2, 0, 1, 2, 0, 1, 2, 0,
			1, 2, 0, 1, 2, 0, 1, 2,
			0, 1, 2, 0, 1, 2, 0, 1,
			2, 0, 1, 2, 0, 1, 2, 0
		]
		correctFirstInt = 66032381159471
		correctLastInt = 3939357278671015
		firstInt, lastInt = BestMove.encodeToDBArrange(gameArrange=gameArrange)
		assert firstInt == correctFirstInt
		assert lastInt == correctLastInt

	def test_convToGameArrange(self):
		colorArrange = [[0, 1, 2], [1, 0, 2], [1, 1, 0]]
		playerColor = 2
		assert BestMove.convToGameArrange(colorArrange=colorArrange, playerColor=playerColor) == [2, 0, 1, 0, 2, 1, 0, 0, 2]

	def test_encodeToDBMove(self):
		assert BestMove.encodeToDBMove(1, 2) == 10
		assert BestMove.encodeToDBMove(5, 7) == 47

	def test_storeBestMove(self):
		winnersMove = dict()
		winnersMove["arrange"] = [
			[2, 1, 0, 2, 1, 0, 2, 1],
			[0, 2, 1, 0, 2, 1, 0, 2],
			[1, 0, 2, 1, 0, 2, 1, 0],
			[2, 1, 0, 2, 1, 0, 2, 1],
			[0, 2, 1, 0, 2, 1, 0, 2],
			[1, 0, 2, 1, 0, 2, 1, 0],
			[2, 1, 0, 2, 1, 0, 2, 1],
			[0, 2, 1, 0, 2, 1, 0, 2]
		]
		winnersMove["color"] = 1
		winnersMove["row"] = 2
		winnersMove["col"] = 4
		BestMove.storeBestMove(winnersMove=winnersMove)
		bestMove = BestMove.objects.get()
		assert bestMove.first_half_arrangement == 66032381159471
		assert bestMove.last_half_arrangement == 3939357278671015
		assert bestMove.move_index == BestMove.encodeToDBMove(2, 4)
