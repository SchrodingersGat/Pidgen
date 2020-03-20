# -*- coding: utf-8 -*-

from __future__ import print_function

import os


class PyGenElement():
    """
    Base level PyGenElement class.
    Provides low-level functionality inherited by all higher classes
    
    """

    def __init__(self, element_type, **kwargs):
        """
        Initialize the element with some basic information

        kwargs:
            name - Local name of the element
            path - Logical file path of the current element
            data - Data structure (dictionary) loaded from source .yaml file
        
        """

        self.name = kwargs.get("name", "")
        self.path = kwargs.get("path", "")
        self.data = kwargs.get("data", {})

        # Default element name (sub-classes should override)
        self.element_type = element_type

    @property
    def level(self):
        """
        Return the directory level of this element.
        Top-level is level 1.
        """

        return len(self.namespace.split(os.path.sep))

    @property
    def abspath(self):
        """ Return the absolute filepath of this element """
        return os.path.abspath(self.path).strip()

    @property
    def namespace(self):
        """ Return the 'namespace' (basedir) of this element """
        return os.path.dirname(self.path).strip()

    def warning(self, msg):
        """
        Print a warning message
        """

        print("{path}: WARNING - {msg}".format(path=self.path, msg=msg))

    def error(self, msg):
        """
        Print an error message
        """

        print("{path}: ERROR - {msg}".format(path=self.path, msg=msg))

    def __str__(self):
        """ String representation of this item. """

        lvl = "-" * (self.level - 1) if self.level > 1 else ""

        return "{lvl} {el} - {name} - {path}".format(
            lvl=lvl,
            el=self.element_type,
            name=self.name,
            path=self.path,
        )