import scipy.io as sio
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer
from keras.metrics import categorical_accuracy


#Read .mat data into memory
EPOCHS = 10
INIT_LR = 1e-3
BS = 32

plt.close('all')

D_content = sio.loadmat('mat_files/D_VLOS_scaled_mean_mean_alpha6_fft_abs_Frobenius_sphericalWave_B32_U2048.mat')
location_content = sio.loadmat('mat_files/randLocationU2048VIP.mat')

impulse_responses = D_content['D']
locations = location_content['location']


d1, n = impulse_responses.shape
d2, n = locations.shape




#train_length = math.floor(.8*n)
impulses = np.transpose(impulse_responses)
labels = np.transpose(locations[:2,:])

train_length = math.floor(.8*n)
test_impulses = impulses[train_length:,:]
test_labels = labels[train_length:,:]

'''
train_impulses = np.transpose(impulse_responses[:, :train_length])
train_labels = labels[:train_length,:]

test_impulses = np.transpose(impulse_responses[:,train_length:])
test_labels = labels[train_length:,:]

temp = test_labels.copy()

mlb = MultiLabelBinarizer()
labels = mlb.fit_transform(labels)

num_vectors, num_coordinates = labels.shape
train_labels=labels[:train_length, :]
test_labels=labels[train_length:, :]




fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(train_labels[:,0], train_labels[:,1], c='b', marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')


fig1 = plt.figure()
ax = fig1.add_subplot(111)

ax.scatter(test_labels[:,0], test_labels[:,1], c='r', marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')




plt.show()

'''



model = keras.Sequential([
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(2, activation='linear')
])

model.compile(optimizer='adam',
              loss='mape',
              metrics=None)

hist = model.fit(impulses, labels, epochs=100, batch_size=32, validation_split=.2)



predictions = model.predict(test_impulses)






plt.figure(1)
'''
plt.subplot(211)
plt.plot(hist.history['acc'])
plt.plot(hist.history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('epoch')
plt.legend(['train','test'], loc='upper left')

plt.subplot(212)
'''
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','test'], loc='upper left')


predictions = model.predict(test_impulses)


fig1 = plt.figure(2)
ax = fig1.add_subplot(111)

ax.scatter(predictions[:,0], predictions[:,1], c='b', marker='x', label="Predictions")
ax.scatter(test_labels[:,0], test_labels[:,1], c='r', marker='o', label="Actual")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend(loc='upper left')

plt.show()

