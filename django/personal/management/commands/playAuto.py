from datetime import datetime

from django.core.management.base import BaseCommand

from personal.models import BestMove
from personal.utils import basicFunc, game

# numGames = 500
numGames = 10


class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		numWin = 0
		simulateFlg = 1

		for i in range(0, numGames):
			mainGame = game.Game(8, 8)
			mainGame.initialize()
			while not mainGame.is_ended():
				if simulateFlg == 1:
					gameArrange = BestMove.conv_to_game_arrange(mainGame.arrange, mainGame.nextColor)
					if not BestMove.has_move_data(gameArrange):
						bestRow, bestCol, winRatio = mainGame.find_best_move()
						print("Best move is row:%d, col:%d, nextColor:%d, win ratio:%d %s" % (
							bestRow, bestCol, mainGame.nextColor, winRatio, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
						tmpArrangeList = basicFunc.unshared_copy(mainGame.arrange)
						winnersMove = {"arrange": tmpArrangeList, "color": mainGame.nextColor, "row": bestRow, "col": bestCol}
						BestMove.store_best_move(winnersMove)
					else:
						print("Best move is already exist.")

					if mainGame.nextColor == mainGame.BLACK:
						mainGame.go_next_with_auto_move(True)  # with Neural Network move
					else:
						mainGame.go_next_with_auto_move()  # with random move
			print("%s games was finished. BLACK:%d WHITE:%d" % (
				i, mainGame.get_score(mainGame.BLACK), mainGame.get_score(mainGame.WHITE)))

			if mainGame.get_score(mainGame.BLACK) > mainGame.get_score(mainGame.WHITE):
				numWin += 1
		print("Win : %s" % numWin)
