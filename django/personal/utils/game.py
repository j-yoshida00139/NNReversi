from ..models import BestMove
from . import basicFunc
from . import config
import math
import numpy as np
import requests
import json
import os

directions = [
	{"row":  0, "col":  1},
	{"row": -1, "col":  1},
	{"row": -1, "col":  0},
	{"row": -1, "col": -1},
	{"row":  0, "col": -1},
	{"row":  1, "col": -1},
	{"row":  1, "col":  0},
	{"row":  1, "col":  1}
]


class Game(object):
	def __init__(self, rows, cols, arrange_list=[], next_color=0):
		self.rows = rows
		self.cols = cols
		self.NONE = 0
		self.BLACK = 1
		self.WHITE = 2
		self.arrange = arrange_list
		self.blackMove = []
		self.whiteMove = []
		self.nextColor = self.BLACK if next_color == 0 else next_color

	def initialize(self):
		up_row = math.floor((self.rows-1)/2)
		left_col = math.floor((self.cols-1)/2)
		self.arrange = [[0 for col in range(0, self.cols)] for row in range(0, self.rows)]
		self.put_piece(up_row, left_col, self.BLACK)
		self.put_piece(up_row + 1, left_col, self.WHITE)
		self.put_piece(up_row, left_col + 1, self.WHITE)
		self.put_piece(up_row + 1, left_col + 1, self.BLACK)

	def clear_piece(self, row, col):
		self.arrange[row][col] = self.NONE

	def put_piece(self, row, col, color):
		self.arrange[row][col] = color

	def can_put_piece(self, row, col, color):
		if self.arrange[row][col] != self.NONE:
			return False
		if len(self.get_turn_piece_list(row, col, color)) > 0:
			return True
		return False

	def store_move(self, row, col, color):
		tmp_arrange_list = basicFunc.unshared_copy(self.arrange)
		if color == self.BLACK:
			self.blackMove.append({"arrange": tmp_arrange_list, "color": color, "row": row, "col": col})
		else:
			self.whiteMove.append({"arrange": tmp_arrange_list, "color": color, "row": row, "col": col})

	def is_out_of_range(self, row, col):
		if row >= self.rows or col >= self.cols or row < 0 or col < 0:
			return True
		else:
			return False

	def get_score(self, color):
		counter = 0
		for row in range(0, self.rows):
			for col in range(0, self.cols):
				if self.arrange[row][col] == color:
					counter += 1
		return counter

	def get_turn_piece_list(self, row, col, color):
		turn_piece_list = []
		for i in range(0, len(directions)):
			tmp_turn_piece_list = self.get_turn_piece_for_direct(row, col, color, directions[i]['row'], directions[i]['col'])
			for j in range(len(tmp_turn_piece_list)):
				turn_piece_list.append({"row": tmp_turn_piece_list[j]['row'], "col": tmp_turn_piece_list[j]['col']})
		return turn_piece_list

	def get_turn_piece_for_direct(self, row, col, color, y, x):
		check_row, check_col = row+y, col+x
		if self.is_out_of_range(check_row, check_col):
			return []

		if self.arrange[check_row][check_col] == color or self.arrange[check_row][check_col] == self.NONE:
			return []

		turn_piece_list, turn_rows, turn_cols = [], [], []
		turn_rows.append(check_row)
		turn_cols.append(check_col)
		check_row += y
		check_col += x

		while not(self.is_out_of_range(check_row, check_col)):
			if self.arrange[check_row][check_col] == self.NONE:
				return []
			elif self.arrange[check_row][check_col] == color:
				for i in range(0, len(turn_rows)):
					turn_piece_list.append({"row": turn_rows[i], "col": turn_cols[i]})
				return turn_piece_list
			turn_rows.append(check_row)
			turn_cols.append(check_col)
			check_row += y
			check_col += x
		return turn_piece_list

	def can_put_piece_on_board(self, color):
		can_put_list = self.get_can_put_list(color)
		for canPut in can_put_list:
			if canPut == 1:
				return True
		return False

	def get_can_put_list(self, color):
		can_put_list = []
		for y in range(self.rows):
			for x in range(self.cols):
				if self.can_put_piece(y, x, color):
					can_put_list.append(1)
				else:
					can_put_list.append(0)
		return can_put_list

	def get_winners_data(self):
		if self.get_score(self.BLACK) > self.get_score(self.WHITE):
			return self.blackMove
		elif self.get_score(self.BLACK) < self.get_score(self.WHITE):
			return self.whiteMove
		else:
			return None

	def go_next_turn(self):
		self.nextColor = self.WHITE if self.nextColor == self.BLACK else self.BLACK
		if self.can_put_piece_on_board(self.nextColor):
			return True
		else:
			self.nextColor = self.WHITE if self.nextColor == self.BLACK else self.BLACK
			if self.can_put_piece_on_board(self.nextColor):
				return True
			else:
				return False

	def turn_piece(self, turn_piece_list, color):
		for i in range(0, len(turn_piece_list)):
			self.put_piece(turn_piece_list[i]["row"], turn_piece_list[i]["col"], color)

	def return_move_list(self, row, col):
		u"""Return array which has next move's row and column. (for neural network)
		:param row: row of next move
		:param col: column of next move
		:return: converted array for neural network
		"""
		move_list = []
		for y in range(0, self.rows):
			for x in range(0, self.cols):
				if y == row and x == col:
					move_list.append(float(1))
				else:
					move_list.append(float(0))
		return move_list

	@staticmethod
	def return_nn_input_store_list(raw_array):
		arrange_list = []
		for value in raw_array:
			arrange_list.append(value[0])
		return arrange_list

	def set_next_color(self, next_color):
		self.nextColor = next_color
		return True

	def is_ended(self):
		if self.can_put_piece_on_board(self.WHITE) or self.can_put_piece_on_board(self.BLACK):
			return False
		else:
			return True

	def get_winners_color(self):
		if self.get_score(self.BLACK) > self.get_score(self.WHITE):
			return self.BLACK
		elif self.get_score(self.BLACK) < self.get_score(self.WHITE):
			return self.WHITE
		else:
			return self.NONE

	def go_next_with_auto_move(self, nn_flag=False):
		if nn_flag:
			index = self.get_next_move_index_by_nn(self.arrange, self.nextColor)
		else:
			move = np.random.rand(1, 64)  # move[0][0:63]
			index = np.argmax(move[0] * self.get_can_put_list(self.nextColor))
		row, col = divmod(index, 8)
		self.go_next_with_manual_move(row, col)

	def get_next_move_index_by_nn(self, arrange, next_color):
		arrange_list = BestMove.encode_to_nn_arrange(arrange, next_color)
		arrange_list = basicFunc.conv_input(arrange_list)  # arrange_list[0][0:2][0:7][0:7]
		arrange_list = arrange_list.tolist()
		url = config.ENDPOINT_URL + "/nncore/forward/"
		payload = {'nn_input': arrange_list}
		headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
		r = requests.post(url, data=json.dumps(payload), headers=headers)
		move = r.json()["nn_output"]  # move[0][0:63]
		index = np.argmax(np.array(move[0]) * self.get_can_put_list(next_color))
		return index

	def go_next_with_manual_move(self, row, col):
		self.store_move(row, col, self.nextColor)
		self.put_piece(row, col, self.nextColor)
		turn_piece_list = self.get_turn_piece_list(row, col, self.nextColor)
		self.turn_piece(turn_piece_list, self.nextColor)
		self.go_next_turn()

	def find_best_move(self):
		win_ratio, best_row, best_col = 0.0, 0, 0
		for index, value in list(enumerate(self.get_can_put_list(self.nextColor))):
			if value == 0:  # means the piece cannot be put
				continue
			tmp_game = Game(8, 8, basicFunc.unshared_copy(self.arrange), self.nextColor)
			row, col = divmod(index, 8)
			tmp_game.go_next_with_manual_move(row, col)
			tmp_win_ratio = basicFunc.calc_win_ratio(tmp_game.arrange, tmp_game.nextColor, self.nextColor)
			if tmp_win_ratio >= win_ratio:
				best_row, best_col, win_ratio = row, col, tmp_win_ratio
		return best_row, best_col, win_ratio
