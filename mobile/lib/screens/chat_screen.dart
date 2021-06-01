import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/painting.dart';
import 'package:mobile/models/Message.dart';
import 'package:mobile/providers/Authentication.dart';
import 'package:mobile/providers/Chat.dart';
import 'package:mobile/widgets/ChatItem.dart';
import 'package:mobile/widgets/InputField.dart';
import 'package:mobile/widgets/PropositionItem.dart';
import 'package:provider/provider.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({Key? key}) : super(key: key);

  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  TextEditingController _messageController = TextEditingController();

  late Chat _chat;
  late Authentication _authentication;

  @override
  void initState() {
    _chat = Provider.of<Chat>(
      context,
      listen: false,
    );
    _authentication = Provider.of<Authentication>(
      context,
      listen: false,
    );
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Friendy',
          style: TextStyle(color: Colors.blueAccent),
        ),
        actions: [
          IconButton(
            onPressed: displayProfile,
            icon: CircleAvatar(
              backgroundColor: Colors.grey.shade200,
            ),
            splashRadius: 20,
          ),
        ],
        backgroundColor: Colors.white,
        elevation: 0,
      ),
      backgroundColor: Colors.white,
      body: Container(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                reverse: true,
                child: Consumer<Chat>(builder: (_, builder, __) {
                  return Column(
                    children: [
                      for (var message in builder.messages)
                        ChatItem(
                          message: message,
                        )
                    ],
                  );
                }),
              ),
            ),
            Consumer<Chat>(builder: (_, builder, __) {
              return Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  for (var proposition in builder.propositions)
                    PropositionItem(
                        proposition: proposition, onPressed: sendProposition),
                ],
              );
            }),
            Container(
              margin: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
              child: InputField(
                hint: 'What\'s on your mind?',
                icon: Icons.send,
                onPressed: sendMessage,
                controller: _messageController,
              ),
            ),
          ],
        ),
      ),
    );
  }

  void sendMessage() {
    _chat.add(_messageController.text);
    _chat.send(_messageController.text);
    _messageController.clear();
  }

  void sendProposition(String value) {
    _chat.add(value);
    _chat.send(value);
  }

  void displayProfile() {
    showModalBottomSheet(
      context: context,
      builder: (_) {
        return Container(
          height: 150,
          child: Row(
            children: [
              Container(
                margin: EdgeInsets.all(16),
                child: CircleAvatar(
                  backgroundColor: Colors.grey.shade200,
                  radius: 32,
                ),
              ),
              Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.only(bottom: 4.0),
                      child: Text(
                        _authentication.user!.getFullName() ?? '',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    Row(
                      children: [
                        Padding(
                          padding: const EdgeInsets.only(right: 8.0),
                          child: Text(
                            '${_authentication.user!.getAge()} ans',
                            style: TextStyle(
                              color: Colors.grey.shade600,
                            ),
                          ),
                        ),
                        Icon(
                          _authentication.user!.isMale() ? Icons.male : Icons.female,
                          color: _authentication.user!.isMale() ? Colors.blue : Colors.pink,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              Container(
                margin: EdgeInsets.all(16),
                child: Row(
                  children: [
                    IconButton(
                      icon: Icon(Icons.settings),
                      onPressed: () {},
                      splashRadius: 20,
                    ),
                    IconButton(
                      icon: Icon(Icons.logout),
                      onPressed: () {
                        _authentication.logout();
                        Navigator.pop(context);
                      },
                      splashRadius: 20,
                    ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
      barrierColor: Colors.black.withAlpha(16),
    );
  }
}
