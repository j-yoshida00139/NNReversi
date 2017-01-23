import sys, os
import game
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/utils')
import basicFunc


def calcWinRatio(arrangeList, nextColor, yourColor):
	numGame, win, games = 100, 0, 0
	for i in range(numGame):
		tmpGame = game.Game(8, 8, basicFunc.unsharedCopy(arrangeList), nextColor)
		while not tmpGame.isEnded():
			tmpGame.goNextWithAutoMove()
		games += 1 if not tmpGame.getWinnersColor() == 0 else 0 # Not even score
		win += 1 if tmpGame.getWinnersColor() == yourColor else 0
	winRatio = win / games * 100.0 if games != 0 else 0.0
	return winRatio
