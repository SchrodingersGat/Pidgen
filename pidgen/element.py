# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import yaml

from . import debug


class PidgenLoader(yaml.loader.SafeLoader):
    """
    Custom yaml loader implementation.

    - Includes line number information
    """

    def construct_mapping(self, node, deep=False):
        mapping = super(PidgenLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping


class PidgenElement():
    """
    Base level PidgenElement class.
    Provides low-level functionality inherited by all higher classes
    
    """

    # Generic keys we can expect for most element types
    KEY_NAME = "name"
    KEY_TITLE = "title"
    KEY_COMMENT = "comment"

    _BASIC_KEYS = [
        KEY_NAME,
        KEY_TITLE,
        KEY_COMMENT,
    ]

    # Default implementation of _VALID_KEYS is empty
    _VALID_KEYS = []

    # Default implementation of _REQUIRED_KEYS is empty
    _REQUIRED_KEYS = []

    # Options for specifying a "true" value
    _TRUE = ["y", "yes", "1", "true", "on"]
    _FALSE = ["n", "no", "0", "false", "off"]

    def __init__(self, parent, **kwargs):
        """
        Initialize the element with some basic information

        args:
            parent - Parent object for this object. e.g. directory -> file -> packet -> struct -> data

        kwargs:
            xml - Raw xml data associated with this object
            path - Filepath of this object
        """

        self.xml = kwargs.get("xml", None)

        self.children = []

        self.parent = parent

        if self.parent is not None:
            self.parent.addChild(self)

        # Store a copy of the kwargs
        self.kwargs = kwargs

        self.validateKeys()

        self._parse()

    def _parse(self):
        if self.xml is not None:
            self.parse()

    def keys(self):
        """
        Return a list of all top-level tags in this item.
        Remove any 'meta' tags (e.g. line number)
        """

        if self.xml is None:
            return []

        return [k for k in self.xml.keys()]

    def isSet(self, key, default=False):
        """
        Test if the given key's value is "set" (in a boolean sense).

        To be considered "set":
        1) The key must be present
        b) The associated value must "look" like a binary value
        """

        return self.parseBool(self.get(key, default))

    def get(self, key, ret=None, ignore_case=True):
        """
        Return the value associated with the given key, in the XML data.

        Args:
            key - Name of the key

        kwargs:
            ret - Value to return if the key is not found
            ignore_case - If true, key-lookup is not case sensitive (default = True)
        """

        if self.xml is None:
            return ret

        if ignore_case:
            key = key.lower()

            for k in self.keys():
                if key == k.lower():
                    return self.xml.get(k, ret)

            # No matching key found?
            return ret

        else:
            return self.xml.get(key, ret)

    @property
    def name(self):
        """ Return the 'name' for this object """

        return self.get("name", None)

    @property
    def title(self):
        """
        Return the 'title' for this object.
        The title is an optional description text.
        If not present, default to the 'name' field.
        """

        return self.get("title", self.name)

    @property
    def path(self):
        """ Return the filepath for this object """

        # If no path is specified for this object, maybe the parent?
        p = self.kwargs.get('path', None)

        if p is None and parent is not None:
            return parent.path
        else:
            return p

    @property
    def comment(self):
        """ Return the 'comment' for this object """

        return self.get('comment', None)

    @property
    def ancestors(self):
        """ Return flattened list of ancestors for this object """
        a = []

        parent = self.parent

        while parent is not None:
            a.append(parent)
            parent = parent.parent

        return a

    def getDescendants(self, descendants=[]):
        """
        Return a flattened list of all descendants of this object (recursive)

        Args:
            descendants - Flat list of descendants, passed down to lower function calls
        """

        for child in self.children:
            # Add the child to the list
            descendants.append(child)

            # Child then adds its own descendants to the list
            child.getDescendants(descendants)

        return descendants

    def addChild(self, child):
        """ Add a new child object """

        if child not in self.children:
            self.children.append(child)

    def getSetting(self, key):
        """
        Return the value associated with the provided key (if it exists).
        If the key is not found, request it from the parent object (and so-on).
        In this manner, a top-down settings hierarchy is achieved.
        """

        if key in self.kwargs:
            return self.kwargs[key]

        elif self.parent is not None:
            return self.parent.getSetting(key)

        else:
            return None

    def setSettings(self, key, value):
        """
        Set the value of a local settings parameter.
        This value is available to this object and also any children,
        unless those children override the value.
        """

        self.kwargs[key] = value

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

        provided = self.keys()
        
        for key in self.required_keys:
            if key not in provided:
                debug.error("Required key '{k}' missing from '{name}' in {f}".format(
                    k=key,
                    name=self.name,
                    f=self.path
                ))

        # Check for unknown keys
        for el in provided:
            if el.lower() not in self.allowed_keys:
                debug.warning("Unknown key '{k}' found in '{name}' - {f}".format(
                    k=el,
                    name=self.name,
                    f=self.path
                ))

                # TODO - Use Levenstein distance for a "did-you-mean" message

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

    def parseInt(self, value):
        """
        Check if a value looks like an integer. 
        
        Formats supported:
            integer - 123
            string - '123'
            bin - '0b1010'
            hex - '0xA0'
            oct - '0o75'
        """

        if type(value) is int:
            return value
        
        value = str(value)

        try:
            return int(value)
        except ValueError:
            pass

        if value.startswith('0b'):
            try:
                return int(value, 2)
            except ValueError:
                pass

        if value.startswith('0o'):
            try:
                return int(value, 8)
            except ValueError:
                pass

        if value.startswith('0x'):
            try:
                return int(value, 16)
            except ValueError:
                pass

        debug.warning("Value {i} could not be converted to an integer - {f}".format(i=value, f=self.path))

        raise ValueError

    def parseBool(self, value):
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

    def checkBool(self, key):
        """
        Check if the supplied key maps to a boolean parameter
        """

        if key in self.data:
            return self.parseBool(self.data[key])
        else:
            return False
