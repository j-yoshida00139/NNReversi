import sys, os
import game
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/utils')
import network
import network2
import storeBestMove
import csv
import basicFunc

n_input = 192 #366
n_neutral_neuron = 100
n_output = 64 #12

numGames = 100
#numGames = 1
numWin = 0

size = [n_input, n_neutral_neuron, n_output]
#net = network.Network(size)
net = network2.Network(size)

simulateFlg=1

for i in range(0, numGames):
	winnersData = []
	mainGame = game.Game(8, 8)
	mainGame.initialize()
	while not mainGame.isEnded():
		if simulateFlg == 1:
			bestRow, bestCol, winRatio = mainGame.findBestMove()
			print("Best move is row:%d, col:%d, nextColor:%d, win ratio:%d" % (bestRow, bestCol, mainGame.nextColor, winRatio))
			tmpArrangeList = basicFunc.unsharedCopy(mainGame.arrange)
			winnersData.append({"arrange":tmpArrangeList, "color":mainGame.nextColor, "row":bestRow, "col":bestCol})
		if mainGame.nextColor==mainGame.BLACK:
			mainGame.goNextWithAutoMove(True) # with Neural Network move
		else:
			mainGame.goNextWithAutoMove() # with random move
	print("%s games was finished. BLACK:%d WHITE:%d" % (i, mainGame.getScore(mainGame.BLACK), mainGame.getScore(mainGame.WHITE)))
	basicFunc.storeWinnersData(winnersData)

	if mainGame.getScore(mainGame.BLACK) > mainGame.getScore(mainGame.WHITE):
		numWin += 1

print("Win : %s" % numWin)
