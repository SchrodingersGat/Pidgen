# -*- coding: utf-8 -*-

from __future__ import print_function

import os
from . import debug


class PidgenElement():
    """
    Base level PidgenElement class.
    Provides low-level functionality inherited by all higher classes
    
    """

    # Generic keys we can expect for most element types
    KEY_NAME = "name"
    KEY_COMMENT = "comment"

    _BASIC_KEYS = [
        KEY_NAME,
        KEY_COMMENT
    ]

    # Default implementation of _VALID_KEYS is empty
    _VALID_KEYS = []

    # Default implementation of _REQUIRED_KEYS is empty
    _REQUIRED_KEYS = []

    # Options for specifying a "true" value
    _TRUE = ["y", "yes", "1", "true", "on"]
    _FALSE = ["n", "no", "0", "false", "off"]

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

        self.validateKeys()

    @property
    def required_keys(self):
        """ Return a list of keys required for this element """
        return self._REQUIRED_KEYS

    @property
    def allowed_keys(self):
        """ Return a list of keys allowed for this element """
        return self._BASIC_KEYS + self._VALID_KEYS

    def validateKeys(self):
        """
        Ensure that the tags provided under this element are valid.
        """

        # Check that any required keys are provided
        provided = [key.lower() for key in self.data]
        for key in self.required_keys:
            if key not in provided:
                debug.error("Required key '{k}' missing from '{name}' in {f}".format(
                    k=key,
                    name=self.name,
                    f=self.path
                ))

        # Check for unknown keys
        for el in self.data:
            if el.lower() not in self.allowed_keys:
                debug.warning("Unknown key '{k}' found in '{name}' - {f}".format(
                    k=el,
                    name=self.name,
                    f=self.path
                ))
                # TODO - Use Levenstein distance for a "did-you-mean" message

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

    def checkBool(self, value):
        """
        Check if a value looks like a True or a False value
        """

        value = str(value).lower().strip()

        if value in self._TRUE:
            return True

        elif value in self._FALSE:
            return False

        else:
            debug.warning("Value '{v}' not a boolean value - {f}".format(v=value, f=self.path))
            return False
