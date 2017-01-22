import sys, os
import game
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')


def calcWinRatio(arrangeList, nextColor, yourColor):
	numGame = 100
	win = 0
	games = 0
	for i in range(numGame):
		tmpList = game.Game.unshared_copy(arrangeList)
		tmpGame = game.Game(8, 8, tmpList, nextColor)
		while not tmpGame.isEnded():
			move = np.random.rand(1,64) #move[0][0:63]
			index = np.argmax(move[0]*tmpGame.getCanPutList(tmpGame.nextColor))
			row, col = divmod(index, 8)
			tmpGame.putPiece(row, col, tmpGame.nextColor)
			turnPieceList = tmpGame.getTurnPieceList(row, col, tmpGame.nextColor)
			tmpGame.turnPiece(turnPieceList, tmpGame.nextColor)
			tmpGame.goNextTurn()
		if not tmpGame.getWinnersColor() == 0:
			games += 1
		if tmpGame.getWinnersColor() == yourColor:
			win += 1
	if games == 0:
		winRatio = 0.0
	else:
		winRatio = win/games*100.0
	return winRatio
