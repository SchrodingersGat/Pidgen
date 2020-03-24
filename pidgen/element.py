# -*- coding: utf-8 -*-

from __future__ import print_function

import os
from rapidfuzz import fuzz

from . import debug


class PidgenElement():
    """
    Base level PidgenElement class.
    Provides low-level functionality inherited by all higher classes
    
    """

    BASIC_KEYS = [
        "name",
        "title",
        "comment",
    ]

    # Options for specifying a "true" value
    _TRUE = ["y", "yes", "1", "true", "on"]
    _FALSE = ["n", "no", "0", "false", "off"]

    def __repr__(self):
        return "<{tag}>:{name} - {f}:{line}".format(
            tag=self.tag,
            name=self.name,
            f=self.path,
            line=self.lineNumber
        )

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
        self.validateChildren()

        self._parse()

    def _parse(self):
        if self.xml is not None:
            debug.debug("Parsing", str(self))
            self.parse()

    def parse(self):
        """ Default implementation does nothing... """
        pass

    def findStructByName(self, struct_name, global_search=True):
        """
        Lookup a struct using the provided name.

        Args:
            struct_name - Name of the struct to look for (case-insensitive)
            global_search - If True, search the entire protocol. Otherwise, search local object. (Default = True)
        """

        if global_search:
            context = self.protocol
        else:
            context = self

        # Grab list of structs
        structs = context.getChildren("PidgenStruct", traverse_children=global_search)

        for struct in structs:
            if struct.name.lower() == struct_name.lower():
                return struct

        # TODO - Print "best match" for struct name?
        # TODO - Warn if duplicate matches are found...
        return None


    def getChildren(self, pattern, traverse_children=False):
        """
        Return any children under this item which conform to the provided pattern.
        Pattern can be:
        
        a) A class type
        b) A "string" representation of a class type (to get around circular import issues)
        c) A list [] of potential class types as per a) or b)
        """

        # Enforce list format so the following code is consistent
        if type(pattern) not in [list, tuple]:
            pattern = [pattern]

        childs = []

        for child in self.children:
            
            for p in pattern:
                if type(p) is str:
                    if p.lower() in str(child.__class__).lower():
                        childs.append(child)
                        break
                elif isinstance(child, p):
                    childs.append(child)
                    break

            if traverse_children:
                childs += child.getChildren(pattern, True)

        return childs

    @property
    def protocol(self):
        """
        The "Protocol" object is the top-level directory parser.
        So, go obtain the "Protocol" object, simply traverse upwards,
        until there are no higher parent objects.
        """

        if self.parent is None:
            return self
        else:
            return self.parent.protocol

    @property
    def lineNumber(self):
        """ Return the line number of the XML element which defines this object """

        try:
            return self.xml._start_line_number
        except AttributeError:
            return 0

    @property
    def tag(self):
        """ Return the base tag associated with this element """
        if self.xml is None:
            return ''
        else:
            return self.xml.tag

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
            key - Name of the key (or a list of keys to be checked in order)

        kwargs:
            ret - Value to return if the key is not found
            ignore_case - If true, key-lookup is not case sensitive (default = True)
        """

        if self.xml is None:
            return ret

        # Enforce list encoding
        if type(key) not in [list, tuple]:
            key = [key]

        for k in key:
            if ignore_case:
                k = k.lower()

            for sk in self.keys():
                
                if ignore_case:
                    skl = sk.lower()
                else:
                    skl = sk

                if k == skl:
                    return self.xml.get(sk, ret)

        # No matching key found?
        return ret

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

        if p is None and self.parent is not None:
            return self.parent.path
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

        if hasattr(self, "REQUIRED_KEYS"):
            return set(self.REQUIRED_KEYS)
        else:
            return set()

    @property
    def allowed_keys(self):
        """ Return a list of keys allowed for this element """

        # These keys are "allowed" for any element
        allowed = set(self.BASIC_KEYS)

        if hasattr(self, "ALLOWED_KEYS"):
            for k in self.ALLOWED_KEYS:
                allowed.add(k)

        # Required keys are also 'allowed'
        for k in self.required_keys:
            allowed.add(k)
        
        return allowed

    @property
    def required_children(self):
        """ Return a list of child elements required for this element """

        if hasattr(self, "REQUIRED_CHILDREN"):
            return set(self.REQUIRED_CHILDREN)
        else:
            return set()

    @property
    def allowed_children(self):
        """ Return a list of child elements allowed for this element """

        if hasattr(self, "ALLOWED_CHILDREN"):
            return set(self.ALLOWED_CHILDREN)
        else:
            return set()

    def validateKeys(self):
        """
        Ensure that the tags provided under this element are valid.
        """

        # Check that any required keys are provided

        provided = self.keys()
        
        for key in self.required_keys:
            if key not in provided:
                self.missingKey(key)

        # Check for unknown keys
        for el in provided:
            if el.lower() not in self.allowed_keys:
                self.unknownKey(el)

    def validateChildren(self):
        """
        Ensure that the child structures provided under this element are valid.
        """

        if self.xml is None:
            return

        for child in self.xml.getchildren():

            tag = child.tag.lower()

            if tag not in self.allowed_children:
                self.unknownChild(child.tag, line=child._start_line_number)

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

    def parseFloat(self, value):
        """
        Check if a value looks like a floating point
        """

        if type(value) in [int, float]:
            return value

        value = str(value)

        try:
            return float(value)
        except ValueError:
            debug.warning("Value {i} could not be converted to an float - {f}".format(i=value, f=self.path))
            raise ValueError

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

    def missingKey(self, key):
        """
        Display an error about a missing key
        """

        error = "{f}{line} - Missing key '{k}' in <{t}> '{n}'".format(
            f=self.path,
            line=":{n}".format(n=self.lineNumber) if self.lineNumber > 0 else "",
            k=key,
            t=self.tag,
            n=self.name)

        debug.error(error)

    def unknownKey(self, key, line=0):
        """
        Display a warning about an unknown xml key
        """

        warning = "{f}{line} - Unknown key '{k}' in <{t}> '{n}'".format(
            f=self.path,
            line=":{n}".format(n=self.lineNumber) if self.lineNumber > 0 else "",
            k=key,
            t=self.tag,
            n=self.name
        )

        if line > 0:
            warning += " (line {n})".format(n=line)

        allowed = self.allowed_keys

        if len(allowed) > 0:
            warning += " (Allowed elements = '" + ", ".join([k for k in allowed]) + "')"

        debug.warning(warning)

        # Use Levenstein distance for a "did-you-mean" message
        best_match = None
        best_score = 0

        for k in allowed:
            score = fuzz.partial_ratio(key.lower(), k)

            if score > best_score:
                best_score = score
                best_match = k

        if best_match is not None and best_score > 60:
            did_you_mean = "Instead of '{k}', did you mean '{match}'?".format(k=key, match=best_match)

            debug.warning(did_you_mean)

    def unknownChild(self, element, line=0):
        """
        Display a warning about an unknown child element.
        """

        warning = "{f}{line} - Unknown child element '{e}' in <{t}> '{n}'".format(
            f=self.path,
            line=":{n}".format(n=line) if line > 0 else "",
            e=element,
            t=self.tag,
            n=self.name
        )

        allowed = self.allowed_children

        if len(allowed) > 0:
            warning += " (Allowed elements = '" + ", ".join([k for k in allowed]) + "')"
        
        debug.warning(warning)

        # Use Levenstein distance for a "did-you-mean" message
        best_match = None
        best_score = 0

        for key in allowed:
            score = fuzz.partial_ratio(element.lower(), key)

            if score > best_score:
                best_score = score
                best_match = key

        if best_match is not None and best_score > 60:
            did_you_mean = "Instead of '{k}', did you mean '{match}'?".format(k=element, match=best_match)

            debug.warning(did_you_mean)
