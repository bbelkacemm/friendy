import 'package:flutter/material.dart';

typedef OnPressed = void Function();

class InputField extends StatelessWidget {
  final String hint;
  final IconData? icon;
  final bool obscureText;
  final OnPressed? onPressed;
  final TextEditingController controller;

  const InputField({
    Key? key,
    this.onPressed,
    required this.controller,
    required this.hint,
    this.icon,
    this.obscureText = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(64),
        color: Colors.grey.shade100,
      ),
      child: Row(
        children: [
          Expanded(
            child: Container(
              padding: EdgeInsets.symmetric(horizontal: 32, vertical: 4),
              child: TextField(
                obscureText: obscureText,
                controller: controller,
                decoration: InputDecoration(
                  border: InputBorder.none,
                  hintText: hint,
                  hintStyle: TextStyle(color: Colors.grey.shade400),
                ),
              ),
            ),
          ),
          if (icon != null)
            IconButton(
              onPressed: onPressed,
              icon: Icon(
                icon,
                color: Colors.blueAccent,
              ),
              highlightColor: Colors.white,
              splashColor: Colors.white,
            )
        ],
      ),
    );
  }
}
