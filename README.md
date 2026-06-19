# Thesis Power Controller

STM32G071 Arduino firmware for an isolated converter controller.

## Current Firmware

| Item | Value |
|---|---|
| Firmware | `PWR-1.9.9` |
| MCU target | STM32G071 Nucleo-64 style board |
| Gate carrier | PA8 / PA9, fixed 1 MHz |
| Power throttle | PA10 EN burst control |
| Feedback | DMA ADC on PA0, PA1, PA2 |
| Active control | PA1 secondary-voltage bang-bang |
| Optional high-line aid | PA0 primary-voltage feed-forward duty cap |
| Command UART | PC5 RX, PC4 TX, 115200 baud |

`PWR-1.9.9` keeps the control loop bang-bang only. PA1 secondary voltage decides when EN goes high or low. Optional `LINEFF` uses PA0 only to reduce the high EN duty as primary voltage rises, so a tune made near 110 Vac can be used more safely at 220 Vac.

## Quick Bench Setup

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

Optional high-line feed-forward after tuning at low line:

```text
LINEFF
LFFCAL
SAVE
```

Return to secondary-voltage-only bang-bang:

```text
VSBONLY
```

## Repository Layout

| Path | Purpose |
|---|---|
| [thesi_power_control.ino](thesi_power_control.ino) | Current working firmware source |
| [docs/power-control.md](docs/power-control.md) | Full firmware manual, version notes, limits, and tuning commands |
| [docs/uart-commands.md](docs/uart-commands.md) | Compact UART command reference |
| [firmware/archive/snapshots](firmware/archive/snapshots) | Historical source snapshots |
| [firmware/compile-sketches](firmware/compile-sketches) | Older Arduino wrapper sketches kept for reference |

## Build

Build with Arduino CLI and the STM32 core. Arduino expects the `.ino` file to live in a sketch folder with the same name, so create a temporary wrapper folder first:

```powershell
New-Item -ItemType Directory -Path .\build-sketch\thesi_power_control -Force
Copy-Item .\thesi_power_control.ino .\build-sketch\thesi_power_control\thesi_power_control.ino -Force
arduino-cli compile --clean --fqbn "STMicroelectronics:stm32:Nucleo_64:pnum=NUCLEO_G071RB" .\build-sketch\thesi_power_control
```

Compiled `.hex`, `.bin`, and `.elf` files are intentionally not committed to the repo. Published binary builds live on the [GitHub Releases page](https://github.com/kform-danish-office/Thesis/releases).

Flash a release or local build with STM32CubeProgrammer:

```powershell
STM32_Programmer_CLI.exe -c port=SWD -w firmware.hex -v -rst
```

## Notes

- ADC feedback is DMA-only; the control loop does not call blocking `analogRead()`.
- EEPROM writes are deferred while the output is active so UART setting changes do not stall live control.
- Current/power readings are diagnostic in the active firmware; voltage bang-bang control is the only closed-loop control path.
