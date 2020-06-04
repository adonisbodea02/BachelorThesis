import 'package:timezone/data/latest.dart' as tz;
import 'package:timezone/timezone.dart' as tz;
import 'package:tuple/tuple.dart';

class TimezoneHelper {
  TimezoneHelper() {
    setup();
  }

  Future<void> setup() async {
    tz.initializeTimeZones();
  }

  /// Function which converts the local time of the user to the CET time
  /// return: Tuple2<int, int>, a tuple of Integers which denote the hour and the minute of the converted time
  Tuple2<int, int> convertLocalToCET() {
    tz.TZDateTime parisTime = new tz.TZDateTime.from(DateTime.now(), tz.getLocation('Europe/Paris'));
    return Tuple2<int, int>(parisTime.hour, parisTime.minute);
  }
}