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

    ALLOWED_CHILDREN = [
        "pkt", "packet",  # Synonymous
        "struct", "structure",  # Synonymous
        "enum", "enumeration",  # Synonymous
    ]

    def __init__(self, parent, **kwargs):
        
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

        print("File:", self)
        print("Structs:", self.structs)
        print("Packets:", self.packets)
        print("Enums:", self.enumerations)

    @property
    def enumerations(self):
        """
        Return a list of enumerations which exist under this file.
        """

        return self.getChildren(PidgenEnumeration)

    @property
    def packets(self):
        """
        Return a list of packets which exist under this file.
        """

        return self.getChildren(PidgenPacket)
        
    @property
    def structs(self):
        """
        Return a list of structs which exist under this file
        """

        return self.getChildren(PidgenStruct)
