from typing import Self
from dataclasses import dataclass

from typed_registers import BlockRegister


@dataclass(slots=True, frozen=True)
class REG_FIELD_DATA(BlockRegister):
    ADDRESS = 0x1D
    WIDTH = 17

    new_data: bool
    gas_measuring: bool
    measuring: bool
    res: int
    gas_meas_index: int
    sub_meas_index: int

    temperature_adc: int
    pressure_adc: int
    humidity_adc: int
    gas_adc: int
    gas_range: int

    @classmethod
    def _decode(cls, d: bytes) -> Self:
        meas_status = d[0]

        press = (d[2] << 12) | (d[3] << 4) | (d[4] >> 4)
        temp = (d[5] << 12) | (d[6] << 4) | (d[7] >> 4)
        hum = (d[8] << 8) | d[9]
        gas_adc = (d[15] << 2) | (d[16] >> 6)
        gas_range = d[16] & 0x0F

        return cls(
            new_data=bool(meas_status & 0x80),
            gas_measuring=bool(meas_status & 0x40),
            measuring=bool(meas_status & 0x20),
            res=(meas_status >> 4) & 0x01,
            gas_meas_index=meas_status & 0x0F,
            sub_meas_index=d[1],
            temperature_adc=temp,
            pressure_adc=press,
            humidity_adc=hum,
            gas_adc=gas_adc,
            gas_range=gas_range,
        )
