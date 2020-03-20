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

        PyGenElement.__init__(self, **kwargs)

        self._files = []
        self._dirs = []

        self.parse()

    def parse(self):
        """ Parse the current directory.
        - Look for any subdirectories
        - Look for any protocol files (.yaml)
        - Note: .yaml files prefixed with _ character are treated differently.
        """

        debug.debug("Parsing directory:", self.path)

        listing = os.listdir(self.path)

        files = []
        dirs = []

        for item in listing:
            path = os.path.join(self.path, item)

            if os.path.isdir(path):
                dirs.append(item)

            if os.path.isfile(path) and item.endswith(".yaml"):
                files.append(item)

        if len(files) == 0:
            debug.info("No protocol files found in directory '{d}'".format(d=self.path))

        # Parse all protocol files
        for f in files:

            if f.startswith("_"):
                # TODO - Special files which augment the protocol generation
                continue

            self._files.append(PyGenFile(os.path.join(self.path, f), settings=self.settings))

        # Parse all subdirectories
        for d in dirs:

            self._dirs.append(PyGenParser(os.path.join(self.path, d), settings=self.settings))


class PyGenFile(PyGenElement):

    def __init__(self, filepath, **kwargs):

        if "path" not in kwargs:
            kwargs["path"] = filepath

        PyGenElement.__init__(self, **kwargs)

        self.enums = []
        self.packets = []

        self.parse()

    def parse(self):
        """
        Parse an individual protocol file.
        """

        debug.debug("Parsing file:", self.path)

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

            self.enums.append(PyGenEnumeration(
                name=enum,
                data=enums[enum],
                path=self.path,
                settings=self.settings
            ))
