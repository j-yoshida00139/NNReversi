from django.core.management.base import BaseCommand
from ...models import BestMove
import requests

numGames = 10


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		best_moves = BestMove.objects.all()
		for bestMove in best_moves:
			url = 'http://nnreversi.tgen.jp.net/api/best_moves/'
			# url = 'http://localhost:8000/api/best_moves/'
			data = {
				"first_half_arrangement": bestMove.first_half_arrangement,
				"last_half_arrangement": bestMove.last_half_arrangement,
				"move_index": bestMove.move_index
			}
			print(data)
			headers = {'content-type':'application/json', 'Accept-Charset':'UTF-8'}
			response = requests.post(url, json=data, headers=headers)
			print(response)
