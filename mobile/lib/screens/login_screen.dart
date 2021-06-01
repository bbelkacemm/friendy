import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:mobile/providers/Authentication.dart';
import 'package:mobile/widgets/InputField.dart';
import 'package:provider/provider.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  late Authentication _authentication;

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
    return Scaffold(
      body: Container(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                margin: EdgeInsets.all(4),
                child: InputField(
                  hint: AppLocalizations.of(context)!.username.toUpperCase(),
                  controller: _usernameController,
                ),
              ),
              Container(
                margin: EdgeInsets.all(4),
                child: InputField(
                  hint: AppLocalizations.of(context)!.password.toUpperCase(),
                  obscureText: true,
                  controller: _passwordController,
                ),
              ),
              Row(
                children: [
                  Container(
                    margin: EdgeInsets.all(4),
                    child: TextButton(
                      onPressed: () {},
                      child: Text(
                        AppLocalizations.of(context)!.signup.toUpperCase(),
                        style: TextStyle(
                          color: Colors.grey,
                        ),
                      ),
                    ),
                  ),
                  Expanded(
                    child: Container(
                      margin: EdgeInsets.all(4),
                      child: OutlinedButton(
                        onPressed: login,
                        child: Text(
                          AppLocalizations.of(context)!.login.toUpperCase(),
                        ),
                      ),
                    ),
                  )
                ],
              )
            ],
          ),
        ),
      ),
    );
  }

  void login() {
    _authentication.login(_usernameController.value.text, _passwordController.value.text);
  }
}
