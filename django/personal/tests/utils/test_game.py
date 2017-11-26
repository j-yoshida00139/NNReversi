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
