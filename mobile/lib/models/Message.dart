enum Owner { USER, BOT }

class Message {
  String? value;
  Owner? owner;
  DateTime? dateTime;

  Message({this.value, this.owner, this.dateTime});

  static Message fromJson(json) {
    return Message(
      value: json['response'],
      owner: Owner.BOT,
      dateTime: DateTime.now(),
    );
  }
}
