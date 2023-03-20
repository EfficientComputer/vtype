def bits(typ):
    if type(typ) is type:
        typ = typ()
    return typ.width()


def bitwidth(v):
    if type(v) is type:
        v = v()
    return int(v).bit_length()


def clog2(v):
    if type(v) is type:
        v = v()
    return int(v - 1).bit_length()
