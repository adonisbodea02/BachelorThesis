import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';

class ServerHelper{

  static ServerHelper _serverHelper;
  String _url = "https://api.exchangeratesapi.io";
  String _urlPrediction = "http://10.0.2.2:5000/prediction/";

  ServerHelper._createInstance();

  /// Factory for creating a single instance of this class during runtime
  factory ServerHelper(){
    if (_serverHelper == null) {
      _serverHelper = ServerHelper._createInstance();
    }
    return _serverHelper;
  }

  /// Function which calls the Prediction Server in order to retrieve the prediction specified by the local and foreign currencies and date
  /// @param: String local, the local currency of the exchange rate
  /// @param: String foreign, the local currency of the exchange rate
  /// @param: DateTime date, the date for which the value of the prediction is needed
  /// return: Future<double>, the value of the prediction wrapped in a Future container due to the asynchronous nature of the call
  Future<double> getPrediction(String local, String foreign, DateTime date) async {
    var formatter = new DateFormat('yyyy-MM-dd');
    String formattedDate = formatter.format(date);
    var response = await http.get(_urlPrediction + local + foreign + "/" + formattedDate);
    var responseDecoded = await json.decode(response.body);
    double prediction = double.parse(responseDecoded['prediction']);
    return prediction;
  }

  /// Function which calls the Exchange Rates API in order to retrieve the latest value of the specified exchange rate
  /// @param: String local, the local currency of the exchange rate
  /// @param: String foreign, the local currency of the exchange rate
  /// return: Future<double>, the value of the exchange rate wrapped in a Future container due to the asynchronous nature of the call
  Future<double> getCurrentRate(String local, String foreign) async{
    var response = await http.get(_url + "/latest?base=" + local + "&symbols=" + foreign);
    var responseDecoded = await json.decode(response.body);
    double rate = responseDecoded['rates'][foreign];
    return rate;
  }

  /// Function which calls the Exchange Rates API in order to retrieve the value specified by the exchange rate and the date
  /// @param: String local, the local currency of the exchange rate
  /// @param: String foreign, the local currency of the exchange rate
  /// @param: DateTime date, the date for which the value of the exchange rate is needed
  /// return: Future<double>, the value of the exchange rate wrapped in a Future container due to the asynchronous nature of the call
  Future<double> getPastRate(String from, String to, DateTime day) async{
    var formatter = new DateFormat('yyyy-MM-dd');
    String formattedDate = formatter.format(day);
    var response = await http.get(_url + "/" + formattedDate + "?base=" + from + "&symbols=" + to);
    var responseDecoded = await json.decode(response.body);
    double rate = responseDecoded['rates'][to];
    return rate;
  }






}

