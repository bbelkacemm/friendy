import 'package:intl/intl.dart';

class User {
  String username;
  String firstName;
  String lastName;
  String gender;
  DateTime birthdate;

  User(this.username, this.firstName, this.lastName, this.gender,
      this.birthdate);

  static User fromJson(json) {
    return User(
      json['username'],
      json['firstName'],
      json['lastName'],
      json['gender'],
      DateFormat('EEE, d MMM yyyy').parse(json['birthdate']),
    );
  }

  String getFullName() {
    return '$firstName $lastName';
  }

  int getAge() {
    return DateTime.now().year - birthdate.year;
  }

  bool isMale() {
    return gender == 'm';
  }
}
