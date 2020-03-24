# -*- coding: utf-8 -*-

"""
Run this script to parse a set of protocol files using Pidgen.

python -m Pidgen <path/to/protocol>

For help, run:

python -m Pidgen -h
"""

from __future__ import print_function

import argparse
import os
import sys

from .version import PIDGEN_VERSION
from .directoryparser import PidgenDirectoryParser
from . import debug

__version__ = PIDGEN_VERSION


def main():

    parser = argparse.ArgumentParser(description="Pidgen - Protocol Generation Tool - v{version}".format(version=PIDGEN_VERSION))

    # Position arguments
    parser.add_argument("protocol", help="Path to top-level protocol directory")

    # Optional arguments
    parser.add_argument("--no-color", help="Disable colorized debug output", action="store_true")
    parser.add_argument("-v", "--verbose", help="Print verbose output", action="count")

    parser.add_argument("--version", action="version", version="Pidgen version: {v}".format(v=PIDGEN_VERSION))

    args = parser.parse_args()

    # Prevent color output if specified
    if args.no_color:
        debug.setDebugColorOn(False)

    # Set the global debugging level
    debug.setDebugLevel(int(args.verbose) if args.verbose is not None else debug.MSG_ERROR)

    # Extract the protocol directory, and ensure that it is a valid directory
    protocol_dir = args.protocol

    if not os.path.exists(protocol_dir) or not os.path.isdir(protocol_dir):
        debug.error("Directory '{d}' is not a valid directory".format(d=protocol_dir), fail=True)

    debug.message("Loading protocol from '{d}'".format(d=protocol_dir))

    # Parse the protocol
    PidgenDirectoryParser(None, protocol_dir, settings={})

    errors = debug.getErrorCount()

    if errors > 0:
        debug.error("Exiting with {n} errors".format(n=errors))

    sys.exit(errors)


if __name__ == '__main__':
    main()
