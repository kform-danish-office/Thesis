# PWR-2.0.1 — Browser control and logging

Release date: October 24, 2026.

This firmware adds the opt-in browser protocol used by the
[Converter test bench](https://thesis-power-lab.vercel.app) to the existing
STM32F410CBU6 and STM32G071 controller. It retains the PWR-2.0.0 board port and
control behavior.

## Changes

- Structured JSON telemetry, firmware identification, correlated command
  acknowledgments, and explicit command rejection over the existing UART.
- Fixed-size transmit queues and bounded writes to avoid blocking the control
  loop on normal telemetry transmission.
- An explicitly armed communication lease disables output when renewals stop;
  the browser app normally requests five seconds. Opening the app or entering
  `WEB HELLO` does not automatically enable output or apply settings.
- Explicit SAVE with output OFF persists settings. The original terminal
  workflow remains available before a web session; reset exits that session.
  Plain OFF is still accepted during the web session.
- A native host harness exercises the production protocol functions without
  opening hardware or flashing a board.

Read the [protocol and wiring instructions](../../docs/web-protocol.md).
USB communication requires an appropriately isolated 3.3 V USB-to-UART adapter
at 115200 baud, 8N1. These builds do not provide native USB CDC.

## Downloads and flashing

| Download | Board |
| --- | --- |
| `pwr-2.0.1-stm32f410cbu6.hex` | New STM32F410CBU6 schematic-12 board |
| `pwr-2.0.1-stm32g071-nucleo64.hex` | Original STM32G071 / NUCLEO_G071RB build target |
| `pwr-2.0.1-firmware.zip` | Both HEX images, debugging ELF files, selected source, build tools, and documentation |
| `pwr-2.0.1-build.json` | Source commit, target configurations, verification results, and file hashes |
| `pwr-2.0.1-SHA256SUMS.txt` | Checksums of the downloadable release files |

Choose the HEX for the actual board. The F410 uses a custom linker: reset
vectors are at 0x08000000, settings occupy 0x08004000–0x08007FFF, and application
code starts at 0x08008000. Its release HEX excludes the settings sector. Use
HEX and avoid full-chip erase to retain settings. No F410 raw BIN is supplied
because it spans the reserved address gap.

With STM32CubeProgrammer and the correct board connected over SWD:

```powershell
STM32_Programmer_CLI.exe -c port=SWD -w pwr-2.0.1-stm32f410cbu6.hex -v -rst
```

For the original G071 board, substitute its HEX filename. See the
[F410 port notes](../../docs/stm32f410-port.md) for pin assignments, sensor
population assumptions, and first-start verification.

## Verification

Fresh builds used Arduino CLI 1.5.0 and STM32 Arduino core 2.8.1.

| Target | Program storage | Static RAM |
| --- | --- | --- |
| STM32F410CBU6 | 85,184 / 98,304 bytes | 6,820 / 32,768 bytes |
| STM32G071 | 127,340 / 131,072 bytes | 9,524 / 32,768 bytes |

- Both build images contain `PWR-2.0.1` and match the current firmware source.
- Both HEX images passed record checksums, boot-vector, and flash-range checks.
  The F410 additionally passed the dedicated settings-sector exclusion check.
- The production-protocol host harness passed with 46 JSON frames, covering
  malformed input, acknowledgments and rejections, failed saves, enable
  interlocks, lease expiry and timer wrap, congestion, null telemetry, and
  bounded UART writes.

These checks do not validate electrical operation, USB adapter behavior,
control-loop timing, runtime stack/heap use, or flash writes on a physical
board. G071 has 3,732 bytes of reported program storage remaining. Verify the
actual divider population and voltage scaling before enabling power; current
and power telemetry remain diagnostics rather than calibrated output readings.
The communication lease is serviced by the main loop, not an independent
hardware watchdog. Existing saved BOOTON settings remain effective after a
firmware update; the default OFF state does not override saved settings.

## Rebuild

From the source checkout with the installed STM32 core:

```powershell
.\firmware\build.ps1 -Target F410
.\firmware\build.ps1 -Target G071
python firmware/test_web_protocol.py
python firmware/verify_f410_hex.py arduino-build-f410/thesi_power_control.ino.hex
```

The host protocol test requires Visual Studio C++ Build Tools on Windows.
