from datetime import datetime
from django.core.management.base import BaseCommand
from ...models import BestMove
from ...utils import basicFunc, game
import random

# numGames = 500
numGames = 10


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		num_win = 0
		for i in range(0, numGames):
			main_game = game.Game(8, 8)
			main_game.initialize()
			while not main_game.is_ended():
				game_arrange = BestMove.conv_to_game_arrange(main_game.arrange, main_game.nextColor)
				if not BestMove.has_move_data(game_arrange):
					best_row, best_col, win_ratio = main_game.find_best_move()
					print("Best move is row:%d, col:%d, nextColor:%d, win ratio:%d %s" % (
						best_row, best_col, main_game.nextColor, win_ratio, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
					tmp_arrange_list = basicFunc.unshared_copy(main_game.arrange)
					winners_move = {"arrange": tmp_arrange_list, "color": main_game.nextColor, "row": best_row, "col": best_col}
					BestMove.store_best_move(winners_move)
				else:
					print("Best move is already exist.")
				main_game.go_next_with_auto_move(random.choice([True, False]))
			print("%s games was finished. BLACK:%d WHITE:%d" % (
				i, main_game.get_score(main_game.BLACK), main_game.get_score(main_game.WHITE)))

			if main_game.get_score(main_game.BLACK) > main_game.get_score(main_game.WHITE):
				num_win += 1
		print("Win : %s" % num_win)
