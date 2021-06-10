import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:mobile/constants/api.dart';
import 'package:mobile/models/Message.dart';
import 'package:http/http.dart' as http;
import 'package:mobile/models/Proposition.dart';

class Chat with ChangeNotifier {
  List<Message> messages = [];
  List<Proposition> propositions = [];

  Future<dynamic> send(String userInput) async {
    var uri = Uri.http(
      URL,
      BOT_PATH,
      {
        'lang': 'en',
        'user-input': userInput,
        'tag': 'prod',
      },
    );
    var response = await http.get(uri);
    if (response.statusCode == 200) {
      Message message = Message.fromJson(jsonDecode(response.body));
      messages.add(message);
      propositions = Proposition.fromJson(jsonDecode(response.body));
      notifyListeners();
      return {'value': true};
    } else {
      return {
        'value': false,
        'message': response.body,
      };
    }
  }

  void add(String userInput) {
    messages.add(Message(
      value: userInput,
      owner: Owner.USER,
      dateTime: DateTime.now(),
    ));
    notifyListeners();
  }
}
