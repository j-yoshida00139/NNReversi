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

	def save(self):
		try:
			conn = sqlite3.connect('../db.sqlite3')
			with conn:
				cursor = conn.cursor()
				cursor.execute("insert into best_moves (first_half_arrangement, last_half_arrangement, move_index) values (?, ?, ?)", (self.first_half_arrangement, self.last_half_arrangement, self.move_index))
				conn.commit()
			print("The data was added.")
		except sqlite3.IntegrityError:
			print ("couldn't add the data due to the data integrity problem.")

	def retreiveAll(self):
		conn = sqlite3.connect('../db.sqlite3')
		with conn:
			cursor = conn.cursor()
			cursor.execute("select id, first_half_arrangement, last_half_arrangement, move_index, created_at, updated_at from best_moves")
			resultList = cursor.fetchall()
			print(len(resultList))
		return resultList
