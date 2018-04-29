from django.db import models
import numpy as np


class BestMove(models.Model):
	first_half_arrangement = models.BigIntegerField(null=False)
	last_half_arrangement = models.BigIntegerField(null=False)
	move_index = models.IntegerField(null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	replicated = models.BooleanField(default=False)

	class Meta:
		unique_together = ('first_half_arrangement', 'last_half_arrangement')

	def save_or_update(self):
		best_move_in_db = BestMove.objects.filter(
			first_half_arrangement=self.first_half_arrangement).filter(last_half_arrangement=self.last_half_arrangement)
		if best_move_in_db.count() == 0:
			self.save()
		else:
			best_move = best_move_in_db.get()
			best_move.move_index = self.move_index
			best_move.save()

	@staticmethod
	def has_move_data(game_arrange):
		first_half, last_half = BestMove.encode_to_db_arrange(game_arrange)
		count_in_db = BestMove.objects.filter(
			first_half_arrangement=first_half).filter(last_half_arrangement=last_half).count()
		if count_in_db == 0:
			return False
		else:
			return True

	@staticmethod
	def encode_to_db_arrange(game_arrange):
		arrange_int = 0
		for i in game_arrange:
			arrange_int = arrange_int * 3 + i
		first_int, last_int = BestMove.get_first_last_arrange_int(arrange_int)
		return first_int, last_int

	@staticmethod
	def encode_to_nn_arrange(arrange_2dim, player_color):
		nn_arrange = []
		arrange_1dim = np.array(arrange_2dim).reshape(64).tolist()
		for color in arrange_1dim:
			if color == 0:
				nn_arrange.extend([[float(0)], [float(0)], [float(1)]])
			elif color == player_color:
				nn_arrange.extend([[float(0)], [float(1)], [float(0)]])
			else:
				nn_arrange.extend([[float(1)], [float(0)], [float(0)]])
		return nn_arrange

	@staticmethod
	def conv_to_game_arrange(color_arrange, player_color):
		game_arrange = []
		for row_i, row in enumerate(color_arrange):
			for col_i, col in enumerate(row):
				if color_arrange[row_i][col_i] == 0:
					game_arrange.append(0)
				elif color_arrange[row_i][col_i] == player_color:
					game_arrange.append(1)
				else:
					game_arrange.append(2)
		return game_arrange

	@staticmethod
	def store_best_move(winners_move):
		game_arrange = BestMove.conv_to_game_arrange(winners_move["arrange"], winners_move["color"])
		first_half, last_half = BestMove.encode_to_db_arrange(game_arrange)
		out_index = BestMove.encode_to_db_move(winners_move["row"], winners_move["col"])
		best_move = BestMove(first_half_arrangement=first_half, last_half_arrangement=last_half, move_index=out_index)
		best_move.save()

	@staticmethod
	def encode_to_db_move(row, col):
		move_index = row * 8 + col
		return move_index

	@staticmethod
	def get_first_last_arrange_int(arrange_int):
		first_half, last_half = divmod(arrange_int, int(1E16))
		return first_half, last_half

	@staticmethod
	def get_whole_arrange_int(first_int, last_int):
		return first_int * int(1E16) + last_int
