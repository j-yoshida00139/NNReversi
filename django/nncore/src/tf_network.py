from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.INFO)


class TfNetwork(object):

	def __init__(self):
		self.model_path = "nncore/reversi_model"

	@staticmethod
	def cnn_model_fn(features, labels, mode):
		"""Model function for CNN."""
		# Input Layer
		input_layer = tf.reshape(features["x"], [-1, 8, 8, 3])

		conv1 = tf.layers.conv2d(
			inputs=input_layer, filters=16, kernel_size=[3, 3], padding="valid", activation=tf.nn.relu)
		# pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)
		conv2 = tf.layers.conv2d(
			inputs=conv1, filters=16, kernel_size=[3, 3], padding="same", activation=tf.nn.relu)
		conv3 = tf.layers.conv2d(
			inputs=conv2, filters=32, kernel_size=[3, 3], padding="valid", activation=tf.nn.relu)
		# conv4 = tf.layers.conv2d(
		# 	inputs=conv3, filters=32, kernel_size=[4, 4], padding="same", activation=tf.nn.relu)
		# conv5 = tf.layers.conv2d(
		# 	inputs=conv4, filters=64, kernel_size=[4, 4], padding="same", activation=tf.nn.relu)
		# conv6 = tf.layers.conv2d(
		# 	inputs=conv5, filters=64, kernel_size=[2, 2], padding="same", activation=tf.nn.relu)
		# pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

		conv6_flat = tf.reshape(conv3, [-1, 4 * 4 * 32])
		dense = tf.layers.dense(inputs=conv6_flat, units=1024, activation=tf.nn.relu)
		# dropout = tf.layers.dropout(
		# 	inputs=dense, rate=0.2, training=mode == tf.estimator.ModeKeys.TRAIN)

		logits = tf.layers.dense(inputs=dense, units=64)
		# logits = tf.layers.dense(inputs=dropout, units=64)

		predictions = {
			"classes": tf.argmax(input=logits, axis=1),
			"probabilities": tf.nn.softmax(logits, name="softmax_tensor")
		}

		if mode == tf.estimator.ModeKeys.PREDICT:
			return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

		# Calculate Loss (for both TRAIN and EVAL modes)
		loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

		# Configure the Training Op (for TRAIN mode)
		if mode == tf.estimator.ModeKeys.TRAIN:
			optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.0)
			train_op = optimizer.minimize(loss=loss, global_step=tf.train.get_global_step())
			return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

		# Add evaluation metrics (for EVAL mode)
		eval_metric_ops = {
			"accuracy": tf.metrics.accuracy(
				labels=labels, predictions=predictions["classes"])}
		return tf.estimator.EstimatorSpec(
			mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

	def feed_forward(self, x):
		if len(x.shape) < 4:
			x = np.array([x])
		input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": x}, y=None, num_epochs=1, shuffle=False)
		classifier = tf.estimator.Estimator(model_fn=self.cnn_model_fn, model_dir=self.model_path)
		estimated_result = classifier.predict(input_fn=input_fn)
		probabilities = []
		for result in estimated_result:
			probabilities.append(result['probabilities'])
		return probabilities
