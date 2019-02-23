import requests
from django.core.management.base import BaseCommand

from ...models import BestMove
from ...utils import config

numGames = 10


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        best_moves = BestMove.objects.all()
        for bestMove in best_moves:
            url = config.ENDPOINT_URL + '/api/best_moves/'
            data = {
                "first_half_arrangement": bestMove.first_half_arrangement,
                "last_half_arrangement": bestMove.last_half_arrangement,
                "move_index": bestMove.move_index
            }
            headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
            response = requests.post(url, json=data, headers=headers)
            if response.text == \
                    '{"non_field_errors":["The fields first_half_arrangement,' + \
                    ' last_half_arrangement must make a unique set."]}':
                print("The data has already existed")
            else:
                print(response)
