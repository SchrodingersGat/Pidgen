# -*- coding: utf-8 -*-

from .element import PidgenElement
from . import debug


class PidgenEnumerationValue(PidgenElement):
    """
    Single element in an enumeration struct
    """

    ALLOWED_KEYS = [
        "value",
        "title",
        "ignoreprefix",
        "ignoresuffix",
    ]

    REQUIRED_KEYS = [
        "name"
    ]

    def __init__(self, parent, **kwargs):

        PidgenElement.__init__(self, parent, **kwargs)

    @property
    def prefix(self):
        if self.isSet("ignoreprefix"):
            return ""
        elif isinstance(self.parent, PidgenEnumeration):
            return self.parent.prefix
        else:
            return ""

    @property
    def suffix(self):
        if self.isSet("ignoresuffix"):
            return ""
        elif isinstance(self.parent, PidgenEnumeration):
            return self.parent.suffix
        else:
            return ""

    @property
    def enum_title(self):
        """ Render the complete enum title of this element """
        t = self.prefix + self.name + self.suffix
        return t.upper()


class PidgenEnumeration(PidgenElement):
    """
    The PidgenEnumeration class provides support for integer enumerations.
    """

    ALLOWED_KEYS = [
        "prefix",
        "suffix",
    ]

    REQUIRED_KEYS = [
        "name",
    ]

    ALLOWED_CHILDREN = [
        "value"
    ]

    def __init__(self, parent, **kwargs):

        PidgenElement.__init__(self, parent, **kwargs)

    @property
    def values(self):
        """ Return all the values under this enumeration """
        return [c for c in self.children if isinstance(c, PidgenEnumerationValue)]

    def parse(self):

        # Look for all the 'value' objects
        for child in self.xml.getchildren():
            tag = child.tag.lower()

            if tag == "value":

                # Create a new enumeration value
                PidgenEnumerationValue(self, xml=child)

    def calculate(self):
        """
        Calculate the enumerated values
        """

        # Seed the iterator index
        idx = 0

        # Keep track of which values have been observed
        values_seen = set()

        for item in self.values:

            # Extract the data associated with this enum entry
            value = item.value_raw()

            """
            If no value is explicitly provided, use the incrementing index.
            """

            if value is None:
                # No value specified - use the current accumulated index
                value = idx

            elif type(value) in [str, int]:
                try:
                    value = self.parseInt(value)

                    # Reset the iterator to this new value
                    idx = value

                except ValueError:
                    debug.warning("Enum {e}:{i} - Value '{v}' is invalid - {f}".format(
                        e=self.name,
                        i=item,
                        v=value,
                        f=self.path
                    ))

                    # Default to the current index
                    value = idx
                else:
                    value = idx

            else:
                debug.error("Unknown value for enum '{e}': {i} = '{v}' - {f}".format(
                    e=self.name,
                    i=item,
                    v=value,
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

            # Increment the index for the next loop
            idx = idx + 1

            debug.debug("Found enumeration value:", item.name, "->", value)

    @property
    def prefix(self):
        """ Return the prefix for this enumeration """
        return self.get("prefix", "")

    @property
    def suffix(self):
        """ Return the suffix for this enumeration """
        return self.get("suffix", "")

    def renderKey(self, key, capitalize=True):
        """ Render a key for this enumeration """

        key = key.strip()

        if capitalize:
            key = key.upper()

        return self.prefix + key
