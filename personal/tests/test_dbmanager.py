import pytest
from personal.dbmanager import *


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
