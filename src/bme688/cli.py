from dataclasses import dataclass

try:
    import click
except ImportError:
    raise RuntimeError("Install with: pip install bme688[cli]")

import smbus2

from typed_registers import SMBusRegisterBus

from . import BME688


@dataclass
class CLIContext:
    device: BME688


pass_context = click.make_pass_decorator(CLIContext)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option()
@click.option("--bus", default=1, show_default=True, type=int)
@click.pass_context
def main(ctx: click.Context, bus: int) -> None:
    """BME688 CLI tool."""
    ctx.obj = CLIContext(
        device=BME688(SMBusRegisterBus(smbus2.SMBus(bus))),
    )


@main.command()
@pass_context
def init(ctx: CLIContext) -> None:
    ctx.device.initialize()


@main.command()
@pass_context
def read(ctx: CLIContext) -> None:
    reading = ctx.device.read()
    print(f"Temperature: {reading.temperature_c:.2f} °C")
    print(f"Pressure:    {reading.pressure_pa:.2f} Pa")
    print(f"Humidity:    {reading.humidity_rh:.2f} %RH")


@main.command()
@pass_context
def dump(ctx: CLIContext) -> None:
    print("BME688")
    print("  CALIB       ", ctx.device.calib)
    print("  CHIP_ID     ", ctx.device.chip_id)
    print("  CTRL_HUM    ", ctx.device.ctrl_hum)
    print("  CTRL_MEAS   ", ctx.device.ctrl_meas)
    print("  FIELD_DATA  ", ctx.device.field_data)
    print("  RESET       ", ctx.device.reset)
