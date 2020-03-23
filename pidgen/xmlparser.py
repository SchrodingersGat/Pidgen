# -*- coding: utf-8 -*-

"""
Special implementation of the ElementTree parser,
which provides line-number information for the decoded xml structure(s).

TODO - Implement the line-number information?

Ref: https://stackoverflow.com/questions/6949395/is-there-a-way-to-get-a-line-number-from-an-elementtree-element
"""

import xml.etree.ElementTree as ElementTree


def parseXML(filename):
    return ElementTree.parse(filename)
