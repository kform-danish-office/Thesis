# PWR-2.0.3 — bench settings build

Software-validation build; powered bench validation pending. No board was
flashed, load switched or hardware setting changed during cloud validation.
No public GitHub release was created.

Adds `bench_settings_v1` alongside the existing `calibration_v1` capability.
Telemetry now reports load-reference resistances (`LOAD1`–`LOAD3`), selected slot
(`ACTLOAD`), no-load duty, auto-tune scan settings and startup precharge timing.
The browser uses these readbacks in Setup rather than assuming device defaults.
Advanced edits and reference-slot selection require output OFF. Apply changes
updates RAM; explicit SAVE with output OFF persists them.

Resistance entries describe the physical references connected by the operator.
They do not change or switch a resistor/electronic load. Zero means unconfigured,
not a short circuit. Selecting a slot can apply its stored profile when one
exists, but selected-slot readback does not prove calibration validity. The
existing scan retains its minimum-duty/step rules; a low AUTOMAX value is not an
independent strict ceiling. DMAX remains the output ceiling.

The dashboard separates Monitor, Setup, Calibration and Sessions. USB and active
recording continue between views, with global Output OFF and recording controls.
PWR-2.0.2 retains calibration support; PWR-2.0.1 retains ordinary monitoring and
control. Neither gains extended bench settings from a browser update alone.
See [the protocol specification](../../docs/web-protocol.md#pwr-203-bench-settings-capability)
for supported keys, units and authoritative ranges.

Defaults, control/calibration algorithms, board pins, saved-settings format and
F410 reserved settings sector are unchanged. The app does not flash hardware.

## Validation

- Web tests: 60 passed, zero failed/skipped. Covers extended settings validation,
  output-OFF/capability/readback restrictions and existing calibration transport.
- Native production protocol runner: 96 JSON frames, including extended settings,
  slot selection, OFF/busy guards and serialization stress. Worst tested frame is
  913 wire bytes, within the 1024-byte buffer. Physical routines are mocked.
- Browser checks: reference resistance Apply/readback, slot selection, invalid
  input focus, output-ON restrictions, recording across views, legacy capability
  gating and calibration compatibility. Desktop/mobile layouts and keyboard focus
  checked at 320, 390 and 1440 CSS-pixel widths, with text-size/reduced-motion checks.
- F410: 87,736/98,304 bytes program, 6,828/32,768 bytes RAM. HEX validation passes:
  88,220 programmed bytes, SP 0x20008000, reset 0x080162D1; the settings sector
  0x08004000–0x08007FFF is excluded.
- G071: 130,424/131,072 bytes program, 9,544/32,768 bytes RAM. Only 648 bytes of
  program headroom remain; rerun both board builds after firmware changes.

Build using `firmware/build.ps1 -Target F410` / `G071`, or this environment's
`/workspace/tooling/build-working-firmware.sh F410` / `G071` helpers. F410 requires
the custom linker and HEX; do not use a BIN spanning the reserved settings sector.
Private HEX copies, hashes and evidence are under
`/workspace/tooling/dashboard-review/firmware`; firmware is excluded from the web
deployment. Follow the existing board bring-up/SWD procedure separately.

Physical USB, powered converter behavior, actual stop latency, calibration
accuracy and on-board flash writes remain unverified. No screen-reader or
physical-hardware certification is implied by browser/native software checks.
