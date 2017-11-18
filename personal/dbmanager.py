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


def encodeToNNArrange(gameArrange):
	nnArrange = []
	for pieceColor in gameArrange:
		if pieceColor == 2:  # No piece
			nnArrange.extend([1.0, 0.0, 0.0])
		elif pieceColor == 1:  # Color of the player
			nnArrange.extend([0.0, 1.0, 0.0])
		elif pieceColor == 0:  # Color of opposite
			nnArrange.extend([0.0, 0.0, 1.0])
	return nnArrange


def decodeDBMove(moveIndex):
	moveList = [0.0] * 64
	moveList[moveIndex] = 1.0
	return moveList


def get_data_by_list(n_list):
	bestMoveList = BestMove.objects.all()
	tmparrangementList = []
	tmpmoveList = []
	for bestMove in bestMoveList:
		arrange64 = decodeDBArrange(bestMove.first_half_arrangement, bestMove.last_half_arrangement)
		arrangeList = BestMove.encodeToNNArrange(arrange64, 1)
		tmparrangementList.append(arrangeList)
		tmpmoveList.append(decodeDBMove(bestMove.move_index))
	arrangementList = []
	moveList = []
	for i in n_list:
		arrangementList.append(tmparrangementList[i])
		moveList.append(tmpmoveList[i])
	arrangementList = np.array([np.reshape(x, (192)) for x in arrangementList])
	moveList = np.array([np.reshape(x, (64)) for x in moveList])
	return arrangementList, moveList


def replicateMoveData():
	bestMoveList = BestMove.objects.all()
	for bestMove in bestMoveList:
		arrangeInt = BestMove.getWholeArrangeInt(bestMove.first_half_arrangement, bestMove.last_half_arrangement)

		# Horizontal Symmetry Data
		symmArrangeInt = flipArrangeInt(arrangeInt)
		firstInt, lastInt = BestMove.getFirstLastArrangeInt(symmArrangeInt)
		moveInt = int(flipMoveInt(bestMove.move_index, "Horizontal"))
		save_or_update(firstInt, lastInt, moveInt)

		# Vertical Symmetry Data
		symmArrangeInt = flipArrangeInt(arrangeInt, "Vertical")
		firstInt, lastInt = BestMove.getFirstLastArrangeInt(symmArrangeInt)
		moveInt = int(flipMoveInt(bestMove.move_index, "Vertical"))
		save_or_update(firstInt, lastInt, moveInt)


def save_or_update(firstInt, lastInt, moveInt):
	bestMoveInDb = BestMove.objects.filter(first_half_arrangement=firstInt).filter(last_half_arrangement=lastInt)
	if bestMoveInDb.count() == 0:
		newBestMove = BestMove(first_half_arrangement=firstInt, last_half_arrangement=lastInt, move_index=moveInt)
		newBestMove.save()
	else:
		bestMoveInDb.move_index = moveInt
		bestMoveInDb.save()
