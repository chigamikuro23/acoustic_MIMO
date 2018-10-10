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




train_length = math.floor(.8*n)

labels = np.transpose(np.rint(locations[:2,:]))


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



'''
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

print(len(mlb.classes_))


model = keras.Sequential([
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(1000, activation='relu'),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(num_coordinates, activation='sigmoid')
])

model.compile(optimizer='sgd',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(train_impulses, train_labels, epochs=30, batch_size=128, validation_data=(test_impulses,test_labels))

test_loss, test_acc = model.evaluate(test_impulses, test_labels)

print('Test accuracy: ', test_acc)

predictions = model.predict(test_impulses)



print(predictions.shape)

idx = (-predictions).argsort()[:,:2]
print(list(zip(mlb.classes_[idx[:,1]],mlb.classes_[idx[:,0]])))

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(mlb.classes_[idx[:,1]], mlb.classes_[idx[:,0]], c='b', marker='s', label='Predicted')


ax.scatter(temp[:,0], temp[:,1], c='r', marker='o', label='Actual')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')



plt.legend(loc='upper left')
plt.show()
