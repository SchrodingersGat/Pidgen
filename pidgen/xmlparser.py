# -*- coding: utf-8 -*-

"""
Special implementation of the ElementTree parser,
which provides line-number information for the decoded xml structure(s).
"""

from . import debug

import sys

sys.modules['_elementtree'] = None
import xml.etree.ElementTree as ElementTree

class LineNumberingParser(ElementTree.XMLParser):
    """
    Custom XML parser which scrapes line numbers from elements.

    Ref: https://stackoverflow.com/questions/6949395/is-there-a-way-to-get-a-line-number-from-an-elementtree-element
    """

    def _start(self, *args, **kwargs):
        # Here we assume the default XML parser which is expat
        # and copy its element position attributes into output Elements
        element = super(self.__class__, self)._start(*args, **kwargs)
        element._start_line_number = self.parser.CurrentLineNumber
        element._start_column_number = self.parser.CurrentColumnNumber
        element._start_byte_index = self.parser.CurrentByteIndex

        return element

    def _end(self, *args, **kwargs):
        element = super(self.__class__, self)._end(*args, **kwargs)
        element._end_line_number = self.parser.CurrentLineNumber
        element._end_column_number = self.parser.CurrentColumnNumber
        element._end_byte_index = self.parser.CurrentByteIndex
        return element


def parseXML(filename):
    try:
        return ElementTree.parse(filename, parser=LineNumberingParser())
        #return ElementTree.parse(filename)
    except ElementTree.ParseError as e:
        debug.error("Error parsing XML file - '{f}' : {e}".format(f=filename, e=e), fail=True)
