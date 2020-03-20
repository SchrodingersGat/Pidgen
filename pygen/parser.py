# -*- coding: utf-8 -*-

"""
Directory and file parser code
"""

import os
import yaml


class PyGenParser():
    """
    Class for parsing a directory of protocol definition files.
    """

    def __init__(self, path, **kwargs):

        self.path = path

        self.yaml_files = []
        self.sub_dirs = []

        # Optional arguments
        self.prefix = kwargs.get("prefix", "")

    def parse(self):
        """ Parse the current directory.
        - Look for any subdirectories
        - Look for any protocol files (.yaml)
        - Note: .yaml files prefixed with _ character are treated differently.
        """

        listing = os.listdir(self.path)

        for item in listing:
            path = os.path.join(self.path, item)

            if os.path.isdir(path):
                self.sub_dirs.append(item)

            if os.path.isfile(path) and item.endswith(".yaml"):
                self.yaml_files.append(item)

        print("Directory:", self.path)

        # Parse all files
        for f in self.yaml_files:

            if f.startswith("_"):
                # TODO
                continue

            p = PyGenFileParser(os.path.join(self.path, f))
            p.parse()

        # Parse all subdirectories
        for d in self.sub_dirs:

            p = PyGenParser(os.path.join(self.path, d))
            p.parse()


class PyGenFileParser():

    def __init__(self, path, **kwargs):

        self.path = path
        self.data = {}

    def parse(self):
        print("Parsing -", self.path)

        with open(self.path, 'r') as yaml_file:
            self.data = yaml.safe_load(yaml_file)

        print(self.data)
