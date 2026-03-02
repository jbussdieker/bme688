from dataclasses import dataclass


@dataclass(frozen=True)
class Reading:
    temperature_c: float
    pressure_pa: float
    humidity_rh: float
