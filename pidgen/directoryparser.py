# -*- coding: utf-8 -*-


"""
Directory parsing
"""

import os
from .element import PidgenElement
from .fileparser import PidgenFileParser
from . import debug
from .xmlparser import parseXML


class PidgenDirectoryParser(PidgenElement):
    """
    Class for parsing a directory of protocol definition files.
    """

    def __init__(self, parent, dirpath, **kwargs):

        # Set the directory path
        kwargs["path"] = dirpath

        PidgenElement.__init__(self, parent, **kwargs)

        self.parse()

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

        for item in listing:
            path = os.path.join(self.path, item)

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

            if f.startswith("_"):
                # TODO - Special files which augment the protocol generation
                continue

            # Read in the xml doc
            doc = parseXML(f)
            root = doc.getroot()

            debug.info("Reading file: {f}".format(f=f))

            if root.tag.lower() == 'protocol':

                # Create a new file parser instance
                PidgenFileParser(self, xml=root, path=f)
            else:
                debug.warning("File {f} has root tag '{t}' - skipping.".format(
                    f=f,
                    t=root.tag
                ))

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
