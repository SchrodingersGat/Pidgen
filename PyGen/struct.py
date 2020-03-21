# -*- coding: utf-8 -*-

from .element import PyGenElement
from .data import PyGenData
from . import debug


class PyGenStruct(PyGenElement):
    """
    A PyGenStruct object is equivalent to a 'struct' in C-like languages.
    It contains sequential data elements (which can be other structs).
    Structs can be arbitrarily nested

    Attributes:
        data - Array of data contained within this struct
    """

    KEY_DATA = "data"

    _VALID_KEYS = [
        KEY_DATA,
    ]

    def __init__(self, **kwargs):

        PyGenElement.__init__(self, **kwargs)

        # List of variables which exist in this struct
        self.variables = []
        
        self.parse()

    def parse(self):
        debug.debug("Parsing struct:", self.name)

        self.parse_data()

    def parse_data(self):
        """
        Parse the variables provided under the 'data' tag.
        """

        if self.KEY_DATA not in self.data:
            debug.warning("Empty struct '{s}'".format(s=self.name), self.path)
            return

        variables = self.data[self.KEY_DATA]

        for var in variables:

            var_data = variables[var]

            # Is the variable a 'struct'?
            if PyGenData.KEY_STRUCT in var:
                self.variables.append(PyGenStruct(
                    name=var,
                    data=var_data,
                    path=self.path,
                    settings=self.settings
                ))

            else:
                self.variables.append(PyGenData(
                    name=var,
                    data=var_data,
                    path=self.path,
                    settings=self.settings
                ))
