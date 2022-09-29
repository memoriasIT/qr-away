#!/usr/bin/env python3

import sys
import argparse


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
        default=0,
        help="increase output verbosity (default: %(default)s)",
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

    try:
        args = parseArgs()
        print(args)
    except:
        print('Try $python <script_name> "Hello" 123 --enable')

    print()
