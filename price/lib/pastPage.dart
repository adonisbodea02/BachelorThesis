import 'dart:convert';

import 'package:connectivity/connectivity.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';

import 'DrawerOnly.dart';
import 'ServerHelper.dart';

class PastPage extends StatefulWidget {
  PastPage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _PastPageState createState() => _PastPageState();
}

class _PastPageState extends State<PastPage> {

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
                PastWidget(),
              ]
          )
      ),// This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}

class PastWidget extends StatefulWidget {
  PastWidget({Key key}) : super(key: key);

  @override
  _PastWidgetState createState() => new _PastWidgetState();
}

class _PastWidgetState extends State<PastWidget> {

  ServerHelper _server = ServerHelper();
  List<String> _currencies = <String>[];
  String _currentLocalCurrency;
  String _currentForeignCurrency;
  DateTime _pastDate;
  DateFormat _formatter;
  TextEditingController _pastDateController = TextEditingController();
  TextField _pastDateTextField;
  RaisedButton _getPastRateButton;
  TextEditingController _resultController = TextEditingController();
  TextField _resultTextField;

  /// Function for retrieving and initializing the list of currencies available
  /// The currencies are read from a JSON file
  getCurrencyList() async {
    String jsonRes = await rootBundle.loadString('assets/currencies.json');
    var res = json.decode(jsonRes);
    setState(() {
      res.forEach((k,v) => _currencies.add(k + " (" + v + ")"));
    });
  }

  /// Function which validates the input from the user
  /// return: String, a message which contains all the wrong inputs of the user
  ///         the empty String denotes no problem with the input
  String checkInput(){
    String message = "";
    if(_currentLocalCurrency == null) {
      message += "Please choose a local currency!\n";}
    if(_currentForeignCurrency == null) {
      message += "Please choose a foreing currency!\n";}
    return message;
  }

  /// The function which collects the input from the user and retrieves the value of the exchange rate specified by the local and
  /// foreign currencies in the selected day
  /// This function is bound to the getPastRateButton button
  getPastRate() async{
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
        double result = await _server.getPastRate(_currentLocalCurrency.substring(0,3),
            _currentForeignCurrency.substring(0,3), _pastDate);
        _resultController.text = result.toString();}
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
    getCurrencyList();
    _getPastRateButton = RaisedButton(
      onPressed: getPastRate,
      child: Text("Get rate"),
    );
    _pastDateTextField = TextField(
      controller: _pastDateController,
      textAlign: TextAlign.center,
      readOnly: true,
    );
    _resultTextField = TextField(
      controller: _resultController,
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
    for (String currency in _currencies) {
      items.add(new DropdownMenuItem(
          value: currency,
          child: new Text(currency)
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
                child: new Text("Please choose the local currency: ",
                  style: new TextStyle(
                    fontSize: 15.0,
                  ),
                ),
              ),
              new DropdownButton<String>(
                  value: _currentLocalCurrency,
                  items: getDropDownMenuItems(),
                  onChanged: (String newValue) {
                    setState(() {
                      _currentLocalCurrency = newValue;
                    });
                  }
              ),
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: new Text("Please choose the foreign currency: ",
                  style: new TextStyle(
                    fontSize: 15.0,
                  ),
                ),
              ),
              new DropdownButton<String>(
                  value: _currentForeignCurrency,
                  items: getDropDownMenuItems(),
                  onChanged: (String newValue) {
                    setState(() {
                      _currentForeignCurrency = newValue;
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
              _getPastRateButton,
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: Container(
                    width: 235.0,
                    child: _resultTextField),
              ),
            ],
          )
      ),
    );
  }
}