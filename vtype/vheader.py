class VHeader(object):

    def __init__(self, name):
        self.name = name
        self.members = []

    def append(self, t):
        self.members.append(t)

    def __iadd__(self, other):
        assert type(other) is list, 'not a list'
        self.members += other
        return self

    def verilog(self):
        name = self.name.upper()
        s = f'`ifndef {name}_VH_\n'
        s += f'`define {name}_VH_\n'
        s += f'package {name};\n'

        refs = set()
        for member in self.members:
            s += member.verilog(refs=refs) + '\n'
            refs.add(member.vtype())

        s += f'endpackage : {name}\n'
        s += '`endif\n'
        return s
