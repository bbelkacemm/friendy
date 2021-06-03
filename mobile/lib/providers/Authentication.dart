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
    if (response.statusCode == 200) {
      user = User.fromJson(jsonDecode(response.body));
    }
    notifyListeners();
  }

  void loginAsGuest() {
    user = User(
      'guest.guest',
      'Guest',
      'Guest',
      'm',
      DateTime.now(),
    );
    notifyListeners();
  }

  Future<bool> signup({
    String? username,
    String? password,
    String? firstName,
    String? lastName,
    DateTime? birthdate,
    String? gender,
  }) async {
    var uri = Uri.http(URL, SIGN_UP);
    var response = await http.post(
      uri,
      body: jsonEncode({
        'username': username,
        'password': password,
        'first_name': firstName,
        'last_name': lastName,
        'birth_date': birthdate.toString(),
        'gender': gender,
      }),
      headers: {"Content-Type": "application/json"},
    );
    if (response.statusCode == 201) {
      return true;
    }
    return false;
  }

  void logout() {
    user = null;
    notifyListeners();
  }
}
