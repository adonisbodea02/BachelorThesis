import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
from split_sequence import split_sequence
from keras import metrics
from numpy import array


data = pd.read_csv("EUR_GBP Historical Data.csv")

training_data = []
for i in range(len(data) - 1, len(data) - int(60*len(data) / 100) + 1, -1):
    training_data.append(float("{:.4f}".format(data.at[i, "Price"])))

validation_data = []
for i in range(len(data) - int(60*len(data) / 100) + 1, len(data) - int(80*len(data) / 100), -1):
    validation_data.append(float("{:.4f}".format(data.at[i, "Price"])))

test_data = []
for i in range(len(data) - int(80*len(data) / 100), -1, -1):
    test_data.append(float("{:.4f}".format(data.at[i, "Price"])))

look_back = 20

training_data_X, training_data_Y = split_sequence(training_data, look_back)
validation_data_X, validation_data_Y = split_sequence(validation_data, look_back)
test_data_X, test_data_Y = split_sequence(test_data, look_back)

test_loss = 0
test_mae = 0
test_rse = 0

for k in range(5):
    model = Sequential()
    model.add(Dense(2000, activation='relu', input_dim=look_back))
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
    fig1.suptitle('Training and validation history FFNN EUR-GBP UNIVARIATE ' + str(look_back) +
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
        sample = i.reshape(1, look_back)
        predictions.append(model.predict(sample, verbose=0))
        predictions[-1] = predictions[-1][0]
    predictions = array(predictions)
    fig2 = plt.figure(2)
    fig2.suptitle('Predicted vs Actual FFNN EUR-GBP UNIVARIATE ' + str(look_back) + ' PAST OBSERVATIONS RUN ' +
                  str(k+1), fontsize=8, y=0.99, verticalalignment='top')
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
    model.save_weights('ffnn_eur_gbp_univariate_' + str(look_back) + '_past_observations_run_' + str(k+1) +
                       '.h5')

print('Average Test loss:', test_loss/5)
print('Average Test MAE:', test_mae/5)
print('Average Test RMSE:', test_rse/5)
