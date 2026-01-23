import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_app/bloc/qr_event.dart';
import 'package:flutter_app/bloc/qr_state.dart';
import 'package:flutter_app/models/qr_data.dart';
import 'package:palette_generator/palette_generator.dart';
import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';

class QrBloc extends Bloc<QrEvent, QrState> {
  QrBloc() : super(QrState.initial()) {
    on<QrStyleChanged>(_onStyleChanged);
    on<QrContentChanged>(_onContentChanged);
    on<QrCardAdded>(_onCardAdded);
    on<QrCardRemoved>(_onCardRemoved);
    on<QrImageUploaded>(_onImageUploaded);
  }

  void _onStyleChanged(QrStyleChanged event, Emitter<QrState> emit) {
    emit(state.copyWith(style: event.style));
  }

  void _onContentChanged(QrContentChanged event, Emitter<QrState> emit) {
    final updatedCards = state.cards.map((card) {
      return card.id == event.content.id ? event.content : card;
    }).toList();
    emit(state.copyWith(cards: updatedCards));
  }

  void _onCardAdded(QrCardAdded event, Emitter<QrState> emit) {
    // Clone the last card's content for convenience, or default
    final lastCard = state.cards.isNotEmpty ? state.cards.last : null;
    final newContent = lastCard?.copyWith() ?? const QrContent(id: ''); // id overwritten below

    // We need to create a new QrContent with a new ID but same data
    final newCard = QrContent(
      id: const Uuid().v4(),
      url: newContent.url,
      appName: newContent.appName,
      appVersion: newContent.appVersion,
      platform: newContent.platform,
    );

    emit(state.copyWith(cards: [...state.cards, newCard]));
  }

  void _onCardRemoved(QrCardRemoved event, Emitter<QrState> emit) {
    if (state.cards.length <= 1) return; // Prevent removing the last card
    final updatedCards = state.cards.where((c) => c.id != event.cardId).toList();
    emit(state.copyWith(cards: updatedCards));
  }

  Future<void> _onImageUploaded(QrImageUploaded event, Emitter<QrState> emit) async {
    emit(state.copyWith(isLoading: true));

    try {
      final paletteGenerator = await PaletteGenerator.fromImageProvider(event.imageProvider, maximumColorCount: 20);

      final colors = paletteGenerator.paletteColors.map((paletteColor) => paletteColor.color).toList();

      colors.sort((a, b) => HSVColor.fromColor(a).hue.compareTo(HSVColor.fromColor(b).hue));

      emit(state.copyWith(isLoading: false, extractedColors: colors));
    } catch (e) {
      // Handle error
      emit(state.copyWith(isLoading: false));
    }
  }
}
