import sys, os
import game
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
import network
import network2
import storeBestMove
import csv

n_input = 192 #366
n_neutral_neuron = 100
n_output = 64 #12

numGames = 10
#numGames = 1

size = [n_input, n_neutral_neuron, n_output]
#net = network.Network(size)
net = network2.Network(size)


numWin = 0

winnersData = []

def storeMove(arrange, row, col, color):
	arrangeTpl = mainGame.list_to_tuple(arrange)
	winnersData.append({"arrange":arrangeTpl, "color":color, "row":row, "col":col})

def storeWinnersData():
	lastFileNo = mainGame.getLastFileNo()
	for i in range(len(winnersData)):
		winnersMove = winnersData[i]
		inputList = mainGame.returnNnInputList(winnersMove["arrange"], winnersMove["color"])
		fileNo = lastFileNo + i
		fileNameInput = os.path.dirname(os.path.abspath(__file__)) + "/nncore/winnersData/input_{0:08d}".format(
			fileNo + 1)
		fileNameOutput = os.path.dirname(
			os.path.abspath(__file__)) + "/nncore/winnersData/output_{0:08d}".format(fileNo + 1)
		fIn = open(fileNameInput + '.csv', 'w')
		fOut = open(fileNameOutput + '.csv', 'w')

		row = winnersMove["row"]
		col = winnersMove["col"]
		moveList = mainGame.returnMoveList(row, col)

		dataWriterIn = csv.writer(fIn)
		dataWriterIn.writerow(mainGame.returnNnInputStoreList(inputList))
		fIn.close()
		dataWriterOut = csv.writer(fOut)
		dataWriterOut.writerow(moveList)
		fOut.close()
	return True

for i in range(0, numGames):
	winnersData = []
	mainGame = game.Game(8, 8)
	mainGame.initialize()
	while not mainGame.isEnded():
		winRatio = 0.0
		bestRow, bestCol = 0, 0
		for index, value in list(enumerate(mainGame.getCanPutList(mainGame.nextColor))):
			if value == 1: # means the piece can be put
				row, col = divmod(index, 8)
				tmpGame = game.Game(8, 8, mainGame.unshared_copy(mainGame.arrange), mainGame.nextColor)
				tmpGame.putPiece(row, col, tmpGame.nextColor)
				turnPieceList = tmpGame.getTurnPieceList(row, col, tmpGame.nextColor)
				tmpGame.turnPiece(turnPieceList, tmpGame.nextColor)
				tmpGame.goNextTurn()
				tmpWinRatio = storeBestMove.calcWinRatio(tmpGame.arrange, tmpGame.nextColor, mainGame.nextColor)
				if tmpWinRatio > winRatio:
					bestRow, bestCol, winRatio = row, col, tmpWinRatio
				print("row, col, color, winRatio:", row, col, mainGame.nextColor, tmpWinRatio)
		print("Best move is row:%d, col:%d, win ratio:%d" % (bestRow, bestCol, winRatio))

		print("==================== Calculating was finished. ====================")
		print("==================== Calculating was finished. ====================")
		print("==================== Calculating was finished. ====================")
		storeMove(mainGame.arrange, bestRow, bestCol, mainGame.nextColor)

		arrangeList = mainGame.returnNnInputList(mainGame.arrange, mainGame.nextColor)
		if mainGame.nextColor==mainGame.BLACK:
			move = net.feedforward(arrangeList) #move[0][0:63]
		else:
			move = np.random.rand(1,64) #move[0][0:63]
		index = np.argmax(move[0]*mainGame.getCanPutList(mainGame.nextColor))
		row, col = divmod(index, 8)

		mainGame.storeMove(row, col, mainGame.nextColor)
		mainGame.putPiece(row, col, mainGame.nextColor)

		turnPieceList = mainGame.getTurnPieceList(row, col, mainGame.nextColor)
		mainGame.turnPiece(turnPieceList, mainGame.nextColor)
		mainGame.goNextTurn()

	print("%s games was finished. BLACK:%d WHITE:%d" % (i, mainGame.getScore(mainGame.BLACK), mainGame.getScore(mainGame.WHITE)))
	storeWinnersData()

	if mainGame.getScore(mainGame.BLACK) > mainGame.getScore(mainGame.WHITE):
		numWin += 1

print("Win : %s" % numWin)

