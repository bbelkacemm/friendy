import 'package:flutter/material.dart';
import 'package:mobile/models/Proposition.dart';

typedef OnPressed = void Function(String message);

class PropositionItem extends StatelessWidget {
  final Proposition proposition;
  final OnPressed onPressed;

  const PropositionItem(
      {Key? key, required this.proposition, required this.onPressed})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {
        onPressed(proposition.value!);
      },
      child: Container(
        margin: EdgeInsets.all(4),
        padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(64),
          color: Colors.grey.shade200,
          boxShadow: [
            BoxShadow(
              color: Colors.grey.shade300,
              offset: Offset(0.0, 4), //(x,y)
              blurRadius: 4.0,
            ),
          ],
        ),
        child: Text(
          proposition.value!,
        ),
      ),
    );
  }
}
