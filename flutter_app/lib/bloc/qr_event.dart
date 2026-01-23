import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';
import 'package:flutter_app/models/qr_data.dart';

abstract class QrEvent extends Equatable {
  const QrEvent();

  @override
  List<Object?> get props => [];
}

class QrStyleChanged extends QrEvent {
  final QrStyle style;

  const QrStyleChanged(this.style);

  @override
  List<Object?> get props => [style];
}

class QrContentChanged extends QrEvent {
  final QrContent content;

  const QrContentChanged(this.content);

  @override
  List<Object?> get props => [content];
}

class QrCardAdded extends QrEvent {}

class QrCardRemoved extends QrEvent {
  final String cardId;

  const QrCardRemoved(this.cardId);

  @override
  List<Object?> get props => [cardId];
}

class QrImageUploaded extends QrEvent {
  final String imagePath;
  final ImageProvider imageProvider;

  const QrImageUploaded(this.imagePath, this.imageProvider);
  @override
  List<Object?> get props => [imagePath, imageProvider];
}
