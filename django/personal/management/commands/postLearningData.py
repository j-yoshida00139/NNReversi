import pickle

from django.core.management.base import BaseCommand

from ...utils import move_loader


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        n_batch_size = 500
        # n_batch_size = math.floor(BestMove.objects.all().count() / 20000) * 100
        print("batch size is :")
        print(n_batch_size)

        x_train, t_train, x_eva, t_eva, x_test, t_test = move_loader.load_data(n_batch_size, flatten=False)
        params = dict()
        params["x_train"], params["t_train"], params["x_test"], params["t_test"] = \
            x_train, t_train, x_test, t_test
        with open("nncore/input_data/learn_input.pkl", 'wb') as f:
            pickle.dump(params, f)
