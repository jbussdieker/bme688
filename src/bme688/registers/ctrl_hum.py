from dataclasses import dataclass
from typing import Self

from typed_registers import ByteRegister


@dataclass(slots=True, frozen=True)
class REG_CTRL_HUM(ByteRegister):
    ADDRESS = 0x72
    osrs_h: int = 0

    def __post_init__(self) -> None:
        if not 0 <= self.osrs_h <= 5:
            raise ValueError("osrs_h out of range")

    def to_byte(self) -> int:
        return self.osrs_h & 0b111

    @classmethod
    def from_byte(cls, b: int) -> Self:
        return cls(osrs_h=b & 0b111)
