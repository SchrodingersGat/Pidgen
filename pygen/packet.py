# -*- coding: utf-8 -*-

from .element import PyGenElement


class PyGenPacket(PyGenElement):

    def __init__(self, **kwargs):

        PyGenElement.__init__(self, **kwargs)

        print("Parsing packet:", self.name)

        self.elements = []

        self.parse()

    def parse(self):
        
        for element in self.data:
            print(" - ", element)
