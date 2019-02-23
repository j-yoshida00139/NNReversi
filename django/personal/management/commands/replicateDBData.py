from django.core.management.base import BaseCommand

from ...models import BestMove
from ...utils import dbmanager


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        best_move_list = BestMove.objects.filter(replicated=False)[:1000]
        print("Number of data:{0}".format(len(best_move_list)))
        count = 0
        direction_list = ["Horizontal", "Vertical"]
        for bestMove in best_move_list:
            arrange_int = BestMove.get_whole_arrange_int(bestMove.first_half_arrangement,
                                                         bestMove.last_half_arrangement)

            for direction in direction_list:
                symm_arrange_int = dbmanager.flip_arrange_int(arrange_int, direction)
                first_int, last_int = BestMove.get_first_last_arrange_int(symm_arrange_int)
                move_int = int(dbmanager.flip_move_int(bestMove.move_index, direction))
                new_best_move = BestMove(
                    first_half_arrangement=first_int, last_half_arrangement=last_int, move_index=move_int,
                    replicated=True)
                new_best_move.save_or_update()

            for degree in [90, 180, 270]:
                rotated_arrange_int = dbmanager.rotate_arrange_int(arrange_int, degree)
                first_int, last_int = BestMove.get_first_last_arrange_int(rotated_arrange_int)
                move_int = int(dbmanager.rotate_move_int(bestMove.move_index, degree))
                new_best_move = BestMove(
                    first_half_arrangement=first_int, last_half_arrangement=last_int, move_index=move_int,
                    replicated=True)
                new_best_move.save_or_update()

            rotated_arrange_int = dbmanager.rotate_arrange_int(arrange_int, 90)
            rotated_move_int = int(dbmanager.rotate_move_int(bestMove.move_index, 90))
            for direction in direction_list:
                symm_arrange_int = dbmanager.flip_arrange_int(rotated_arrange_int, direction)
                first_int, last_int = BestMove.get_first_last_arrange_int(symm_arrange_int)
                move_int = int(dbmanager.flip_move_int(rotated_move_int, direction))
                new_best_move = BestMove(
                    first_half_arrangement=first_int, last_half_arrangement=last_int, move_index=move_int,
                    replicated=True)
                new_best_move.save_or_update()

            bestMove.replicated = True
            bestMove.save()
            count += 1
            print("No.{0} is replicated. {1}%".format(count, float(count * 100) / len(best_move_list)))
