# -*- coding: utf-8 -*-

"""
File parsing
"""

from .element import PidgenElement
from .struct import PidgenStruct
from .packet import PidgenPacket
from .enumeration import PidgenEnumeration


class PidgenFileParser(PidgenElement):
    """
    Class for representing a single protocol file.
    """

    _VALID_KEYS = [
        "pkt", "packet",  # Synonymous
        "struct", "structure",  # Synonymous
        "enum", "enumeration",  # Synonymous
    ]

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

            if tag in ["enum", "enumeration"]:
                # Construct an Enumeration under this file
                PidgenEnumeration(self, xml=child)

            elif tag in ["pkt", "packet"]:
                # Construct a Packet under this file
                PidgenPacket(self, xml=child)

            elif tag in ["struct", "structure"]:
                # Construct a struct under this file
                PidgenStruct(self, xml=child)

            else:
                self.unknownElement(child.tag)

    @property
    def enumerations(self):
        """
        Return a list of enumerations which exist under this file.
        """

        return [c for c in self.children if isinstance(c, PidgenEnumeration)]

    @property
    def packets(self):
        """
        Return a list of packets which exist under this file.
        """

        return [c for c in self.children if isinstance(c, PidgenPacket)]

    @property
    def structs(self):
        """
        Return a list of structs which exist under this file
        """

        return [c for c in self.children if isinstance(c, PidgenStruct)]
