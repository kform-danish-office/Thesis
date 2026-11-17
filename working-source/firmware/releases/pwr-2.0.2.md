# PWR-2.0.2 — web calibration build

Software-validation build; powered bench validation pending. No public GitHub
release, board flashing or hardware setting change was performed during setup.

Adds `calibration_v1`: queued precharge/no-load/load-slot tuning, current zero,
line reference, telemetry progress, cooperative UART/OFF/lease handling during
legacy waits, rollback after interruption/failure and RAM-only results until
explicit SAVE. All outcomes leave output OFF. Boot preference and prior mode
are retained. CAL3 is represented as separate operator-confirmed physical slots.

The prior series-control defaults, pins, flash layout and saved-settings format
are retained. Legacy terminal algorithms are reused; this does not establish
physical measurement accuracy, powered safety, actual stop latency or EEPROM
behavior on a board. A browser update cannot add these commands to PWR-2.0.1.

## Validation

- Web tests:54 passed, zero failed/skipped.
- Native production protocol/calibration runner:68 JSON frames; queue vs execution,
  output-OFF preconditions, conflict rejection, OFF under TX congestion, stop,
  active/queued lease expiry, fault cancellation,180s timeout, rollback and
  pending-save behavior. Physical calibration steps are mocked.
- Mock-board browser tests: capability gating, explicit confirmation, slot2,
  running/stop/complete states, explicit save, legacy rejection, desktop/mobile.
- F410 build:86,888/98,304 bytes program,6,828/32,768 bytes RAM. HEX validator
  passes:87,372 programmed bytes; SP0x20008000, reset0x08016031; settings sector
  0x08004000–0x08007FFF excluded.
- G071 build:129,336/131,072 bytes program,9,544/32,768 bytes RAM. Flash headroom
  is limited; rerun both targets after further firmware changes.

Build with the existing firmware/build.ps1 targets, or the environment's
/workspace/tooling/build-working-firmware.sh F410 / G071 helpers. For F410 use
the HEX and custom linker, never a BIN spanning the reserved settings sector.

Privately prepared HEX copies, hashes and build evidence are under
/workspace/tooling/autocal-review/firmware. No files from that directory are
included in the web deployment. Follow the existing board bring-up/SWD procedure;
no automatic flashing is provided by the web app.
