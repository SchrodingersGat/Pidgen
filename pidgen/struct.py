# -*- coding: utf-8 -*-

from .element import PidgenElement
from .data import PidgenDataElement


class PidgenStruct(PidgenElement):
    """
    A PidgenStruct object is equivalent to a 'struct' in C-like languages.
    It contains sequential data elements (which can be other structs).
    Structs can be arbitrarily nested

    Attributes:
        data - Array of data contained within this struct
    """

    _REQUIRED_KEYS = [
        "name"
    ]

    def __init__(self, parent, **kwargs):

        PidgenElement.__init__(self, parent, **kwargs)

    def parse(self):

        for child in self.xml.getchildren():

            tag = child.tag.lower()

            if tag == "data":

                # Create a new data value
                PidgenDataElement(self, xml=child)
            
            elif tag in ["struct", "structure"]:

                # Create a new sub-struct
                # TODO - What does it mean to have a struct inside a struct?
                PidgenStruct(self, xml=child)

            else:
                # Unknown tag
                self.unknownElement(child.tag())
