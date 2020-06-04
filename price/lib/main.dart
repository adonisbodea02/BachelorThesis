import 'dart:convert';

import 'package:connectivity/connectivity.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'DrawerOnly.dart';
import 'ServerHelper.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Current exchange rates'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      drawer: new DrawerOnly(),
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: ListView(
          children: <Widget>[
            CurrentWidget(),
          ]
        )
      ),// This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}

class CurrentWidget extends StatefulWidget {
  CurrentWidget({Key key}) : super(key: key);

  @override
  _CurrentWidgetState createState() => new _CurrentWidgetState();
}

class _CurrentWidgetState extends State<CurrentWidget> {

  ServerHelper _server = ServerHelper();
  List<String> _currencies = <String>[];
  String _currentLocalCurrency;
  String _currentForeignCurrency;
  TextEditingController _sumController = TextEditingController();
  TextField _sumText;
  RaisedButton _convertButton;
  TextEditingController _resultController = TextEditingController();
  TextField _resultText;

  /// Function for retrieving and initializing the list of currencies available
  /// The currencies are read from a JSON file
  getCurrencyList() async {
    String jsonRes = await rootBundle.loadString('assets/currencies.json');
    var res = json.decode(jsonRes);
    setState(() {
      res.forEach((k,v) => _currencies.add(k + " (" + v + ")"));
    });
  }

  /// Function which checks if a string can be interpreted as a number
  /// @param: String string, the String to be checked
  /// return: Boolean, true if the string can be interpreted as a number, false otherwise
  isNumeric(string) => num.tryParse(string) != null;

  /// Function which validates the input from the user
  /// return: String, a message which contains all the wrong inputs of the user
  ///         the empty String denotes no problem with the input
  String checkInput(){
    String message = "";
    if(_currentLocalCurrency == null) {
      message += "Please choose a local currency!\n";}
    if(_currentForeignCurrency == null) {
      message += "Please choose a foreing currency!\n";}
    if(_sumController.text.isEmpty) {
      message += "Please type a number!\n"; }
    else {
      if(!isNumeric(_sumController.text)) {
        message += "Please type a proper number!\n";}
      else{
        if(double.parse(_sumController.text) < 0){
          message += "Please type a positive number!\n";
        }
      }
    }
    return message;
  }

  /// The function which collects the input from the user and converts the sum specified from the local currency to the foreign one
  /// This function is bound to the convert convertButton
  convert() async{
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
        double result = await _server.getCurrentRate(_currentLocalCurrency.substring(0,3),_currentForeignCurrency.substring(0,3));
        result = result * double.parse(_sumController.text);
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
    _sumText = TextField(
      controller: _sumController,
      keyboardType: TextInputType.number,
      textAlign: TextAlign.center,
    );
    _convertButton = RaisedButton(
      onPressed: convert,
      child: Text("Convert"),
    );
    _resultText = TextField(
      controller: _resultController,
      textAlign: TextAlign.center,
      readOnly: true,
    );
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
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: new Text("Please type the sum: ",
                  style: new TextStyle(
                    fontSize: 15.0,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(10.0),
                child: Container(
                    width: 235.0,
                    child: _sumText),
              ),
              _convertButton,
              Padding(
                padding: const EdgeInsets.all(10.0),
                child:               Container(
                    width: 235.0,
                    child: _resultText),
              ),
            ],
          )
      ),
    );
  }
}







