import 'package:flutter/material.dart';

class ColorPickerTile extends StatelessWidget {
  final Color color;
  final bool isSelected;
  final VoidCallback onTap;

  const ColorPickerTile({super.key, required this.color, required this.isSelected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 40,
        height: 40,
        decoration: BoxDecoration(
          color: color,
          shape: BoxShape.circle,
          border: isSelected
              ? Border.all(color: Theme.of(context).colorScheme.primary, width: 3)
              : Border.all(color: Colors.grey.shade300),
          boxShadow: [BoxShadow(color: Colors.black.withAlpha(26), blurRadius: 4, offset: const Offset(0, 2))],
        ),
        child: isSelected ? const Icon(Icons.check, color: Colors.white, size: 20) : null,
      ),
    );
  }
}
