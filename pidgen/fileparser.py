# -*- coding: utf-8 -*-

"""
File parsing
"""

import os

from .element import PidgenElement
from .struct import PidgenStruct
from .packet import PidgenPacket
from .enumeration import PidgenEnumeration
from .xmlparser import parseXML
from . import debug


class PidgenDirectoryParser(PidgenElement):
    """
    Class for parsing a directory of protocol definition files.
    """

    def __init__(self, parent, dirpath, **kwargs):

        # Set the directory path
        kwargs["path"] = dirpath

        PidgenElement.__init__(self, parent, **kwargs)

    def parse(self):
        """ Parse the current directory.
        - Look for any subdirectories
        - Look for any protocol files (.xml)
        - Note: .xml files prefixed with _ character are treated differently.
        """

        debug.info("Parsing directory:", self.path)

        listing = os.listdir(self.path)

        files = []
        dirs = []

        ignore_list = self.getConfigValue("ignore", [])

        if type(ignore_list) not in [list, tuple]:
            debug.warning("'ignore' values in {f}protocol.xml must be a list".format(f=self.path))
            ignore_list = []

        # Ignore values should be case-insensitive
        ignore = [x.lower() for x in ignore_list]

        for item in listing:

            path = os.path.join(self.path, item)

            if item.lower() in ignore:
                debug.info("Skipping {f}".format(f=path))
                continue

            if os.path.isdir(path):
                dirs.append(item)

            if os.path.isfile(path) and item.endswith(".xml"):
                files.append(path)

        # Parse any files first
        self.parseFiles(files)

        # Then parse any sub-directories
        self.parseSubDirs(dirs)

    def parseFiles(self, files):
        """
        Parse list of .xml files discovered in the local directory.
        """

        if len(files) == 0:
            debug.info("No protocol files found in directory '{d}'".format(d=self.path))

        # Parse all protocol files
        for f in files:

            self.includePath(self, f)

    def parseSubDirs(self, dirs):
        for d in dirs:

            # Create a new DirectoryParser instance
            PidgenDirectoryParser(self, os.path.join(self.path, d))

    @property
    def files(self):
        """ Return a list of protocol files under this directory """
        return self.getChildren(PidgenFileParser)

    @property
    def dirs(self):
        """ Return a list of directories under this directory """
        return self.getChildren(PidgenDirectoryParser)


class PidgenFileParser(PidgenElement):
    """
    Class for representing a single protocol file.
    """

    ALLOWED_CHILDREN = [
        "pkt", "packet",  # Synonymous
        "struct", "structure",  # Synonymous
        "enum", "enumeration",  # Synonymous
        "require",
    ]

    def __init__(self, parent, **kwargs):

        PidgenElement.__init__(self, parent, **kwargs)

    def parse(self):
        """
        Parse an individual protocol file.
        The root-node has been checked by the directory parser, so we know this file is valid.
        """

        children = self.xml.getchildren()

        for child in children:
            # Iterate through each top-level structure in the XML file
            tag = child.tag.lower()

            if tag in ["enum", "enumeration"]:
                # Construct an Enumeration under this file
                PidgenEnumeration(self, xml=child)

            elif tag in ["pkt", "packet"]:
                # Construct a Packet under this file
                PidgenPacket(self, xml=child)

            elif tag in ["struct", "structure"]:
                # Construct a struct under this file
                PidgenStruct(self, xml=child)
            
            elif tag in ['require']:

                # Loop through all keys, rather than using get()
                # This is to circumvent case-sensitive search
                for key in child.keys():
                    if key.lower() in ['file']:
                        self.includeFile(child.get(key))
                        break

                    elif key.lower() in ['dir', 'directory']:
                        # TODO - Include relative directories
                        pass

    @property
    def enumerations(self):
        """
        Return a list of enumerations which exist under this file.
        """

        return self.getChildren(PidgenEnumeration)

    @property
    def packets(self):
        """
        Return a list of packets which exist under this file.
        """

        return self.getChildren(PidgenPacket)
        
    @property
    def structs(self):
        """
        Return a list of structs which exist under this file
        """

        return self.getChildren(PidgenStruct)

    def includeFile(self, filename):
        """
        Include a file relative to this one.
        """

        debug.info("{f} - Including file '{p}'".format(f=self.path, p=filename))

        abspath = os.path.join(self.directory, filename)

        if not self.checkPath(abspath):
            return False

        if os.path.isfile(abspath):

            doc = parseXML(abspath)
            root = doc.getroot()

            if root.tag.lower() == 'protocol':
                
                # Load the file
                PidgenFileParser(self, xml=root, path=abspath)

            else:
                debug.warning("File '{f}' has root tag '{t}' - skipping.".format(
                    f=filename,
                    t=root.tag
                ))
