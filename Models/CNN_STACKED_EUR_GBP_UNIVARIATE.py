import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers.convolutional import Conv1D, MaxPooling1D
import pandas as pd
from split_sequence import split_sequence
from keras import metrics
from numpy import array
from keras import backend as K


def relative_squared_error(y_true, y_pred):
    return K.sum(K.square(y_pred - y_true)) / K.sum(K.square(K.mean(y_pred) - y_pred))


def relative_absolute_error(y_true, y_pred):
    return K.sum(K.abs(y_pred - y_true)) / K.sum(K.abs(K.mean(y_pred) - y_pred))


data = pd.read_csv("EUR_GBP Historical Data 2005-2020.csv")

training_data = []
for i in range(len(data) - 1, len(data) - int(60*len(data) / 100) + 1, -1):
    training_data.append(float("{:.4f}".format(data.at[i, "Price"])))

validation_data = []
for i in range(len(data) - int(60*len(data) / 100) + 1, len(data) - int(80*len(data) / 100), -1):
    validation_data.append(float("{:.4f}".format(data.at[i, "Price"])))

test_data = []
for i in range(len(data) - int(80*len(data) / 100), -1, -1):
    test_data.append(float("{:.4f}".format(data.at[i, "Price"])))

look_back = 15

training_data_X, training_data_Y = split_sequence(training_data, look_back)
validation_data_X, validation_data_Y = split_sequence(validation_data, look_back)
test_data_X, test_data_Y = split_sequence(test_data, look_back)

training_data_X = training_data_X.reshape(training_data_X.shape[0], training_data_X.shape[1], 1)
validation_data_X = validation_data_X.reshape(validation_data_X.shape[0], validation_data_X.shape[1], 1)
test_data_X = test_data_X.reshape(test_data_X.shape[0], test_data_X.shape[1], 1)


model = Sequential()
model.add(Conv1D(filters=100, kernel_size=2, activation='relu', input_shape=(look_back, 1)))
model.add(Conv1D(filters=100, kernel_size=2, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(2000, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse', metrics=[metrics.mae, relative_squared_error])

train_history = model.fit(training_data_X, training_data_Y, epochs=500, verbose=2, validation_data=(validation_data_X,
                                                                                                    validation_data_Y))
loss = train_history.history['loss']
val_loss = train_history.history['val_loss']
mae_loss = train_history.history['mean_absolute_error']
mae_val_loss = train_history.history['val_mean_absolute_error']
plt.figure(1)
plt.plot(loss)
plt.plot(val_loss)
plt.plot(mae_loss)
plt.plot(mae_val_loss)
plt.legend(['loss', 'val_loss', 'mae', 'val_mae'])
plt.ylim(0, 0.01)
dates = [i for i in range(len(test_data_X))]
dates = array(dates)
predictions = []
for i in test_data_X:
    sample = i.reshape((1, look_back, 1))
    predictions.append(model.predict(sample, verbose=0))
    predictions[-1] = predictions[-1][0]
predictions = array(predictions)
plt.figure(2)
plt.plot(dates, predictions)
plt.plot(dates, test_data_Y)
plt.legend(['predictions', 'values'])
plt.show()

test_history = model.evaluate(test_data_X, test_data_Y, verbose=1)
print(test_history)
print('Test loss:', test_history[0])
print('MAE:', test_history[1])
print('RSE:', test_history[2])

dummy = array([0.9115, 0.9124, 0.9427, 0.9308, 0.9186, 0.9284, 0.9176, 0.9159, 0.9038, 0.8944])
# dummy = array([0.9284, 0.9176, 0.9159, 0.9038, 0.8944])
dummy = dummy.reshape((1, look_back, 1))
print(model.predict(dummy, verbose=0))
