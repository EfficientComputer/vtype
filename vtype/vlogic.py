from .vobject import VObject, VEndian
import numpy as np
from functools import reduce


class VBit(VObject):
    def __init__(self):
        self._val = 0

    def vtype(self):
        name = super().vtype()
        if name != "logic":
            return name

    def __str__(self):
        return str(self._val)

    def __le__(self, other):
        try:
            self._val = int(other)
            return
        except:
            pass
        self._val = other.val()

    def val(self):
        return self._val

    def width(self):
        return 1

    def shape(self):
        return (1,)

    def serialize(self, endian=VEndian.BIG):
        return [self._val]

    def verilog(self, name=None, refs=set(), inline=False, indent=0):
        if name is None:
            name = self.vtype()
        inline = "" if inline else "typedef "
        indent = "\t" * indent
        return f"{inline}{indent}logic {name.lower()};"


class VLogic(VObject):
    def __init__(self, shape=(1), base_type=VBit, overwrite_values=False):
        if type(shape) is not tuple:
            shape = (shape,)
        shape = tuple(map(int, shape))

        self._count = reduce(lambda x, y: x * y, shape)
        self._shape = shape

        self._indices = np.arange(self._count, dtype=np.uint32).reshape(shape)
        if not overwrite_values:
            self._val = [base_type() for _ in range(self._count)]
        self._base_type = base_type
        self._width = self._count * base_type().width()

    def __getitem__(self, key):
        indices = self._indices[key]
        if isinstance(indices, np.uint32):
            return self._val[indices]

        new = VLogic(indices.shape, self._base_type, True)
        new._val = [self._val[idx] for idx in indices.flatten()]
        return new

    def __le__(self, other):
        try:
            v = int(other)
            for i in range(self._width):
                self._val[i] <= ((v >> i) & 0x1)
            return
        except Exception as e:
            pass

        v = other.serialize(VEndian.LITTLE)
        for i in range(self._width):
            self._val[i] <= v[i]

    def __int__(self):
        bits = self.serialize()[::-1]
        return sum([b << i for i, b in enumerate(bits)])

    def val(self):
        return self._val

    def update_val(self, val):
        self._val = val

    def width(self):
        return self._width

    def shape(self):
        return self._shape

    def vtype(self):
        name = super().vtype()
        if name != "logic":
            return name

        str_shape = ""
        for dim in self._shape:
            str_shape += f"{dim}_"
        str_shape = str_shape[:-1]

        return f"{name}_{str_shape}"

    def serialize(self, endian=VEndian.BIG):
        if self._val is None:
            return [0 for _ in range(self._width)]

        bits = []
        for v in self._val:
            bits += v.serialize(endian)

        return bits[::-1] if endian == VEndian.BIG else bits

    def verilog(self, name=None, refs=set(), inline=False, indent=0):
        if name is None:
            name = self.vtype()
        inline = "" if inline else "typedef "
        indent = "\t" * indent
        str_shape = ""
        for dim in self._shape:
            str_shape += "[%d:0]" % (dim - 1)
        return f"{inline}{indent}logic {str_shape} {name.lower()};"
