import math
import sys, os
import csv
from os import listdir
from os.path import isfile, join
import numpy as np


directions = [
	{"row": 0, "col": 1},
	{"row":-1, "col": 1},
	{"row":-1, "col": 0},
	{"row":-1, "col":-1},
	{"row": 0, "col":-1},
	{"row": 1, "col":-1},
	{"row": 1, "col": 0},
	{"row": 1, "col": 1}
]


class Game(object):
	def __init__(self, rows, cols, arrangeList=(), nextColor=0):
		self.rows = rows
		self.cols = cols
		self.NONE  = 0
		self.BLACK = 1
		self.WHITE = 2
		self.arrange = []
		self.nextColor = self.BLACK
		if arrangeList:
			tmpList = list(arrangeList)
			self.arrange = self.unshared_copy(arrangeList)
		if nextColor:
			self.nextColor = nextColor

	def initialize(self):
		self.blackMove = []
		self.whiteMove = []
		self.nextColor = self.BLACK
		upRow   = math.floor((self.rows-1)/2)
		leftCol = math.floor((self.cols-1)/2)
		self.arrange = [[0 for col in range(0, self.cols)] for row in range(0, self.rows)]

		self.putPiece(upRow  , leftCol  , self.BLACK)
		self.putPiece(upRow+1, leftCol  , self.WHITE)
		self.putPiece(upRow  , leftCol+1, self.WHITE)
		self.putPiece(upRow+1, leftCol+1, self.BLACK)

	def clearPiece(self, row, col):
		self.arrange[row][col] = self.NONE

	def putPiece(self, row, col, color):
		self.arrange[row][col] = color

	def canPutPiece(self, row, col, color):
		if self.arrange[row][col]!=self.NONE:
			return False
		if len(self.getTurnPieceList(row, col, color))>0:
			return True
		return False

	def storeMove(self, row, col, color):
		arrangeTpl = Game.list_to_tuple(self.arrange)
		if color==self.BLACK :
			self.blackMove.append({"arrange":arrangeTpl, "color":color, "row":row, "col":col})
		else:
			self.whiteMove.append({"arrange":arrangeTpl, "color":color, "row":row, "col":col})

	def isOutOfRange(self, row, col):
		if row>=self.rows or col>=self.cols or row<0 or col<0:
			return True
		else:
			return False

	def getScore(self, color):
		counter = 0
		for row in range(0, self.rows):
			for col in range(0, self.cols):
				if self.arrange[row][col]==color:
					counter+=1
		return counter

	def getTurnPieceList(self, row, col, color):
		turnPieceList = []
		for i in range(0, len(directions)):
			tmpTurnPieceList = self.getTurnPieceForDirect(row, col, color,  directions[i]['row'], directions[i]['col'])
			if len(tmpTurnPieceList)>0:
				for j in range(0, len(tmpTurnPieceList)):
					turnPieceList.append({"row":tmpTurnPieceList[j]['row'], "col":tmpTurnPieceList[j]['col']})
		return turnPieceList

	def getTurnPieceForDirect(self, row, col, color, y, x):
		turnPieceList = []
		if self.isOutOfRange(row+y, col+x):
			return []

		checkRow = row+y
		checkCol = col+x
		if self.arrange[checkRow][checkCol]==color or self.arrange[checkRow][checkCol]==self.NONE:
			return []

		turnRows = []
		turnCols = []
		turnRows.append(checkRow)
		turnCols.append(checkCol)
		checkRow += y
		checkCol += x

		while not(self.isOutOfRange(checkRow, checkCol)):
			if self.arrange[checkRow][checkCol]==self.NONE:
				return []
			elif self.arrange[checkRow][checkCol]==color:
				for i in range(0, len(turnRows)):
					turnPieceList.append({"row":turnRows[i], "col":turnCols[i]})
				return turnPieceList
			turnRows.append(checkRow)
			turnCols.append(checkCol)
			checkRow += y
			checkCol += x
		return turnPieceList

	def canPutPieceOnBoard(self, color):
		canPutList = self.getCanPutList(color)
		for i in range(0, len(canPutList)):
			if canPutList[i]==1:
				return True
		return False

	def getCanPutList(self, color):
		canPutList = []
		for y in range(0, self.rows):
			for x in range(0, self.cols):
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
		self.nextColor = self.WHITE if self.nextColor==self.BLACK else self.BLACK
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

	@staticmethod
	def returnNnInputList(rawArray, color):
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

	def storeWinnersData(self, winnersData):
		lastFileNo = self.getLastFileNo()

		for i in range(len(winnersData)):
			winnersMove = winnersData[i]
			inputList = Game.returnNnInputList(winnersMove["arrange"], winnersMove["color"])
			fileNo = lastFileNo + i
			fileNameInput = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/input_{0:08d}".format(
				fileNo + 1)
			fileNameOutput = os.path.dirname(
				os.path.abspath(__file__)) + "/nncore/winnersData/output_{0:08d}".format(fileNo + 1)
			fIn = open(fileNameInput + '.csv', 'w')
			fOut = open(fileNameOutput + '.csv', 'w')

			row = winnersMove["row"]
			col = winnersMove["col"]
			moveList = self.returnMoveList(row, col)

			dataWriterIn = csv.writer(fIn)
			dataWriterIn.writerow(Game.returnNnInputStoreList(inputList))
			fIn.close()
			dataWriterOut = csv.writer(fOut)
			dataWriterOut.writerow(moveList)
			fOut.close()

		return True

	@staticmethod
	def getLastFileNo():
		path = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/"
		fileNoList = [Game.retrieveFileNo(f) for f in listdir(path) if isfile(join(path, f))]
		return np.max(fileNoList)

	def returnMoveList(self, row, col):
		u"""Return array which has next move's row and column. (for neural network)
		:param row: row of next move
		:param col: column of next move
		:return: converted array for neural network
		"""
		moveList = []
		for y in range(0, self.rows):
			for x in range(0, self.cols):
				if y==row and x==col:
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

	@staticmethod
	def retrieveFileNo(filename):
		if filename.count(".csv"):
			tmpFileName = filename.replace("input_", "")
			tmpFileName = tmpFileName.replace("output_", "")
			tmpFileName = tmpFileName.replace(".csv", "")
			return int(tmpFileName)
		else:
			return 0

	@staticmethod
	def list_to_tuple(_list):
		tpl = ()
		for elm in _list:
			if isinstance(elm,list):
				tpl += (Game.list_to_tuple(elm),)
			else:
				tpl += (elm,)
		return tpl

	@staticmethod
	def unshared_copy(inList):
		if isinstance(inList, list):
			return list(map(Game.unshared_copy, inList))
		return inList

	def setArrange(self, arrangeList):
		self.arrange = arrangeList
		return True

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