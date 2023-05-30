import numpy as np

from enum import IntEnum
from functools import reduce


class VEndian(IntEnum):
    BIG = 0x0
    LITTLE = 0x1


class VObject(object):
    def vtype(self) -> str:
        name = type(self).__qualname__
        return name.replace("_T.", "_").replace(".", "_").lower()

    def __str__(self):
        return self.verilog()

    def __repr__(self):
        return str(self)

    def __le__(self, other) -> None:
        raise NotImplementedError()

    def width(self) -> int:
        raise NotImplementedError()

    def shape(self) -> tuple[int, ...]:
        raise NotImplementedError()

    def serialize(self, endian: VEndian = VEndian.BIG) -> list[int]:
        raise NotImplementedError()

    def verilog(self, inline: bool = False, indent: int = 0) -> str:
        raise NotImplementedError()
