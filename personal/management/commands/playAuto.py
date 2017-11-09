from django.core.management.base import BaseCommand
from datetime import datetime
from personal import game
from personal import dbmanager
from personal.models import BestMove
# from personal.nncore import network
from personal.utils import basicFunc

n_input = 192  # 366
n_neutral_neuron = 100
n_output = 64  # 12

numGames = 500
# numGames = 1

# size = [n_input, n_neutral_neuron, n_output]
# net = network.Network()


class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		numWin = 0
		simulateFlg = 1

		for i in range(0, numGames):
			winnersData = []
			mainGame = game.Game(8, 8)
			mainGame.initialize()
			while not mainGame.isEnded():
				if simulateFlg == 1:
					inputList = basicFunc.conv64ListToNnInputList(mainGame.arrange, mainGame.nextColor)
					inputInt = dbmanager.encodeArrangement(inputList)
					firstHalfInt, lastHalfInt = divmod(inputInt, int(1E16))
					bestMove = BestMove.objects.filter(
						first_half_arrangement=firstHalfInt).filter(last_half_arrangement=lastHalfInt).count()
					if bestMove == 0:
						bestRow, bestCol, winRatio = mainGame.findBestMove()
						print("Best move is row:%d, col:%d, nextColor:%d, win ratio:%d %s" % (
							bestRow, bestCol, mainGame.nextColor, winRatio, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
						tmpArrangeList = basicFunc.unsharedCopy(mainGame.arrange)
						winnersData.append({
							"arrange": tmpArrangeList, "color": mainGame.nextColor, "row": bestRow, "col": bestCol})
					else:
						print("Best move is already exist.")

					if mainGame.nextColor == mainGame.BLACK:
						mainGame.goNextWithAutoMove(True)  # with Neural Network move
					else:
						mainGame.goNextWithAutoMove()  # with random move
			print("%s games was finished. BLACK:%d WHITE:%d" % (
				i, mainGame.getScore(mainGame.BLACK), mainGame.getScore(mainGame.WHITE)))
			basicFunc.storeWinnersData(winnersData)

			if mainGame.getScore(mainGame.BLACK) > mainGame.getScore(mainGame.WHITE):
				numWin += 1
		print("Win : %s" % numWin)
