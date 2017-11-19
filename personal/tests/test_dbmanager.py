import pytest
from personal.dbmanager import *

pytestmark = pytest.mark.django_db


def test_decodeDBArrange():
	firstInt = 66032381159471
	lastInt = 3939357278671015
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
	assert decodeDBArrange(firstInt, lastInt) == gameArrange


def test_flipTwoDimList():
	sample = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	assert flipTwoDimList(sample, "Horizontal") == [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
	sample = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	assert flipTwoDimList(sample, "Vertical") == [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
	with pytest.raises(BaseException):
		flipTwoDimList(sample, "Other")


def test_flipArrangeInt():
	arrangeInt = 660323811594713939357278671015
	flippedIntHor = 1452430613618011145185326950141
	assert flipArrangeInt(arrangeInt, "Horizontal") == flippedIntHor
	flippedIntVer = 2509029184243533849258951963655
	assert flipArrangeInt(arrangeInt, "Vertical") == flippedIntVer
	with pytest.raises(BaseException):
		flipArrangeInt(arrangeInt, "Other")


def test_flipMoveInt():
	samplesHor = [[0, 7], [1, 6], [9, 14], [17, 22]]
	samplesVer = [[0, 56], [1, 57], [9, 49], [17, 41]]
	for sample, correct in samplesHor:
		assert flipMoveInt(sample, "Horizontal") == correct
	for sample, correct in samplesVer:
		assert flipMoveInt(sample, "Vertical") == correct
	with pytest.raises(BaseException):
		flipMoveInt(-1, "Horizontal")
	with pytest.raises(BaseException):
		flipMoveInt(64, "Vertical")
	with pytest.raises(BaseException):
		flipMoveInt(1, "Other")
	with pytest.raises(BaseException):
		flipMoveInt(64, "Other")


def test_extractListByIndices():
	nList = [1, 3, 6]
	targetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	extractedList = extractListByIndices(targetList, nList)
	assert extractedList == ['b', 'd', 'g']


def test_extractNNDataByIndices():
	BestMove(first_half_arrangement=66032381159471, last_half_arrangement=3939357278671015, move_index=5).save()
	BestMove(first_half_arrangement=145243061361801, last_half_arrangement=1145185326950141, move_index=10).save()
	BestMove(first_half_arrangement=250902918424353, last_half_arrangement=3849258951963655, move_index=25).save()
	nList = [2, 1, 0]
	correctNNArrangeList = [
		BestMove.encodeToNNArrange([
			2, 0, 1, 2, 0, 1, 2, 0,
			0, 1, 2, 0, 1, 2, 0, 1,
			1, 2, 0, 1, 2, 0, 1, 2,
			2, 0, 1, 2, 0, 1, 2, 0,
			0, 1, 2, 0, 1, 2, 0, 1,
			1, 2, 0, 1, 2, 0, 1, 2,
			2, 0, 1, 2, 0, 1, 2, 0,
			0, 1, 2, 0, 1, 2, 0, 1
		], 1),
		BestMove.encodeToNNArrange([
			1, 0, 2, 1, 0, 2, 1, 0,
			0, 2, 1, 0, 2, 1, 0, 2,
			2, 1, 0, 2, 1, 0, 2, 1,
			1, 0, 2, 1, 0, 2, 1, 0,
			0, 2, 1, 0, 2, 1, 0, 2,
			2, 1, 0, 2, 1, 0, 2, 1,
			1, 0, 2, 1, 0, 2, 1, 0,
			0, 2, 1, 0, 2, 1, 0, 2
		], 1),
		BestMove.encodeToNNArrange([
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
	correctNNMoveList = [
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
	npArrangeList, npMoveList = extractNNDataByIndices(nList)
	correctNpArrangeList = np.array([np.reshape(correctNNArrange, 192) for correctNNArrange in correctNNArrangeList])
	assert npArrangeList.all() == correctNpArrangeList.all()
	correctNpMoveList = np.array([np.reshape(correctNNMove, 64) for correctNNMove in correctNNMoveList])
	assert npMoveList.all() == correctNpMoveList.all()
