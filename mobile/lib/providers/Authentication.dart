import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:mobile/constants/api.dart';
import 'package:mobile/models/User.dart';
import 'package:http/http.dart' as http;

class Authentication with ChangeNotifier {
  User? user;

  void login(String username, String password) async {
    var uri = Uri.http(URL, LOGIN_PATH);
    var response = await http.post(
      uri,
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
      headers: {"Content-Type": "application/json"},
    );
    if(response.statusCode == 200) {
      user = User.fromJson(jsonDecode(response.body));
    }
    notifyListeners();
  }

  void logout() {
    user = null;
    notifyListeners();
  }
}
