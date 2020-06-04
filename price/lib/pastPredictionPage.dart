import 'package:connectivity/connectivity.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import 'DrawerOnly.dart';
import 'ServerHelper.dart';

class PastPredictionPage extends StatefulWidget {
  PastPredictionPage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _PastPredictionPageState createState() => _PastPredictionPageState();
}

class _PastPredictionPageState extends State<PastPredictionPage> {

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
                PastPredictionWidget(),
              ]
          )
      ),// This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}

class PastPredictionWidget extends StatefulWidget {
  PastPredictionWidget({Key key}) : super(key: key);

  @override
  _PastPredictionWidgetState createState() => new _PastPredictionWidgetState();
}

class _PastPredictionWidgetState extends State<PastPredictionWidget> {

  ServerHelper _server = ServerHelper();
  List<String> _rates = <String>["EUR/GBP", "EUR/USD", "GBP/USD"];
  String _rate;
  DateTime _pastDate;
  DateFormat _formatter;
  TextEditingController _pastDateController = TextEditingController();
  TextField _pastDateTextField;
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

  /// The function which collects the input from the user and retrieves the prediction for the specified exchange rate and date
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
      double result = await _server.getPrediction(_rate.substring(0,3),_rate.substring(4,7), _pastDate);
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
    _pastDateTextField = TextField(
      controller: _pastDateController,
      textAlign: TextAlign.center,
      readOnly: true,
    );
    _pastDate = DateTime.now();
    _formatter = new DateFormat('yyyy-MM-dd');
    _pastDateController.text = _formatter.format(_pastDate);
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
              RaisedButton(
                child: Text('Select a date'),
                onPressed: () {
                  // calendar is displayed to the user
                  showDatePicker(
                      context: context,
                      initialDate: _pastDate == null ? DateTime.now() : _pastDate,
                      firstDate: DateTime(2000),
                      lastDate: DateTime.now()
                  ).then((date) {
                    // after the user chose the date, the selected date is saved
                    // and displayed to the user
                    setState(() {
                      _pastDate = date;
                      _pastDateController.text = _formatter.format(date);
                    });
                  });
                },
              ),
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: Container(
                    width: 235.0,
                    child: _pastDateTextField),
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
