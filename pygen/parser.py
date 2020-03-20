# -*- coding: utf-8 -*-

"""
Directory and file parser code
"""

import os
import yaml

from .element import PyGenElement
from .packet import PyGenPacket
from .enumeration import PyGenEnumeration


class PyGenParser(PyGenElement):
    """
    Class for parsing a directory of protocol definition files.
    """

    def __init__(self, path, **kwargs):

        kwargs["path"] = path

        PyGenElement.__init__(self, **kwargs)

        self.yaml_files = []
        self.sub_dirs = []

        self.parse()

    def parse(self):
        """ Parse the current directory.
        - Look for any subdirectories
        - Look for any protocol files (.yaml)
        - Note: .yaml files prefixed with _ character are treated differently.
        """

        listing = os.listdir(self.path)

        for item in listing:
            path = os.path.join(self.path, item)

            if os.path.isdir(path):
                self.sub_dirs.append(item)

            if os.path.isfile(path) and item.endswith(".yaml"):
                self.yaml_files.append(item)

        print("Directory:", self.path)

        # Parse all files
        for f in self.yaml_files:

            if f.startswith("_"):
                # TODO
                continue

            p = PyGenFile(os.path.join(self.path, f))
            p.parse()

        # Parse all subdirectories
        for d in self.sub_dirs:

            p = PyGenParser(os.path.join(self.path, d))
            p.parse()


class PyGenFile(PyGenElement):

    def __init__(self, path, **kwargs):

        kwargs["path"] = path

        PyGenElement.__init__(self, **kwargs)

        self.enums = []
        self.packets = []

    def parse(self):
        print("Parsing file: ", self.path, self.namespace)

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
                path=self.path
            ))

    def parseEnums(self):

        enums = self.data.get("enumerations", {})

        for enum in enums:

            self.enums.append(PyGenEnumeration(enum))
