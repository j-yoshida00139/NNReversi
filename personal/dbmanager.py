"""memo for database schema
create table best_moves(
	id integer primary key AUTOINCREMENT NOT NULL,
	first_half_arrangement int NOT NULL,
	last_half_arrangement int NOT NULL,
	move_index int NOT NULL,
	created_at DATETIME NOT NULL DEFAULT current_timestamp,
	updated_at timestamp NOT NULL DEFAULT current_timestamp,
	UNIQUE(first_half_arrangement, last_half_arrangement)
);
"""

import sqlite3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/Model')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/utils')
import BestMove
import move_loader
import basicFunc
import numpy as np


def migrateFromText():
	print("getting last file number...")
	maxFileNo = basicFunc.getLastFileNo()
	print("getting whole data...")
	i = 0
	for inputs, outputs in move_loader.get_data_by_list(range(maxFileNo)):
		print(i)
		i += 1
		inputInt = encodeArrangement(inputs)
		firstHalf, lastHalf = divmod(inputInt, int(1E16))
		outIndex = np.argmax(outputs)
		outIndex = int(outIndex)
		bestMove = BestMove.BestMove(first_half_arrangement = firstHalf, last_half_arrangement = lastHalf, move_index = outIndex)
		bestMove.save()


def getFirstAndLastHalf(arrangeInt):
	firstHalf, lastHalf = divmod(arrangeInt, int(1E16))
	return firstHalf, lastHalf


def getWholeArrangeInt(firstInt, lastInt):
	return firstInt * int(1E16) + lastInt


def convNNInputListTo64List(arrangeList):
	arrangeNpArray = np.array(arrangeList).reshape(-1, 3)
	arrange64 = []
	for a, b, c in arrangeNpArray:
		arrange64.append(a * 2 + b * 1 + c * 0)
	return arrange64


def conv64ListToNNInputListForCalc(arrange64List):
	arrangeList = []
	for value in arrange64List:
		if value == 2:
			arrangeList.append(float(1))
			arrangeList.append(float(0))
			arrangeList.append(float(0))
		elif value == 1:
			arrangeList.append(float(0))
			arrangeList.append(float(1))
			arrangeList.append(float(0))
		else:
			arrangeList.append(float(0))
			arrangeList.append(float(0))
			arrangeList.append(float(1))
	return arrangeList


def convLeftRightSymm(arrange64):
	arrange8x8 = np.array(arrange64).reshape(8,8)
	for row in range(8):
		for col in range(4):
			arrange8x8[row][col], arrange8x8[row][7-col] = arrange8x8[row][7-col], arrange8x8[row][col]
	arrange64 = arrange8x8.reshape(64)
	return arrange64


def convLeftRightSymmInt(arrangeInt):
	firstHalf, lastHalf = getFirstAndLastHalf(arrangeInt)
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
	except:
		print("LeftRight converting error! MoveInt is {0}".format(moveInt))
	symmMove64 = convUpDownSymm(move64)
	npMoveArray = np.array(symmMove64)
	convertedMoveInt = np.argmax(npMoveArray)
	if not convertedMoveInt>=0 or not convertedMoveInt<64:
		print("LeftRight converting error. MoveInt is {0}, convertedMoveInt is {1}".format(moveInt, convertedMoveInt))
	return convertedMoveInt


def convUpDownSymm(arrange64):
	arrange8x8 = np.array(arrange64).reshape(8,8)
	for col in range(8):
		for row in range(4):
			arrange8x8[row][col], arrange8x8[7-row][col] = arrange8x8[7-row][col], arrange8x8[row][col]
	arrange64 = arrange8x8.reshape(64)
	return arrange64


def convUpDownSymmInt(arrangeInt):
	firstHalf, lastHalf = getFirstAndLastHalf(arrangeInt)
	arrangeList = decodeArrangement(firstHalf, lastHalf)
	arrange64 = convNNInputListTo64List(arrangeList)
	arrange64 = convUpDownSymm(arrange64)
	newArrangeInt = 0
	for val in arrange64:
		newArrangeInt = newArrangeInt * 3 + int(val)
	return newArrangeInt


def convUpDownSymmIntMove(moveInt):
	try:
		move64 = [0 for x in range(64)]
		move64[moveInt] = 1
	except:
		print("UpDown converting error! MoveInt is {0}".format(moveInt))
	symmMove64 = convUpDownSymm(move64)
	npMoveArray = np.array(symmMove64)
	convertedMoveInt = np.argmax(npMoveArray)
	if not convertedMoveInt>=0 or not convertedMoveInt<64:
		print("UpDown converting error. MoveInt is {0}, convertedMoveInt is {1}".format(moveInt, convertedMoveInt))
	return convertedMoveInt


def encodeArrangement(arrangeList):
	arrangeInt = 0
	np_inputs = np.array(arrangeList).reshape((-1, 3))
	for a, b, c in np_inputs:
		input = int(a * 2 + b * 1 + c * 0)
		arrangeInt = arrangeInt * 3 + input
	return arrangeInt


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
	bestMoveList = BestMove.BestMove.retrieveAll()
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
	bestMoveList = BestMove.BestMove.retrieveAll()
	for bestMove in bestMoveList:
		arrangeInt = getWholeArrangeInt(bestMove.first_half_arrangement, bestMove.last_half_arrangement)

		# Left Right Symmetory Data
		symmArrangeInt = convLeftRightSymmInt(arrangeInt)
		firstInt, lastInt = getFirstAndLastHalf(symmArrangeInt)
		moveInt = int(convLeftRightSymmIntMove(bestMove.move_index))
		if not moveInt < 64:
			print(firstInt, lastInt, bestMove.move_index, moveInt)
			exit()
		newBestMove = BestMove.BestMove(first_half_arrangement=firstInt, last_half_arrangement=lastInt,
										move_index=moveInt)

		if BestMove.BestMove.retrieveFromArrange(firstInt, lastInt) == None:
			newBestMove.save()
			#print("Is inserted.")
		else:
			newBestMove.update()
			#print("Already exists.")

		# Up Down Symmetory Data
		symmArrangeInt = convUpDownSymmInt(arrangeInt)
		firstInt, lastInt = getFirstAndLastHalf(symmArrangeInt)
		moveInt = int(convUpDownSymmIntMove(bestMove.move_index))
		if not moveInt < 64:
			print(firstInt, lastInt, bestMove.move_index, moveInt)
			exit()
		newBestMove = BestMove.BestMove(first_half_arrangement=firstInt, last_half_arrangement=lastInt,
										move_index=moveInt)
		if BestMove.BestMove.retrieveFromArrange(firstInt, lastInt) == None:
			newBestMove.save()
			#print("Is inserted.")
		else:
			newBestMove.update()
			#print("Already exists.")

