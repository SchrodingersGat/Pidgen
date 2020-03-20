# -*- coding: utf-8 -*-

from __future__ import print_function

import os


class PyGenElement():
    """
    Base level PyGenElement class.
    Provides low-level functionality inherited by all higher classes
    
    """

    def __init__(self, **kwargs):
        """
        Initialize the element with some basic information

        kwargs:
            name - Local name of the element
            path - Logical file path of the current element
            data - Data structure (dictionary) loaded from source .yaml file
            verbosity - Verbosity level of debug output
        """

        # Store a copy of the kwargs
        self.kwargs = kwargs

        self.name = kwargs.get("name", "")
        self.path = kwargs.get("path", "")
        self.data = kwargs.get("data", {})

        # Store settings dict (default = empty dict)
        self.settings = kwargs.get("settings", {})

    @property
    def verbosity(self):
        """
        Get the message 'verbosity' level.
        By default, ERROR and WARNING messages are displayed.
        """
        return self.settings.get('verbosity', self._MSG_WARN)

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
