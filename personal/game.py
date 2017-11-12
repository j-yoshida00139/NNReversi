from personal.nncore import network
from personal.utils import basicFunc
from personal.utils import mathFunc
from personal import storeBestMove
import math
import numpy as np

directions = [
	{"row":  0, "col":  1},
	{"row": -1, "col":  1},
	{"row": -1, "col":  0},
	{"row": -1, "col": -1},
	{"row":  0, "col": -1},
	{"row":  1, "col": -1},
	{"row":  1, "col":  0},
	{"row":  1, "col":  1}
]

net = network.Network()


class Game(object):
	def __init__(self, rows, cols, arrangeList=[], nextColor=0):
		self.rows = rows
		self.cols = cols
		self.NONE = 0
		self.BLACK = 1
		self.WHITE = 2
		self.arrange = arrangeList
		self.blackMove = []
		self.whiteMove = []
		self.nextColor = self.BLACK if nextColor == 0 else nextColor
		self.net = net

	def initialize(self):
		upRow = math.floor((self.rows-1)/2)
		leftCol = math.floor((self.cols-1)/2)
		self.arrange = [[0 for col in range(0, self.cols)] for row in range(0, self.rows)]
		self.putPiece(upRow,   leftCol,   self.BLACK)
		self.putPiece(upRow+1, leftCol,   self.WHITE)
		self.putPiece(upRow,   leftCol+1, self.WHITE)
		self.putPiece(upRow+1, leftCol+1, self.BLACK)

	def clearPiece(self, row, col):
		self.arrange[row][col] = self.NONE

	def putPiece(self, row, col, color):
		self.arrange[row][col] = color

	def canPutPiece(self, row, col, color):
		if self.arrange[row][col] != self.NONE:
			return False
		if len(self.getTurnPieceList(row, col, color)) > 0:
			return True
		return False

	def storeMove(self, row, col, color):
		tmpArrangeList = basicFunc.unsharedCopy(self.arrange)
		if color == self.BLACK:
			self.blackMove.append({"arrange": tmpArrangeList, "color": color, "row": row, "col": col})
		else:
			self.whiteMove.append({"arrange": tmpArrangeList, "color": color, "row": row, "col": col})

	def isOutOfRange(self, row, col):
		if row >= self.rows or col >= self.cols or row < 0 or col < 0:
			return True
		else:
			return False

	def getScore(self, color):
		counter = 0
		for row in range(0, self.rows):
			for col in range(0, self.cols):
				if self.arrange[row][col] == color:
					counter += 1
		return counter

	def getTurnPieceList(self, row, col, color):
		turnPieceList = []
		for i in range(0, len(directions)):
			tmpTurnPieceList = self.getTurnPieceForDirect(row, col, color,  directions[i]['row'], directions[i]['col'])
			for j in range(len(tmpTurnPieceList)):
				turnPieceList.append({"row": tmpTurnPieceList[j]['row'], "col": tmpTurnPieceList[j]['col']})
		return turnPieceList

	def getTurnPieceForDirect(self, row, col, color, y, x):
		checkRow, checkCol = row+y, col+x
		if self.isOutOfRange(checkRow, checkCol):
			return []

		if self.arrange[checkRow][checkCol] == color or self.arrange[checkRow][checkCol] == self.NONE:
			return []

		turnPieceList, turnRows, turnCols = [], [], []
		turnRows.append(checkRow)
		turnCols.append(checkCol)
		checkRow += y
		checkCol += x

		while not(self.isOutOfRange(checkRow, checkCol)):
			if self.arrange[checkRow][checkCol] == self.NONE:
				return []
			elif self.arrange[checkRow][checkCol] == color:
				for i in range(0, len(turnRows)):
					turnPieceList.append({"row": turnRows[i], "col": turnCols[i]})
				return turnPieceList
			turnRows.append(checkRow)
			turnCols.append(checkCol)
			checkRow += y
			checkCol += x
		return turnPieceList

	def canPutPieceOnBoard(self, color):
		canPutList = self.getCanPutList(color)
		for canPut in canPutList:
			if canPut == 1:
				return True
		return False

	def getCanPutList(self, color):
		canPutList = []
		for y in range(self.rows):
			for x in range(self.cols):
				if self.canPutPiece(y, x, color):
					canPutList.append(1)
				else:
					canPutList.append(0)
		return canPutList

	def getWinnersData(self):
		if self.getScore(self.BLACK) > self.getScore(self.WHITE):
			return self.blackMove
		else:
			return self.whiteMove

	def goNextTurn(self):
		self.nextColor = self.WHITE if self.nextColor == self.BLACK else self.BLACK
		if self.canPutPieceOnBoard(self.nextColor):
			return True
		else:
			self.nextColor = self.WHITE if self.nextColor == self.BLACK else self.BLACK
			if self.canPutPieceOnBoard(self.nextColor):
				return True
			else:
				return False

	def turnPiece(self, turnPieceList, color):
		for i in range(0, len(turnPieceList)):
			self.putPiece(turnPieceList[i]["row"], turnPieceList[i]["col"], color)

	def returnMoveList(self, row, col):
		u"""Return array which has next move's row and column. (for neural network)
		:param row: row of next move
		:param col: column of next move
		:return: converted array for neural network
		"""
		moveList = []
		for y in range(0, self.rows):
			for x in range(0, self.cols):
				if y == row and x == col:
					moveList.append(float(1))
				else:
					moveList.append(float(0))
		return moveList

	@staticmethod
	def returnNnInputStoreList(rawArray):
		arrangeList = []
		for value in rawArray:
			arrangeList.append(value[0])
		return arrangeList

	def setNextColor(self, nextColor):
		self.nextColor = nextColor
		return True

	def isEnded(self):
		if self.canPutPieceOnBoard(self.WHITE) or self.canPutPieceOnBoard(self.BLACK):
			return False
		else:
			return True

	def getWinnersColor(self):
		if self.getScore(self.BLACK) > self.getScore(self.WHITE):
			return self.BLACK
		elif self.getScore(self.BLACK) < self.getScore(self.WHITE):
			return self.WHITE
		else:
			return self.NONE

	def goNextWithAutoMove(self, nnFlag=False):
		if nnFlag:
			arrangeList = basicFunc.conv64ListToNnInputList(self.arrange, self.nextColor)
			arrangeList = basicFunc.convInput(arrangeList)
			move = self.net.feedforward(np.array(arrangeList))  # move[0][0:63]
			# move = self.net.feedforward(np.array(arrangeList).T)  # move[0][0:63]
			move = mathFunc.softmax(move)
		else:
			move = np.random.rand(1,64) #move[0][0:63]
		index = np.argmax(move[0]*self.getCanPutList(self.nextColor))
		row, col = divmod(index, 8)
		self.goNextWithManualMove(row, col)

	def goNextWithManualMove(self, row, col):
		self.storeMove(row, col, self.nextColor)
		self.putPiece(row, col, self.nextColor)
		turnPieceList = self.getTurnPieceList(row, col, self.nextColor)
		self.turnPiece(turnPieceList, self.nextColor)
		self.goNextTurn()

	def findBestMove(self):
		winRatio, bestRow, bestCol = 0.0, 0, 0
		for index, value in list(enumerate(self.getCanPutList(self.nextColor))):
			if value == 0:  # means the piece cannot be put
				continue
			tmpGame = Game(8, 8, basicFunc.unsharedCopy(self.arrange), self.nextColor)
			row, col = divmod(index, 8)
			tmpGame.goNextWithManualMove(row, col)
			tmpWinRatio = storeBestMove.calcWinRatio(tmpGame.arrange, tmpGame.nextColor, self.nextColor)
			# print("    row:%d, col:%d, WinRatio:%f" % (row, col, tmpWinRatio))
			if tmpWinRatio >= winRatio:
				bestRow, bestCol, winRatio = row, col, tmpWinRatio
		return bestRow, bestCol, winRatio
