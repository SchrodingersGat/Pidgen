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

    KEY_PROTOCOL = 'protocol'
    KEY_STRUCT = "struct"
    
    KEYS_PACKET = ["packet", "pkt"]
    
    KEYS_ENUM = ["enumeration", "enum"]

    _VALID_KEYS = [
        KEY_STRUCT
    ] + KEYS_ENUM + KEYS_PACKET

    def __init__(self, parent, **kwargs):

        self.enums = []
        self.packets = []
        self.structs = []
        
        PidgenElement.__init__(self, parent, **kwargs)

    def parse(self):
        """
        Parse an individual protocol file.
        The root-node has been checked by the directory parser, so we know this file is valid.
        """

        children = self.xml.getchildren()

        for child in children:
            # Iterate through each top-level structure in the XML file
            tag = child.tag.lower()

            if tag in self.KEYS_ENUM:
                print("Enum:", child)

            elif tag in self.KEYS_PACKET:
                print("Packet:", child)

            elif tag == self.KEY_STRUCT:
                print("Struct:", child)

            else:
                # TODO - Make <line> number available here somehow...
                debug.warning("{f} - Unknown element '{e}' at <line>".format(
                    f=self.path,
                    e=tag
                ))
