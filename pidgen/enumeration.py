# -*- coding: utf-8 -*-

from .element import PidgenElement
from . import debug


class PidgenEnumeration(PidgenElement):
    """
    The PidgenEnumeration class provides support for integer enumerations.
    """

    # Keys associated with the enumeration
    KEY_VALUES = "values"
    KEY_PREFIX = "prefix"
    
    # Keys associated with an enumeration value
    KEY_VALUE = "value"

    _VALID_KEYS = [
        KEY_VALUES,
        KEY_PREFIX
    ]

    _REQUIRED_KEYS = [
        KEY_VALUES,
    ]

    def __init__(self, parent, **kwargs):

        PidgenElement.__init__(self, parent, **kwargs)

        self.parse()

    def parse(self):
        
        debug.debug("Parsing enumeration -", self.name)

        values = self.data.get(self.KEY_VALUES, [])

        # Seed the iterator index
        idx = 0

        # Keep track of which values have been observed
        values_seen = set()

        # Keep track of the enumeration key:value pairs
        self._values = {}

        for item in values:

            # Extract the data associated with this enum entry
            data = values[item]

            # Create an empty dict to store information about this enum value
            item_attributes = {}

            """
            The simplest way to specify an enumeration value is simply with a "key" line:
            e.g. "key:"
            In this case the value-type is None, and we simply use the current incrementing index.
 
            Or, an enumeration value may be specified simply on a single line,
            e.g. key: value
            In such a case, extra options are not avaialable.
            
            Finally, the provided data may be a dict{} containing extra information about the enum

            So, a set of enumeration values could look like:

            values:
                cat: 1
                dog:
                mouse:
                    comment: The value of this item will be 3
                camel:
                    value: 100
                    comment: Reset the value of this item
                octopus: 8

            Which will evaluate to:

            cat -> 1
            dog -> 2
            mouse -> 3
            octopus -> 8
            camel -> 100

            """

            if data is None:
                value = idx

            elif type(data) in [str, int]:
                try:
                    value = int(data)

                    # Reset the iterator to this new value
                    idx = value

                except ValueError:
                    debug.warning("Enum {e}:{i} - Value '{v}' is invalid - {f}".format(
                        e=self.name,
                        i=item,
                        v=data,
                        f=self.path
                    ))

                    # Default to the current index
                    value = idx

            elif type(data) is dict:
                if self.KEY_VALUE in data:
                    value = data[self.KEY_VALUE]
                    try:
                        value = int(value)

                        # Reset the iterator to this new value
                        idx = value

                    except ValueError:
                        debug.warning("Enum {e}:{i} - Value '{v}' invalid - {f}".format(
                            e=self.name,
                            i=item,
                            v=value,
                            f=self.file
                        ))

                        value = idx
                else:
                    value = idx

                # Copy across all other data (for later use)
                for k in data.keys():
                    item_attributes[k] = data[k]

            else:
                debug.error("Unknown value for enum '{e}': {i} = '{v}' - {f}".format(
                    e=self.name,
                    i=item,
                    v=data,
                    f=self.path
                ))

                # Revert to the current index
                value = idx

            # Check that the computed value has not been seen previously
            if value in values_seen:
                debug.warning("Enum {e}:{i} - Value '{v}' is duplicated - {f}".format(
                    e=self.name,
                    i=item,
                    v=value,
                    f=self.path
                ))
            else:
                values_seen.add(value)

            item_attributes[self.KEY_VALUE] = value

            # Increment the index for the next loop
            idx = idx + 1

            # Record this enumeration
            self._values[item] = item_attributes

            debug.debug("Found enumeration value:", self.renderKey(item), "->", self.getValue(item))

    @property
    def prefix(self):
        """ Return the prefix for this enumeration """
        return self.data.get(self.KEY_PREFIX, "").strip()

    def renderKey(self, key, capitalize=True):
        """ Render a key for this enumeration """

        key = key.strip()

        if capitalize:
            key = key.upper()

        return self.prefix + key

    @property
    def keys(self):
        """ Return the available enumeration keys """
        return [k for k in self._values.keys()]

    @property
    def values(self):
        """ Return a set of values defined for this enumeration """

        v = set()

        for key in self.keys:
            value = self.getValue(key)
            if value:
                v.add(value)

        return v

    def getData(self, key):
        """
        Return the dataset associated with the provided key.
        If an invalid key is provided, an empty dict is returned.
        """
        if key in self.keys:
            return self._values[key]
        else:
            debug.warning("Enum '{e}' does not contain the key '{k}' - {f}".format(
                e=self.name,
                k=key,
                f=self.path
            ))

            return {}

    def getValue(self, key):
        """ Return the value associated with the provided key """

        return self.getData(key).get(self.KEY_VALUE, None)

    def getComment(self, key):
        """ Return the comment associated with the provided key """

        return self.getData(key).get(self.KEY_COMMENT, "")

    def getKey(self, value):
        """ Return the key associated with the provided value """
        for k in self.keys:
            if self._values[k] == value:
                return k

        debug.warning("Enum '{e}' does not contain the value '{v}' - {f}".format(
            e=self.name,
            v=value,
            f=self.path
        ))

        return None
