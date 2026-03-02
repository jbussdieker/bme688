# BME688

**bme688** is a **typed, register-accurate Python driver** for the Bosch BME688 environmental sensor.

It provides temperature, pressure, and humidity readings using a clean, explicit register model built on top of typed-registers.

The goal is to make working with the sensor:

* **transparent** (registers are first-class)
* **typed** (dataclasses, no raw byte juggling)
* **predictable** (no hidden state or magic)

## Features

* ✅ Typed register definitions (dataclasses)
* ✅ Accurate Bosch compensation algorithms
* ✅ Temperature, pressure, and humidity readings
* ✅ Forced-mode measurement with polling
* ✅ Clean separation of:

  * register layer
  * device behavior
  * compensation math
* ✅ CLI for quick testing

## Installation

```bash
pip install bme688[i2c,cli]
```

## Requirements

* Python ≥ 3.11
* I²C enabled (e.g. Raspberry Pi)
* `smbus2`

## Quick Start

```python
from smbus2 import SMBus
from typed_registers import SMBusRegisterBus
from bme688 import BME688

bus = SMBusRegisterBus(SMBus(1))
sensor = BME688(bus)

sensor.initialize()

reading = sensor.read()

print(reading)
```

Example output:

```
Reading(
    temperature_c=23.46,
    pressure_pa=101021.0,
    humidity_rh=41.46
)
```

## CLI Usage

Initialize the device:

```bash
bme688 init
```

Read sensor values:

```bash
bme688 read
```

Example:

```
Temperature: 23.46 °C
Pressure:    101021.00 Pa
Humidity:    41.46 %RH
```

Dump raw register state:

```bash
bme688 dump
```

## Architecture

The driver is intentionally structured in layers:

```
Device API
    ↓
Compensation (Bosch algorithms)
    ↓
Typed Registers
    ↓
typed-registers
    ↓
Bus (I²C / SMBus / etc.)
```

### Registers

Each hardware register is modeled as a typed dataclass:

```python
REG_CTRL_MEAS(osrs_t=1, osrs_p=1, mode=0)
```

Multi-byte registers use structured decoding:

```python
REG_FIELD_DATA(
    new_data=True,
    temperature_adc=...,
    pressure_adc=...,
    humidity_adc=...
)
```

## Design Philosophy

This driver follows a simple rule:

> The register map *is* the API.

* No hidden abstractions
* No implicit conversions
* No “magic” state

Everything maps directly to the datasheet.

## Status

**Alpha**

* Temperature, pressure, humidity: ✅ stable
* Gas resistance: ⚠️ partial (raw values available, full pipeline not implemented)

## Development

```bash
pip install -e .[dev]
mypy src/
```

## License

MIT License

## Author

**Joshua B. Bussdieker**
[https://github.com/jbussdieker](https://github.com/jbussdieker)
