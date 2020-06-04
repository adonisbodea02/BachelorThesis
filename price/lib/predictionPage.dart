import 'package:connectivity/connectivity.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'DrawerOnly.dart';
import 'ServerHelper.dart';

class PredictionPage extends StatefulWidget {
  PredictionPage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _PredictionPageState createState() => _PredictionPageState();
}

class _PredictionPageState extends State<PredictionPage> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: new DrawerOnly(),
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
          child: ListView(
              children: <Widget>[
                PredictionWidget(),
              ]
          )
      ),// This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}

class PredictionWidget extends StatefulWidget {
  PredictionWidget({Key key}) : super(key: key);

  @override
  _PredictionWidgetState createState() => new _PredictionWidgetState();
}

class _PredictionWidgetState extends State<PredictionWidget> {

  ServerHelper _server = ServerHelper();
  List<String> _rates = <String>["EUR/GBP", "EUR/USD", "GBP/USD"];
  String _rate;
  RaisedButton _getPredictionButton;
  TextEditingController _predictionController = TextEditingController();
  TextField _predictionTextField;

  /// Function which validates the input from the user
  /// return: String, a message which contains all the wrong inputs of the user
  ///         the empty String denotes no problem with the input
  String checkInput(){
    String message = "";
    if(_rate == null) {
      message += "Please choose an exchange rate!\n";}
    return message;
  }

  /// Function which computes the date for tomorrow
  /// return: String, the date in the format Year-Month-Day
  String getTomorrowDate() {
    final tomorrowDate = DateTime.now().add((Duration(days: 1)));
    final formatter = new DateFormat('yyyy-MM-dd');
    String formattedDate = formatter.format(tomorrowDate);
    return formattedDate;
  }

  /// The function which collects the input from the user and retrieves the prediction for the specified exchange rate
  /// This function is bound to the getPredictionButton button
  getPrediction() async{
    var connectivityResult = await (Connectivity().checkConnectivity());
    // check for network connectivity
    if (!(connectivityResult == ConnectivityResult.mobile || connectivityResult == ConnectivityResult.wifi)){
      // if no connection is available, explain it to the user
      showAlertDialog("Oops, you did something wrong", "Please connect the device to Internet!");
    }
    else{
      // check the input from the user
      String message = checkInput();
      if(message.isEmpty){
        // if there is no problem with the input, make the call to the server
      double result = await _server.getPrediction(_rate.substring(0,3),_rate.substring(4,7), DateTime.now().add(Duration(days: 1)));
      _predictionController.text = result.toStringAsPrecision(6);}
      else{
        // display error message to the user explaining where the mistakes were
        showAlertDialog("Oops, you did something wrong", message);
      }
    }
  }

  /// Function for displaying error states
  /// @param: String title, the title of the error
  /// @param: String message, details explaining the error
  void showAlertDialog(String title, String message) {
    AlertDialog alertDialog = AlertDialog(
      title: Text(title),
      content: Text(message),
    );
    showDialog(
        context: context,
        builder: (_) => alertDialog
    );
  }

  @override
  void initState() {
    super.initState();
    _getPredictionButton = RaisedButton(
      onPressed: getPrediction,
      child: Text("Get prediction"),
    );
    _predictionTextField = TextField(
      controller: _predictionController,
      textAlign: TextAlign.center,
      readOnly: true,
    );
  }

  /// Function for creating the list with items in the dropdown
  /// return: List<DropdownMenuItem<String>>, a list with elements of DropdownMenuItem<> of type String
  List<DropdownMenuItem<String>> getDropDownMenuItems() {
    List<DropdownMenuItem<String>> items = new List();
    for (String rate in _rates) {
      items.add(new DropdownMenuItem(
          value: rate,
          child: new Text(rate)
      ));
    }
    return items;
  }

  @override
  Widget build(BuildContext context) {
    return new Container(
      color: Colors.white,
      child: new Center(
          child: new Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.all(20.0),
                child: new Text("Predict exchange rates for " + getTomorrowDate(),
                  style: new TextStyle(
                    fontSize: 20.0,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: new Text("Please choose the exchange rate: ",
                  style: new TextStyle(
                    fontSize: 15.0,
                  ),
                ),
              ),
              new DropdownButton<String>(
                  value: _rate,
                  items: getDropDownMenuItems(),
                  onChanged: (String newValue) {
                    setState(() {
                      _rate = newValue;
                    });
                  }
              ),
              _getPredictionButton,
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: Container(
                    width: 235.0,
                    child: _predictionTextField),
              ),
            ],
          )
      ),
    );
  }
}
