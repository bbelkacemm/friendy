import 'package:flutter/cupertino.dart';

class Configurations with ChangeNotifier {
  String? language;

  void setLanguage(language) {
    this.language = language;
    notifyListeners();
  }
}
