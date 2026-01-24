# QR Away 🚀

<div align="center">
  <img src="flutter_app/assets/qraway.svg" alt="QR Away Logo" width="200"/>
  <p align="center">
    <strong>Create beautiful, branded QR codes for your applications with ease.</strong>
  </p>
</div>

---

**QR Away** is a modern and intuitive Flutter application designed to help developers and creators generate stylized QR codes. Whether you need to share a URL, an app download link, or any data, QR Away allows you to customize every aspect of the QR code to match your brand's identity.

## ✨ Features

- 🎨 **Dynamic Styling**: Customize QR code colors, background colors, and card styles.
- 🖼️ **Color Extraction**: Upload an image (like your brand logo) to automatically extract a matching color palette.
- 🛠️ **Deep Customization**: 
  - Change data module shapes (Square, Circle).
  - Adjust eye shapes (Square, Circle).
  - Select Error Correction Levels (Low, Medium, Quartile, High).
- 📱 **Platform Context**: Add app names, versions, and platform icons (Android/iOS) to your QR cards.
- 🗂️ **Batch Generation**: Create and manage multiple QR cards simultaneously.
- 💾 **High-Quality Export**: Capture your stylized cards and download them as high-resolution PNG images.

## 🚀 Getting Started

### Prerequisites

- [Flutter SDK](https://docs.flutter.dev/get-started/install) (v3.10.4 or higher)
- [Dart SDK](https://dart.dev/get-started/sdk)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/memoriasIT/qr-away.git
   cd qr-away/flutter_app
   ```

2. **Install dependencies:**
   ```bash
   flutter pub get
   ```

3. **Run the application:**
   ```bash
   flutter run
   ```

## 📁 Project Structure

The repository is organized as follows:

- **`flutter_app/`**: The main Flutter application (Current Version).
- **`old-python-impl/`**: Legacy Python implementation (Deprecated).


## 🛠️ Tech Stack

- **Framework**: [Flutter](https://flutter.dev/)
- **State Management**: [Flutter BLoC](https://pub.dev/packages/flutter_bloc)
- **Design System**: Material 3 with [Google Fonts (Outfit)](https://fonts.google.com/specimen/Outfit)
- **QR Generation**: [qr_flutter](https://pub.dev/packages/qr_flutter)
- **Palette Generation**: [palette_generator](https://pub.dev/packages/palette_generator)

## 🤝 Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, feel free to open an issue or submit a pull request.

---

<p align="center">
  Made with ❤️ by <strong>MemoriasIT</strong>
</p>
