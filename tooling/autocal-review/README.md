# Hardware auto-calibration integration — 2026-10-25

User clarified that auto cal means hardware calibration controls, not calculator
recalculation. Implemented the controls plus compatible PWR-2.0.2 firmware; no
physical calibration or flashing was run. Selected GitHub checkout, original
source archives, thesis and imported skill files remain intact. Work is in the
private current working-source copy, with no Git commit/push or firmware release.

## Included routines

- Startup precharge (existing AUTOPRE algorithm).
- No-load soft-switch cap (existing AUTOBANG algorithm).
- Individual physical load-reference slots1–3 (existing CALLOAD algorithm).
- Current-sensor zero offset (existing ZEROI sampling).
- Primary line-reference capture and feed-forward enable (LFFCAL-equivalent).

Multi-load calibration is operator-guided: run one slot, leave output OFF,
physically change the load, explicitly confirm and start the next. No browser
operation switches a physical load or runs legacy CAL3 blindly.

## Execution and compatibility

The browser requires a physical connection, fresh calibration telemetry,
calibration_v1 capability, output OFF, no reported fault, no unsubmitted form
edits and a fresh operator confirmation. Demo cannot calibrate hardware.
PWR-2.0.1 continues to monitor/control normally but shows an upgrade message.

CAL is queued outside the serial parser. The existing algorithms cooperatively
service UART/OFF, lease, telemetry and faults during measurement waits. Human
serial tune output is suppressed in web mode, preventing mixed JSON fragments.
Stop remains operable during tuning, and OFF is executed during reply congestion.
The runner rejects conflicting mutations and cancels on OFF, lease expiry,
fault, unavailable ADC/gate hardware or180s timeout. Every outcome disables
output/gates. Interrupted/failed results roll back; successful changes remain
pending in RAM until an explicit SAVE while OFF. Flash writes are inhibited
throughout the transaction. Existing boot preference and prior control mode are
preserved. Default pins, stored-settings layout and tuning algorithms are retained.

Native and mock tests do not certify powered behavior, actual stop latency,
calibration accuracy or on-board flash behavior. These remain bench validation.
No automatic firmware flashing or public firmware upload was performed.

## Evidence

- Web suite:54 tests passed, zero failures/skips, including new capability/
  conflict/output-OFF/telemetry validation tests.
- Native production protocol+runner:68 JSON frames; original protocol assertions,
  queued vs execution state, stop under congestion, cancellation, active/queued
  lease expiry, fault cancellation, duration timeout, rollback and pending RAM
  result behavior pass. Legacy physical sweeps/measurements are mocked.
- Mock-board Chromium UI: old firmware blocked; explicit confirmation required;
  slot2 command, running/stop/complete states, pending/save behavior, conflicting
  controls disabled, no page errors; no document overflow at1440/390/320px.
  Evidence browser-results.json and calibration-*.png. No real USB was opened.
- Existing demo recording/export/persistence and calculator flows pass (regression.log).
- Both Arduino targets compile with CLI1.5.0, STM32 core2.8.1; logs under
  /workspace/tooling/autocal-f410.log and autocal-g071.log.
- F410 program86,888/98,304 bytes; RAM6,828/32,768. HEX passes vector/checksum/
  settings-sector exclusion checks:87,372 programmed bytes, reset0x08016031.
- G071 program129,336/131,072 bytes; RAM9,544/32,768. Limited flash headroom.
- Static build:15 app/font/license assets, no new external dependency.
- Production deployment dpl_FokP8hQGSGGzXipdwcJwkJxXfWUS is READY at
  https://thesis-power-lab.vercel.app/#calibration. All15 live assets byte-match
  the current build (deployment.json). Only static app files/fonts were uploaded;
  firmware, thesis, skills, credentials, tests and local logs were excluded.
- Native browser live HTTPS verification still has the previously observed
  environment certificate-trust limitation; local Chromium plus production-byte
  equality verified the delivered app. TLS verification was not disabled.
- Original archives/current authorized hashes and clean GitHub reference verify
  via /workspace/tooling/verify-sources.py. Current-source changes include firmware,
  tests and documentation, separately recorded in ui-change-manifest.json.

## Private firmware artifacts

pwr-2.0.2-calibration-builds.zip contains both target-specific HEX files,
SHA256SUMS and notes. ZIP CRC and copied artifact equality checks pass.

F410 SHA-256 e79a290f60e036921c48138aaea5891e506e84b48953fa66eeb2bb07de20c326
G071 SHA-256 91c461b639921935e445746dccd957b07594d362dc4a810bac44d8cd91d658b0

Use only the correct board target. F410 must retain its custom linker and use
HEX rather than a raw BIN spanning the reserved settings sector. Follow existing
board bring-up/SWD instructions; no hardware is flashed by the app. Firmware and
build notes also remain at /workspace/working-source/firmware/releases/pwr-2.0.2.md.

The cloud environment remains user-managed/Only me; no sharing or environment
publication was performed. Review/save the updated draft and publish the
prepared filesystem when desired to retain the current source/tools/artifacts.
