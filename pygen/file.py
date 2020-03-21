# -*- coding: utf-8 -*-

"""
File parsing
"""

import yaml

from .element import PyGenElement
from .struct import PyGenStruct
from .packet import PyGenPacket
from .enumeration import PyGenEnumeration

from . import debug


class PyGenFileParser(PyGenElement):

    KEY_STRUCTS = "structs"
    KEY_PACKETS = "packets"
    KEY_ENUMS = "enumerations"

    _VALID_KEYS = [
        KEY_STRUCTS,
        KEY_PACKETS,
        KEY_ENUMS
    ]

    def __init__(self, filepath, **kwargs):

        if "path" not in kwargs:
            kwargs["path"] = filepath

        PyGenElement.__init__(self, **kwargs)

        self.enums = []
        self.packets = []
        self.structs = []

        self.parse()

    def parse(self):
        """
        Parse an individual protocol file.
        """

        debug.debug("Parsing file:", self.path)

        with open(self.path, 'r') as yaml_file:
            try:
                self.data = yaml.safe_load(yaml_file)
            except yaml.parser.ParserError as e:
                debug.error("Error parsing file -", self.path)
                debug.error(e, fail=True)

        self.parseStructs()
        self.parsePackets()
        self.parseEnums()

    def parseStructs(self):

        structs = self.data.get(self.KEY_STRUCTS, {})

        for struct in structs:
            
            self.structs.append(PyGenStruct(
                name=struct,
                data=structs[struct],
                path=self.path,
                settings=self.settings
            ))

    def parsePackets(self):
        
        packets = self.data.get(self.KEY_PACKETS, {})

        for packet in packets:

            self.packets.append(PyGenPacket(
                name=packet,
                data=packets[packet],
                path=self.path,
                settings=self.settings
            ))

    def parseEnums(self):

        enums = self.data.get(self.KEY_ENUMS, {})

        for enum in enums:

            self.enums.append(PyGenEnumeration(
                name=enum,
                data=enums[enum],
                path=self.path,
                settings=self.settings
            ))
