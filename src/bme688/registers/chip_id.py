from dataclasses import dataclass
from typing import Self

from typed_registers import ByteRegister


@dataclass(slots=True, frozen=True)
class REG_CHIP_ID(ByteRegister):
    ADDRESS = 0xD0
    value: int = 0

    def to_byte(self) -> int:
        return self.value & 0xFF

    @classmethod
    def from_byte(cls, b: int) -> Self:
        return cls(value=b)
