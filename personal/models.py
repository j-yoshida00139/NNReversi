from django.db import models
import numpy as np


class BestMove(models.Model):
	first_half_arrangement = models.BigIntegerField(null=False)
	last_half_arrangement = models.BigIntegerField(null=False)
	move_index = models.IntegerField(null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('first_half_arrangement', 'last_half_arrangement')

	@staticmethod
	def hasMoveData(arrange, color):
		firstHalf, lastHalf = BestMove.convArrangeToDBInput(arrange, color)
		countInDB = BestMove.objects.filter(
			first_half_arrangement=firstHalf).filter(last_half_arrangement=lastHalf).count()
		if countInDB == 0:
			return False
		else:
			return True

	@staticmethod
	def encodeArrangement(arrangeList):
		arrangeInt = 0
		np_inputs = np.array(arrangeList).reshape((-1, 3))
		for a, b, c in np_inputs:
			input_data = int(a * 2 + b * 1 + c * 0)
			arrangeInt = arrangeInt * 3 + input_data
		return arrangeInt

	@staticmethod
	def conv64ListToNnInputList(rawArray, color):
		arrangeList = []
		for cols in rawArray:
			for value in cols:
				if value == 0:
					arrangeList.append([float(1)])
					arrangeList.append([float(0)])
					arrangeList.append([float(0)])
				elif value == color:
					arrangeList.append([float(0)])
					arrangeList.append([float(1)])
					arrangeList.append([float(0)])
				else:
					arrangeList.append([float(0)])
					arrangeList.append([float(0)])
					arrangeList.append([float(1)])
		return arrangeList

	@staticmethod
	def storeBestMove(winnersMove):
		firstHalf, lastHalf = BestMove.convArrangeToDBInput(winnersMove["arrange"], winnersMove["color"])
		outIndex = BestMove.convMoveIndexToDBInput(winnersMove["row"], winnersMove["col"])
		bestMove = BestMove(first_half_arrangement=firstHalf, last_half_arrangement=lastHalf, move_index=outIndex)
		bestMove.save()

	@staticmethod
	def convArrangeToDBInput(arrange, color):
		inputList = BestMove.conv64ListToNnInputList(arrange, color)
		inputInt = BestMove.encodeArrangement(inputList)
		firstHalf, lastHalf = BestMove.getFirstAndLastHalf(inputInt)
		return firstHalf, lastHalf

	@staticmethod
	def convMoveIndexToDBInput(row, col):
		moveIndex = row * 8 + col
		return moveIndex

	@staticmethod
	def getFirstAndLastHalf(arrangeInt):
		firstHalf, lastHalf = divmod(arrangeInt, int(1E16))
		return firstHalf, lastHalf

	@staticmethod
	def getWholeArrangeInt(firstInt, lastInt):
		return firstInt * int(1E16) + lastInt
