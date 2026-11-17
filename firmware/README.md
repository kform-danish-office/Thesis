# Firmware Files

The active firmware is kept at the repository root:

- [../thesi_power_control.ino](../thesi_power_control.ino)

The current V2 / F410 candidate is `PWR-2.0.4`, adding `carrier_timing_v1` for an
atomic output-OFF switching-carrier/deadtime pair. `TIMING <Hz> <ns>` accepts whole
numbers from 500000–2000000 Hz and 20–200 ns, subject to timer quantization and
pair constraints. The default remains 1 MHz / 40 ns; TIM1 now uses edge-aligned
complementary CH1/CH1N. Timer limits are not an electrically validated operating
range. G071 remains `PWR-2.0.3` with its fixed carrier. See
[PWR-2.0.4 pre-release notes](releases/pwr-2.0.4.md).
Download the V2 HEX and matching source snapshot from the
[GitHub pre-release](https://github.com/kform-danish-office/Thesis/releases/tag/pwr-2.0.4); the automatic Source code archives
use the older repository baseline.

An effective timing change clears all three learned load profiles and tuned
metadata, retaining physical load-reference resistances and sensor calibration.
Retune explicitly. Web edits remain in RAM until SAVE while OFF. Before
`WEB HELLO`, legacy terminal edits retain the existing auto-save after 1.5 s
quiet while OFF, unless `BEGINCFG` holds an import; SAVE/ENDCFG also persists.
Timing and calibration are stored together in a new F410 488-byte journal
wrapper. Legacy records load without boot-time writes; older firmware cannot
read the new wrapper. Review migration/downgrade notes before flashing.

Both targets retain capability-gated load-reference, reference-slot, no-load
duty, calibration-scan and startup-precharge settings from
[PWR-2.0.3](releases/pwr-2.0.3.md). Setting resistance or selecting a slot does
not switch a physical load or prove calibration validity. The F410 candidate is
software-validated; powered bench validation and physical flashing remain pending.

Web calibration remains available through `calibration_v1`, introduced in
[PWR-2.0.2](releases/pwr-2.0.2.md), with cooperative stop/lease handling and
pending-save results. Earlier PWR-2.0.2 boards can still use calibration, but need
PWR-2.0.3 for the new `bench_settings_v1` settings controls.

`PWR-2.0.1` originally added the opt-in web control/logging protocol over the existing
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
| [test_web_protocol.py](test_web_protocol.py) | Native tests of production protocol, timing math/application, scheduler and watchdog; GCC/Clang or Visual Studio C++ Build Tools |
| [test_carrier_storage.py](test_carrier_storage.py) | Production F410 journal migration, corruption and interrupted-append tests with mocked HAL flash |

Current development should happen in [../thesi_power_control.ino](../thesi_power_control.ino).

For the new board, run `./firmware/build.ps1 -Target F410` from the repository root.
Read [the F410 port notes](../docs/stm32f410-port.md) for the schematic pin map,
sense-divider discrepancy, flash layout, and first-start commands.

Cloud validation ran `python3 /workspace/tooling/test-working-protocol-linux.py`
against the repository's production protocol harness and
`python3 firmware/test_carrier_storage.py` without hardware. These passed
131 JSON protocol frames and all 122 interrupted-append word boundaries.
The protocol runner also has a Windows Visual Studio build path; Windows
execution was not tested in this environment.
The F410 build uses 90,268/98,304 bytes of program and 6,868/32,768 bytes of RAM;
unchanged G071 uses 130,424/131,072 and 9,544/32,768 bytes respectively (648 bytes
of program headroom). Physical USB, gate/EN waveforms, stop latency, sensing
accuracy and on-board flash writes still require bench verification.
