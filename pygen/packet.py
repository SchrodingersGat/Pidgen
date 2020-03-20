# -*- coding: utf-8 -*-

from .element import PyGenElement
from .struct import PyGenData
from . import debug


class PyGenPacket(PyGenElement):

    def __init__(self, **kwargs):

        PyGenElement.__init__(self, "PACKET", **kwargs)

        self.entries = []

        self.parse()

    def parse(self):
        """
        Parse a packet object
        """

        debug.debug("Parsing packet:", self.path)
        
        for entry in self.data:
            self.entries.append(PyGenData(
                name=entry,
                data=self.data[entry],
                path=self.path
            ))
