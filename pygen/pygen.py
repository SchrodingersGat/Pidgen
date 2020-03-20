# -*- coding: utf-8 -*-

"""
    @package

    pygen - Low level protocol generation tool.

"""

import argparse

from version import PYGEN_VERSION


parser = argparse.ArgumentParser(description="PyGen - Protocol Generation Tool")

parser.add_argument("protocol", help="Path to top-level protocol directory")

parser.add_argument("--version", action="version", version="PyGen version: {v}".format(v=PYGEN_VERSION))

args = parser.parse_args()

