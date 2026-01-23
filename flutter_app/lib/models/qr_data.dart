import 'package:flutter/material.dart';
import 'package:equatable/equatable.dart';
import 'package:qr_flutter/qr_flutter.dart';

enum AppPlatform { android, ios, none }

class QrContent extends Equatable {
  final String id;
  final String url;
  final String appName;
  final String appVersion;
  final AppPlatform platform;

  const QrContent({
    required this.id,
    this.url = 'https://example.com',
    this.appName = 'My App',
    this.appVersion = 'v1.0.0',
    this.platform = AppPlatform.android,
  });

  QrContent copyWith({String? url, String? appName, String? appVersion, AppPlatform? platform}) {
    return QrContent(
      id: id,
      url: url ?? this.url,
      appName: appName ?? this.appName,
      appVersion: appVersion ?? this.appVersion,
      platform: platform ?? this.platform,
    );
  }

  @override
  List<Object?> get props => [id, url, appName, appVersion, platform];
}

class QrStyle extends Equatable {
  final Color qrColor;
  final Color backgroundColor;
  final Color qrSectionColor;
  final int errorCorrectionLevel; // QrErrorCorrectLevel
  final QrDataModuleShape dataModuleShape;
  final QrEyeShape eyeShape;
  final ImageProvider? embeddedImage;

  const QrStyle({
    this.qrColor = Colors.black,
    this.backgroundColor = Colors.white,
    this.qrSectionColor = Colors.white,
    this.errorCorrectionLevel = QrErrorCorrectLevel.M,
    this.dataModuleShape = QrDataModuleShape.square,
    this.eyeShape = QrEyeShape.square,
    this.embeddedImage,
  });

  QrStyle copyWith({
    Color? qrColor,
    Color? backgroundColor,
    Color? qrSectionColor,
    int? errorCorrectionLevel,
    QrDataModuleShape? dataModuleShape,
    QrEyeShape? eyeShape,
    ImageProvider? embeddedImage,
  }) {
    return QrStyle(
      qrColor: qrColor ?? this.qrColor,
      backgroundColor: backgroundColor ?? this.backgroundColor,
      qrSectionColor: qrSectionColor ?? this.qrSectionColor,
      errorCorrectionLevel: errorCorrectionLevel ?? this.errorCorrectionLevel,
      dataModuleShape: dataModuleShape ?? this.dataModuleShape,
      eyeShape: eyeShape ?? this.eyeShape,
      embeddedImage: embeddedImage ?? this.embeddedImage,
    );
  }

  @override
  List<Object?> get props => [
    qrColor,
    backgroundColor,
    qrSectionColor,
    errorCorrectionLevel,
    dataModuleShape,
    eyeShape,
    embeddedImage,
  ];
}
