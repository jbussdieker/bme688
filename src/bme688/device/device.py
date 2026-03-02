import time
from dataclasses import dataclass, replace

from typed_registers import RegisterBus

from .reading import Reading
from . import control
from .. import compensate
from .. import registers


class BME688:
    def __init__(self, bus: RegisterBus, addr: int = 0x77):
        self.bus = bus
        self.addr = addr
        self._calib: registers.REG_CALIB | None = None

    @property
    def calib(self) -> registers.REG_CALIB:
        if self._calib is None:
            self._calib = registers.REG_CALIB.read(self.bus, self.addr)
        return self._calib

    @property
    def chip_id(self) -> registers.REG_CHIP_ID:
        return registers.REG_CHIP_ID.read(self.bus, self.addr)

    @property
    def ctrl_hum(self) -> registers.REG_CTRL_HUM:
        return registers.REG_CTRL_HUM.read(self.bus, self.addr)

    @property
    def ctrl_meas(self) -> registers.REG_CTRL_MEAS:
        return registers.REG_CTRL_MEAS.read(self.bus, self.addr)

    @property
    def field_data(self) -> registers.REG_FIELD_DATA:
        return registers.REG_FIELD_DATA.read(self.bus, self.addr)

    @property
    def reset(self) -> registers.REG_RESET:
        return registers.REG_RESET.read(self.bus, self.addr)

    def initialize(self) -> None:
        control._soft_reset(self.bus, self.addr)
        control._set_defaults(self.bus, self.addr)
        self._calib = registers.REG_CALIB.read(self.bus, self.addr)

    def trigger_measurement(self) -> None:
        replace(self.ctrl_meas, mode=1).write(self.bus, self.addr)

    def read_field_data(
        self,
        *,
        timeout: float = 1.0,
        poll_interval: float = 0.005,
    ) -> registers.REG_FIELD_DATA:
        deadline = time.monotonic() + timeout

        while True:
            field = self.field_data
            if field.new_data:
                return field

            if time.monotonic() >= deadline:
                raise TimeoutError("Timed out waiting for BME688 new data")

            time.sleep(poll_interval)

    def read(self) -> Reading:
        self.trigger_measurement()
        field = self.read_field_data()

        temp = compensate.temperature(field.temperature_adc, self.calib)
        press = compensate.pressure(field.pressure_adc, self.calib, temp.t_fine)
        hum = compensate.humidity(field.humidity_adc, self.calib, temp.t_fine)

        return Reading(
            temperature_c=temp.celsius,
            pressure_pa=press,
            humidity_rh=hum,
        )
