from django.core.management.base import BaseCommand
from ...utils import move_loader
from ...utils import config
from ...models import BestMove
import math
import requests
import json
import pickle


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		n_batch_size = math.floor(BestMove.objects.all().count() / 200) * 100
		print("batch size is :")
		print(n_batch_size)

		x_train, t_train, x_eva, t_eva, x_test, t_test = move_loader.load_data(n_batch_size, flatten=False)
		params = dict()
		params["x_train"], params["t_train"], params["x_test"], params["t_test"] = \
			x_train, t_train, x_test, t_test
		with open("nncore/input_data/learn_input.pkl", 'wb') as f:
			pickle.dump(params, f)

		# url = config.ENDPOINT_URL + "/nncore/upload_input/"
		# payload = {
		# 	"x_train": x_train.tolist(),
		# 	"t_train": t_train.tolist(),
		# 	"x_test": x_test.tolist(),
		# 	"t_test": t_test.tolist()}
		# headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
		# response = requests.post(url, data=json.dumps(payload), headers=headers)
		# print(url)
		# print(response.status_code)
		# if response.status_code == 200:
		# 	print("The data is stored.")
		# else:
		# 	print("Error. Check the logs.")
