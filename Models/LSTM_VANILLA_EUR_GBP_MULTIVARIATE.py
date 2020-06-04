import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import pandas as pd
from split_sequence_multivariate import split_sequence_multivariate
from keras import metrics
from numpy import array


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
                          oil_data[i],
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
                            oil_data[i],
                            # float("{:.4f}".format(float(inflation_EU_data.at[i, "Price"][:-1]))),
                            # float("{:.4f}".format(float(inflation_UK_data.at[i, "Price"][:-1]))),
                            # float("{:.4f}".format(float(interest_EU_data.at[i, "Price"][:-1]))),
                            # float("{:.4f}".format(float(interest_UK_data.at[i, "Price"][:-1])))
                            ])
test_data = []
for i in range(len(rates_data) - int(80 * len(rates_data) / 100), -1, -1):
    test_data.append([float("{:.4f}".format(rates_data.at[i, "Price"])),
                      gold_data[i],
                      oil_data[i],
                      # float("{:.4f}".format(float(inflation_EU_data.at[i, "Price"][:-1]))),
                      # float("{:.4f}".format(float(inflation_UK_data.at[i, "Price"][:-1]))),
                      # float("{:.4f}".format(float(interest_EU_data.at[i, "Price"][:-1]))),
                      # float("{:.4f}".format(float(interest_UK_data.at[i, "Price"][:-1])))
                      ])

look_back = 15
features = 3

training_data_X, training_data_Y = split_sequence_multivariate(training_data, look_back)
validation_data_X, validation_data_Y = split_sequence_multivariate(validation_data, look_back)
test_data_X, test_data_Y = split_sequence_multivariate(test_data, look_back)

training_data_X = training_data_X.reshape(training_data_X.shape[0], training_data_X.shape[1], features)
validation_data_X = validation_data_X.reshape(validation_data_X.shape[0], validation_data_X.shape[1], features)
test_data_X = test_data_X.reshape(test_data_X.shape[0], test_data_X.shape[1], features)

test_loss = 0
test_mae = 0
test_rse = 0

for k in range(5):
    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(look_back, features)))
    # model.add(Dense(100, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=[metrics.mae, metrics.RootMeanSquaredError()])

    train_history = model.fit(training_data_X, training_data_Y, epochs=500, verbose=2, validation_data=(validation_data_X,
                                                                                                        validation_data_Y))
    loss = train_history.history['loss']
    val_loss = train_history.history['val_loss']
    mae_loss = train_history.history['mean_absolute_error']
    mae_val_loss = train_history.history['val_mean_absolute_error']
    fig1 = plt.figure(1)
    fig1.suptitle('Training and validation history LSTM VANILLA EUR-GBP MULTIVARIATE GOLD OIL' + str(look_back) +
                  ' PAST OBSERVATIONS RUN ' + str(k+1), fontsize=8, y=0.99, verticalalignment='top')
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
        sample = i.reshape((1, look_back, features))
        predictions.append(model.predict(sample, verbose=0))
        predictions[-1] = predictions[-1][0]
    predictions = array(predictions)
    fig2 = plt.figure(2)
    fig2.suptitle('Predicted vs Actual LSTM EUR-GBP MULTIVARIATE GOLD OIL' + str(look_back) + ' PAST OBSERVATIONS RUN '
                  + str(k+1), fontsize=8, y=0.99, verticalalignment='top')
    plt.plot(dates, predictions)
    plt.plot(dates, test_data_Y)
    plt.legend(['predictions', 'values'])
    plt.show()

    test_history = model.evaluate(test_data_X, test_data_Y, verbose=1)
    print(test_history)
    print('Test loss:', test_history[0])
    print('MAE:', test_history[1])
    print('RMSE:', test_history[2])
    test_loss += test_history[0]
    test_mae += test_history[1]
    test_rse += test_history[2]
    model.save_weights('lstm_vanilla_eur_gbp_multivariate_gold_oil_' + str(look_back) + '_past_observations_run_' + str(k+1)
                       + '.h5')

print('Average Test loss:', test_loss/5)
print('Average Test MAE:', test_mae/5)
print('Average Test RMSE:', test_rse/5)
