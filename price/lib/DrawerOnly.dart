import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:price/pastPage.dart';
import 'package:price/pastPredictionPage.dart';
import 'package:price/predictionPage.dart';

import 'main.dart';

class DrawerOnly extends StatelessWidget{
  @override
  Widget build(BuildContext context) {
    return new Drawer(
        child: new ListView(
          children: <Widget>[
            new ListTile(
              title: new Text("See current exchange rates"),
              onTap: (){
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => new MyHomePage(title: 'Current exchange rates')));
              },
            ),
            new ListTile(
              title: new Text("Predict exchange rates"),
              onTap: (){
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => new PredictionPage(title: 'Predictions')));
              },
            ),
            new ListTile(
              title: new Text("See past exchange rates"),
              onTap: (){
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => new PastPage(title: "Past exchange rates")));
              },
            ),
            new ListTile(
              title: new Text("See past predictions of exchange rates"),
              onTap: (){
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => new PastPredictionPage(title: "Past predictions")));},
            ),
          ],
        ),
    );
  }
}