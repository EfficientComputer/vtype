from .vobject import VObject, VEndian


class VUnion(VObject):

    def members(self):
        return {
            k: v
            for k, v in self.__dict__.items() if isinstance(v, VObject)
        }

    def width(self):
        for v in self.members().values():
            return v.width()

    def shape(self):
        return (self.width(), )

    def __le__(self, other):
        for k, v in self.members().items():
            assert hasattr(other, k)
            v <= getattr(other, k)

    def __setattr__(self, k, v):
        if isinstance(v, VObject):
            if not hasattr(self, 'underlying'):
                dict.__setattr__(self, 'underlying', v)
            assert v.width() == self.underlying.width()
            v.update_val(self.underlying.val())

        dict.__setattr__(self, k, v)

    def val(self):
        return self.underlying.val()

    def update_val(self, val):
        self.underlying.update_val(val)

    def serialize(self, endian=VEndian.BIG):
        for v in self.members().values():
            return v.serialize(endian)

    def verilog(self, name=None, refs=set(), inline=False, indent=0):
        if name is None: name = self.vtype()
        ind = '\t' * indent
        inline = '' if inline else 'typedef '

        s = f'{ind}{inline}union packed {{\n'

        for k, v in self.members().items():
            if v.vtype() in refs:
                s += f'{ind}\t{v.vtype()} {k};'
            else:
                s += v.verilog(refs=refs,
                               name=k,
                               inline=True,
                               indent=indent + 1)
            s += '\n'

        s += f'{ind}}} {name.lower()};'
        return s
