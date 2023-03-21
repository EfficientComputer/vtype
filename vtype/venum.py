from .vobject import VObject, VEndian
from .vlogic import VLogic


def VEnum(width):

    class VerilogEnum(VObject):

        def __init__(self, value: int = 0):
            self.v = VLogic(width, value)

        def __le__(self, other):
            assert type(other) is int or type(other) == type(self)
            if type(other) == type(self):
                self.v <= other.v
                return
            self.v <= other

        def __int__(self):
            return int(self.v)

        def width(self):
            return width

        def shape(self):
            return (width, )

        def val(self):
            return self.v.val()

        def update_val(self, val):
            self.v.update_val(val)

        def serialize(self, endian: VEndian = VEndian.BIG):
            return self.v.serialize(endian)

        def verilog(self, name=None, refs=set(), inline=False, indent=0):
            if name is None: name = self.vtype()
            indent = '\t' * indent
            inline = '' if inline else 'typedef '
            s = f'{inline}{indent}enum logic [{width-1}:0] {{\n'

            members = \
                {k: v for k, v in type(self).__dict__.items() if type(v) is int}
            for k, v in members.items():
                s += f'{indent}\t{k} = {width}\'d{v},\n'

            s = s[:-2] + '\n'
            s += f'{indent}}} {name.lower()};'
            return s

    return VerilogEnum
