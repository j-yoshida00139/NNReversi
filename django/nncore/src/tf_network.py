from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Imports
import numpy as np
import tensorflow as tf

import os
import pickle

tf.logging.set_verbosity(tf.logging.INFO)


def cnn_model_fn(features, labels, mode):
	"""Model function for CNN."""
	# Input Layer
	input_layer = tf.reshape(features["x"], [-1, 8, 8, 3])

	# Convolutional Layer #1
	conv1 = tf.layers.conv2d(
		inputs=input_layer, filters=16, kernel_size=[4, 4], padding="same", activation=tf.nn.relu)

	# Pooling Layer #1
	# pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

	# Convolutional Layer #2 and Pooling Layer #2
	conv2 = tf.layers.conv2d(
		inputs=conv1, filters=16, kernel_size=[4, 4], padding="same", activation=tf.nn.relu)
	conv3 = tf.layers.conv2d(
		inputs=conv2, filters=32, kernel_size=[4, 4], padding="same", activation=tf.nn.relu)
	conv4 = tf.layers.conv2d(
		inputs=conv3, filters=32, kernel_size=[4, 4], padding="same", activation=tf.nn.relu)
	conv5 = tf.layers.conv2d(
		inputs=conv4, filters=64, kernel_size=[4, 4], padding="same", activation=tf.nn.relu)
	conv6 = tf.layers.conv2d(
		inputs=conv5, filters=64, kernel_size=[2, 2], padding="same", activation=tf.nn.relu)
	# pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

	# Dense Layer
	conv6_flat = tf.reshape(conv6, [-1, 8 * 8 * 64])
	dense = tf.layers.dense(inputs=conv6_flat, units=1024, activation=tf.nn.relu)
	# dropout = tf.layers.dropout(
	# 	inputs=dense, rate=0.2, training=mode == tf.estimator.ModeKeys.TRAIN)

	# Logits Layer
	logits = tf.layers.dense(inputs=dense, units=64)
	# logits = tf.layers.dense(inputs=dropout, units=64)

	predictions = {
		# Generate predictions (for PREDICT and EVAL mode)
		"classes": tf.argmax(input=logits, axis=1),
		# Add `softmax_tensor` to the graph. It is used for PREDICT and by the
		# `logging_hook`.
		"probabilities": tf.nn.softmax(logits, name="softmax_tensor")
	}

	if mode == tf.estimator.ModeKeys.PREDICT:
		return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

	# Calculate Loss (for both TRAIN and EVAL modes)
	loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

	# Configure the Training Op (for TRAIN mode)
	if mode == tf.estimator.ModeKeys.TRAIN:
		optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.0)
		train_op = optimizer.minimize(
			loss=loss,
			global_step=tf.train.get_global_step())
		return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

	# Add evaluation metrics (for EVAL mode)
	eval_metric_ops = {
		"accuracy": tf.metrics.accuracy(
			labels=labels, predictions=predictions["classes"])}
	return tf.estimator.EstimatorSpec(
		mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)


def main(unused_argv):
	# Load training and eval data

	file_name = '../input_data/learn_input.pkl'
	if not os.path.exists(file_name):
		print('Input data does not exist.')
		raise BaseException
	with open(file_name, 'rb') as f:
		params = pickle.load(f)
	x_train, t_train, x_test, t_test = params["x_train"], params["t_train"], params["x_test"], params["t_test"]
	x_train = np.float16(x_train.reshape(-1, 192))
	t_train = np.float16(t_train.reshape(-1, 64))
	x_test = np.float16(x_test.reshape(-1, 192))
	t_test = np.float16(t_test.reshape(-1, 64))

	t_train = np.argmax(t_train, axis=1)
	t_test = np.argmax(t_test, axis=1)

	# Create the Estimator
	mnist_classifier = tf.estimator.Estimator(
		model_fn=cnn_model_fn, model_dir="/tmp/reversi_model")

	# Set up logging for predictions
	tensors_to_log = {"probabilities": "softmax_tensor"}
	logging_hook = tf.train.LoggingTensorHook(
		tensors=tensors_to_log, every_n_iter=50)

	# Train the model
	train_input_fn = tf.estimator.inputs.numpy_input_fn(
		x={"x": x_train},
		y=t_train,
		batch_size=100,
		# batch_size=100,
		num_epochs=None,
		shuffle=True)
	mnist_classifier.train(
		input_fn=train_input_fn,
		steps=1000,
		# steps=20000,
		hooks=[logging_hook])

	# Evaluate the model and print results
	eval_input_fn = tf.estimator.inputs.numpy_input_fn(
		x={"x": x_test},
		y=t_test,
		num_epochs=1,
		shuffle=False)
	eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
	print(eval_results)


if __name__ == "__main__":
	tf.app.run()
