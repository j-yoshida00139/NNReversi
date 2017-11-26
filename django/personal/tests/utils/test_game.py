import pytest
from personal.utils.game import *


pytestmark = pytest.mark.django_db


class TestGame:
	def test_clear_piece(self):
		game = Game(8, 8)
		game.initialize()
		assert game.arrange[3][3] == game.BLACK
		game.clear_piece(3, 3)
		assert game.arrange[3][3] == game.NONE

	def test_get_winners_data(self):
		game = Game(8, 8)
		game.initialize()
		assert game.get_winners_data() is None
		black_move = [{"arrange": basicFunc.unshared_copy(game.arrange), "color": game.BLACK, "row": 4, "col": 2}]
		game.go_next_with_manual_move(4, 2)
		print(game.get_winners_data()[0]["arrange"])
		print(black_move[0]["arrange"])
		assert game.get_winners_data() == black_move
