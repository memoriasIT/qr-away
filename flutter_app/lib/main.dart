import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_app/bloc/qr_bloc.dart';
import 'package:flutter_app/screens/home_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [BlocProvider<QrBloc>(create: (context) => QrBloc())],
      child: MaterialApp(
        title: 'QR Away',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Color(0xFF049cef)),
          useMaterial3: true,
          textTheme: GoogleFonts.outfitTextTheme(),
        ),
        home: const HomeScreen(),
      ),
    );
  }
}
