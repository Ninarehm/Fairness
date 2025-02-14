import sklearn
import sklearn.tree
import sklearn.ensemble
import sklearn.metrics
import pandas as pd
import numpy as np
import scipy
import scipy.optimize
import pdb
import tensorflow as tf
import argparse

tf.random.set_random_seed(2019)
overall_numbers = {}
results = []

parser = argparse.ArgumentParser()
parser.add_argument('--loss_type', default="equality")
parser.add_argument('--beta', default=0.5)
args = parser.parse_args()


whole_data_raw = pd.read_csv('adult', sep=', ', engine='python')
best_dec_acc = 0
best_train_acc = 0
for h in range(10):
	print(h)
	shuffled = whole_data_raw.sample(frac=1,random_state=h).reset_index(drop=True)
	df_train_raw = shuffled[0:int(len(shuffled)*0.8)]
	df_train_raw.reset_index(inplace=True)
	df_dev_raw = shuffled[int(len(shuffled)*0.8):int(len(shuffled)*0.8+len(shuffled)*0.1)]
	df_dev_raw.reset_index(inplace=True)
	df_test_raw = shuffled[int(len(shuffled)*0.8+len(shuffled)*0.1):]
	df_test_raw.reset_index(inplace=True)
	
	n_train = len(df_train_raw)
	n_dev = len(df_dev_raw)
	n_test = len(df_test_raw)
	general_n_test = len(df_test_raw)
	df_raw = pd.concat([df_train_raw, df_dev_raw,df_test_raw])

	df = pd.get_dummies(df_raw, columns=['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country', 'Y'])

	
	df = df.drop(columns=['sex_Male', 'Y_<=50K'])
	X = df.drop(columns=['Y_>50K'])
	group_label = X['sex_Female']


	Y = df['Y_>50K']

	
	for i in range(10):
		group_label = X['sex_Female']

		scaler = sklearn.preprocessing.StandardScaler()
		X_scaled = scaler.fit_transform(X)

		X_train = X_scaled[:n_train]
		X_dev = X_scaled[n_train:n_train+n_dev]
		X_test = X_scaled[n_train+n_dev:]
		Y_train = Y.iloc[:n_train]
		Y_dev = Y.iloc[n_train:n_train+n_dev]
		Y_test = Y.iloc[n_train+n_dev:]

		index_male_train = np.where(group_label[:n_train] == 0)[0].astype(np.int32)
		index_female_train = np.where(group_label[:n_train] == 1)[0].astype(np.int32)
		index_male_true_train = np.where(np.logical_and(group_label[:n_train] == 0, Y_train==1))[0].astype(np.int32)
		index_male_false_train = np.where(np.logical_and(group_label[:n_train] == 0, Y_train==0))[0].astype(np.int32)
		index_female_true_train = np.where(np.logical_and(group_label[:n_train] == 1, Y_train==1))[0].astype(np.int32)
		index_female_false_train = np.where(np.logical_and(group_label[:n_train] == 1, Y_train==0))[0].astype(np.int32)

		index_male_dev = np.where(group_label[n_train:n_train+n_dev] == 0)[0].astype(np.int32)
		index_female_dev = np.where(group_label[n_train:n_train+n_dev] == 1)[0].astype(np.int32)
		index_male_true_dev = np.where(np.logical_and(group_label[n_train:n_train+n_dev] == 0, Y_dev==1))[0].astype(np.int32)
		index_male_false_dev = np.where(np.logical_and(group_label[n_train:n_train+n_dev] == 0, Y_dev==0))[0].astype(np.int32)
		index_female_true_dev = np.where(np.logical_and(group_label[n_train:n_train+n_dev] == 1, Y_dev==1))[0].astype(np.int32)
		index_female_false_dev = np.where(np.logical_and(group_label[n_train:n_train+n_dev] == 1, Y_dev==0))[0].astype(np.int32)

		index_male_test = np.where(group_label[n_train+n_dev:] == 0)[0].astype(np.int32)
		index_female_test = np.where(group_label[n_train+n_dev:] == 1)[0].astype(np.int32)
		index_male_true_test = np.where(np.logical_and(group_label[n_train+n_dev:] == 0, Y_test==1))[0].astype(np.int32)
		index_male_false_test = np.where(np.logical_and(group_label[n_train+n_dev:] == 0, Y_test==0))[0].astype(np.int32)
		index_female_true_test = np.where(np.logical_and(group_label[n_train+n_dev:] == 1, Y_test==1))[0].astype(np.int32)
		index_female_false_test = np.where(np.logical_and(group_label[n_train+n_dev:] == 1, Y_test==0))[0].astype(np.int32)

		train_data_one_female_prob = index_female_true_train.shape[0]/index_female_train.shape[0]
		train_data_zero_female_prob = index_female_false_train.shape[0] /index_female_train.shape[0]
		train_data_one_male_prob = index_male_true_train.shape[0]/index_male_train.shape[0]
		train_data_zero_male_prob = index_male_false_train.shape[0]/index_male_train.shape[0]

		print(abs(train_data_one_female_prob-train_data_one_male_prob))
		if(h==0):
			results.append(abs(train_data_one_female_prob-train_data_one_male_prob))
		else:
			results[i] = results[i]+abs(train_data_one_female_prob-train_data_one_male_prob)

		if(h==0):
			overall_numbers[i]= []
			overall_numbers[i].append(abs(train_data_one_female_prob-train_data_one_male_prob))
		else:
			overall_numbers[i].append(abs(train_data_one_female_prob-train_data_one_male_prob))

		dev_data_one_female_prob = index_female_true_dev.shape[0]/index_female_dev.shape[0]
		dev_data_zero_female_prob = index_female_false_dev.shape[0]/index_female_dev.shape[0]
		dev_data_one_male_prob = index_male_true_dev.shape[0]/index_male_dev.shape[0]
		dev_data_zero_male_prob = index_male_false_dev.shape[0]/index_male_dev.shape[0]

		test_data_one_female_prob = index_female_true_test.shape[0]/index_female_test.shape[0]
		test_data_zero_female_prob = index_female_false_test.shape[0]/index_female_test.shape[0]
		test_data_one_male_prob = index_male_true_test.shape[0]/index_male_test.shape[0]
		test_data_zero_male_prob = index_male_false_test.shape[0]/index_male_test.shape[0]


		# put Y into one hot label
		Y_train = np.stack([1-Y_train, Y_train]).T
		Y_dev = np.stack([1-Y_dev, Y_dev]).T
		Y_test = np.stack([1-Y_test, Y_test]).T

		DIM_INPUT = X_train.shape[1]
		DIM_HIDDEN = 256
		DIM_OUTPUT = 2

		X_placeholder = tf.placeholder(tf.float32, [None, DIM_INPUT])
		Y_placeholder = tf.placeholder(tf.float32, [None, DIM_OUTPUT])
		index_male_placeholder = tf.placeholder(tf.int32, [None])
		index_female_placeholder = tf.placeholder(tf.int32, [None])
		index_male_true_placeholder = tf.placeholder(tf.int32, [None])
		index_male_false_placeholder = tf.placeholder(tf.int32, [None])
		index_female_true_placeholder = tf.placeholder(tf.int32, [None])
		index_female_false_placeholder = tf.placeholder(tf.int32, [None])
		data_female_one_placeholder = tf.placeholder(tf.float32)
		data_female_zero_placeholder = tf.placeholder(tf.float32)
		data_male_one_placeholder = tf.placeholder(tf.float32)
		data_male_zero_placeholder = tf.placeholder(tf.float32)

		
		raw_w = tf.Variable(0.5, name='w')
		w = tf.clip_by_value(raw_w, 0, 1)

		beta = float(args.beta)

		L1_output = tf.layers.dense(X_placeholder, DIM_HIDDEN, activation=tf.nn.tanh)
		output = tf.layers.dense(L1_output, DIM_OUTPUT, activation=None)

		prob = tf.nn.softmax(output)
		prob_male = tf.nn.embedding_lookup(prob, index_male_placeholder)
		prob_female = tf.nn.embedding_lookup(prob, index_female_placeholder)
		prob_male_true = tf.nn.embedding_lookup(prob, index_male_true_placeholder)
		prob_male_false = tf.nn.embedding_lookup(prob, index_male_false_placeholder)
		prob_female_true = tf.nn.embedding_lookup(prob, index_female_true_placeholder)
		prob_female_false = tf.nn.embedding_lookup(prob, index_female_false_placeholder)

		if(args.loss_type == "equity"):
			fairness_loss = tf.math.squared_difference(tf.reduce_mean(prob_female[:, 1])+data_female_one_placeholder, tf.reduce_mean(prob_male[:, 1])+data_male_one_placeholder) \
					  + tf.math.squared_difference(tf.reduce_mean(prob_female[:, 0])+data_female_zero_placeholder, tf.reduce_mean(prob_male[:, 0])+data_male_zero_placeholder)
		else:
			fairness_loss = tf.math.squared_difference(tf.reduce_mean(prob_female[:, 1]), tf.reduce_mean(prob_male[:, 1])) \
					  + tf.math.squared_difference(tf.reduce_mean(prob_female[:, 0]), tf.reduce_mean(prob_male[:, 0]))

		label_male = tf.nn.embedding_lookup(Y_placeholder, index_male_placeholder)
		label_female = tf.nn.embedding_lookup(Y_placeholder, index_female_placeholder)
		output_male = tf.nn.embedding_lookup(output, index_male_placeholder)
		output_female = tf.nn.embedding_lookup(output, index_female_placeholder)

		pred = tf.math.argmax(prob, axis=1)
		diff = tf.to_float(pred) - Y_placeholder[:, 1]
		accuracy = 1 - tf.math.reduce_mean(tf.math.abs(diff))
		loss_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=Y_placeholder, logits=output))

		loss_total = beta * (fairness_loss) + (1-beta)*loss_entropy

		variables = [v for v in tf.trainable_variables() if v != raw_w]
		for v in variables:
			loss_total += 1e-4 * tf.nn.l2_loss(v) + 1e-6 * tf.losses.absolute_difference(v, tf.zeros(tf.shape(v)))

		lr = tf.Variable(0.01, name='lr', trainable=False)
		lr_decay_op = lr.assign(lr * 0.95)
		optimizer = tf.train.AdamOptimizer(lr)
		train_op = optimizer.minimize(loss_total)
		with tf.Session() as sess:
			sess.run(tf.global_variables_initializer())

			wait = 0
			smallest_loss_total_dev = float('inf')
			smallest_weight = None
			patience_lr_decay = 5
			patience_wait = 100

			def _save_weight():
				global smallest_weight
				tf_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
				smallest_weight = sess.run(tf_vars)

			def _load_weights():
				tf_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
				ops = []
				for i_tf in range(len(tf_vars)):
					ops.append(tf.assign(tf_vars[i_tf], smallest_weight[i_tf]))
				sess.run(ops)

			for epoch in range(10000):
				w_train, loss_total_train, loss_entropy_train, accuracy_train, fairness_loss_train, pred_train, train_step = sess.run(
					[w, loss_total, loss_entropy, accuracy, fairness_loss,  pred, train_op],
						feed_dict={
							X_placeholder: X_train,
							Y_placeholder: Y_train,
							index_male_placeholder: index_male_train,
							index_female_placeholder: index_female_train,
							index_male_true_placeholder: index_male_true_train,
							index_male_false_placeholder: index_male_false_train,
							index_female_true_placeholder: index_female_true_train,
							index_female_false_placeholder: index_female_false_train,
							data_female_one_placeholder: train_data_one_female_prob,
							data_female_zero_placeholder: train_data_zero_female_prob,
							data_male_one_placeholder: train_data_one_male_prob,
							data_male_zero_placeholder: train_data_zero_male_prob
						}
				)

				loss_total_dev, loss_entropy_dev, accuracy_dev, fairness_loss_dev, pred_dev= sess.run(
					[loss_total, loss_entropy, accuracy, fairness_loss, pred],
						feed_dict={
							X_placeholder: X_dev,
							Y_placeholder: Y_dev,
							index_male_placeholder: index_male_dev,
							index_female_placeholder: index_female_dev,
							index_male_true_placeholder: index_male_true_dev,
							index_male_false_placeholder: index_male_false_dev,
							index_female_true_placeholder: index_female_true_dev,
							index_female_false_placeholder: index_female_false_dev,
							data_female_one_placeholder: dev_data_one_female_prob,
							data_female_zero_placeholder: dev_data_zero_female_prob,
							data_male_one_placeholder: dev_data_one_male_prob,
							data_male_zero_placeholder: dev_data_zero_male_prob
						}
				)

				if loss_total_dev <= smallest_loss_total_dev:
					smallest_loss_total_dev = loss_total_dev
					_save_weight()
					wait = 0
				else:
					wait += 1
					if wait % patience_lr_decay == 0:
						sess.run(lr_decay_op)

				if wait == patience_wait:
			 		break


			_load_weights()
			loss_total_test, loss_entropy_test, accuracy_test, fairness_loss_test, pred_test = sess.run(
					[loss_total, loss_entropy, accuracy, fairness_loss,  pred],
						feed_dict={
							X_placeholder: X_test,
							Y_placeholder: Y_test,
							index_male_placeholder: index_male_test,
							index_female_placeholder: index_female_test,
							index_male_true_placeholder: index_male_true_test,
							index_male_false_placeholder: index_male_false_test,
							index_female_true_placeholder: index_female_true_test,
							index_female_false_placeholder: index_female_false_test,
							data_female_one_placeholder: test_data_one_female_prob,
							data_female_zero_placeholder: test_data_zero_female_prob,
							data_male_one_placeholder: test_data_one_male_prob,
							data_male_zero_placeholder: test_data_zero_male_prob
						}
			)
			loss_total_dev, loss_entropy_dev, accuracy_dev, fairness_loss_dev, pred_dev= sess.run(
					[loss_total, loss_entropy, accuracy, fairness_loss, pred],
						feed_dict={
							X_placeholder: X_dev,
							Y_placeholder: Y_dev,
							index_male_placeholder: index_male_dev,
							index_female_placeholder: index_female_dev,
							index_male_true_placeholder: index_male_true_dev,
							index_male_false_placeholder: index_male_false_dev,
							index_female_true_placeholder: index_female_true_dev,
							index_female_false_placeholder: index_female_false_dev,
							data_female_one_placeholder: dev_data_one_female_prob,
							data_female_zero_placeholder: dev_data_zero_female_prob,
							data_male_one_placeholder: dev_data_one_male_prob,
							data_male_zero_placeholder: dev_data_zero_male_prob
						}
				)
			loss_total_train, loss_entropy_train, accuracy_train, fairness_loss_train, pred_train = sess.run(
					[ loss_total, loss_entropy, accuracy, fairness_loss,  pred],
						feed_dict={
							X_placeholder: X_train,
							Y_placeholder: Y_train,
							index_male_placeholder: index_male_train,
							index_female_placeholder: index_female_train,
							index_male_true_placeholder: index_male_true_train,
							index_male_false_placeholder: index_male_false_train,
							index_female_true_placeholder: index_female_true_train,
							index_female_false_placeholder: index_female_false_train,
							data_female_one_placeholder: train_data_one_female_prob,
							data_female_zero_placeholder: train_data_zero_female_prob,
							data_male_one_placeholder: train_data_one_male_prob,
							data_male_zero_placeholder: train_data_zero_male_prob
						}
				)

			train_female_one_prediction = np.where(pred_train[index_female_train] == 1)[0].astype(np.int32)
			train_female_zero_prediction = np.where(pred_train[index_female_train] == 0)[0].astype(np.int32)
			train_male_one_prediction = np.where(pred_train[index_male_train] == 1)[0].astype(np.int32)
			train_male_zero_prediction = np.where(pred_train[index_male_train] == 0)[0].astype(np.int32)

			dev_female_one_prediction = np.where(pred_dev[index_female_dev] == 1)[0].astype(np.int32)
			dev_female_zero_prediction = np.where(pred_dev[index_female_dev] == 0)[0].astype(np.int32)
			dev_male_one_prediction = np.where(pred_dev[index_male_dev] == 1)[0].astype(np.int32)
			dev_male_zero_prediction = np.where(pred_dev[index_male_dev] == 0)[0].astype(np.int32)

			test_female_one_prediction = np.where(pred_test[index_female_test] == 1)[0].astype(np.int32)
			test_female_zero_prediction = np.where(pred_test[index_female_test] == 0)[0].astype(np.int32)
			test_male_one_prediction = np.where(pred_test[index_male_test] == 1)[0].astype(np.int32)
			test_male_zero_prediction = np.where(pred_test[index_male_test] == 0)[0].astype(np.int32)

			
			dataset =pd.Series(pred_test[int(-0.1*general_n_test):])
			X = pd.concat([X[int(-0.1*general_n_test):],X]).reset_index(drop=True)
			Y = pd.concat([dataset,Y]).reset_index(drop=True)
			X.drop(X.tail(int(0.1*general_n_test)).index,inplace=True)
			Y.drop(Y.tail(int(0.1*general_n_test)).index,inplace=True)
			n_train = n_train+(int(0.1*general_n_test))
			n_test = n_test-(int(0.1*general_n_test))

	tf.reset_default_graph()
	tf.random.set_random_seed(2019)

import statistics
for elem in overall_numbers:
	print(elem)
	print(overall_numbers[elem])
	print("STDV: " + str(statistics.stdev(overall_numbers[elem])) )
	print("Mean: " + str(statistics.mean(overall_numbers[elem])) )


