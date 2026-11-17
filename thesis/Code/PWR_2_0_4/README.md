# Thesis Power Controller

STM32F410CBU6 and STM32G071 Arduino firmware for an isolated converter controller.

## Current Firmware

| Item | Value |
|---|---|
| Firmware | F410: `PWR-2.0.4` carrier-timing candidate; G071: `PWR-2.0.3` (powered bench validation pending) |
| MCU targets | STM32F410CBU6 (schematic 12) and original STM32G071 |
| Gate carrier | F410: PA8 / PB13, complementary TIM1 CH1/CH1N, OFF-only adjustable carrier/deadtime; G071: PA8 / PA9, fixed 1 MHz |
| Power throttle | F410: PA11 EN; G071: PA10 EN |
| Feedback | DMA ADC on PA0, PA1, PA2 |
| Active control | PA1 secondary-voltage bang-bang |
| Optional high-line aid | PA0 primary-voltage feed-forward duty cap |
| Command UART | F410: PA10 RX, PA9 TX; G071: PC5 RX, PC4 TX; 115200 baud |

`PWR-2.0.0` ports the existing controller to the new schematic. PA1 remains the closed-loop signal. At light load it uses voltage bang-bang with the no-load guard; once PA2 classifies a real load, `LSTEADY` retains and slowly trims an averaged EN duty instead of chopping between 0 and 100 percent. Droop below `VON` activates `LBOOST`, while high voltage still cuts EN immediately. Non-static EN edges use bounded polling of the TIM1 carrier. Optional `LINEFF` uses PA0 as a high-line duty cap.

See [STM32F410 port and pinout](docs/stm32f410-port.md) before using the new board. The PDF contains unresolved sense-divider population values; the port retains the earlier calibrated divider assumptions.

## Browser Control and Experiment Logging

The [Power Lab app](https://thesis-power-lab.vercel.app) provides live USB-UART
telemetry, converter controls, local experiment sessions, and CSV/JSON downloads.
Open it in desktop Chrome or Edge. USB connects through an isolated 3.3 V UART
interface to the existing command pins; it does not require a cloud USB bridge.

`PWR-2.0.1` adds structured telemetry, command acknowledgements, and an explicit
communication lease that disables output when renewals stop. Flash the new
firmware for your board before connecting. Read the [web protocol and wiring
notes](docs/web-protocol.md) before connecting the app.

`PWR-2.0.2` adds cooperative, capability-gated hardware calibration over the web
protocol. See [calibration build notes](firmware/releases/pwr-2.0.2.md). No board
has been flashed or powered as part of this software validation. Existing
`PWR-2.0.1` boards retain ordinary monitoring/control but cannot run web calibration.

`PWR-2.0.3` adds reported load-reference resistances, reference-slot selection,
no-load duty, calibration scan and startup precharge settings. These controls
require the `bench_settings_v1` capability and output OFF. Applying changes updates
RAM; **Save to device** explicitly persists them. Resistance fields describe the
physical reference loads and do not change or switch a resistor/electronic load.
A selected slot does not establish that its calibration is valid. See
[bench-settings build notes](firmware/releases/pwr-2.0.3.md).

`PWR-2.0.4` adds V2 / F410-only switching-carrier and deadtime control through
`carrier_timing_v1`. With output OFF and startup/calibration idle, `TIMING <Hz> <ns>`
applies both values atomically. Requests accept whole numbers from 500000–2000000 Hz
and 20–200 ns; the timer quantizes them and rejects incompatible pairs. The default
remains 1 MHz / 40 ns, but the carrier now uses edge-aligned timing. These are timer
bounds, not an electrically validated operating range. Natural LC resonance is
set by hardware; `FEN` controls the separate EN burst frequency.

Setup's collapsed **V2 switching/carrier timing** section shows requested values,
a draft preview and verified actual readback. A change to actual timing clears
learned load profiles and tuned calibration metadata while retaining physical
load resistances; retune explicitly. Web changes stay in RAM until **Save to
device** with output OFF. See the [pre-release notes](firmware/releases/pwr-2.0.4.md)
for timing quantization, journal migration, downgrade limits and required scope
checks. G071 retains its fixed carrier and `PWR-2.0.3` behavior.

The app separates **Monitor**, **Setup**, **Calibration**, and **Sessions** to keep
live measurements clear. USB connection and recording continue between views;
Output OFF remains available throughout. The calculator opens in a separate tab.

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
SET NLSOVPEN 1
SET NLSOVP 33.5
SET NLSOVPR 23
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

Copy a known-good calibration to another board:

```text
EXPORT
```

## Repository Layout

| Path | Purpose |
|---|---|
| [thesi_power_control.ino](thesi_power_control.ino) | Current working firmware source |
| [docs/firmware-flow.md](docs/firmware-flow.md) | Mermaid diagrams of firmware startup, control, safety, and EN timing |
| [docs/power-control.md](docs/power-control.md) | Full firmware manual, version notes, limits, and tuning commands |
| [docs/uart-commands.md](docs/uart-commands.md) | Compact UART command reference |
| [firmware/archive/snapshots](firmware/archive/snapshots) | Historical source snapshots |
| [firmware/compile-sketches](firmware/compile-sketches) | Older Arduino wrapper sketches kept for reference |

## Build

Build with Arduino CLI and STM32 core 2.8.1. The script creates the matching sketch folder and applies the F410 linker layout that protects saved settings:

```powershell
.\firmware\build.ps1 -Target F410
.\firmware\build.ps1 -Target G071
```

Outputs are in `arduino-build-f410/` or `arduino-build-g071/`. For F410, use the `.hex` file: it includes both reset vectors and application code while leaving the settings sector out of its address records. A raw `.bin` spans the settings gap and can erase saved settings. Do not build the F410 using the stock linker script.

Compiled `.hex`, `.bin`, and `.elf` files are intentionally not committed to the
repo. Historical published builds live on the [GitHub Releases page](https://github.com/kform-danish-office/Thesis/releases).
The V2 / F410 `PWR-2.0.4` firmware is available as a [GitHub pre-release](https://github.com/kform-danish-office/Thesis/releases/tag/pwr-2.0.4).
Software checks pass; powered bench validation remains pending and no board was
flashed during cloud validation. Use its attached V2 source snapshot for this
version; GitHub’s automatic source archives contain the older repository baseline.

Flash a release or local build with STM32CubeProgrammer:

```powershell
STM32_Programmer_CLI.exe -c port=SWD -w firmware.hex -v -rst
```

## Notes

- ADC feedback is DMA-only; the control loop does not call blocking `analogRead()`.
- EEPROM writes are deferred while the output is active so UART setting changes do not stall live control.
- Current/power readings are diagnostic in the active firmware; voltage bang-bang control is the only closed-loop control path.
- Non-static EN burst edges use TIM1 carrier-update polling; static 100 percent EN remains continuously high.
- At high-line light load, `NLSOVP` is a soft holdoff. Hard `OVP` still latches if voltage rises past the hard margin or the load is not light/no-load.
