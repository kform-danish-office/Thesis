# Dashboard workspace QA

Read-only application review on 2026-10-25. Source: `/workspace/working-source/web`; browser: Playwright Chromium (`/usr/bin/chromium --no-sandbox`). Tested the server already running at `http://127.0.0.1:4173`; QA did not start or own it.

Applied `/workspace/skills/web-design-engineer/SKILL.md` and `/workspace/skills/better-accessibility/SKILL.md` guidance for actual browser rendering, responsive behavior, focus, labels, disclosure accessibility, and motion. No app source was edited. No real USB/device was used; all device behavior was Demo or a fake serial fixture.

## Verification

- `node /workspace/tooling/dashboard-review/qa/check.cjs`: passed. Monitor/Setup/Calibration/Sessions views, Demo LOAD1 edit to 47.5 with readback, explicit LOAD2 reference selection, output-ON edit gating, global OFF from Setup, invalid advanced setting opening/focusing its disclosure, recording while returning to Monitor, global stop/save, deep links/reload/back, existing ARIA/label references, no page errors, no horizontal overflow at 1440/390/320.
- `node /workspace/tooling/dashboard-review/qa/calibration.cjs`: passed. Old firmware cannot bypass capability checks; firmware with `calibration_v1` but no `bench_settings_v1` can still calibrate; extended settings gated; existing voltage control available. Explicit confirmation, run/stop/retry/complete/save verified using fake serial.
- `node /workspace/tooling/dashboard-review/qa/stress.cjs`: passed reflow. No document overflow in all four views at 720 CSS pixels with DPR2 (a 200%-zoom viewport equivalent, not native browser zoom), and with all text font sizes doubled at 1440 CSS pixels. Only intentional 1px visually-hidden fieldset legends matched clip scanning. Reduced-motion styles had no animation and 0s transition. Native keyboard traversal at 320px had no hidden/offscreen/unstyled focus stops.
- `node /workspace/tooling/dashboard-review/qa/obscure.cjs`: extra expanded-disclosure keyboard hit testing at 320/390. Identified a 390px fixed global OFF overlap with the focused Duty tab and terminal Send button. Parent corrected root mobile scroll padding. Retest passed all four workspaces at both widths; 39 Setup focus stops with disclosures expanded, none obscured.
- `node /workspace/tooling/dashboard-review/qa/anchors.cjs`: passed. Legacy connection, terminal, capture and output anchors route to the correct view, open their disclosure where needed, and focus/scroll to visible content below sticky navigation at 1440/390/320.
- `node /workspace/tooling/dashboard-review/qa/capture.cjs`: final Monitor and Setup captures at 1440/390/320. Monitor has output enabled in the clearly labeled synthetic Demo to show active traces, followed by output OFF and exiting Demo. Waited 350ms for settled controls before screenshots.

## Evidence

- `results.json`, `browser-results.json`, `stress.json`, `obscure.json`, `anchors.json`
- `final-dashboard-{1440,390,320}.png`
- `final-device-setup-{1440,390,320}.png`
- `obscured-390-dashboard-11.png`, `obscured-390-device-setup-38.png`: focus-under-OFF repro before correction
- `calibration-{1440,390,320}.png`, `legacy.png`
- `text-resize-*.png`, `zoom-equivalent-*.png`

Real hardware calibration/persistence, physical load values and USB permission prompts were not tested. Screen-reader output and native browser zoom were not tested.

Final focused integration review found Reset edits disabled for slot-only/mode-only drafts. Corrected the shared enable condition; `check.cjs` now exercises discarding a slot-only draft and passed again. A separate real-browser check verified discarding a mode-only draft from Setup. No further review findings.
