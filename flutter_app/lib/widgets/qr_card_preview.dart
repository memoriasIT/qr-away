import 'package:flutter/material.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_app/models/qr_data.dart';

class QrCardPreview extends StatelessWidget {
  final QrStyle style;
  final QrContent content;

  const QrCardPreview({super.key, required this.style, required this.content});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 350,
      height: 550,
      clipBehavior: Clip.antiAlias,
      decoration: BoxDecoration(
        color: style.backgroundColor, // Card background color
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.black.withAlpha(51), blurRadius: 10, offset: const Offset(0, 5))],
      ),
      child: Column(
        children: [
          // QR Code Section
          Expanded(
            flex: 3,
            child: Container(
              color: style.qrSectionColor, // QR Section Background
              child: Center(
                child: QrImageView(
                  data: content.url,
                  version: QrVersions.auto,
                  size: 280.0,
                  backgroundColor: style.qrSectionColor, // Match background
                  errorCorrectionLevel: style.errorCorrectionLevel,
                  embeddedImage: style.embeddedImage,
                  embeddedImageStyle: const QrEmbeddedImageStyle(size: Size(50, 50)),
                  dataModuleStyle: QrDataModuleStyle(dataModuleShape: style.dataModuleShape, color: style.qrColor),
                  eyeStyle: QrEyeStyle(eyeShape: style.eyeShape, color: style.qrColor),
                ),
              ),
            ),
          ),

          // Details Section
          Expanded(
            flex: 2,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  content.appName,
                  style: GoogleFonts.roboto(
                    textStyle: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.black),
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  content.appVersion,
                  style: GoogleFonts.roboto(
                    textStyle: const TextStyle(fontSize: 20, fontWeight: FontWeight.w300, color: Colors.black),
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                if (content.platform != AppPlatform.none)
                  Image.asset(
                    content.platform == AppPlatform.android ? 'assets/android-icon.png' : 'assets/ios-icon.png',
                    width: 40,
                    height: 40,
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
