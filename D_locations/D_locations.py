import scipy.io as sio
import tensorflow as tf
from tensorflow import keras
import numpy as np
import math
import matplotlib.pyplot as plt
from keras import backend as K
def rmse(y_pred, y_actual):

    return K.sqrt(K.mean(K.square(y_pred -y_actual), axis = -1))

#Read .mat data into memory
EPOCHS = 10
INIT_LR = 1e-3
BS = 32

plt.close('all')

D_content = sio.loadmat('mat_files/D_VLOS_scaled_mean_mean_alpha6_fft_abs_Frobenius_sphericalWave_B32_U2048.mat')
location_content = sio.loadmat('mat_files/randLocationU2048VIP.mat')

impulse_responses = D_content['D']
locations = location_content['location']

test_D_content = sio.loadmat('mat_files/D_VLOS_scaled_mean_mean_alpha6_fft_abs_Frobenius_sphericalWave_B32_U20000.mat')
test_location_content = sio.loadmat('mat_files/randLocationU20000VIP.mat')

test_impulse_responses = test_D_content['D']
test_locations = test_location_content['location']


d1, n = impulse_responses.shape
d2, n = locations.shape




#train_length = math.floor(.8*n)
impulses = np.transpose(test_impulse_responses)
labels = np.transpose(test_locations[:2,:])

test_impulses = np.transpose(impulse_responses)
test_labels = np.transpose(locations[:2,:])




#Two hidden layers
#One output layer
model = keras.Sequential([
    keras.layers.BatchNormalization(),
    keras.layers.Dense(2048, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(.25),
    keras.layers.Dense(2048, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(.25),
    keras.layers.Dense(2048, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(.25),
    keras.layers.Dense(2, activation='linear'),
])
optimizer = keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model.compile(optimizer=optimizer,
              loss='mse',
              metrics=[rmse])

early_stop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=.1)
hist = model.fit(impulses, labels, epochs=10, batch_size = 200, callbacks=[early_stop],validation_split=.2)

predictions = model.predict(test_impulses)


#Plots mean absolute distance between predictions and actual data
plt.figure(1)

plt.subplot(211)
plt.plot(hist.history['rmse'])
plt.semilogy(hist.history['val_rmse'])
plt.title('Model RMS Error')
plt.ylabel('RMS Error')
plt.xlabel('epoch')
plt.legend(['train','validation'], loc='upper left')

plt.subplot(212)
plt.plot(hist.history['loss'])
plt.semilogy(hist.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','validation'], loc='upper left')



predictions = model.predict(test_impulses)


fig1 = plt.figure(2)
ax = fig1.add_subplot(111)

ax.scatter(predictions[:,0], predictions[:,1], c='b', marker='x', label="Predictions")
ax.scatter(test_labels[:,0], test_labels[:,1], c='r', marker='o', label="Actual")
#ax.plot(test_labels, predictions,'ro-')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend(loc='upper left')

plt.show()

