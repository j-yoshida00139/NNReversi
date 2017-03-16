from datetime import datetime
import sqlite3


class BestMove(object):
	def __init__(self,
				id = 0,
				first_half_arrangement = 0,
				last_half_arrangement = 0,
				move_index = 0,
				created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
				updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
				):
		self.id = id
		self.first_half_arrangement = first_half_arrangement
		self.last_half_arrangement = last_half_arrangement
		self.move_index = move_index
		self.created_at = created_at
		self.updated_at = updated_at

	def __str__(self):
		return "id:" + self.str_id()

	def str_id(self):
		return str(self.id)

	def getArrangementVals(self):
		return (self.first_half_arrangement, self.last_half_arrangement)

	def save(self):
		try:
			conn = sqlite3.connect('../db.sqlite3')
			with conn:
				cursor = conn.cursor()
				cursor.execute("insert into best_moves (first_half_arrangement, last_half_arrangement, move_index) values (?, ?, ?)", (self.first_half_arrangement, self.last_half_arrangement, self.move_index))
				conn.commit()
		except sqlite3.IntegrityError:
			print ("couldn't add the data due to the data integrity problem.")

	def update(self):
		try:
			conn = sqlite3.connect('../db.sqlite3')
			with conn:
				cursor = conn.cursor()
				cursor.execute("update best_moves set move_index=? where first_half_arrangement=? and last_half_arrangement=?", (self.move_index, self.first_half_arrangement, self.last_half_arrangement))
		except sqlite3.IntegrityError:
			print("couldn't update the data due to the data integrity problem.")

	@staticmethod
	def retrieveAll():
		conn = sqlite3.connect('../db.sqlite3')
		#conn = sqlite3.connect('../../db.sqlite3')
		bestMoveList = []
		with conn:
			cursor = conn.cursor()
			cursor.execute("select id, first_half_arrangement, last_half_arrangement, move_index, created_at, updated_at from best_moves")
			for result in cursor.fetchall():
				bestMoveList.append(BestMove(*result))
		return bestMoveList

	@staticmethod
	def retrieveFromArrange(first_half, last_half):
		conn = sqlite3.connect('../db.sqlite3')
		bestMove = None
		with conn:
			cursor = conn.cursor()
			cursor.execute("select id, first_half_arrangement, last_half_arrangement, move_index, created_at, updated_at from best_moves where first_half_arrangement=? and last_half_arrangement=?", (first_half, last_half))
			for result in cursor.fetchall():
				bestMove = BestMove(*result)
		return bestMove


	@staticmethod
	def getCount():
		conn = sqlite3.connect('../../db.sqlite3')
		with conn:
			cursor = conn.cursor()
			cursor.execute("select count(id) from best_moves")
			count = cursor.fetchone()
		return count
