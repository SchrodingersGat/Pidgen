# -*- coding: utf-8 -*-

"""
File parsing
"""

from .element import PidgenElement
from .struct import PidgenStruct
from .packet import PidgenPacket
from .enumeration import PidgenEnumeration

from . import debug


class PidgenFileParser(PidgenElement):

    KEY_STRUCTS = "structs"
    KEY_PACKETS = "packets"
    KEY_ENUMS = "enumerations"

    _VALID_KEYS = [
        KEY_STRUCTS,
        KEY_PACKETS,
        KEY_ENUMS
    ]

    def __init__(self, parent, filepath, **kwargs):

        # Override the path argument
        kwargs["path"] = filepath

        PidgenElement.__init__(self, parent, **kwargs)

        self.enums = []
        self.packets = []
        self.structs = []

        self.parse()

    def parse(self):
        """
        Parse an individual protocol file.
        """

        self.parseYaml(self.path)

        self.parseStructs()
        self.parsePackets()
        self.parseEnums()

    def parseStructs(self):

        structs = self.data.get(self.KEY_STRUCTS, {})

        for struct in structs:
            
            self.structs.append(PidgenStruct(
                name=struct,
                data=structs[struct],
                path=self.path
            ))

    def parsePackets(self):
        
        packets = self.data.get(self.KEY_PACKETS, {})

        for packet in packets:

            self.packets.append(PidgenPacket(
                self,
                name=packet,
                data=packets[packet],
                path=self.path
            ))

    def parseEnums(self):

        enums = self.data.get(self.KEY_ENUMS, {})

        for enum in enums:

            self.enums.append(PidgenEnumeration(
                self,
                name=enum,
                data=enums[enum],
                path=self.path
            ))
