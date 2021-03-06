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

    ALLOWED_KEYS = [
    ]

    REQUIRED_KEYS = [
        "name"
    ]

    ALLOWED_CHILDREN = [
        "data"
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

    @property
    def data(self):
        """ Return all data elements in this struct """

        return self.getChildren(PidgenDataElement)

    @property
    def structs(self):
        """ Return all structs which exist under this one """

        return self.getChildren(PidgenStruct)

    def hasValidators(self):
        """
        Return True if this struct (or any sub-structs) contain any data validators.
        """

        for struct in self.structs:
            if struct.hasValidators():
                return True

        for data in self.data:
            if data.hasValidators():
                return True

        return False

    def hasInitializers(self):
        """
        Return True if this struct (or any sub-structs) contain any data initializers.
        """

        for struct in self.structs:
            if struct.hasInitializers():
                return True

        for data in self.data:
            if data.hasInitializers():
                return True

        return False
