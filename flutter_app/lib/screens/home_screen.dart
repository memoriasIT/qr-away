import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:image_picker/image_picker.dart';
import 'package:flutter_app/bloc/qr_bloc.dart';
import 'package:flutter_app/bloc/qr_event.dart';
import 'package:flutter_app/bloc/qr_state.dart';
import 'package:flutter_app/models/qr_data.dart';
import 'package:flutter_app/widgets/qr_card_preview.dart';
import 'package:flutter_app/widgets/color_picker_tile.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import 'dart:typed_data';
import 'dart:ui' as ui;
import 'package:flutter/rendering.dart';
import 'package:universal_html/html.dart' as html;
import 'package:flutter_svg/flutter_svg.dart';
import 'package:qr_flutter/qr_flutter.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final GlobalKey _globalKey = GlobalKey();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            SvgPicture.asset('assets/qraway.svg', height: 50),
            Padding(
              padding: const EdgeInsets.only(bottom: 8.0, left: 8),
              child: const Text('by MemoriasIT', style: TextStyle(fontSize: 10, color: Colors.black54)),
            ),
          ],
        ),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [IconButton(icon: const Icon(Icons.download), onPressed: _captureAndSavePng, tooltip: 'Download Png')],
      ),
      body: BlocBuilder<QrBloc, QrState>(
        builder: (context, state) {
          final isWideScreen = MediaQuery.of(context).size.width > 900;

          final preview = Center(
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: RepaintBoundary(
                key: _globalKey,
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: state.cards.map((card) {
                    return Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16.0),
                      child: QrCardPreview(style: state.style, content: card),
                    );
                  }).toList(),
                ),
              ),
            ),
          );

          if (isWideScreen) {
            return Row(
              children: [
                Expanded(
                  flex: 1,
                  child: SingleChildScrollView(
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: _QrForm(
                        state: state,
                        onPickImage: () => _pickImage(context),
                        onPickEmbeddedImage: () => _pickEmbeddedImage(context),
                        onShowColorPicker: (color, onChanged) => _showColorPicker(context, color, onChanged),
                      ),
                    ),
                  ),
                ),
                VerticalDivider(width: 1, color: Colors.grey[300]),
                Expanded(flex: 1, child: preview),
              ],
            );
          } else {
            return SingleChildScrollView(
              child: Column(
                children: [
                  Padding(padding: const EdgeInsets.all(24.0), child: preview),
                  Divider(height: 1, color: Colors.grey[300]),
                  Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: _QrForm(
                      state: state,
                      onPickImage: () => _pickImage(context),
                      onPickEmbeddedImage: () => _pickEmbeddedImage(context),
                      onShowColorPicker: (color, onChanged) => _showColorPicker(context, color, onChanged),
                    ),
                  ),
                ],
              ),
            );
          }
        },
      ),
    );
  }

  Future<void> _pickImage(BuildContext context) async {
    final picker = ImagePicker();
    final XFile? image = await picker.pickImage(source: ImageSource.gallery);

    if (image != null) {
      final Uint8List bytes = await image.readAsBytes();
      final imageProvider = MemoryImage(bytes);

      if (context.mounted) {
        context.read<QrBloc>().add(QrImageUploaded(image.path, imageProvider));
      }
    }
  }

  Future<void> _pickEmbeddedImage(BuildContext context) async {
    final picker = ImagePicker();
    final XFile? image = await picker.pickImage(source: ImageSource.gallery);

    if (image != null) {
      final Uint8List bytes = await image.readAsBytes();
      final imageProvider = MemoryImage(bytes);

      if (context.mounted) {
        context.read<QrBloc>().add(
          QrStyleChanged(context.read<QrBloc>().state.style.copyWith(embeddedImage: imageProvider)),
        );
      }
    }
  }

  void _showColorPicker(BuildContext context, Color currentColor, ValueChanged<Color> onColorChanged) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Pick a color'),
          content: SingleChildScrollView(
            child: ColorPicker(pickerColor: currentColor, onColorChanged: onColorChanged, pickerAreaHeightPercent: 0.8),
          ),
          actions: <Widget>[
            TextButton(
              child: const Text('Got it'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  Future<void> _captureAndSavePng() async {
    try {
      RenderRepaintBoundary boundary = _globalKey.currentContext!.findRenderObject() as RenderRepaintBoundary;
      // Increase pixel ratio for higher quality
      ui.Image image = await boundary.toImage(pixelRatio: 3.0);
      ByteData? byteData = await image.toByteData(format: ui.ImageByteFormat.png);
      Uint8List pngBytes = byteData!.buffer.asUint8List();

      // Create a blob and download it
      final blob = html.Blob([pngBytes]);
      final url = html.Url.createObjectUrlFromBlob(blob);
      html.AnchorElement(href: url)
        ..setAttribute("download", "qr_cards.png")
        ..click();
      html.Url.revokeObjectUrl(url);
    } catch (e) {
      debugPrint(e.toString());
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Failed to download image')));
      }
    }
  }
}

class _QrForm extends StatelessWidget {
  final QrState state;
  final VoidCallback onPickImage;
  final VoidCallback onPickEmbeddedImage;
  final Function(Color, ValueChanged<Color>) onShowColorPicker;

  const _QrForm({
    required this.state,
    required this.onPickImage,
    required this.onPickEmbeddedImage,
    required this.onShowColorPicker,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _StyleSection(
          state: state,
          onPickImage: onPickImage,
          onPickEmbeddedImage: onPickEmbeddedImage,
          onShowColorPicker: onShowColorPicker,
        ),
        const SizedBox(height: 32),
        _ContentSection(state: state),
      ],
    );
  }
}

class _StyleSection extends StatelessWidget {
  final QrState state;
  final VoidCallback onPickImage;
  final VoidCallback onPickEmbeddedImage;
  final Function(Color, ValueChanged<Color>) onShowColorPicker;

  const _StyleSection({
    required this.state,
    required this.onPickImage,
    required this.onPickEmbeddedImage,
    required this.onShowColorPicker,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const _SectionTitle(title: 'Global Styles'),
        const SizedBox(height: 16),
        Center(
          child: ElevatedButton.icon(
            onPressed: onPickImage,
            icon: const Icon(Icons.image),
            label: const Text('Pick Image for Colors'),
          ),
        ),
        if (state.isLoading) const LinearProgressIndicator(),
        const SizedBox(height: 16),
        if (state.extractedColors.isNotEmpty) ...[
          const Text('Extracted Colors:'),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: state.extractedColors.map((color) {
              return ColorPickerTile(
                color: color,
                isSelected: state.style.qrColor == color,
                onTap: () {
                  context.read<QrBloc>().add(QrStyleChanged(state.style.copyWith(qrColor: color)));
                },
              );
            }).toList(),
          ),
          const SizedBox(height: 16),
        ],
        const Text('QR Code Color:'),
        const SizedBox(height: 8),
        ColorPickerTile(
          color: state.style.qrColor,
          isSelected: true,
          onTap: () {
            onShowColorPicker(state.style.qrColor, (color) {
              context.read<QrBloc>().add(QrStyleChanged(state.style.copyWith(qrColor: color)));
            });
          },
        ),
        const SizedBox(height: 16),
        const Text('QR Background Color:'),
        const SizedBox(height: 8),
        ColorPickerTile(
          color: state.style.qrSectionColor,
          isSelected: true,
          onTap: () {
            onShowColorPicker(state.style.qrSectionColor, (color) {
              context.read<QrBloc>().add(QrStyleChanged(state.style.copyWith(qrSectionColor: color)));
            });
          },
        ),
        const SizedBox(height: 16),
        const Text('Card Background Color:'),
        const SizedBox(height: 8),
        ColorPickerTile(
          color: state.style.backgroundColor,
          isSelected: true,
          onTap: () {
            onShowColorPicker(state.style.backgroundColor, (color) {
              context.read<QrBloc>().add(QrStyleChanged(state.style.copyWith(backgroundColor: color)));
            });
          },
        ),
        const SizedBox(height: 16),
        DropdownButtonFormField<int>(
          decoration: const InputDecoration(labelText: 'Error Correction Level', border: OutlineInputBorder()),
          initialValue: state.style.errorCorrectionLevel,
          items: const [
            DropdownMenuItem(value: QrErrorCorrectLevel.L, child: Text('Low')),
            DropdownMenuItem(value: QrErrorCorrectLevel.M, child: Text('Medium')),
            DropdownMenuItem(value: QrErrorCorrectLevel.Q, child: Text('Quartile')),
            DropdownMenuItem(value: QrErrorCorrectLevel.H, child: Text('High')),
          ],
          onChanged: (value) {
            if (value != null) {
              context.read<QrBloc>().add(QrStyleChanged(state.style.copyWith(errorCorrectionLevel: value)));
            }
          },
        ),
        const SizedBox(height: 16),
        DropdownButtonFormField<QrDataModuleShape>(
          decoration: const InputDecoration(labelText: 'Data Module Shape', border: OutlineInputBorder()),
          initialValue: state.style.dataModuleShape,
          items: const [
            DropdownMenuItem(value: QrDataModuleShape.square, child: Text('Square')),
            DropdownMenuItem(value: QrDataModuleShape.circle, child: Text('Circle')),
          ],
          onChanged: (value) {
            if (value != null) {
              context.read<QrBloc>().add(QrStyleChanged(state.style.copyWith(dataModuleShape: value)));
            }
          },
        ),
        const SizedBox(height: 16),
        DropdownButtonFormField<QrEyeShape>(
          decoration: const InputDecoration(labelText: 'Eye Shape', border: OutlineInputBorder()),
          initialValue: state.style.eyeShape,
          items: const [
            DropdownMenuItem(value: QrEyeShape.square, child: Text('Square')),
            DropdownMenuItem(value: QrEyeShape.circle, child: Text('Circle')),
          ],
          onChanged: (value) {
            if (value != null) {
              context.read<QrBloc>().add(QrStyleChanged(state.style.copyWith(eyeShape: value)));
            }
          },
        ),
        const SizedBox(height: 16),
        Center(
          child: ElevatedButton.icon(
            onPressed: onPickEmbeddedImage,
            icon: const Icon(Icons.add_photo_alternate),
            label: const Text('Pick Embedded Image'),
          ),
        ),
      ],
    );
  }
}

class _ContentSection extends StatelessWidget {
  final QrState state;

  const _ContentSection({required this.state});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const _SectionTitle(title: 'Cards Content'),
            ElevatedButton.icon(
              onPressed: () {
                context.read<QrBloc>().add(QrCardAdded());
              },
              icon: const Icon(Icons.add),
              label: const Text('Add Card'),
            ),
          ],
        ),
        const SizedBox(height: 16),
        ...state.cards.asMap().entries.map((entry) {
          final index = entry.key;
          final card = entry.value;
          return _CardContentItem(key: ValueKey(card.id), index: index, card: card, showDelete: state.cards.length > 1);
        }),
      ],
    );
  }
}

class _CardContentItem extends StatefulWidget {
  final int index;
  final QrContent card;
  final bool showDelete;

  const _CardContentItem({super.key, required this.index, required this.card, required this.showDelete});

  @override
  State<_CardContentItem> createState() => _CardContentItemState();
}

class _CardContentItemState extends State<_CardContentItem> {
  late TextEditingController _urlController;
  late TextEditingController _appNameController;
  late TextEditingController _appVersionController;

  @override
  void initState() {
    super.initState();
    _urlController = TextEditingController(text: widget.card.url);
    _appNameController = TextEditingController(text: widget.card.appName);
    _appVersionController = TextEditingController(text: widget.card.appVersion);
  }

  @override
  void didUpdateWidget(_CardContentItem oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.card.url != _urlController.text) {
      _urlController.text = widget.card.url;
    }
    if (widget.card.appName != _appNameController.text) {
      _appNameController.text = widget.card.appName;
    }
    if (widget.card.appVersion != _appVersionController.text) {
      _appVersionController.text = widget.card.appVersion;
    }
  }

  @override
  void dispose() {
    _urlController.dispose();
    _appNameController.dispose();
    _appVersionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Card ${widget.index + 1}', style: const TextStyle(fontWeight: FontWeight.bold)),
                if (widget.showDelete)
                  IconButton(
                    icon: const Icon(Icons.delete, color: Colors.red),
                    onPressed: () {
                      context.read<QrBloc>().add(QrCardRemoved(widget.card.id));
                    },
                  ),
              ],
            ),
            const SizedBox(height: 16),
            TextField(
              decoration: const InputDecoration(labelText: 'URL / Data', border: OutlineInputBorder()),
              controller: _urlController,
              onChanged: (value) {
                context.read<QrBloc>().add(QrContentChanged(widget.card.copyWith(url: value)));
              },
            ),
            const SizedBox(height: 16),
            TextField(
              decoration: const InputDecoration(labelText: 'App Name', border: OutlineInputBorder()),
              controller: _appNameController,
              onChanged: (value) {
                context.read<QrBloc>().add(QrContentChanged(widget.card.copyWith(appName: value)));
              },
            ),
            const SizedBox(height: 16),
            TextField(
              decoration: const InputDecoration(labelText: 'App Version', border: OutlineInputBorder()),
              controller: _appVersionController,
              onChanged: (value) {
                context.read<QrBloc>().add(QrContentChanged(widget.card.copyWith(appVersion: value)));
              },
            ),
            const SizedBox(height: 16),
            const Text('Platform Icon'),
            Row(
              children: [
                _PlatformChoice(
                  card: widget.card,
                  platform: AppPlatform.android,
                  label: 'Android',
                  icon: Icons.android,
                ),
                const SizedBox(width: 8),
                _PlatformChoice(card: widget.card, platform: AppPlatform.ios, label: 'iOS', icon: Icons.apple),
                const SizedBox(width: 8),
                _PlatformChoice(card: widget.card, platform: AppPlatform.none, label: 'None', icon: Icons.block),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _PlatformChoice extends StatelessWidget {
  final QrContent card;
  final AppPlatform platform;
  final String label;
  final IconData icon;

  const _PlatformChoice({required this.card, required this.platform, required this.label, required this.icon});

  @override
  Widget build(BuildContext context) {
    final isSelected = card.platform == platform;
    return ChoiceChip(
      showCheckmark: false,
      avatar: Icon(icon, size: 16),
      label: Text(label),
      selected: isSelected,
      onSelected: (selected) {
        if (selected) {
          context.read<QrBloc>().add(QrContentChanged(card.copyWith(platform: platform)));
        }
      },
    );
  }
}

class _SectionTitle extends StatelessWidget {
  final String title;

  const _SectionTitle({required this.title});

  @override
  Widget build(BuildContext context) {
    return Text(
      title,
      style: Theme.of(
        context,
      ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold, color: Theme.of(context).colorScheme.primary),
    );
  }
}
