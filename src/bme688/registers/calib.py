from typing import Self
from dataclasses import dataclass

from typed_registers import RegisterBus, BlockRegister


@dataclass(slots=True, frozen=True)
class REG_CALIB(BlockRegister):
    ADDRESS = 0x89
    WIDTH = 41

    par_t1: int
    par_t2: int
    par_t3: int

    par_p1: int
    par_p2: int
    par_p3: int
    par_p4: int
    par_p5: int
    par_p6: int
    par_p7: int
    par_p8: int
    par_p9: int
    par_p10: int

    par_h1: int
    par_h2: int
    par_h3: int
    par_h4: int
    par_h5: int
    par_h6: int
    par_h7: int

    @staticmethod
    def _u16(lsb: int, msb: int) -> int:
        return (msb << 8) | lsb

    @staticmethod
    def _s16(lsb: int, msb: int) -> int:
        v = (msb << 8) | lsb
        return v - 0x10000 if v & 0x8000 else v

    @staticmethod
    def _s8(v: int) -> int:
        return v - 0x100 if v & 0x80 else v

    @classmethod
    def _decode(cls, d: bytes) -> Self:
        # block1: 0x89..0xA1 => d[0]..d[24]
        # block2: 0xE1..0xF0 => d[25]..d[40]

        par_t1 = cls._u16(d[33], d[34])  # 0xE9 / 0xEA
        par_t2 = cls._s16(d[1], d[2])  # 0x8A / 0x8B
        par_t3 = cls._s8(d[3])  # 0x8C

        par_p1 = cls._u16(d[5], d[6])  # 0x8E / 0x8F
        par_p2 = cls._s16(d[7], d[8])  # 0x90 / 0x91
        par_p3 = cls._s8(d[9])  # 0x92
        par_p4 = cls._s16(d[11], d[12])  # 0x94 / 0x95
        par_p5 = cls._s16(d[13], d[14])  # 0x96 / 0x97
        par_p6 = cls._s8(d[16])  # 0x99
        par_p7 = cls._s8(d[15])  # 0x98
        par_p8 = cls._s16(d[19], d[20])  # 0x9C / 0x9D
        par_p9 = cls._s16(d[21], d[22])  # 0x9E / 0x9F
        par_p10 = d[23]  # 0xA0

        # Humidity bit packing from datasheet table 15
        par_h1 = (d[27] << 4) | (d[26] & 0x0F)  # 0xE3 / 0xE2<3:0>
        par_h2 = (d[25] << 4) | (d[26] >> 4)  # 0xE1 / 0xE2<7:4>
        par_h3 = cls._s8(d[28])  # 0xE4
        par_h4 = cls._s8(d[29])  # 0xE5
        par_h5 = cls._s8(d[30])  # 0xE6
        par_h6 = d[31]  # 0xE7
        par_h7 = cls._s8(d[32])  # 0xE8

        return cls(
            par_t1=par_t1,
            par_t2=par_t2,
            par_t3=par_t3,
            par_p1=par_p1,
            par_p2=par_p2,
            par_p3=par_p3,
            par_p4=par_p4,
            par_p5=par_p5,
            par_p6=par_p6,
            par_p7=par_p7,
            par_p8=par_p8,
            par_p9=par_p9,
            par_p10=par_p10,
            par_h1=par_h1,
            par_h2=par_h2,
            par_h3=par_h3,
            par_h4=par_h4,
            par_h5=par_h5,
            par_h6=par_h6,
            par_h7=par_h7,
        )

    @classmethod
    def read(cls, bus: RegisterBus, addr: int) -> Self:
        block1 = bus.read(addr, 0x89, 25)
        block2 = bus.read(addr, 0xE1, 16)
        return cls.from_bytes(bytes(block1 + block2))
