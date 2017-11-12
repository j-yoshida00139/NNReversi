import numpy as np
from personal.models import BestMove


def convNNInputListTo64List(arrangeList):
	arrangeNpArray = np.array(arrangeList).reshape(-1, 3)
	arrange64 = []
	for a, b, c in arrangeNpArray:
		arrange64.append(a * 2 + b * 1 + c * 0)
	return arrange64


def convLeftRightSymm(arrange64):
	arrange8x8 = np.array(arrange64).reshape(8, 8)
	for row in range(8):
		for col in range(4):
			arrange8x8[row][col], arrange8x8[row][7-col] = arrange8x8[row][7-col], arrange8x8[row][col]
	arrange64 = arrange8x8.reshape(64)
	return arrange64


def convLeftRightSymmInt(arrangeInt):
	firstHalf, lastHalf = BestMove.getFirstAndLastHalf(arrangeInt)
	arrangeList = decodeArrangement(firstHalf, lastHalf)
	arrange64 = convNNInputListTo64List(arrangeList)
	arrange64 = convLeftRightSymm(arrange64)
	newArrangeInt = 0
	for val in arrange64:
		newArrangeInt = newArrangeInt * 3 + int(val)
	return newArrangeInt


def convLeftRightSymmIntMove(moveInt):
	try:
		move64 = [0 for x in range(64)]
		move64[moveInt] = 1
		symmMove64 = convUpDownSymm(move64)
		npMoveArray = np.array(symmMove64)
		convertedMoveInt = np.argmax(npMoveArray)
		if not convertedMoveInt >= 0 or not convertedMoveInt < 64:
			print(
				"LeftRight converting error. MoveInt is {0}, convertedMoveInt is {1}".format(moveInt, convertedMoveInt))
	except:
		print("LeftRight converting error! MoveInt is {0}".format(moveInt))
	return convertedMoveInt


def convUpDownSymm(arrange64):
	arrange8x8 = np.array(arrange64).reshape(8, 8)
	for col in range(8):
		for row in range(4):
			arrange8x8[row][col], arrange8x8[7-row][col] = arrange8x8[7-row][col], arrange8x8[row][col]
	arrange64 = arrange8x8.reshape(64)
	return arrange64


def convUpDownSymmInt(arrangeInt):
	firstHalf, lastHalf = BestMove.getFirstAndLastHalf(arrangeInt)
	arrangeList = decodeArrangement(firstHalf, lastHalf)
	arrange64 = convNNInputListTo64List(arrangeList)
	arrange64 = convUpDownSymm(arrange64)
	newArrangeInt = 0
	for val in arrange64:
		newArrangeInt = newArrangeInt * 3 + int(val)
	return newArrangeInt


def convUpDownSymmIntMove(moveInt):
	move64 = [0 for x in range(64)]
	move64[moveInt] = 1
	symmMove64 = convUpDownSymm(move64)
	npMoveArray = np.array(symmMove64)
	convertedMoveInt = np.argmax(npMoveArray)
	if not convertedMoveInt >= 0 or not convertedMoveInt < 64:
		print("UpDown converting error. MoveInt is {0}, convertedMoveInt is {1}".format(moveInt, convertedMoveInt))
	return convertedMoveInt


def decodeArrangement(first_half, last_half):
	arrangement_int = first_half * int(1E16) + last_half
	tmpArrangements = []
	for i in range(64):
		arrangement_int, tmp_a = divmod(arrangement_int, 3)
		tmpArrangements.append(tmp_a)
	tmpArrangements.reverse()
	arrangements = []
	for tmpArrangement in tmpArrangements:
		if tmpArrangement == 2:
			arrangements.extend([1.0, 0.0, 0.0])
		elif tmpArrangement == 1:
			arrangements.extend([0.0, 1.0, 0.0])
		elif tmpArrangement == 0:
			arrangements.extend([0.0, 0.0, 1.0])
	return arrangements


def decodeMove(moveIndex):
	moveList = [0.0 for x in range(64)]
	moveList[moveIndex] = 1.0
	return moveList


def get_data_by_list(n_list):
	# bestMoveList = BestMove.BestMove.retrieveAll()
	bestMoveList = BestMove.objects.all()
	tmparrangementList = []
	tmpmoveList = []
	for bestMove in bestMoveList:
		tmparrangementList.append(decodeArrangement(bestMove.first_half_arrangement, bestMove.last_half_arrangement))
		tmpmoveList.append(decodeMove(bestMove.move_index))
	arrangementList = []
	moveList = []
	for i in n_list:
		arrangementList.append(tmparrangementList[i])
		moveList.append(tmpmoveList[i])
	arrangementList = np.array([np.reshape(x, (192)) for x in arrangementList])
	moveList = np.array([np.reshape(x, (64)) for x in moveList])
	return arrangementList, moveList


def replicateMoveData():
	# bestMoveList = BestMove.BestMove.retrieveAll()
	bestMoveList = BestMove.objects.all()
	for bestMove in bestMoveList:
		arrangeInt = BestMove.getWholeArrangeInt(bestMove.first_half_arrangement, bestMove.last_half_arrangement)

		# Left Right Symmetry Data
		symmArrangeInt = convLeftRightSymmInt(arrangeInt)
		firstInt, lastInt = BestMove.getFirstAndLastHalf(symmArrangeInt)
		moveInt = int(convLeftRightSymmIntMove(bestMove.move_index))
		if not moveInt < 64:
			print(firstInt, lastInt, bestMove.move_index, moveInt)
			exit()
		save_or_update(firstInt, lastInt, moveInt)

		# Up Down Symmetry Data
		symmArrangeInt = convUpDownSymmInt(arrangeInt)
		firstInt, lastInt = BestMove.getFirstAndLastHalf(symmArrangeInt)
		moveInt = int(convUpDownSymmIntMove(bestMove.move_index))
		if not moveInt < 64:
			print(firstInt, lastInt, bestMove.move_index, moveInt)
			exit()
		save_or_update(firstInt, lastInt, moveInt)


def save_or_update(firstInt, lastInt, moveInt):
	bestMoveInDb = BestMove.objects.filter(first_half_arrangement=firstInt).filter(last_half_arrangement=lastInt)
	if bestMoveInDb.count() == 0:
		newBestMove = BestMove(first_half_arrangement=firstInt, last_half_arrangement=lastInt, move_index=moveInt)
		newBestMove.save()
	else:
		bestMoveInDb.move_index = moveInt
		bestMoveInDb.save()
