# -*- coding: utf-8 -*-

from .struct import PyGenStruct
from . import debug


class PyGenPacket(PyGenStruct):
    """
    A Packet is a sub-set of a struct.
    """

    def __init__(self, **kwargs):

        PyGenStruct.__init__(self, **kwargs)

        self.parse_packet()

    def parse_packet(self):
        """
        Parse a packet object
        """

        debug.debug("Parsing packet:", self.name)

        # Note - the underlying struct data has already been parsed here
