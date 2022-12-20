def bits(typ):
    return typ.width()


def bitwidth(v):
    return int(v).bit_length()


def clog2(v):
    return int(v - 1).bit_length()
