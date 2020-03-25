# -*- coding: utf-8 -*-

import sys
import os

from .element import PidgenElement
from .fileparser import PidgenDirectoryParser, PidgenFileParser
from .xmlparser import parseXML
from . import debug


class PidgenProtocolParser(PidgenFileParser):
    """
    The PidgenProtocolParser represents the top-level protocol object.
    
    A protocol definition starts with a single master .xml file,
    which can then optionally include other .xml files (or entire directories).

    Thus the PidgenProtocolParser is a subclass of the PidgenFileParser class.


    """

    REQUIRED_KEYS = [
        "name",
        "version",
    ]

    ALLOWED_KEYS = [
    ]

    def __init__(self, protocol_file, **kwargs):

        """
        Before initializing any lower-level items,
        first ensure that the protocol_file is valid.
        """

        if not os.path.exists or not os.path.isfile(protocol_file):
            debug.error("Protocol file '{f}' is not valid".format(f=protocol_file), fail=True)

        if not protocol_file.endswith(".xml"):
            debug.error("Protocol file '{f}' is not a .xml file".format(f=protocol_file), fail=True)

        # Read the data
        doc = parseXML(protocol_file)
        root = doc.getroot()

        debug.info("Reading protocol file - {f}".format(f=protocol_file))

        kwargs['path'] = protocol_file
        kwargs['xml'] = root

        # Keep a list of files that have been parsed against this protocol
        # To ensure that files are not parsed multiple times
        self.files = []

        # Add the curent file
        self.checkPath(protocol_file)

        PidgenElement.__init__(self, self, **kwargs)

    @property
    def version(self):
        """
        Return the protocol version
        """

        return self.get('version', None)