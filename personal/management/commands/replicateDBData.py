from django.core.management.base import BaseCommand
from personal.models import BestMove
from personal import dbmanager


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		bestMoveList = BestMove.objects.filter(replicated=False)[:1000]
		print("Number of data:{0}".format(len(bestMoveList)))
		count = 0
		for bestMove in bestMoveList:
			arrangeInt = BestMove.getWholeArrangeInt(bestMove.first_half_arrangement, bestMove.last_half_arrangement)

			# Horizontal Symmetry Data
			symmArrangeInt = dbmanager.flipArrangeInt(arrangeInt, "Horizontal")
			firstInt, lastInt = BestMove.getFirstLastArrangeInt(symmArrangeInt)
			moveInt = int(dbmanager.flipMoveInt(bestMove.move_index, "Horizontal"))
			newBestMove = BestMove(first_half_arrangement=firstInt, last_half_arrangement=lastInt, move_index=moveInt)
			newBestMove.save_or_update()

			# Vertical Symmetry Data
			symmArrangeInt = dbmanager.flipArrangeInt(arrangeInt, "Vertical")
			firstInt, lastInt = BestMove.getFirstLastArrangeInt(symmArrangeInt)
			moveInt = int(dbmanager.flipMoveInt(bestMove.move_index, "Vertical"))
			newBestMove = BestMove(first_half_arrangement=firstInt, last_half_arrangement=lastInt, move_index=moveInt)
			newBestMove.save_or_update()

			bestMove.replicated = True
			bestMove.save()
			count += 1
			print("No.{0} is replicated. {1}%".format(count, float(count*100)/len(bestMoveList)))
