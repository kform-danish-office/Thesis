# Firmware Files

The active firmware is kept at the repository root:

- [../thesi_power_control.ino](../thesi_power_control.ino)

`PWR-2.0.1` adds the opt-in web control/logging protocol over the existing
115200-baud UART. Read [the browser protocol](../docs/web-protocol.md) for the
USB-UART connection, correlated commands, telemetry, and link-lease shutdown.
Download board-specific HEX files from [GitHub Releases](https://github.com/kform-danish-office/Thesis/releases/tag/pwr-2.0.1).
See [PWR-2.0.1 release notes](releases/pwr-2.0.1.md) for validation and flashing.

Supporting firmware folders:

| Path | Purpose |
|---|---|
| [archive/snapshots](archive/snapshots) | Historical `.ino` source snapshots by firmware version |
| [archive/legacy-autofull](archive/legacy-autofull) | Early voltage/autofull experiment kept for traceability |
| [compile-sketches](compile-sketches) | Older Arduino wrapper sketches kept for reference |
| [build.ps1](build.ps1) | Builds the current source for F410CBU6 or G071 |
| [stm32f410.ld](stm32f410.ld) | F410 memory layout: reset vectors, reserved settings sector, application |
| [test_web_protocol.py](test_web_protocol.py) | Native host tests of production web command, telemetry, and watchdog code; requires Visual Studio C++ Build Tools |

Current development should happen in [../thesi_power_control.ino](../thesi_power_control.ino).

For the new board, run `./firmware/build.ps1 -Target F410` from the repository root.
Read [the F410 port notes](../docs/stm32f410-port.md) for the schematic pin map,
sense-divider discrepancy, flash layout, and first-start commands.

Run `python firmware/test_web_protocol.py` to exercise the web protocol without
hardware. These tests use mocked UART/control dependencies; physical USB, EN
timing, fault detection, populated sensing values, and actual flash writes still
require bench verification.
