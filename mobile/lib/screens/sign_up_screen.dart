import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:mobile/generated/l10n.dart';
import 'package:mobile/providers/Authentication.dart';
import 'package:mobile/widgets/InputField.dart';
import 'package:provider/provider.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({Key? key}) : super(key: key);

  @override
  _SignUpScreenState createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  late Authentication _authentication;

  TextEditingController _usernameController = TextEditingController();
  TextEditingController _passwordController = TextEditingController();
  TextEditingController _confirmPasswordController = TextEditingController();
  TextEditingController _firstNameController = TextEditingController();
  TextEditingController _lastNameController = TextEditingController();
  TextEditingController _birthdateController = TextEditingController();

  DateTime? _birthdate;

  List<bool> _gender = List.generate(2, (index) => false);

  final _formKey = GlobalKey<FormState>();

  @override
  void initState() {
    _authentication = Provider.of<Authentication>(
      context,
      listen: false,
    );
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.white,
          elevation: 0,
          iconTheme: IconThemeData(color: Colors.black),
        ),
        body: SingleChildScrollView(
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                  child: InputField(
                    controller: _usernameController,
                    hint: S.of(context).username.toUpperCase(),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return S.of(context).requiredField;
                      }
                      return null;
                    },
                  ),
                ),
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                  child: InputField(
                    obscureText: true,
                    controller: _passwordController,
                    hint: S.of(context).password.toUpperCase(),
                    validator: (value) {
                      if (value == null) {
                        return S.of(context).requiredField;
                      } else if (value.length < 8) {
                        return S.of(context).passwordLength;
                      }
                      return null;
                    },
                  ),
                ),
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                  child: InputField(
                    obscureText: true,
                    controller: _confirmPasswordController,
                    hint: S.of(context).confirmPassword.toUpperCase(),
                    validator: (value) {
                      if (value == null) {
                        return S.of(context).requiredField;
                      } else if (value.length < 8) {
                        return S.of(context).passwordLength;
                      } else if (value != _passwordController.text) {
                        return S.of(context).passwordMatch;
                      }
                      return null;
                    },
                  ),
                ),
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                  child: InputField(
                    controller: _firstNameController,
                    hint: S.of(context).firstName.toUpperCase(),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return S.of(context).requiredField;
                      }
                      return null;
                    },
                  ),
                ),
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                  child: InputField(
                    controller: _lastNameController,
                    hint: S.of(context).lastName.toUpperCase(),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return S.of(context).requiredField;
                      }
                      return null;
                    },
                  ),
                ),
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                  child: InputField(
                    readOnly: true,
                    controller: _birthdateController,
                    hint: S.of(context).birthdate.toUpperCase(),
                    icon: Icons.calendar_today,
                    onPressed: () {
                      _selectDate(context);
                    },
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return S.of(context).requiredField;
                      }
                      return null;
                    },
                  ),
                ),
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 0, vertical: 4),
                  child: ToggleButtons(
                    borderRadius: BorderRadius.circular(64),
                    children: [
                      Container(
                        width: (MediaQuery.of(context).size.width - 32) / 2,
                        child: Icon(Icons.female),
                      ),
                      Container(
                        width: (MediaQuery.of(context).size.width - 32) / 2,
                        child: Icon(Icons.male),
                      ),
                    ],
                    onPressed: (int index) {
                      setState(() {
                        for (int buttonIndex = 0;
                            buttonIndex < _gender.length;
                            buttonIndex++) {
                          if (buttonIndex == index) {
                            _gender[buttonIndex] = true;
                          } else {
                            _gender[buttonIndex] = false;
                          }
                        }
                      });
                    },
                    isSelected: _gender,
                  ),
                ),
                Container(
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 16),
                  child: Row(
                    children: [
                      Container(
                        margin: EdgeInsets.all(4),
                        child: TextButton(
                          onPressed: () {
                            _usernameController.clear();
                            _passwordController.clear();
                            _confirmPasswordController.clear();
                            _firstNameController.clear();
                            _lastNameController.clear();
                            _birthdateController.clear();
                          },
                          style: ButtonStyle(
                            shape: MaterialStateProperty.all<
                                RoundedRectangleBorder>(
                              RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(64),
                              ),
                            ),
                          ),
                          child: Text(
                            S.of(context).clear.toUpperCase(),
                            style: TextStyle(
                              color: Colors.grey,
                            ),
                          ),
                        ),
                      ),
                      Expanded(
                        child: Container(
                          margin: EdgeInsets.all(4),
                          child: ElevatedButton(
                            style: ButtonStyle(
                              shape: MaterialStateProperty.all<
                                  RoundedRectangleBorder>(
                                RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(64),
                                ),
                              ),
                            ),
                            onPressed: () async {
                              if (_formKey.currentState!.validate()) {
                                bool result = await _authentication.signup(
                                  username: _usernameController.text,
                                  password: _passwordController.text,
                                  firstName: _firstNameController.text,
                                  lastName: _lastNameController.text,
                                  birthdate: _birthdate,
                                  gender: _gender[0] == true ? 'f' : 'm',
                                );
                                if (result == true) {
                                  Navigator.pop(context);
                                }
                              }
                            },
                            child: Text(
                              S.of(context).signup.toUpperCase(),
                            ),
                          ),
                        ),
                      )
                    ],
                  ),
                )
              ],
            ),
          ),
        ),
        backgroundColor: Colors.white,
      ),
    );
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? selected = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );
    if (selected != null && selected != _birthdate) {
      setState(() {
        _birthdate = selected;
        _birthdateController.text =
            DateFormat('EEEE dd MMM yyyy').format(_birthdate!).toString();
      });
    }
  }
}
