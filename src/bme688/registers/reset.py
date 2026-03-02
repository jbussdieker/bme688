from dataclasses import dataclass
from typing import Self

from typed_registers import ByteRegister


@dataclass(slots=True, frozen=True)
class REG_RESET(ByteRegister):
    ADDRESS = 0xE0

    value: int = 0x00

    def to_byte(self) -> int:
        return self.value & 0xFF

    @classmethod
    def from_byte(cls, b: int) -> Self:
        return cls(value=b)
