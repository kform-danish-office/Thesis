# Power Lab UI refinement — 2026-10-25

Scope: current monitor and resonant-tank calculator in `/workspace/working-source/web`. User authorized UI improvements after the original onboarding import. The GitHub reference checkout, firmware, protocol/transport/storage/math code, thesis, hardware settings and original ZIPs remain unchanged. No commit, push, public deployment or environment publication was performed.

## Design

Applied user-provided `web-design-engineer`, `frontend-design`, `better-ui`, typography/color and responsive guidance from `/workspace/skills`. This is a redesign within the existing instrument workspace: signal acquisition remains the main visual anchor, measurements and channel colors remain identifiable, forms keep their behavior and semantics.

Shared palette: canvas #f4f6f5, ink #142d30, header #122e32, action #087f72, structural line #dce4e1, dark plot #12191f. Existing channel colors stay consistent with the actual plot. Self-hosted IBM Plex Sans and IBM Plex Mono come from the user's skill bundle, with OFL-IBMPlex.txt retained in the built asset folder. The signal mark is a simple UI mark drawn for Power Lab, not an institutional logo. No external fonts, CDN, framework or dependency added.

Replaced the layered monitor stylesheet with a coherent shared stylesheet. Improved spacing, navigation, hierarchy, empty/disabled states, control boundaries, contrast, touch controls, tabular readings, keyboard focus, hover behavior and reduced-motion support. Calculator has clearer computed-result emphasis, larger controls/plot, quiet source notes, readable tables and narrow-screen stacking. Unnecessary decorative numbering/eyebrows were removed after skill review. Local build/server allowlists include only the app and local fonts/license.

Changed existing files: `index.html`, `styles.css`, `calculator.html`, `calculator.css`, `build.mjs`, `server.mjs`. Added `fonts/IBMPlexSans-Regular.ttf`, `fonts/IBMPlexSans-Bold.ttf`, `fonts/IBMPlexMono-Medium.ttf`, `fonts/OFL-IBMPlex.txt`. Original import hashes remain in `working-source-manifest.json`; the authorized current revision is recorded separately in `/workspace/tooling/ui-change-manifest.json`. Original presentation files are backed up under `/workspace/tooling/ui-originals`.

## Validation

- `cd /workspace/working-source/web && npm test`: 46 passed, zero failures/skips.
- `npm run build`: 15 files (11 app files, 3 fonts, 1 license); no source/test/thesis payload.
- Chromium with installed Playwright: monitor demo telemetry, recording, save, JSON export, reload persistence and exit pass. Simulator-only output was enabled for a signal screenshot, then turned off and exited; no hardware connection made.
- Calculator: nominal 988.9 kHz, input edits, invalid field/error association, invalid export blocking/recovery, JSON export, solve modes, positive-resistance response and pump validation pass.
- Keyboard-only recording/export flows pass; skip link works, focus is visible and not hidden behind sticky navigation. Mobile walk checks 17 monitor and 33 calculator focus stops.
- Browser layout/screenshots inspected at 320, 390, 768 and 1440 CSS px: no document overflow. Tables retain deliberate local scrolling. Initial, simulator, result and error states checked.
- 200% text-size stress and browser-zoom-equivalent reflow (720 CSS px at DPR2 representing a 1440 display) pass. A unit-width issue found during text stress was fixed. Literal native browser zoom and actual screen-reader output were not verified.
- Reduced-motion emulation disables transitions/animations. Hover treatments are restricted to hover-capable pointers. Press feedback is limited to enabled actions when motion is allowed.
- Essential enabled text and control-boundary contrast pairs were measured; fixes include metric units, command codes, footer, focus rings and inputs. This targeted review is not a claim of full WCAG certification.
- All font routes return 200 with correct MIME. Firmware, main.tex, tests, README/package and QA file requests return 404. No browser page errors in exercised flows.

Evidence scripts and JSON records live in this directory. Key screenshots: `final-monitor-demo-desktop.png`, `final-monitor-1440.png`, `final-monitor-390.png`, `final-calculator-1440.png`, `final-calculator-390.png`. Historic UI-REVIEW.md in the imported source describes an older deployment; this refinement has NOT been deployed there.

## Skills import

All 17 skills / 118 files from skills.zip are in `/workspace/skills`, with original `.system` paths retained. ZIP CRC and all imported file bytes verified. Archive SHA-256: c7c519c459a2ac4766a5294947311f0b62c2bda01fe30caf8e9e0c3ab2e1d9d7. References/assets/scripts/licenses preserved. `/workspace/AGENTS.md` catalogs paths for future workspace agents; the platform's skill-menu registration is not claimed. No global/builtin skill directories were overwritten. Original ZIP retained under `/workspace/source-archives/skills.zip`.

Keep access Only me. Sharing controls are not exposed by available tools and were not changed. Save/review the updated draft in environment settings and publish when desired to capture this prepared filesystem; fresh-task restoration has not been tested.
