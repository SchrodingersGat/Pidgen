# -*- coding: utf-8 -*-

from .element import PyGenElement
from . import debug


class PyGenData(PyGenElement):
    """
    A PyGenData object is a basic data entry,
    which can be defined in either a struct or a packet

    Attributes:
        datatype - Native datatype of this entry
        encoding - "On the wire" encoding of this entry (optional)
        units - Natural units of the represented data
    """

    KEY_STRUCT = "struct"
    KEY_DATATYPE = "datatype"
    KEY_ENCODING = "encoding"
    KEY_UNITS = "units"

    _VALID_KEYS = [
        KEY_STRUCT,
        KEY_DATATYPE,
        KEY_ENCODING,
        KEY_UNITS
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

    def __init__(self, **kwargs):

        PyGenElement.__init__(self, **kwargs)

        self.parse()

    def parse(self):
        debug.debug("Parsing data entry:", self.name, self.datatype)

    @property
    def datatype(self):
        """
        Return the 'datatype' for this packet element.

        If no 'datatype' is specified, look for an 'encoding' specification.
        """

        dt = ""

        if self.KEY_DATATYPE in self.data:
            dt = self.data[self.KEY_DATATYPE]
        elif self.KEY_ENCODING in self.data:
            dt = self.data[self.KEY_ENCODING]
        else:
            debug.error("No '{key}' set for entry '{name}' - {f}".format(
                key=self.KEY_DATATYPE,
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

        if self.KEY_ENCODING in self.data:
            enc = self.data[self.KEY_ENCODING]
        elif self.KEY_DATATYPE in self.data:
            enc = self.data[self.KEY_DATATYPE]
        else:
            debug.error("No '{key}' provided for entry '{name}' - {f}".format(
                key=self.KEY_ENCODING,
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
        return self.data.get(self.KEY_UNITS, "")
