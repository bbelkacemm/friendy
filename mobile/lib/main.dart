import 'package:flutter/material.dart';
import 'package:mobile/providers/Authentication.dart';
import 'package:mobile/providers/Chat.dart';
import 'package:mobile/screens/chat_screen.dart';
import 'package:mobile/screens/login_screen.dart';

import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (_) => Authentication()),
    ],
    child: MyApp(),
  ));
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Friendy',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      localizationsDelegates: [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: [
        const Locale('en', ''),
        const Locale('fr', ''),
        const Locale('ar', ''),
      ],
      home: Scaffold(
        body: Center(
          child: Consumer<Authentication>(
            builder: (_, builder, __) {
              if (builder.user != null) {
                return MultiProvider(
                  providers: [
                    ChangeNotifierProvider(create: (_) => Chat()),
                  ],
                  child: ChatScreen(),
                );
              }
              return LoginScreen();
            },
          ),
        ),
      ),
    );
  }
}
