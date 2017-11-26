from django.core.management.base import BaseCommand
from personal.utils.game import Game
import random


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		num_games = 100
		num_win = 0
		for i in range(0, num_games):
			main_game = Game(8, 8)
			main_game.initialize()
			nn_color = random.choice([main_game.BLACK, main_game.WHITE])
			while not main_game.is_ended():
				nn_flag = True if main_game.nextColor == nn_color else False
				main_game.go_next_with_auto_move(nn_flag)
			print("%s games was finished. BLACK:%d WHITE:%d" % (
				i, main_game.get_score(main_game.BLACK), main_game.get_score(main_game.WHITE)))
			if main_game.get_winners_color() == nn_color:
				print("AI wins.")
				num_win += 1
		print("Win : {0}%".format(float(num_win*100.0/num_games)))
