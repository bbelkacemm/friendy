import 'package:flutter/material.dart';

typedef OnPressed = void Function();
typedef Validator = String? Function(String? value);

class InputField extends StatefulWidget {
  final String hint;
  final IconData? icon;
  final bool obscureText;
  final bool readOnly;
  final OnPressed? onPressed;
  final TextEditingController controller;
  final Validator? validator;

  const InputField({
    Key? key,
    this.onPressed,
    required this.controller,
    required this.hint,
    this.icon,
    this.obscureText = false,
    this.readOnly = false,
    this.validator,
  }) : super(key: key);

  @override
  _InputFieldState createState() => _InputFieldState();
}

class _InputFieldState extends State<InputField> {
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
              child: TextFormField(
                readOnly: widget.readOnly,
                obscureText: widget.obscureText,
                controller: widget.controller,
                validator: widget.validator,
                decoration: InputDecoration(
                  border: InputBorder.none,
                  hintText: widget.hint,
                  hintStyle: TextStyle(color: Colors.grey.shade400),
                ),
              ),
            ),
          ),
          if (widget.icon != null)
            Container(
              margin: EdgeInsets.only(right: 8),
              child: IconButton(
                onPressed: widget.onPressed,
                icon: Icon(
                  widget.icon,
                  color: Colors.blueAccent,
                ),
                highlightColor: Colors.white,
                splashColor: Colors.white,
              ),
            )
        ],
      ),
    );
  }
}
