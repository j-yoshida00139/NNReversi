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
		print(firstHalf, lastHalf)
		bestMove = BestMove.BestMove(first_half_arrangement = firstHalf, last_half_arrangement = lastHalf, move_index = outIndex)
		bestMove.save()

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
	#arrangements = np.array([])
	arrangements = []
	for tmpArrangement in tmpArrangements:
		if tmpArrangement == 2:
			arrangements.extend([1.0, 0.0, 0.0])
			#arrangements = np.append(arrangements, [1.0, 0.0, 0.0])
		elif tmpArrangement == 1:
			arrangements.extend([0.0, 1.0, 0.0])
			#arrangements = np.append(arrangements, [0.0, 1.0, 0.0])
		elif tmpArrangement == 0:
			arrangements.extend([0.0, 0.0, 1.0])
			#arrangements = np.append(arrangements, [0.0, 0.0, 1.0])
	return arrangements

def decodeMove(moveIndex):
	moveList = [0.0 for x in range(64)]
	moveList[moveIndex] = 1.0
	return moveList


def get_data_by_list(n_list):
	bestMoveList = BestMove.BestMove.retrieveAll()
	arrangementList = []
	moveList = []
	for bestMove in bestMoveList:
		arrangementList.append(decodeArrangement(bestMove.first_half_arrangement, bestMove.last_half_arrangement))
		moveList.append(decodeMove(bestMove.move_index))
	arrangementList = [np.reshape(x, (192, 1)) for x in arrangementList]
	moveList = [np.reshape(x, (64, 1)) for x in moveList]
	allResultList = list(zip(arrangementList, moveList))
	resultList = []
	for i in n_list:
		resultList.append(allResultList[i])
	return resultList
