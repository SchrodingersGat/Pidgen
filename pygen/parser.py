# -*- coding: utf-8 -*-

"""
Directory and file parser code
"""

import os
import yaml

from .element import PyGenElement
from .packet import PyGenPacket
from .enumeration import PyGenEnumeration
from . import debug


class PyGenParser(PyGenElement):
    """
    Class for parsing a directory of protocol definition files.
    """

    def __init__(self, dirpath, **kwargs):

        if "path" not in kwargs:
            kwargs["path"] = dirpath

        PyGenElement.__init__(self, "DIRECTORY", **kwargs)

        self.yaml_files = []
        self.sub_dirs = []

        self.parse()

    def parse(self):
        """ Parse the current directory.
        - Look for any subdirectories
        - Look for any protocol files (.yaml)
        - Note: .yaml files prefixed with _ character are treated differently.
        """

        debug.info("Parsing directory:", self.path)

        listing = os.listdir(self.path)

        for item in listing:
            path = os.path.join(self.path, item)

            if os.path.isdir(path):
                self.sub_dirs.append(item)

            if os.path.isfile(path) and item.endswith(".yaml"):
                self.yaml_files.append(item)

        # Parse all files
        for f in self.yaml_files:

            if f.startswith("_"):
                # TODO - Special files which augment the protocol generation
                continue

            p = PyGenFile(os.path.join(self.path, f), settings=self.settings)

        # Parse all subdirectories
        for d in self.sub_dirs:

            p = PyGenParser(os.path.join(self.path, d), settings=self.settings)


class PyGenFile(PyGenElement):

    def __init__(self, filepath, **kwargs):

        if "path" not in kwargs:
            kwargs["path"] = filepath

        PyGenElement.__init__(self, "FILE", **kwargs)

        self.enums = []
        self.packets = []

        self.parse()

    def parse(self):
        """
        Parse an individual protocol file.
        """

        debug.info("Parsing file:", self.path)

        with open(self.path, 'r') as yaml_file:
            self.data = yaml.safe_load(yaml_file)

        self.parsePackets()
        self.parseEnums()

    def parsePackets(self):
        
        packets = self.data.get("packets", {})

        for packet in packets:

            self.packets.append(PyGenPacket(
                name=packet,
                data=packets[packet],
                path=self.path,
                settings=self.settings
            ))

    def parseEnums(self):

        enums = self.data.get("enumerations", {})

        for enum in enums:

            # TODO
            pass
