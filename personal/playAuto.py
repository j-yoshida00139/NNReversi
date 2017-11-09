# import sys, os
# import game
# import numpy as np
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/utils')
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/Model')
# import network
# import storeBestMove
# import csv
# import basicFunc
# import BestMove
# import dbmanager
# from datetime import datetime
#
# n_input = 192 #366
# n_neutral_neuron = 100
# n_output = 64 #12
#
# numGames = 500
# #numGames = 1
# numWin = 0
#
# size = [n_input, n_neutral_neuron, n_output]
# net = network.Network()
# #net = network2_edit.Network(size)
#
# simulateFlg=1
#
# for i in range(0, numGames):
# 	winnersData = []
# 	mainGame = game.Game(8, 8)
# 	mainGame.initialize()
# 	while not mainGame.isEnded():
# 		if simulateFlg == 1:
# 			inputList = basicFunc.conv64ListToNnInputList(mainGame.arrange, mainGame.nextColor)
# 			inputInt = dbmanager.encodeArrangement(inputList)
# 			firstHalfInt, lastHalfInt = divmod(inputInt, int(1E16))
# 			bestMove = BestMove.BestMove.retrieveFromArrange(firstHalfInt, lastHalfInt)
# 			if bestMove == None:
# 				bestRow, bestCol, winRatio = mainGame.findBestMove()
# 				print("Best move is row:%d, col:%d, nextColor:%d, win ratio:%d %s" % (bestRow, bestCol, mainGame.nextColor, winRatio, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
# 				tmpArrangeList = basicFunc.unsharedCopy(mainGame.arrange)
# 				winnersData.append({"arrange":tmpArrangeList, "color":mainGame.nextColor, "row":bestRow, "col":bestCol})
# 			else:
# 				print("Best move is already exist.")
#
# 			if mainGame.nextColor==mainGame.BLACK:
# 				mainGame.goNextWithAutoMove(True) # with Neural Network move
# 			else:
# 				mainGame.goNextWithAutoMove() # with random move
# 	print("%s games was finished. BLACK:%d WHITE:%d" % (i, mainGame.getScore(mainGame.BLACK), mainGame.getScore(mainGame.WHITE)))
# 	basicFunc.storeWinnersData(winnersData)
#
# 	if mainGame.getScore(mainGame.BLACK) > mainGame.getScore(mainGame.WHITE):
# 		numWin += 1
#
# print("Win : %s" % numWin)
