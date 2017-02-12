"""memo for database schema
create table best_moves(
	id integer primary key AUTOINCREMENT NOT NULL,
	first_half_arrangement int NOT NULL,
	last_half_arrangement int NOT NULL,
	move_index int NOT NULL,
	created_at DATETIME NOT NULL DEFAULT current_timestamp,
	updated_at timestamp NOT NULL DEFAULT current_timestamp,
	UNIQUE(first_half_arrangement, last_half_arrangement)
);
"""

import sqlite3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/Model')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nncore')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/utils')
import BestMove
import move_loader
import basicFunc
import numpy as np


#conn = sqlite3.connect('../db.sqlite3')
#cursor = conn.cursor()

#cursor.execute("select id, first_part, second_part, created_at, updated_at from best_moves")

#bestMoves = []
#for record in cursor.fetchall():
#	bestMoves.append(BestMove(*record))

#print (bestMoves)
#for bestMove in bestMoves:
#	print(bestMove)

print("getting last file number...")
maxFileNo = basicFunc.getLastFileNo()
print("getting whole data...")
i = 0
for inputs, outputs in move_loader.get_data_by_list(range(maxFileNo)):
	print(i)
	i += 1
	inputInt = 0
	np_inputs = np.array(inputs).reshape((-1,3))
	for a, b, c in np_inputs:
		input = int(a*3+b*2+c)
		inputInt = inputInt*3 + input
	firstHalf, lastHalf = divmod(inputInt, int(1E16))
	outIndex = np.argmax(outputs)
	outIndex = int(outIndex)
	bestMove = BestMove.BestMove(first_half_arrangement = firstHalf, last_half_arrangement = lastHalf, move_index = outIndex)
	bestMove.save()

	#sys.exit()