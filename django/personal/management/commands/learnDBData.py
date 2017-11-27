from django.core.management.base import BaseCommand
from ...nncore import move_loader
from ...nncore import network
from ...utils.trainer import Trainer
from ...models import BestMove
import math


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		n_epoch = 1
		n_batch_size = math.floor(BestMove.objects.all().count() / 200) * 100
		print("batch size is :")
		print(n_batch_size)
		print("started")

		for x in range(n_epoch):
			print("cycle number : {0:03d}".format(x+1))
			x_train, t_train, x_eva, t_eva, x_test, t_test = move_loader.load_data(n_batch_size, flatten=False)

			net = network.Network()
			trainer = Trainer(
				net, x_train, t_train, x_test, t_test,
				epochs=20, mini_batch_size=100,
				optimizer='Adam', optimizer_param={'lr': 0.001},
				evaluate_sample_num_per_epoch=1000)
			trainer.train()
