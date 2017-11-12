from django.db import models
# from personal.utils import basicFunc
# from personal import dbmanager
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
	def hasMoveData(winnersMove):
		inputList = BestMove.conv64ListToNnInputList(winnersMove["arrange"], winnersMove["color"])
		inputInt = BestMove.encodeArrangement(inputList)
		firstHalfInt, lastHalfInt = divmod(inputInt, int(1E16))
		bestMove = BestMove.objects.filter(
			first_half_arrangement=firstHalfInt).filter(last_half_arrangement=lastHalfInt).count()
		if bestMove == 0:
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

	# @staticmethod
	# def unsharedCopy(inList):
	# 	if isinstance(inList, list):
	# 		return list(map(unsharedCopy, inList))
	# 	return inList
