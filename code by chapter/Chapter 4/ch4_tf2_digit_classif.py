#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 14:49:49 2020

@author: tom verguts
written for TensorFlow 2

digit classification; could a two-layer network solve this task...?
"""

#%% imports and initializations
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


# import digits dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# downscale to make data set smaller (and training faster)
train_size, test_size = 1000, 50
x_train, y_train, x_test, y_test = x_train[:train_size,:], y_train[:train_size], x_test[:test_size,:], y_test[:test_size]

# estimation parameters
learning_rate = 0.001
epochs = 50
batch_size = 100
batches = int(x_train.shape[0] / batch_size)

# plot some images from the data set
fig, axes = plt.subplots(1, 4, figsize=(7,3))
for img, label, ax in zip(x_train[:4], y_train[:4], axes):
      ax.set_title(label)
      ax.imshow(img)
      ax.axis("off")

#%% pre-processing
n_labels = int(np.max(y_train)+1)
image_size = x_train.shape[1]*x_train.shape[2]
x_train = x_train.reshape(x_train.shape[0], image_size)  / 255   # from 3D to 2D input data
x_test  = x_test.reshape(x_test.shape[0], image_size)    / 255   # same here
y_train = tf.one_hot(y_train, n_labels)
y_test  = tf.one_hot(y_test, n_labels)

#%% model construction
model = tf.keras.Sequential([
			tf.keras.Input(shape=(image_size,)),
			tf.keras.layers.Dense(n_labels, activation = "softmax")
			] )
model.build()

loss = tf.keras.losses.CategoricalCrossentropy() # don't worry about the details; it's another error function for multi-category, binary data
opt = tf.keras.optimizers.Adam(learning_rate = learning_rate)
model.compile(optimizer = opt, loss = loss)

#%% model fitting; this part typically takes the longest time
history = model.fit(x_train, y_train, batch_size = batch_size, epochs = epochs)

#%% show output
# print a summary
model.summary()

# error curve
fig, ax = plt.subplots(1, figsize=(7,3))
ax.plot(history.history["loss"], color = "black")

# print test data results
to_test_x, to_test_y = [x_train, x_test], [y_train, y_test]
labels =  ["train", "test"] # we plot results separately for training data and for testing data
print("\n")
for loop in range(2):
    y_pred = model.predict(to_test_x[loop])
    testdata_loss = tf.keras.losses.categorical_crossentropy(to_test_y[loop], y_pred)
    testdata_loss_summary = np.mean(testdata_loss.numpy())
    print("mean {} data performance: {:.2f}".format(labels[loop], testdata_loss_summary))	