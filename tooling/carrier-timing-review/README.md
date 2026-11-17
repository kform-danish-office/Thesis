# V2 carrier frequency and dead time — 2026-10-25

The user requested adjustable resonant-drive frequency, adjustable dead time,
and a firmware push after compilation, then restricted the feature to V2.
Implemented the controls for **V2 / STM32F410CBU6 only**, as PWR-2.0.4. G071
retains PWR-2.0.3, its existing fixed timing and its previous program size.
The physical tank's natural resonance remains set by its L/C components.

## Delivered behavior

Setup has a collapsed **V2 switching/carrier timing** section, separate from
EN burst frequency. Both values are applied atomically with output OFF and no
startup/autotune/calibration running. No operation enables output automatically.
Requested frequency is 500,000–2,000,000 Hz and requested dead time 20–200 ns,
with a coupled timer check that rejects impossible pairs. These are software
limits, not a measured electrical operating range.

V2 uses even-period, edge-aligned complementary TIM1 CH1/CH1N on PA8/PB13.
At the nominal 100 MHz timer, the balanced period grid is 20 ns and dead-time
ticks are 10 ns. Near 1 MHz the frequency grid is about 20 kHz; arbitrary 1 Hz
input resolution does not imply 1 Hz output resolution. Dead time rounds up.
For example 950,000 Hz / 53 ns realizes 106 period ticks / 6 dead ticks,
943,396 Hz / 60 ns. At 2 MHz, 120 ns passes and 130 ns fails. Actual register
fractions and requested values are both reported. The new edge-aligned mode
preserves nominal steady 1 MHz / 40 ns but changes startup phase; bench scope
verification is required.

`carrier_timing_v1` is advertised only by F410. The browser sends
`WEB <id> TIMING <Hz> <ns>` and requires both ACK and matching-ID timing readback.
Independent stale/missing timing locks the controls. OFF priority, lease expiry,
fault/busy guards and older-firmware behavior are retained. Demo is synthetic
V2 timing and cannot run physical calibration.

Effective timer changes invalidate the three learned load profiles, tuned
metadata and prior calibration-complete state. Physical resistance references,
sensor calibration and applied duty settings are retained. Retuning remains an
explicit operator action. Browser changes stay in RAM until Save to device;
native terminal retains the existing 1.5 s quiet-OFF deferred save.

New F410 records are 488 bytes: distinct prefix, unchanged packed 471-byte
settings payload, one new alignment byte, timing requests and outer checksum.
Legacy F410 records use a 472-byte stride and load without boot writes/erase.
Timing and calibration now persist together. Old firmware cannot read new
records and may use older records/defaults after downgrade. Single-sector erase
on journal wrap retains its existing power-loss limitation.

Session JSON and CSV preserve initial and per-sample timing. CSV adds ten
requested/actual/tick/revision/source/time columns. Stale/absent timing stays
blank; session metadata does not fill old samples. Timing events record changes
without flooding the event limit on every stream poll.

## Build and test evidence

| Check | Result |
| --- | --- |
| `cd /workspace/working-source/web; npm test` | 76 passed, no failed/skipped |
| `npm run build` in that directory | 15 web/font/license assets |
| `python3 /workspace/tooling/test-working-protocol-linux.py` | 131 JSON frames; production math/scheduler/application/profile tests |
| `python3 /workspace/working-source/firmware/test_carrier_storage.py` | Migration, integrity, coherent reboot and all 122 interrupted append-word boundaries passed |
| `bash /workspace/tooling/build-working-firmware.sh F410` | 90,268/98,304 program bytes; 6,868/32,768 RAM |
| `bash /workspace/tooling/build-working-firmware.sh G071` | 130,424/131,072 program bytes; 9,544 RAM; 648 program bytes remain |
| F410 HEX verifier | 90,752 programmed bytes; SP 0x20008000; reset 0x08016939; settings sector excluded |
| `python3 /workspace/tooling/verify-sources.py` | Original archives, current source revisions, V2 entry assets, imported skills and unchanged clean GitHub reference passed |

Native tests include 34,390 timing-pair attempts, exact rational cycle
conversions, locked-state recheck/IRQ restoration, failed timer readback,
calibration invalidation, no automatic ON and bounded UART queues. Worst frame
sizes: telemetry 913 bytes, timing 350 bytes within 1024. Periodic pairs preserve
two reply/event slots. Physical HAL, flash and calibration actions are mocked.

Browser QA passed 11 functional groups, 12 viewport checks, 8 keyboard walks and
8 text/reflow checks. Actual exported fixture recordings have 41 samples, five
stale/null timing samples and only two timing events across repeated polls.
320/390/1440 layouts, mobile fixed-OFF focus, existing calibration, old firmware,
missing/mismatched readback, pending drafts and disconnect were checked.
`browser/README.md` records evidence and limits; no application JavaScript errors.
The incidental favicon 404 is unrelated. A representative timing screenshot was
also inspected by the primary agent.

Logs, source snapshots/hashes and detailed firmware notes are in this directory.
The protocol runner is now portable; the old Linux helper delegates to it.
Its compatibility entrypoint and the storage test were rerun after that helper
update. The install script now runs the new storage suite as well; existing
dependencies/commands were preserved. Tools: Arduino CLI 1.5.0, STM32 core 2.8.1,
ARM GCC 13.2.1-1.1, native GCC 14.2.0, Node 24.19.0, npm 11.9.0 and Chromium.
Windows/MSVC execution, real screen-reader output, native browser zoom and
physical electrical/flash behavior were not tested.

## Delivery, persistence and push limitation

Private V2 package: `pwr-2.0.4-v2-f410-timing.zip`, 103,372 bytes, SHA-256
`bdb20a73e73a041f42938b4d1d91216cf105c1557239250c9df0cca7ab60b4c8`.
HEX: `firmware/pwr-2.0.4-v2-stm32f410cbu6.hex`, SHA-256
`fe3a6b02f06b025ba83e53dd482bbfdf9dd166f9f2afc0fe806062eab14ded47`.
CRC/copy/hash checks passed. The package includes instructions, release notes
and hashes. Use the verified sparse HEX and the existing SWD bring-up procedure;
do not use a full-chip erase or a flat BIN spanning the settings gap when
preserving settings. No automatic flasher is included.

Web controls deployed under the user's existing Vercel authorization:
https://thesis-power-lab.vercel.app/#device-setup . Deployment
`dpl_zw1813ksvrYLVwtvwzYCNXDWBGZw` is READY. All 15 live asset bodies match the
final build through TLS-verified curl (`deployment-verification.json`). Only web
assets/configuration were uploaded; firmware, thesis, skills, logs and credentials
were excluded. The optional CLI npm update check failed after READY; deployment
and live-byte verification succeeded. Browser flows were tested locally; direct
live Chromium had an existing environment certificate-trust limitation, which
was not bypassed.

**Firmware push remains blocked by the missing destination/device connection.**
An asynchronous clarification asked whether push means local board flash,
download or GitHub upload. The later V2-only clarification did not specify that
destination. This cloud machine exposes no USB sysfs devices, ttyUSB/ttyACM nodes
or connected programmer. No physical flash is possible from the current runtime.
No public GitHub upload/release, commit or push was inferred from the ambiguous
request. The compiled private package is ready; physical flashing needs a local
programmer or a deliberately connected supported device. A GitHub upload needs
an explicit repository/release destination consistent with the user's privacy
requirements.

Current editable code remains `/workspace/working-source`; before-edit snapshots
contain 120 files under `before/`. The current source now has eight additions
relative to the original import, recorded with 26 edited original files in
`/workspace/tooling/ui-change-manifest.json` (34 entries). Original ZIPs/import
manifests, thesis/V2 data-entry assets and `/workspace/Thesis` are unchanged.
No hardware setting was applied to a real board. Access settings were untouched.
Install/start instructions were saved as a draft for user review/save/publication
with Only me; no environment publication or fresh-task restoration was performed.
