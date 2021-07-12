import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:mobile/providers/Authentication.dart';
import 'package:mobile/providers/Chat.dart';
import 'package:mobile/providers/Configurations.dart';
import 'package:mobile/screens/chat_screen.dart';
import 'package:mobile/screens/login_screen.dart';

import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';
import 'package:flutter/services.dart';

import 'generated/l10n.dart';

void main() {
  SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle(
    systemNavigationBarIconBrightness: Brightness.dark,
    statusBarIconBrightness: Brightness.dark,
    systemNavigationBarColor: Colors.white,
    statusBarColor: Colors.white,
  ));

  runApp(MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (_) => Configurations()),
      ChangeNotifierProvider(create: (_) => Authentication()),
    ],
    child: MyApp(),
  ));
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Friendy',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      localizationsDelegates: [
        S.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: [
        const Locale('en', ''),
        const Locale('fr', ''),
        const Locale('ar', ''),
      ],
      home: Consumer<Configurations>(
        builder: (_, builder, __) {
          return Directionality(
            textDirection: builder.language == 'ar'
                ? TextDirection.rtl
                : TextDirection.ltr,
            child: Scaffold(
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
        },
      ),
    );
  }
}
