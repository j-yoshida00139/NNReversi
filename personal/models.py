from django.db import models
import numpy as np


class BestMove(models.Model):
	first_half_arrangement = models.BigIntegerField(null=False)
	last_half_arrangement = models.BigIntegerField(null=False)
	move_index = models.IntegerField(null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	replicated = models.BooleanField(default=False)

	class Meta:
		unique_together = ('first_half_arrangement', 'last_half_arrangement')

	def save_or_update(self):
		bestMoveInDb = BestMove.objects.filter(
			first_half_arrangement=self.first_half_arrangement).filter(last_half_arrangement=self.last_half_arrangement)
		if bestMoveInDb.count() == 0:
			self.save()
		else:
			bestMove = bestMoveInDb.get()
			bestMove.move_index = self.move_index
			bestMove.save()

	@staticmethod
	def hasMoveData(gameArrange):
		firstHalf, lastHalf = BestMove.encodeToDBArrange(gameArrange)
		countInDB = BestMove.objects.filter(
			first_half_arrangement=firstHalf).filter(last_half_arrangement=lastHalf).count()
		if countInDB == 0:
			return False
		else:
			return True

	@staticmethod
	def encodeToDBArrange(gameArrange):
		arrangeInt = 0
		for i in gameArrange:
			arrangeInt = arrangeInt * 3 + i
		firstInt, lastInt = BestMove.getFirstLastArrangeInt(arrangeInt)
		return firstInt, lastInt

	@staticmethod
	def encodeToNNArrange(arrange2Dim, playerColor):
		nnArrange = []
		arrange1Dim = np.array(arrange2Dim).reshape(64).tolist()
		for color in arrange1Dim:
			if color == 0:
				nnArrange.extend([[float(1)], [float(0)], [float(0)]])
			elif color == playerColor:
				nnArrange.extend([[float(0)], [float(1)], [float(0)]])
			else:
				nnArrange.extend([[float(0)], [float(0)], [float(1)]])
		return nnArrange

	@staticmethod
	def convToGameArrange(colorArrange, playerColor):
		gameArrange = []
		for row_i, row in enumerate(colorArrange):
			for col_i, col in enumerate(row):
				if colorArrange[row_i][col_i] == 0:
					gameArrange.append(2)
				elif colorArrange[row_i][col_i] == playerColor:
					gameArrange.append(1)
				else:
					gameArrange.append(0)
		return gameArrange

	@staticmethod
	def storeBestMove(winnersMove):
		gameArrange = BestMove.convToGameArrange(winnersMove["arrange"], winnersMove["color"])
		firstHalf, lastHalf = BestMove.encodeToDBArrange(gameArrange)
		outIndex = BestMove.encodeToDBMove(winnersMove["row"], winnersMove["col"])
		bestMove = BestMove(first_half_arrangement=firstHalf, last_half_arrangement=lastHalf, move_index=outIndex)
		bestMove.save()

	@staticmethod
	def encodeToDBMove(row, col):
		moveIndex = row * 8 + col
		return moveIndex

	@staticmethod
	def getFirstLastArrangeInt(arrangeInt):
		firstHalf, lastHalf = divmod(arrangeInt, int(1E16))
		return firstHalf, lastHalf

	@staticmethod
	def getWholeArrangeInt(firstInt, lastInt):
		return firstInt * int(1E16) + lastInt
