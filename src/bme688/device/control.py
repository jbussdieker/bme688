import time

from typed_registers import RegisterBus
from ..registers import (
    REG_CTRL_HUM,
    REG_CTRL_MEAS,
    REG_RESET,
)

RESET_COMMAND = 0xB6


def _soft_reset(bus: RegisterBus, addr: int) -> None:
    """
    Perform BME688 soft reset.

    Datasheet:
        Write 0xB6 to register 0xE0.
    """

    REG_RESET(RESET_COMMAND).write(bus, addr)

    # Datasheet minimum ≈2 ms
    # Give hardware time to reload calibration + state
    time.sleep(0.01)


def _set_defaults(bus: RegisterBus, addr: int) -> None:
    """
    Apply sane driver defaults after reset.

    Defaults chosen:
        humidity oversampling  = x1
        temperature oversampling = x1
        pressure oversampling = x1
        mode = sleep (0)
    """

    # Humidity must be written BEFORE ctrl_meas
    # (Bosch ordering requirement)
    ctrl_hum = REG_CTRL_HUM(osrs_h=1)
    ctrl_hum.write(bus, addr)

    ctrl_meas = REG_CTRL_MEAS(
        osrs_t=1,
        osrs_p=1,
        mode=0,  # sleep
    )
    ctrl_meas.write(bus, addr)
