# -*- coding: utf-8 -*-

from .element import PyGenElement
from . import debug


class PyGenEnumeration(PyGenElement):
    """
    The PyGenEnumeration class provides support for integer enumerations.
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

    def __init__(self, **kwargs):

        PyGenElement.__init__(self, **kwargs)

        self.parse()

    def parse(self):
        
        debug.debug("Parsing enumeration -", self.name)

        values = self.data.get(self.KEY_VALUES, [])

        # Seed the iterator index
        idx = 0

        # Keep track of which values have been observed
        values_seen = set()

        for item in values:

            data = values[item]

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

            else:
                debug.error("Unknown value for enum '{e}': {i} = '{v}' - {f}".format(
                    e=self.name,
                    i=item,
                    v=data,
                    f=self.path
                ))

                # Revert to the current index
                value = idx

            data = values[item]

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

            # Increment the index for the next loop
            idx = idx + 1

            debug.debug("Found enumeration value:", self.renderKey(item), "->", value)

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
