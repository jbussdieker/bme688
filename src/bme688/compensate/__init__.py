from dataclasses import dataclass

from ..registers import REG_CALIB


@dataclass(frozen=True)
class TemperatureResult:
    celsius: float
    t_fine: int


def temperature(raw: int, calib: REG_CALIB) -> TemperatureResult:
    var1 = (raw >> 3) - (calib.par_t1 << 1)
    var2 = (var1 * calib.par_t2) >> 11
    var3 = ((((var1 >> 1) * (var1 >> 1)) >> 12) * (calib.par_t3 << 4)) >> 14
    t_fine = var2 + var3
    temp_c = ((t_fine * 5) + 128) >> 8
    return TemperatureResult(temp_c / 100.0, t_fine)


def pressure(raw: int, calib: REG_CALIB, t_fine: int) -> float:
    pres_ovf_check = 0x40000000

    var1 = (t_fine >> 1) - 64000
    var2 = ((((var1 >> 2) * (var1 >> 2)) >> 11) * calib.par_p6) >> 2
    var2 = var2 + ((var1 * calib.par_p5) << 1)
    var2 = (var2 >> 2) + (calib.par_p4 << 16)

    var1 = (((((var1 >> 2) * (var1 >> 2)) >> 13) * (calib.par_p3 << 5)) >> 3) + (
        (calib.par_p2 * var1) >> 1
    )
    var1 = var1 >> 18
    var1 = ((32768 + var1) * calib.par_p1) >> 15

    if var1 == 0:
        raise ZeroDivisionError(
            "Invalid pressure calibration: par_p1 produced division by zero"
        )

    pressure_comp = 1048576 - raw
    pressure_comp = int((pressure_comp - (var2 >> 12)) * 3125)

    if pressure_comp >= pres_ovf_check:
        pressure_comp = (pressure_comp // var1) << 1
    else:
        pressure_comp = (pressure_comp << 1) // var1

    var1 = (calib.par_p9 * (((pressure_comp >> 3) * (pressure_comp >> 3)) >> 13)) >> 12
    var2 = ((pressure_comp >> 2) * calib.par_p8) >> 13
    var3 = (
        (pressure_comp >> 8)
        * (pressure_comp >> 8)
        * (pressure_comp >> 8)
        * calib.par_p10
    ) >> 17

    pressure_comp = pressure_comp + ((var1 + var2 + var3 + (calib.par_p7 << 7)) >> 4)
    return float(pressure_comp)  # Pa


def humidity(raw: int, calib: REG_CALIB, t_fine: int) -> float:
    temp_scaled = ((t_fine * 5) + 128) >> 8

    var1 = raw - (calib.par_h1 << 4) - (((temp_scaled * calib.par_h3) // 100) >> 1)
    var2 = (
        calib.par_h2
        * (
            ((temp_scaled * calib.par_h4) // 100)
            + ((((temp_scaled * ((temp_scaled * calib.par_h5) // 100)) >> 6) // 100))
            + (1 << 14)
        )
    ) >> 10
    var3 = var1 * var2
    var4 = ((calib.par_h6 << 7) + ((temp_scaled * calib.par_h7) // 100)) >> 4
    var5 = ((var3 >> 14) * (var3 >> 14)) >> 10
    var6 = (var4 * var5) >> 1

    calc_hum = (((var3 + var6) >> 10) * 1000) >> 12

    if calc_hum > 100000:
        calc_hum = 100000
    elif calc_hum < 0:
        calc_hum = 0

    return calc_hum / 1000.0  # %RH
