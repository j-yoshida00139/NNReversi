import os
import pickle

import numpy as np
import tensorflow as tf
from django.core.management.base import BaseCommand

from ...src import tf_network

net = tf_network.TfNetwork()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        file_name = 'nncore/input_data/learn_input.pkl'
        if not os.path.exists(file_name):
            print('Input data does not exist.')
            raise BaseException
        with open(file_name, 'rb') as f:
            params = pickle.load(f)

        x_train, t_train, x_test, t_test = params["x_train"], params["t_train"], params["x_test"], params["t_test"]
        x_train = np.float16(x_train.swapaxes(1, 2).swapaxes(2, 3).reshape(-1, 192))
        t_train = np.float16(t_train.reshape(-1, 64))
        x_test = np.float16(x_test.swapaxes(1, 2).swapaxes(2, 3).reshape(-1, 192))
        t_test = np.float16(t_test.reshape(-1, 64))

        t_train = np.argmax(t_train, axis=1)
        t_test = np.argmax(t_test, axis=1)

        # Create the Estimator
        classifier = tf.estimator.Estimator(
            model_fn=net.cnn_model_fn, model_dir=net.model_path)

        # Set up logging for predictions
        tensors_to_log = {"probabilities": "softmax_tensor"}
        logging_hook = tf.train.LoggingTensorHook(
            tensors=tensors_to_log, every_n_iter=50)

        # Train the model
        train_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": x_train},
            y=t_train,
            batch_size=100,
            num_epochs=None,
            shuffle=True)
        classifier.train(
            input_fn=train_input_fn,
            steps=1000,
            hooks=[logging_hook])

        # Evaluate the model and print results
        eval_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": x_test},
            y=t_test,
            num_epochs=1,
            shuffle=False)
        eval_results = classifier.evaluate(input_fn=eval_input_fn)
        print(eval_results)
