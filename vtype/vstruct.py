from .vobject import VObject, VEndian


class VStruct(VObject):
    def members(self):
        return {k: v for k, v in self.__dict__.items() if isinstance(v, VObject)}

    def width(self):
        w = 0
        for v in self.members().values():
            w += v.width()

        return w

    def shape(self):
        return (self.width(),)

    def __le__(self, other):
        for k, v in self.members().items():
            assert hasattr(other, k)
            v <= getattr(other, k)

    def val(self):
        v = []
        for v in self.members().values():
            v += v.val()
        return v

    def update_val(self, val):
        running = 0
        for v in self.members().values():
            upper = running + len(v.val())
            v.update_val(val[running:upper])
            running = upper

    def serialize(self, endian=VEndian.BIG):
        bitvector = []
        members = list(self.members().values())

        if endian == VEndian.LITTLE:
            members = members[::-1]

        for v in members:
            bitvector += v.serialize(endian)

        return bitvector

    def verilog(self, name=None, refs=set(), inline=False, indent=0):
        if name is None:
            name = self.vtype()
        ind = "\t" * indent
        inline = "" if inline else "typedef "

        s = f"{ind}{inline}struct packed {{\n"

        for k, v in self.members().items():
            if v.vtype() in refs:
                s += f"{ind}\t{v.vtype()} {k};"
            else:
                s += v.verilog(refs=refs, name=k, inline=True, indent=indent + 1)
            s += "\n"

        s += f"{ind}}} {name.lower()};"
        return s
