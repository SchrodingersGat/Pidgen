# -*- coding: utf-8 -*-

from .element import PidgenElement
from . import debug


class PidgenDataElement(PidgenElement):
    """
    A PidgenData object is a basic data entry,
    which can be defined in either a struct or a packet

    Attributes:
        datatype - Native datatype of this entry
        encoding - "On the wire" encoding of this entry (optional)
        units - Natural units of the represented data
    """

    ALLOWED_KEYS = [
        "datatype", "inmemorytype",  # Synonymous
        "encoding", "encodedtype",  # Synonymous
        "units",
        "default",
    ]

    REQUIRED_KEYS = [
        "name",
    ]

    # Allowable datatypes
    DATA_U8 = 'U8'          # Unsigned integer, 8 bits
    DATA_S8 = "S8"          # Signed integer, 8 bits
    DATA_U16 = "U16"        # Unsigned integer, 16 bits
    DATA_S16 = "S16"        # Signed integer, 16 bits
    DATA_U32 = "U32"        # Unsigned integer, 32 bits
    DATA_S32 = "S32"        # Signed integer, 32 bits
    DATA_U64 = "U64"        # Unsigned integer, 64 bits
    DATA_S64 = "S64"        # Signed integer, 64 bits
    DATA_F16 = "F16"        # Floating point, 16 bits
    DATA_F32 = "F32"        # Floating point, 32 bits
    DATA_F64 = "F64"        # Floating point, 64 bits
    DATA_STR = "STRING"     # String (char*)

    _U_FMT_STRING = ["u{n}", "uint{n}", "uint{n}_t", "unsigned{n}"]
    _S_FMT_STRING = ["i{n}", "s{n}", "int{n}", "sint{n}", "int{n}_t", "sint{n}_t", "signed{n}"]
    _F_FMT_STRING = ["f{n}", "float{n}"]

    # String lookup maps for allowed datatypes
    _DATATYPE_KEYS = {
        DATA_U8: [x.format(n=8) for x in _U_FMT_STRING] + ["char", "unsigned char", "unsigned byte"],
        DATA_S8: [x.format(n=8) for x in _S_FMT_STRING] + ["signed char", "signed byte"],
        DATA_U16: [x.format(n=16) for x in _U_FMT_STRING],
        DATA_S16: [x.format(n=16) for x in _S_FMT_STRING],
        DATA_U32: [x.format(n=32) for x in _U_FMT_STRING],
        DATA_S32: [x.format(n=32) for x in _S_FMT_STRING],
        DATA_U64: [x.format(n=64) for x in _U_FMT_STRING],
        DATA_S64: [x.format(n=64) for x in _S_FMT_STRING],
        DATA_F16: [x.format(n=16) for x in _F_FMT_STRING],
        DATA_F32: [x.format(n=32) for x in _F_FMT_STRING],
        DATA_F64: [x.format(n=64) for x in _F_FMT_STRING],
        DATA_STR: ["str", "string", "text"],
    }

    # Width of each data type (bits)
    _DATA_WIDTH_BITS = {
        DATA_U8: 8,
        DATA_S8: 8,
        DATA_U16: 16,
        DATA_S16: 16,
        DATA_U32: 32,
        DATA_S32: 32,
        DATA_U64: 64,
        DATA_S64: 64,
        DATA_F16: 16,
        DATA_F32: 32,
        DATA_F64: 64,
    }

    def __init__(self, parent, **kwargs):

        PidgenElement.__init__(self, parent, **kwargs)

    def parse(self):
        # TODO

        pass

    @property
    def datatype(self):
        """
        Return the 'datatype' for this packet element.

        If no 'datatype' is specified, look for an 'encoding' specification.
        """

        dt = None

        options = ['datatype', 'inMemoryType', 'encoding', 'encodedType']

        for opt in options:
            dt = self.get(opt)

            if dt:
                break

        if dt is None:
            debug.error("No data-type set for entry '{name}' - {f}".format(
                name=self.name,
                f=self.path
            ))

            return None

        # Ensure lower-case for comparison
        dt = dt.lower()

        for key in self._DATATYPE_KEYS:

            options = self._DATATYPE_KEYS[key]
        
            if dt in options:
                return key

        # No valid datatype determined
        debug.error("Datatype '{dt}' not valid for '{name}' - {f}".format(
            dt=dt,
            name=self.name,
            f=self.path
        ))
        
        return None

    @property
    def encoding(self):
        """
        Return the "on-the-wire" encoding for this data.
        If not explicitly specified using the 'encoding' tag,
        then the 'datatype' tag is used by default.
        """

        options = ['encoding', 'encodedType']

        enc = None

        for opt in options:
            enc = self.get(opt)

        # Default to the internal datatype
        if enc is None:
            enc = self.datatype

        if enc is None:
            debug.error("No encoding provided for entry '{name}' - {f}".format(
                name=self.name,
                f=self.path
            ))

            return None

        enc = enc.lower()

        for key in self._DATATYPE_KEYS:

            options = self._DATATYPE_KEYS[key]

            if enc in options:
                return key

        # No valid encoding type determined
        debug.error("Encoding '{enc}' not valid for '{name}' - {f}".format(
            enc=enc,
            name=self.name,
            f=self.path
        ))

        return None

    @property
    def units(self):
        """ Return the units of this data element """
        return self.get("units")
