# -*- coding: utf-8 -*-

from .struct import PidgenStruct
from . import debug


class PidgenPacket(PidgenStruct):
    """
    A Packet is a sub-set of a struct.
    """

    _VALID_KEYS = PidgenStruct._VALID_KEYS + [
    ]

    def __init__(self, parent, **kwargs):

        PidgenStruct.__init__(self, parent, **kwargs)

    def parse_packet(self):
        """
        Parse a packet object
        """

        debug.debug("Parsing packet:", self.name)

        # Note - the underlying struct data has already been parsed here
