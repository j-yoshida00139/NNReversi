from django.core.management.base import BaseCommand
from personal.models import BestMove
from personal import dbmanager


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		bestMoveList = BestMove.objects.filter(replicated=False)[:1000]
		print("Number of data:{0}".format(len(bestMoveList)))
		count = 0
		for bestMove in bestMoveList:
			arrangeInt = BestMove.get_whole_arrange_int(bestMove.first_half_arrangement, bestMove.last_half_arrangement)

			# Horizontal Symmetry Data
			symmArrangeInt = dbmanager.flip_arrange_int(arrangeInt, "Horizontal")
			firstInt, lastInt = BestMove.get_first_last_arrange_int(symmArrangeInt)
			moveInt = int(dbmanager.flip_move_int(bestMove.move_index, "Horizontal"))
			newBestMove = BestMove(first_half_arrangement=firstInt, last_half_arrangement=lastInt, move_index=moveInt)
			newBestMove.save_or_update()

			# Vertical Symmetry Data
			symmArrangeInt = dbmanager.flip_arrange_int(arrangeInt, "Vertical")
			firstInt, lastInt = BestMove.get_first_last_arrange_int(symmArrangeInt)
			moveInt = int(dbmanager.flip_move_int(bestMove.move_index, "Vertical"))
			newBestMove = BestMove(first_half_arrangement=firstInt, last_half_arrangement=lastInt, move_index=moveInt)
			newBestMove.save_or_update()

			bestMove.replicated = True
			bestMove.save()
			count += 1
			print("No.{0} is replicated. {1}%".format(count, float(count*100)/len(bestMoveList)))
