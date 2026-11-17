# Load settings and dashboard revision — 2026-10-25

Current editable source remains `/workspace/working-source`. The selected GitHub
reference `/workspace/Thesis`, the thesis source `/workspace/thesis`, original
archives and imported skills remain intact. This is the user-authorized
continuation of the UI, hardware-calibration and Vercel work. No Git commits,
pushes, board flashing, physical calibration or environment publication occurred.

## What changed

The previous stacked dashboard is now four views: Monitor (`#dashboard`), Setup
(`#device-setup`), Calibration (`#calibration`) and Sessions (`#experiments`).
Monitor concentrates on live readings, the chart and output/mode controls.
Setup groups device settings and physical load references; scan/precharge
settings, USB instructions and the terminal use disclosures. The separate
calculator remains available. USB, telemetry, calibration and recording stay
connected across views; Output OFF and active recording controls remain global.
Existing deep links and browser history route to the appropriate view.

Applied the workspace web-design-engineer, better-layout and better-writing
guidance; QA also used better-accessibility. The existing teal/IBM Plex design
system is retained, with compact layout, explicit form labels, device readbacks,
responsive disclosures and mobile focus scroll padding.

PWR-2.0.3 adds `bench_settings_v1` alongside `calibration_v1`. Setup now exposes
LOAD1–3 resistance references, explicit reference-slot selection, no-load duty,
calibration scan values and startup timing. Values come from reported device
settings, never assumed defaults on real boards. Extended settings require the
capability, finite readback, fresh telemetry and output OFF. Apply changes RAM;
explicit Save to device persists settings. Existing PWR-2.0.2 calibration remains
usable without the new capability; older firmware retains ordinary control.

Resistance values describe the physical load connected by the operator. They do
not change or switch that load. Zero means unconfigured. Selected-slot readback
does not prove a valid stored calibration profile. The existing scan retains its
minimum-duty/step behavior; AUTOMAX alone is not a strict low-value ceiling.
Defaults, pins, algorithms and stored format were preserved. Authoritative key
ranges and commands are in `working-source/docs/web-protocol.md`; release notes
are in `working-source/firmware/releases/pwr-2.0.3.md`.

## Validation and repeatable commands

| Workflow | Command / result |
| --- | --- |
| Web | In `/workspace/working-source/web`: `npm test` — 60 passed, no failed/skipped; `npm run build` — 15 app/font/license files |
| Native firmware | `python3 /workspace/tooling/test-working-protocol-linux.py` — 96 JSON frames passed; physical routines mocked; worst stressed serializer frame 913 wire bytes within 1024 |
| F410 | `bash /workspace/tooling/build-working-firmware.sh F410` — 87,736/98,304 program bytes, 6,828 RAM; vectors and reserved-sector exclusion passed |
| G071 | `bash /workspace/tooling/build-working-firmware.sh G071` — 130,424/131,072 program bytes, 9,544 RAM; only 648 program bytes remain |
| Browser | `node /workspace/tooling/dashboard-review/qa/check.cjs`, `calibration.cjs`, `stress.cjs`, `obscure.cjs`, `anchors.cjs` — passed; details in `qa/README.md` |
| Source integrity | `python3 /workspace/tooling/verify-sources.py` — original archive hashes/CRCs/counts, retained source revisions, 118 skill files and clean unchanged GitHub reference passed |
| Live assets | `python3 /workspace/tooling/dashboard-review/verify-live.py` — all 15 production assets match final local build with TLS verification |

Browser tests exercise reference resistance apply/readback, slot selection,
output-ON edit restrictions, global OFF, invalid-input disclosure/focus, recording
across views, old-firmware capability gating and prior calibration compatibility.
Responsive checks pass at 320/390/1440 CSS pixels, doubled text, zoom-equivalent
reflow and reduced motion, with no page errors or document overflow. A final
review found Reset edits disabled for slot-only/mode-only drafts; fixed and
retested both recovery paths. Screenshots and machine-readable results are in
`qa/`. Firmware logs are `/workspace/tooling/bench-settings-f410.log` and
`bench-settings-g071.log`; web results are `node-tests.log`.

Tools: Node 24.19.0, npm 11.9.0, Arduino CLI 1.5.0, STM32 core 2.8.1,
ARM GCC 13.2.1-1.1, native GCC 14.2.0, system Chromium via Playwright.

## Delivery and limits

Production: https://thesis-power-lab.vercel.app/#device-setup . Final deployment
`dpl_48HUeWuAWCYPpWe7V3BgXF84YTi4` is READY. Only 15 web/font/license assets and
Vercel configuration were staged at `/workspace/tooling/vercel-dashboard-payload`.
No firmware, thesis, skills, logs or credentials were uploaded. The CLI's optional
npm version-check failed after its READY result; live asset verification passed.
Deployment details and hashes: `deployment-verification.json`.

Private firmware package: `pwr-2.0.3-bench-settings-builds.zip`, SHA-256
`a99c15a098c1e981198bc1e08c938638dea10d7f8725a45e9c9c774178cf8ba9`.
It contains both HEX files, release notes and SHA256SUMS; copy/CRC checks passed.
F410 requires the custom linker and HEX to preserve its settings sector.
The browser does not flash a board. Load-setting access on a real board requires
the matching firmware installed separately using the documented bring-up flow.

Physical USB, load accuracy, powered converter behavior, real stop latency,
calibration accuracy and actual flash persistence require bench validation.
Screen-reader output and native browser zoom were not tested. Browser functional
tests used the local build and synthetic/fake-serial devices; production bodies
were checked through TLS-verified curl. Earlier live Chromium access encountered
the environment's certificate-trust limitation; verification was not bypassed.

Current authorized source hashes: `/workspace/tooling/ui-change-manifest.json`
(23 edited imported files and six added source/font/license files). Original ZIPs
and import manifests remain unchanged. Preserve `/workspace/working-source`,
`/workspace/thesis`, `/workspace/skills`, `/workspace/AGENTS.md`, source archives
and tooling in the private snapshot. Updated startup instructions are saved as
an environment draft; the user retains Only me and reviews/saves/publishes the
environment. Sharing was not changed or independently verified. Environment
publication and restoration in a fresh task remain unperformed.
