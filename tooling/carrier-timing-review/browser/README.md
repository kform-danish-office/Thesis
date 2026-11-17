# Carrier timing browser verification

Passed on 2026-10-25 against `/workspace/working-source/web`. No actionable accessibility or layout findings in the inspected scope. Approve for the browser checks below.

The existing local Node server on port 4173 was reused. This QA started no server, changed no application source, and published nothing. All browser contexts and owned Chromium processes were closed. This folder contains the QA scripts and evidence only.

## Verified behavior

- V2 synthetic Demo is visibly labeled and starts OFF. Timing is a closed Setup disclosure, separate from EN burst settings.
- Requested 950,000 Hz / 53 ns quantizes to 106 period ticks / 6 deadtime ticks at 100 MHz, with actual 943,396 Hz / 60 ns. Preview and verified actual readback remain distinct.
- 2,000,000 Hz / 130 ns is rejected; 120 ns is accepted. Applying and saving timing never enables output.
- Timing drafts block ON, Save, calibration and conflicting Apply actions, including a terminal ON attempt. Settings, mode and reference-slot drafts prevent timing Apply. Reset timing preserves other drafts; Reset edits clears all drafts.
- Output ON locks timing; OFF is available throughout. OFF cancels the remaining settings sequence after the in-flight first SET. Disconnect clears timing values and drafts, including USB and Demo paths.
- Old F410 firmware, G071 and no-capability fixtures leave timing unavailable. Missing timing stays blank while telemetry is fresh. Stale timing is identified independently of fresh telemetry, locks edits, and labels retained actual values as stale.
- A timing ACK plus periodic uncorrelated timing frames cannot complete an Apply. The browser shows the same-command verified-readback timeout, preserves the draft and stays OFF. Additional queued-ON, capability-loss and malformed/mismatched-frame cases are covered by the separate transport test suite, not counted here as browser assertions.
- Existing Monitor, Setup, Calibration and Sessions navigation works. The fake USB board supports the new parser and existing calibration protocol; explicit calibration confirmation, load slot 2, stop, completion and Save were exercised.
- Real UI JSON and CSV downloads retain initial timing and each sample's actual readback. The USB recording contains 41 samples, including 5 stale samples with `timing: null` and blank CSV timing cells. Exactly 2 timing events remain: initial timing and the changed pair, despite repeated polls. Demo recording has synthetic source/firmware/timing and exactly 1 event when unchanged.

## Responsive and accessibility checks

All four views passed document/element overflow checks at 320, 390 and 1440 CSS pixels. Expanded Setup passed the same checks with doubled text and a 720 × 500 zoom-equivalent viewport. Visual inspection covered the timing disclosure/readback, all four views, stale timing, draft preview and mobile action focus.

Keyboard walks at 320 and 390 pixels reached all enabled controls. Expanded Setup with a timing draft has 45 stops, including both inputs, Reset timing edits and Apply timing. Focus indicators remained visible; focused controls were not obscured by the fixed OFF action or navigation. Reduced motion produced zero transition duration and no animation. All label/ARIA ID references resolve; the timing inputs and actions have accessible names in the browser accessibility tree.

No application JavaScript/page errors were observed. Chromium initially requests `/favicon.ico`, which the existing development server returns as 404; that resource notice is recorded separately from application errors and does not affect these checks.

Not verified: a physical board, USB hardware, actual timer pins, switching behavior, electrical safety, firmware flash persistence, a screen reader application, full WCAG contrast audit, RTL/localization, or browser-engine compatibility beyond Chromium. This is software bench QA with synthetic data and a browser-injected serial fixture; it does not establish hardware safety or a board/MCU identification from a photograph.

## Evidence

- `results.json`: combined outcome and exact tested source hashes.
- `functional-results.json`, `interlock-results.json`, `responsive-results.json`: assertions, layout metrics, keyboard results and timing accessible names.
- `recording.json`, `recording.csv`, `demo-recording.json`: exports generated through the application UI.
- `applied-viewport-1440.png`: actual timing after applying 950,000 Hz / 53 ns in Demo.
- `applied-setup-320.png`, `applied-setup-390.png`: complete mobile Setup with applied timing.
- `focus-apply-timing-320.png`, `focus-apply-timing-390.png`: keyboard focus on Apply timing above the fixed OFF action.
- `stale-usb-1440.png`: fresh fixture telemetry and independently stale timing.
- `dashboard-*`, `device-setup-*`, `calibration-*`, `experiments-*`: three viewport sizes per view.
- `double-text-*`, `zoom-equivalent-*`: four views under text and reflow stress.

Run from this folder while the existing app server is running:

```sh
node functional.cjs
node interlocks.cjs
node responsive.cjs
node capture.cjs
```

The scripts require the existing Playwright package at `/opt/codex/cua_node/lib/node_modules/playwright` and Chromium at `/usr/bin/chromium`. No packages were installed. `fixture.cjs` installs a fake `navigator.serial` only inside each test page. Its 150 ms stream accelerates coverage and is not a hardware sampling-rate claim.
