import 'package:flutter/material.dart';
import 'package:mobile/models/Message.dart';

class ChatItem extends StatelessWidget {
  final Message message;

  const ChatItem({Key? key, required this.message}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Builder(builder: (_) {
      if (message.owner == Owner.BOT) {
        return Row(
          children: [
            getAvatar(),
            getMessage(),
            Spacer(),
          ],
        );
      } else {
        return Row(
          children: [
            Spacer(),
            getMessage(),
            getAvatar(),
          ],
        );
      }
    });
  }

  Widget getAvatar() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          CircleAvatar(
            backgroundColor: Colors.grey.shade200,
          ),
          Padding(
            padding: const EdgeInsets.only(top: 4.0),
            child: Text(
              '${message.dateTime?.hour}:${message.dateTime?.minute}',
              style: TextStyle(fontSize: 12, color: Colors.grey.shade500),
            ),
          )
        ],
      ),
    );
  }

  Widget getMessage() {
    return Expanded(
      child: Container(
        child: Text(
          message.value!,
          style: TextStyle(color: message.owner == Owner.BOT ? Colors.white : Colors.grey.shade900),
        ),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.only(
            topLeft: message.owner == Owner.BOT
                ? Radius.circular(8)
                : Radius.circular(16),
            topRight: message.owner == Owner.BOT
                ? Radius.circular(16)
                : Radius.circular(8),
            bottomLeft: Radius.circular(16),
            bottomRight: Radius.circular(16),
          ),
          boxShadow: [
            if (message.owner == Owner.BOT)
              BoxShadow(
                color: Colors.grey.shade300,
                offset: Offset(0.0, 6), //(x,y)
                blurRadius: 4.0,
              ),
          ],
          color: message.owner == Owner.BOT ? Colors.blueAccent : Colors.grey.shade100,
        ),
        padding: EdgeInsets.symmetric(horizontal: 16, vertical: 16),
      ),
    );
  }
}
