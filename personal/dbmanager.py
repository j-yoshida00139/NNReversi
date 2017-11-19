import numpy as np
from personal.models import BestMove


def decodeDBArrange(firstInt, lastInt):
	arrangeInt = BestMove.getWholeArrangeInt(firstInt, lastInt)
	gameArrange = []
	for i in range(64):
		arrangeInt, mod = divmod(arrangeInt, 3)
		gameArrange.append(mod)
	gameArrange.reverse()
	return gameArrange


def flipTwoDimList(twoDimArrange, way):
	if way == "Horizontal":
		axis = 1
	elif way == "Vertical":
		axis = 0
	else:
		raise BaseException("2nd argument should be 'Horizontal' or 'Vertical'")
	npArrange = np.array(twoDimArrange)
	flipped = np.flip(npArrange, axis).tolist()
	return flipped


def flipArrangeInt(arrangeInt, way):
	if not way == "Horizontal" and not way == "Vertical":
		raise BaseException("2nd argument should be 'Horizontal' or 'Vertical'")
	firstHalf, lastHalf = BestMove.getFirstLastArrangeInt(arrangeInt)
	gameArrange = decodeDBArrange(firstHalf, lastHalf)
	twoDimArrange = np.array(gameArrange).reshape(8, 8).tolist()
	flippedArrange = np.array(flipTwoDimList(twoDimArrange, way)).reshape(64).tolist()
	newArrangeInt = 0
	for val in flippedArrange:
		newArrangeInt = newArrangeInt * 3 + int(val)
	return newArrangeInt


def flipMoveInt(moveInt, way):
	if not moveInt >= 0 or not moveInt < 64:
		raise BaseException(
			"Argument should be between 0 and 63, but it's {0}".format(moveInt))
	if not way == "Horizontal" and not way == "Vertical":
		raise BaseException("2nd argument should be 'Horizontal' or 'Vertical'")
	twoDimMove = np.array(decodeDBMove(moveInt)).reshape(8, 8)
	symmMove64 = flipTwoDimList(twoDimMove, way)
	npMoveArray = np.array(symmMove64).reshape(64)
	convertedMoveInt = np.argmax(npMoveArray)
	return convertedMoveInt


def decodeDBMove(moveIndex):
	moveList = [0.0] * 64
	moveList[moveIndex] = 1.0
	return moveList


def extractNNDataByIndices(n_list):
	allBestMove = BestMove.objects.all()
	bestMoveList = extractListByIndices(allBestMove, n_list)
	arrangeList = []
	moveList = []
	for bestMove in bestMoveList:
		gameArrange = decodeDBArrange(bestMove.first_half_arrangement, bestMove.last_half_arrangement)
		nnArrange = BestMove.encodeToNNArrange(gameArrange, 1)
		arrangeList.append(nnArrange)
		moveList.append(decodeDBMove(bestMove.move_index))
	npArrangeList = np.array([np.reshape(x, 192) for x in arrangeList])
	npMoveList = np.array([np.reshape(x, 64) for x in moveList])
	return npArrangeList, npMoveList


def extractListByIndices(targetList, nList):
	extractedList = []
	for i in nList:
		extractedList.append(targetList[i])
	return extractedList
