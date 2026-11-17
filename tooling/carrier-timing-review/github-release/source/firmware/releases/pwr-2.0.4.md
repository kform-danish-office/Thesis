# PWR-2.0.4 — V2 carrier timing candidate

Software-validated V2/F410 pre-release; powered bench validation pending.
No board was flashed or powered during cloud validation. G071 remains PWR-2.0.3 with its fixed carrier and existing
settings format; the candidate firmware package is F410-only.

V2 / STM32F410 advertises `carrier_timing_v1` alongside `calibration_v1` and
`bench_settings_v1`. With output OFF and startup/autotune/calibration idle,
`TIMING <Hz> <ns>` applies the switching carrier and complementary-gate deadtime
as one atomic pair while EN stays low. The browser exposes this in the collapsed
**Setup → V2 switching/carrier timing** section, showing a draft preview separately
from verified actual device readback. A firmware/browser version string alone
does not grant support; capability and fresh readback are required.

## Timing and calibration

- Requests are unsigned decimal integers: 500000–2000000 Hz and 20–200 ns.
  These are timer bounds, not an electrically validated operating range.
- TIM1 uses prescaler 0 and even edge-aligned period ticks for balanced CH1/CH1N
  reference pulses. Frequency selects the nearest two-tick period; deadtime
  rounds up to a timer tick using linear DTG encoding.
- The actual pair must satisfy `4 * dead_ticks < period_ticks`. At 100 MHz,
  2 MHz / 120 ns is accepted; 2 MHz / 130 ns is rejected. Not every combination
  within the individual ranges is valid.
- At 100 MHz, requesting 950000 Hz / 53 ns produces 106 period ticks and
  6 deadtime ticks: exact frequency 100000000/106 Hz, reported 943396 Hz / 60 ns.
  EN scheduling uses the actual clock/period rather than rounded readback Hz.
- The default remains 1 MHz / 40 ns. Carrier alignment changes from center to
  edge; steady CH1/CH1N balance, actual deadtime, first-pulse phase and EN edges
  require scope verification. `FEN` is still the separate EN burst frequency.
  Natural LC resonance is set by the hardware components.

An effective change to period/deadtime ticks clears all three learned load
profiles, tuned metadata and previous web calibration-completion state in RAM.
Physical `LOAD1`–`LOAD3` resistances, sensor calibration and applied duty settings
remain. Retune explicitly before relying on learned profiles.

Web changes remain pending in RAM until **Save to device** / `WEB <id> SAVE`
with output OFF. Before WEB HELLO, terminal `TIMING` reads the current exact
pair, while `TIMING Hz ns` applies it. Legacy terminal auto-save after 1.5 s
quiet while OFF remains, unless BEGINCFG holds an import; SAVE/ENDCFG also
persists. Do not assume terminal timing changes require explicit SAVE only.

Dedicated protocol-1 `timing` frames carry requested/actual Hz and ns, timer
clock, period/deadtime ticks, limits, revision and enabled/busy state. They
accompany streaming, SNAPSHOT and successful TIMING. The browser requires both
the command ACK and matching-ID OFF/idle timing readback, rejects stale or
inconsistent frames and rechecks queued mutations. OFF retains priority.
Conflicting form edits must be applied or reset first. Recordings attach fresh
timing per sample and add ten CSV timing columns; missing/stale timing remains
blank and is never backfilled from later session metadata. See
[the protocol](../../docs/web-protocol.md#pwr-204-carrier-timing-capability).

## Saved-settings compatibility

F410 saves timing and calibration together in a 488-byte wrapper (33 slots in
the existing 16 KB sector): 4-byte version magic + unchanged 471-byte packed
legacy settings payload + explicit new `0xFF` reserved byte + 4-byte requested
Hz + 4-byte requested ns + 4-byte outer checksum. Legacy inner checksums remain.

The loader scans old 472-byte-stride records without rewriting or erasing at
boot. Legacy settings/calibration are retained with default 1 MHz / 40 ns timing.
New saves append after occupied legacy/torn blocks. An interrupted append can
fall back to the previous complete record. The existing single-sector wrap
erase can still lose all saved settings if power fails during erase.

Older firmware cannot read new wrappers; downgrade can recover stale legacy
settings or defaults. Export/review the current configuration and plan a
downgrade before flashing. Use the custom linker and verified HEX, preserve
0x08004000–0x08007FFF and avoid full-chip erase or a BIN spanning the settings
gap. See [F410 storage and flashing notes](../../docs/stm32f410-port.md#saved-settings).

## Validation

- Web: 76 tests passed; functional, responsive and keyboard browser checks
  passed for timing Apply/readback, conflicts, OFF/capability/stale guards and
  recording. Demo uses clearly marked synthetic V2 timing and cannot calibrate
  physical hardware.
- Native protocol: `python3 firmware/test_web_protocol.py`
  passed 131 JSON frames from the repository harness using production timing
  math, scheduler, atomic application, load-profile
  invalidation/application, dispatcher and lease/queue code. Includes a timing
  pair-grid sweep, register failure and interrupt-mask preservation checks.
  Maximum tested telemetry/timing frames are 913/350 wire bytes, within 1024-byte
  slots; periodic pairs reserve two reply/event slots. The Windows/MSVC runner
  was not executed here.
- Storage: `python3 firmware/test_carrier_storage.py` passed production
  loader/writer/checksum tests with mocked HAL flash, including 471-byte payload
  / 472-byte legacy stride migration to 488-byte records, corruption, torn
  records and all 122 interrupted-append word boundaries.
- F410: 90,268/98,304 bytes program, 6,868/32,768 bytes RAM. Verified HEX has
  90,752 programmed bytes and excludes the reserved settings sector.
- G071 regression build: 130,424/131,072 bytes program, 9,544/32,768 bytes RAM,
  unchanged PWR-2.0.3 behavior and 648 bytes of program headroom.

Build from the attached firmware-source root with `firmware/build.ps1 -Target F410`. Verify with
`python3 firmware/verify_f410_hex.py arduino-build-f410/thesi_power_control.ino.hex`.
The attached source ZIP contains the exact firmware/build/test sources for this build, the custom linker, documentation and a source checksum manifest. Firmware is excluded from the static web build.

No USB-UART adapter or ST-LINK is attached to this cloud environment. Physical
USB, on-board flash writes, stop latency, sensing accuracy and powered converter
behavior remain unverified. Scope and bench checks must establish the intended
electrical operating range before relying on these timing settings on hardware.
