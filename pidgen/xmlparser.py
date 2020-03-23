# -*- coding: utf-8 -*-

"""
Special implementation of the ElementTree parser,
which provides line-number information for the decoded xml structure(s).

TODO - Implement the line-number information?

Ref: https://stackoverflow.com/questions/6949395/is-there-a-way-to-get-a-line-number-from-an-elementtree-element
"""

import xml.etree.ElementTree as ElementTree
from . import debug

def parseXML(filename):
    try:
        return ElementTree.parse(filename)
    except ElementTree.ParseError as e:
        debug.error("Error parsing XML file - '{f}' : {e}".format(f=filename, e=e), fail=True)
