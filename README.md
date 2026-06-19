# Thesis Power Controller

STM32G071 Arduino firmware for the thesis isolated converter controller.

Latest firmware: `PWR-1.9.9`

## What This Firmware Does

- Drives PA8 / PA9 as the fixed 1 MHz half-bridge gate carrier.
- Uses PA10 as the EN burst throttle.
- Uses DMA-only ADC feedback on PA0, PA1, and PA2.
- Controls from PA1 secondary voltage in voltage bang-bang mode.
- Optionally caps bang-bang high duty from PA0 primary voltage feed-forward for high-line use.
- Keeps low-load/high-impedance operation in a softer 23 V to 28 V window by default.
- Uses calibrated load slots as reference points, not rigid modes.
- Lets lower-resistance loads demand full `DMAX` instead of getting stuck at the no-load cap.

## Current Build

`PWR-1.9.9` adds optional PA0 line feed-forward while keeping bang-bang control:

- PA1 secondary voltage still decides high/low.
- `LINEFF` uses PA0 only to cap the high EN duty as primary voltage rises.
- `LFFCAL` stores the current PA0 reading as the tuned low-line reference.
- `VSBONLY` disables PA0 influence and returns to secondary-only bang-bang.
- `MAXRATE` requests the fastest supported 20 us control loop preset.

## Quick Bench Commands

```text
VER
FULL
MAXRATE
SET VSET 28
SET VON 28
SET VMAX 32
SET OVP 36
SET NLDROP 5
SET NLSLOT 1
VSBONLY
SAVE
STATUS
```

Optional 110 Vac to 220 Vac high-line feed-forward:

```text
LINEFF
LFFCAL
SAVE
```

## Documentation

- [Power controller README](POWER_CONTROL_README.md)
- [UART command README](UART_COMMANDS_README.md)

## Firmware Releases

Compiled firmware artifacts are attached to GitHub releases.

Latest release: `pwr-1.9.8`

Older quick-switch firmware builds are available on the [Releases page](https://github.com/kform-danish-office/Thesis/releases), including `pwr-1.4.0` through `pwr-1.9.8` where compiled local artifacts exist.

Expected release assets:

- `pwr-1.9.8-stm32g071-nucleo64.hex`
- `pwr-1.9.8-stm32g071-nucleo64.bin`
- `pwr-1.9.8-stm32g071-nucleo64.elf`
- `pwr-1.9.8-sha256.txt`

Flash with STM32CubeProgrammer over ST-Link:

```powershell
STM32_Programmer_CLI.exe -c port=SWD -w pwr-1.9.8-stm32g071-nucleo64.hex -v -rst
```

## Main Source Files

- `thesi_power_control.ino` is the current working firmware source.
- `thesi_closed_loop_PWR_1_9_9.ino` is the archived source snapshot for `PWR-1.9.9`.
- Older `thesi_closed_loop_PWR_*` files are historical firmware snapshots.
