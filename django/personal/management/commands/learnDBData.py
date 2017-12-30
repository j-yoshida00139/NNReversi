from django.core.management.base import BaseCommand
from ...utils import move_loader
from ...utils import config
import requests
import json


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		n_epoch = 1
		n_batch_size = 1000
		print("batch size is :")
		print(n_batch_size)
		print("started")

		for x in range(n_epoch):
			print("cycle number : {0:03d}".format(x+1))
			x_train, t_train, x_eva, t_eva, x_test, t_test = move_loader.load_data(n_batch_size, flatten=False)
			url = config.ENDPOINT_URL + "/nncore/train/"
			payload = {
				"x_train": x_train.tolist(),
				"t_train": t_train.tolist(),
				"x_test": x_test.tolist(),
				"t_test": t_train.tolist()}
			headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
			response = requests.post(url, data=json.dumps(payload), headers=headers)
			print("Finished. Response:" + response)
