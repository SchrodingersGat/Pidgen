# -*- coding: utf-8 -*-

from .struct import PidgenStruct


class PidgenPacket(PidgenStruct):
    """
    A Packet is a sub-set of a struct.
    """

    ALLOWED_KEYS = [
    ]

    REQUIRED_KEYS = [
        "name",
        "id"
    ]

    def __init__(self, parent, **kwargs):

        PidgenStruct.__init__(self, parent, **kwargs)

    def parse_packet(self):
        """
        Parse a packet object
        """

        # Note - the underlying struct data has already been parsed here
