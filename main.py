#!/usr/bin/env python3
import argparse
import logging
import sys

import extract_colors
import fix_image
import parse_scoop
from parse_scoop import AppPlatform
import generate_qr

def parseArgs():
    # Make parser object
    argParser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    argParser.add_argument(
        "required_positional_arg",
        help="desc",
    )
    argParser.add_argument(
        "required_int",
        type=int,
        help="req number",
    )
    argParser.add_argument(
        "--on",
        action="store_true",
        help="include to enable",
    )
    argParser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        choices=[0, 1, 2],
        default=1,
        help="increase or decrease output verbosity (default: %(default)s)",
    )

    group1 = argParser.add_mutually_exclusive_group(required=True)
    group1.add_argument(
        '--enable',
        action="store_true",
    )
    group1.add_argument(
        '--disable',
        action="store_false",
    )

    return (argParser.parse_args())


if __name__ == '__main__':
    # TODO: Investigate what's the minimal version
    # if sys.version_info<(3,0,0):
    #     sys.stderr.write("You need python 3.0 or later to run this script\n")
    #     sys.exit(1)

    verbosity_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    try:
        args = parseArgs()
        print(args)
        level = verbosity_levels[min(args.verbosity, len(verbosity_levels) - 1)]  # cap to last level index
        logging.basicConfig(stream=sys.stderr, level=level)
    except:
        print('Try $python <script_name> "Hello" 123 --enable [-v {0,1,2}]')

    scoop_data = parse_scoop.parseHtml(url="https://scoop.pinch.nl/?page=app-detail&hash=5f9a67584b46133bfddc87043cf8cc23&version=103")
    scoop_data = parse_scoop.parseHtml(url="https://scoop.pinch.nl/?page=app-detail&hash=37072dacec36a10cd1ae04905a7c0224&version=9")
    logging.info(f"Parsed info correctly: {scoop_data}")

    # iOS icon data uses some propietary bytes from apple that make it corrupt to other viewers
    # Images must be then normalized. See more info in fix_image.py
    if (scoop_data.app_platform is AppPlatform.IOS):
        fix_image.defryImage(scoop_data.app_logo_path)
        # Update path to normalized image
        scoop_data.app_logo_path = scoop_data.app_logo_path[:-4]+"_out.png"
        logging.info("iOS image was normalized")
    
    color_palette = extract_colors.extractColors(scoop_data.app_logo_path)
    logging.info(f"Color Scheme obtained: {color_palette}")
    
    qr_output_path = f"out/{scoop_data.app_title}/{scoop_data.app_platform.name}/"
    generate_qr.generateQrImage(data=scoop_data.download_url, colors=color_palette, output_path=qr_output_path)
    logging.info(f"QR image generated at: {qr_output_path}/qr.png")


    
