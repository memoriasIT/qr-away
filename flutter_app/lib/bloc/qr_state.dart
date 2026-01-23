import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';
import 'package:flutter_app/models/qr_data.dart';
import 'package:uuid/uuid.dart';

class QrState extends Equatable {
  final QrStyle style;
  final List<QrContent> cards;
  final bool isLoading;
  final List<Color> extractedColors;

  const QrState({required this.style, required this.cards, this.isLoading = false, this.extractedColors = const []});

  factory QrState.initial() {
    return QrState(
      style: const QrStyle(),
      cards: [QrContent(id: const Uuid().v4())],
    );
  }

  QrState copyWith({QrStyle? style, List<QrContent>? cards, bool? isLoading, List<Color>? extractedColors}) {
    return QrState(
      style: style ?? this.style,
      cards: cards ?? this.cards,
      isLoading: isLoading ?? this.isLoading,
      extractedColors: extractedColors ?? this.extractedColors,
    );
  }

  @override
  List<Object?> get props => [style, cards, isLoading, extractedColors];
}
