import numpy as np
from personal import game


def unsharedCopy(inList):
	if isinstance(inList, list):
		return list(map(unsharedCopy, inList))
	return inList


def convInput(input_array):
	input_tmp_array = []
	for input_data in input_array:
		input_tmp_array.append(input_data[0])
	input_array = input_tmp_array
	input_nparray = np.array([])

	tmp = np.array([])
	tmp = np.append(tmp, np.array([input_array[x] for x in range(0, 192, 3)]).reshape(8, 8))
	tmp = np.append(tmp, np.array([input_array[x] for x in range(1, 192, 3)]).reshape(8, 8))
	tmp = np.append(tmp, np.array([input_array[x] for x in range(2, 192, 3)]).reshape(8, 8))
	input_nparray = np.append(input_nparray, tmp)
	input_nparray = input_nparray.reshape(1, 3, 8, 8)
	return input_nparray


def calcWinRatio(arrangeList, nextColor, yourColor):
	numGame, win, games = 100, 0, 0
	for i in range(numGame):
		tmpGame = game.Game(8, 8, unsharedCopy(arrangeList), nextColor)
		while not tmpGame.isEnded():
			tmpGame.goNextWithAutoMove()
		games += 1 if not tmpGame.getWinnersColor() == 0 else 0 # Not even score
		win += 1 if tmpGame.getWinnersColor() == yourColor else 0
	winRatio = win / games * 100.0 if games != 0 else 0.0
	return winRatio
