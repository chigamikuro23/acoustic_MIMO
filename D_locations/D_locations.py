import scipy.io as sio
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import math


#Read .mat data into memory
D_content = sio.loadmat('mat_files/D_VLOS_scaled_mean_mean_alpha6_fft_abs_Frobenius_sphericalWave_B32_U2048.mat')
location_content = sio.loadmat('mat_files/randLocationU2048VIP.mat')

impulse_responses = D_content['D']
locations = location_content['location']


d1, n = impulse_responses.shape
d2, n = locations.shape


train_length = math.floor(.8*n)


train_impulses = np.transpose(impulse_responses[:, :train_length])
train_labels = np.transpose(locations[:, :train_length])

test_impulses = np.transpose(impulse_responses[:,train_length:])
test_labels = np.transpose(locations[:,train_length:])

model = keras.Sequential([
    keras.layers.Dense(128, activation=tf.nn.relu),

    keras.layers.Dense(3, activation=tf.nn.softmax)
])

model.compile(optimizer='sgd',
              loss='mean_squared_error',
              metrics=['accuracy'])

model.fit(train_impulses, train_labels, epochs=5, validation_data=(test_impulses,test_labels))

test_loss, test_acc = model.evaluate(test_impulses, test_labels)

print('Test accuracy: ', test_acc)


