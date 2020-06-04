from flask import Flask
from flask_restful import Api
from flask import jsonify
from tensorflow import keras
from datetime import timedelta, date
from datetime import datetime
import requests
from numpy import array
import os
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
# specifying the directory where the DB is placed
database_file = "sqlite:///{}".format(os.path.join(project_dir, "predictions.db"))

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Prediction(db.Model):
    """
    Class used for storing the predictions of the model such that they are not computed for every request.
    The class inherits the SQLAlchemy class Model which facilities ORM.
    """
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    day = db.Column(db.Date, nullable=False)
    rate = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Float(precision=4), nullable=False)

    def __repr__(self):
        return self.rate + ", " + str(self.day) + ": " + str(self.value)


db.create_all()
db.session.commit()


def construct_model_eur_gbp():
    """
    Function which constructs the prediction model for the EUR/GBP exchange rate
    :return: an instance of the Keras Sequential Model
    """
    model = keras.models.Sequential()
    model.add(keras.layers.LSTM(100, activation='relu', input_shape=(15, 1)))
    model.add(keras.layers.Dense(1))
    model.compile(optimizer='adam', loss='mse',
                  metrics=[keras.metrics.mae, keras.metrics.RootMeanSquaredError()])
    # the weights are loaded from the file which stored the best run of the model
    model.load_weights('lstm_vanilla_eur_gbp_univariate_15_past_observations_run_2.h5')
    return model


def construct_model_eur_usd():
    """
    Function which constructs the prediction model for the EUR/USD exchange rate
    :return: an instance of the Keras Sequential Model
    """
    model = keras.models.Sequential()
    model.add(keras.layers.LSTM(100, activation='relu', input_shape=(15, 1)))
    model.add(keras.layers.Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=[keras.metrics.mae, keras.metrics.RootMeanSquaredError()])
    # the weights are loaded from the file which stored the best run of the model
    model.load_weights('lstm_vanilla_eur_usd_univariate_15_past_observations_run_3.h5')
    return model


def construct_model_gbp_usd():
    """
    Function which constructs the prediction model for the EUR/USD exchange rate
    :return: an instance of the Keras Sequential Model
    """
    model = keras.models.Sequential()
    model.add(keras.layers.LSTM(100, activation='tanh', input_shape=(15, 1)))
    model.add(keras.layers.Dense(1))
    model.compile(optimizer='adam', loss='mse', metrics=[keras.metrics.mae, keras.metrics.RootMeanSquaredError()])
    # the weights are loaded from the file which stored the best run of the model
    model.load_weights('lstm_vanilla_tanh_gbp_usd_univariate_15_past_observations_run_1.h5')
    return model


def get_weekday_n_days_ago(end_date, n):
    """
    Function which computes the weekday which was n weekdays ago for a given date
    :param end_date: Date, the date from where to start counting backwards
    :param n: Integer, the number of weekdays to look back
    :return: Date, the weekday which was n weekdays ago
    Constraint: n must be less than 30
    """
    prev_days = [end_date - timedelta(days=i) for i in range(1, 40)]
    prev_days = [d for d in prev_days if d.weekday() < 5]
    for d in prev_days:
        if d.month == 5 and d.day == 1:
            prev_days.remove(d)
    return prev_days[n-1]


def get_data(end_date, n, local, foreign):
    """
    Function which retrieves the last n observations of the specified exchange rate with the last observation being on
    the given date
    :param end_date: Date, the date of the last observation
    :param n: Integer, the number of observations needed
    :param local: String, the local currency
    :param foreign: String, the foreign currency
    :return: List of Floats
    """
    URL = "https://api.exchangeratesapi.io/history"
    PARAMS = {'start_at': str(get_weekday_n_days_ago(end_date, n)),
              'end_at': str(end_date),
              'symbols': foreign,
              'base': local}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    input_data = []
    for day in data['rates']:
        input_data.append([datetime.strptime(day, '%Y-%m-%d').date(),
                           float("{:.8f}".format(data['rates'][day][foreign]))])
    input_data.sort(key=lambda x: x[0])
    for i in range(len(input_data)):
        input_data[i] = input_data[i][1]
    return input_data[-n:]


@app.route('/prediction/EURGBP/<day>')
def predict_eur_gbp(day):
    """
    Function which exposes the route from which predictions for the EUR/GBP exchange rate can be retrieved
    :param day: String date, the date of the prediction
    :return: JSON Object, the value of the prediction as a JSON Object of the form {"prediction": "value"},
             where value is a String
    """
    # create date object
    date_obj = datetime.strptime(day, '%Y-%m-%d').date()
    # search for the prediction in the database
    prediction_object = Prediction.query.filter_by(day=date_obj, rate="EURGBP").first()
    if prediction_object is None:
        # compute the prediction since none was found
        # construct the model
        model = construct_model_eur_gbp()
        # get the data for the prediction
        data = get_data(date_obj - timedelta(days=1), 15, "EUR", "GBP")
        data = array(data)
        data = data.reshape((1, 15, 1))
        # compute the prediction
        new_prediction = model.predict(data)
        new_prediction = new_prediction[0][0]
        # store the prediction
        prediction_object = Prediction(day=date_obj, value=new_prediction, rate="EURGBP")
        db.session.add(prediction_object)
        db.session.commit()
        # expose the prediction as an JSON object
        prediction = {"prediction": str(new_prediction)}
        return jsonify(prediction)
    else:
        # since it was found in the database, expose the prediction as an JSON object
        prediction = {"prediction": str(prediction_object.value)}
        return jsonify(prediction)


@app.route('/prediction/EURUSD/<day>')
def predict_eur_usd(day):
    """
    Function which exposes the route from which predictions for the EUR/USD exchange rate can be retrieved
    :param day: String date, the date of the prediction
    :return: JSON Object, the value of the prediction as a JSON Object of the form {"prediction": "value"},
             where value is a String
    """
    # create date object
    date_obj = datetime.strptime(day, '%Y-%m-%d').date()
    # search for the prediction in the database
    prediction_object = Prediction.query.filter_by(day=date_obj, rate="EURUSD").first()
    if prediction_object is None:
        # compute the prediction since none was found
        # construct the model
        model = construct_model_eur_gbp()
        # get the data for the prediction
        data = get_data(date_obj - timedelta(days=1), 15, "EUR", "USD")
        data = array(data)
        data = data.reshape((1, 15, 1))
        # compute the prediction
        new_prediction = model.predict(data)
        new_prediction = new_prediction[0][0]
        # store the prediction
        prediction_object = Prediction(day=date_obj, value=new_prediction, rate="EURUSD")
        db.session.add(prediction_object)
        db.session.commit()
        # expose the prediction as an JSON object
        prediction = {"prediction": str(new_prediction)}
        return jsonify(prediction)
    else:
        # since it was found in the database, expose the prediction as an JSON object
        prediction = {"prediction": str(prediction_object.value)}
        return jsonify(prediction)


@app.route('/prediction/GBPUSD/<day>')
def predict_gbp_usd(day):
    """
    Function which exposes the route from which predictions for the GBP/USD exchange rate can be retrieved
    :param day: String date, the date of the prediction
    :return: JSON Object, the value of the prediction as a JSON Object of the form {"prediction": "value"},
             where value is a String
    """
    # create date object
    date_obj = datetime.strptime(day, '%Y-%m-%d').date()
    # search for the prediction in the database
    prediction_object = Prediction.query.filter_by(day=date_obj, rate="GBPUSD").first()
    if prediction_object is None:
        # compute the prediction since none was found
        # construct the model
        model = construct_model_eur_gbp()
        # get the data for the prediction
        data = get_data(date_obj - timedelta(days=1), 15, "GBP", "USD")
        data = array(data)
        data = data.reshape((1, 15, 1))
        # compute the prediction
        new_prediction = model.predict(data)
        new_prediction = new_prediction[0][0]
        # store the prediction
        prediction_object = Prediction(day=date_obj, value=new_prediction, rate="GBPUSD")
        db.session.add(prediction_object)
        db.session.commit()
        # expose the prediction as an JSON object
        prediction = {"prediction": str(new_prediction)}
        return jsonify(prediction)
    else:
        # since it was found in the database, expose the prediction as an JSON object
        prediction = {"prediction": str(prediction_object.value)}
        return jsonify(prediction)


if __name__ == '__main__':
    app.run(debug=True)
