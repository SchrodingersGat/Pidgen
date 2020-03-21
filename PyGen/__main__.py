# -*- coding: utf-8 -*-

"""
Run this script to parse a set of protocol files using PyGen.
Assuming the PyGen package is correctly installed:

python -m PyGen <path/to/protocol>

For help, run:

python -m PyGen -h
"""

from __future__ import print_function

import argparse
import os
import sys

from .version import PYGEN_VERSION
from .directoryparser import PyGenDirectoryParser
from . import debug

__version__ = PYGEN_VERSION


def main():

    debug.message("PyGen v{version}".format(version=PYGEN_VERSION))

    parser = argparse.ArgumentParser(description="PyGen - Protocol Generation Tool")

    # Position arguments
    parser.add_argument("protocol", help="Path to top-level protocol directory")

    # Optional arguments
    parser.add_argument("-v", "--verbose", help="Print verbose output", action="count")

    parser.add_argument("--version", action="version", version="PyGen version: {v}".format(v=PYGEN_VERSION))

    args = parser.parse_args()

    debug.setDebugLevel(args.verbose if args.verbose is not None else 0)

    # Extract the protocol directory, and ensure that it is a valid directory
    protocol_dir = args.protocol

    if not os.path.exists(protocol_dir):
        debug.error("Directory '{d}' does not exist".format(d=protocol_dir), fail=True)

    if not os.path.isdir(protocol_dir):
        debug.error("Directory '{d}' is not a valid directory".format(d=protocol_dir), fail=True)

    debug.message("Loading protocol from '{d}'".format(d=protocol_dir))

    # Parse the protocol
    PyGenDirectoryParser(protocol_dir, settings={})

    errors = debug.getErrorCount()

    if errors > 0:
        debug.error("Exiting with {n} errors".format(n=errors))

    sys.exit(errors)


if __name__ == '__main__':
    main()
