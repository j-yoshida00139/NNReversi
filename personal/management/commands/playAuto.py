from django.core.management.base import BaseCommand
from datetime import datetime
from personal import game
from personal.models import BestMove
from personal.utils import basicFunc

# numGames = 500
numGames = 1


class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		numWin = 0
		simulateFlg = 1

		for i in range(0, numGames):
			mainGame = game.Game(8, 8)
			mainGame.initialize()
			while not mainGame.isEnded():
				if simulateFlg == 1:
					if not BestMove.hasMoveData(mainGame.arrange, mainGame.nextColor):
						bestRow, bestCol, winRatio = mainGame.findBestMove()
						print("Best move is row:%d, col:%d, nextColor:%d, win ratio:%d %s" % (
							bestRow, bestCol, mainGame.nextColor, winRatio, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
						tmpArrangeList = basicFunc.unsharedCopy(mainGame.arrange)
						winnersMove = {"arrange": tmpArrangeList, "color": mainGame.nextColor, "row": bestRow, "col": bestCol}
						BestMove.storeBestMove(winnersMove)
					else:
						print("Best move is already exist.")

					if mainGame.nextColor == mainGame.BLACK:
						mainGame.goNextWithAutoMove(True)  # with Neural Network move
					else:
						mainGame.goNextWithAutoMove()  # with random move
			print("%s games was finished. BLACK:%d WHITE:%d" % (
				i, mainGame.getScore(mainGame.BLACK), mainGame.getScore(mainGame.WHITE)))

			if mainGame.getScore(mainGame.BLACK) > mainGame.getScore(mainGame.WHITE):
				numWin += 1
		print("Win : %s" % numWin)
