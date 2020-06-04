import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
from split_sequence_multivariate import split_sequence_multivariate
from keras import metrics
from numpy import array
from keras import backend as K


def relative_squared_error(y_true, y_pred):
    return K.sum(K.square(y_pred - y_true)) / K.sum(K.square(K.mean(y_pred) - y_pred))


rates_data = pd.read_csv("EUR_GBP Historical Data.csv")
gold_data_csv = pd.read_csv("Gold Price Historical Data.csv")
oil_data_csv = pd.read_csv("Oil Brent Spot Price.csv")
inflation_EU_data = pd.read_csv("Inflation rate EU.csv")
inflation_UK_data = pd.read_csv("Inflation rate UK.csv")
interest_EU_data = pd.read_csv("Interest rate EU.csv")
interest_UK_data = pd.read_csv("Interest rate UK.csv")

gold_data = []
oil_data = []
for i in range(len(gold_data_csv)):
    gold_data.append(float("{:.4f}".format(gold_data_csv.at[i, "Price"])))
    oil_data.append(float("{:.4f}".format(oil_data_csv.at[i, "Price"])))

max_gold = max(gold_data)
max_oil = max(oil_data)
for i in range(len(gold_data)):
    gold_data[i] /= max_gold
    oil_data[i] /= max_oil

training_data = []
for i in range(len(rates_data) - 1, len(rates_data) - int(60 * len(rates_data) / 100) + 1, -1):
    training_data.append([float("{:.4f}".format(rates_data.at[i, "Price"])),
                          gold_data[i],
                          # oil_data[i],
                          # float("{:.4f}".format(float(inflation_EU_data.at[i, "Price"][:-1]))),
                          # float("{:.4f}".format(float(inflation_UK_data.at[i, "Price"][:-1]))),
                          # float("{:.4f}".format(float(interest_EU_data.at[i, "Price"][:-1]))),
                          # float("{:.4f}".format(float(interest_UK_data.at[i, "Price"][:-1])))
                          ])

validation_data = []
for i in range(len(rates_data) - int(60 * len(rates_data) / 100) + 1,
               len(rates_data) - int(80 * len(rates_data) / 100), -1):
    validation_data.append([float("{:.4f}".format(rates_data.at[i, "Price"])),
                            gold_data[i],
                            # oil_data[i],
                            # float("{:.4f}".format(float(inflation_EU_data.at[i, "Price"][:-1]))),
                            # float("{:.4f}".format(float(inflation_UK_data.at[i, "Price"][:-1]))),
                            # float("{:.4f}".format(float(interest_EU_data.at[i, "Price"][:-1]))),
                            # float("{:.4f}".format(float(interest_UK_data.at[i, "Price"][:-1])))
                            ])
test_data = []
for i in range(len(rates_data) - int(80 * len(rates_data) / 100), -1, -1):
    test_data.append([float("{:.4f}".format(rates_data.at[i, "Price"])),
                      # gold_data[i],
                      oil_data[i],
                      # float("{:.4f}".format(float(inflation_EU_data.at[i, "Price"][:-1]))),
                      # float("{:.4f}".format(float(inflation_UK_data.at[i, "Price"][:-1]))),
                      # float("{:.4f}".format(float(interest_EU_data.at[i, "Price"][:-1]))),
                      # float("{:.4f}".format(float(interest_UK_data.at[i, "Price"][:-1])))
                      ])
look_back = 5

training_data_X, training_data_Y = split_sequence_multivariate(training_data, look_back)
validation_data_X, validation_data_Y = split_sequence_multivariate(validation_data, look_back)
test_data_X, test_data_Y = split_sequence_multivariate(test_data, look_back)

n_input = training_data_X.shape[1] * training_data_X.shape[2]
training_data_X = training_data_X.reshape((training_data_X.shape[0], n_input))

n_input = validation_data_X.shape[1] * validation_data_X.shape[2]
validation_data_X = validation_data_X.reshape((validation_data_X.shape[0], n_input))

n_input = test_data_X.shape[1] * test_data_X.shape[2]
test_data_X = test_data_X.reshape((test_data_X.shape[0], n_input))

model = Sequential()
model.add(Dense(2500, activation='relu', input_dim=n_input))
#model.add(Dense(500, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse', metrics=[metrics.mae, relative_squared_error])

train_history = model.fit(training_data_X, training_data_Y, epochs=500,
                          verbose=2, validation_data=(validation_data_X, validation_data_Y))

loss = train_history.history['loss']
val_loss = train_history.history['val_loss']
mae_loss = train_history.history['mean_absolute_error']
mae_val_loss = train_history.history['val_mean_absolute_error']
plt.figure(1)
plt.plot(loss)
plt.plot(val_loss)
plt.plot(mae_loss)
plt.plot(mae_val_loss)
plt.legend(['loss', 'val_loss', 'mae_loss', 'mae_val_loss'])
plt.ylim(0, 0.01)
dates = [i for i in range(len(test_data_X))]
dates = array(dates)
predictions = []
for i in test_data_X:
    sample = i.reshape((1, 5))
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
#
# # dummy = array([0.9115, 0.9124, 0.9427, 0.9308, 0.9186, 0.9284, 0.9176, 0.9159, 0.9038, 0.8944])
# dummy = array([0.9284, 0.9176, 0.9159, 0.9038, 0.8944])
# dummy = dummy.reshape((1, 5))
# print(model.predict(dummy, verbose=0))

