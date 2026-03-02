from dataclasses import dataclass
from typing import Self

from typed_registers import ByteRegister


@dataclass(slots=True, frozen=True)
class REG_CTRL_MEAS(ByteRegister):
    ADDRESS = 0x74

    osrs_t: int = 0
    osrs_p: int = 0
    mode: int = 0

    def __post_init__(self) -> None:
        if not 0 <= self.osrs_t <= 5:
            raise ValueError("osrs_t out of range")
        if not 0 <= self.osrs_p <= 5:
            raise ValueError("osrs_p out of range")
        if not 0 <= self.mode <= 3:
            raise ValueError("mode out of range")

    def to_byte(self) -> int:
        return (self.osrs_t << 5) | (self.osrs_p << 2) | self.mode

    @classmethod
    def from_byte(cls, b: int) -> Self:
        return cls(
            osrs_t=(b >> 5) & 0b111,
            osrs_p=(b >> 2) & 0b111,
            mode=b & 0b11,
        )
