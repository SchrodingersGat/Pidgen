# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import yaml

from . import debug


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

        required kwargs:
            name - Local name of the element
            path - Logical file path of the current element
            data - Data structure (dictionary) loaded from source .yaml file
        """

        self.children = []

        self.parent = parent

        if self.parent is not None:
            self.parent.addChild(self)

        # Store a copy of the kwargs
        self.kwargs = kwargs

        # Store the dataset associated with this object
        self.data = kwargs.get("data", {})

        self.validateKeys()

    @property
    def name(self):
        """ Return the 'name' for this object """

        return self.kwargs.get('name', None)

    @property
    def title(self):
        """
        Return the 'title' for this object.
        The title is an optional description text.
        If not present, default to the 'name' field.
        """

        return self.kwargs.get('title', self.name)

    @property
    def path(self):
        """ Return the filepath for this object """

        return self.kwargs.get('path', None)

    @property
    def comment(self):
        """ Return the 'comment' for this object """

        return self.kwargs.get('comment', None)

    @property
    def ancestors(self):
        """ Return flattened list of ancestors for this object """
        a = []

        parent = self.parent

        while parent is not None:
            a.append(parent)
            parent = parent.parent

        return a

    @property
    def tags(self):
        """
        Return a list of all top-level tags in this item.
        Remove any 'meta' tags (e.g. line number)
        """

        tags = []

        for k in self.data.keys():
            # Ignore a 'meta-tag'
            if k.startswith("_"):
                continue
            tags.append(k)

        return tags

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

        provided = [str(key).lower() for key in self.tags]
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

    def parseYaml(self, filename):
        """
        Parse an individual .yaml file
        """

        debug.debug("Parsing file:", filename)

        with open(self.path, 'r') as yaml_file:
            try:
                self.data = yaml.safe_load(yaml_file)
            except yaml.parser.ParserError as e:
                debug.error("Error parsing file -", self.path)
                debug.error(e, fail=True)