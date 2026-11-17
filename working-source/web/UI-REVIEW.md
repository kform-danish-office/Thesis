# Workspace UI refinement — October 24, 2026

The design retains the converter's instrument-style workspace. It uses the
Sites skill's task-focused, responsive, accessible design guidance and the
Vercel verification skill's complete-flow checks. A dedicated read-only UI
review identified navigation, contrast, keyboard-order, control-size, error,
and state-clarity problems. No separate UI Designer skill was installed.

## Changes

- Shared typography, panel spacing, focus rings, and darker secondary text.
  Navigation stays available while scrolling; all four tabs fit at 320 px.
- A monitor heading and firmware-download link. Larger live readings and
  controls retain the existing plot and simulator identification.
- Mobile visual order now follows DOM/keyboard order. Direct mobile links
  reach recording and output controls without changing converter state.
- Keyboard skip links, active-section semantics, and discreet connection,
  output, and recording announcements. Held stale readings receive a visible
  note and distinct styling. Telemetry itself is not a live announcement feed.
- The calculator's selected answer stays visible on mobile. Advanced operating
  inputs use a native disclosure, with their current values summarized.
- Short preset names improve scanning; full names remain in titles/exports.
  Source badges identify document baselines, missing values, and assumptions.
- Invalid fields have local text, `aria-invalid`, and associated descriptions.
  Errors preserve focus. Mobile calculator fields use 16 px text and 44 px
  height. The full-result link focuses its destination heading.

## Verification

The monitor flow is source selection → live samples → recording in IndexedDB →
JSON/CSV export. The calculator flow is editable preset → SI calculations →
results/plot → calculation export. Both run in the browser; the preview and
production host serve static assets. No server-side credentials or database
are required for either flow.

- All 46 existing protocol, transport, storage, mathematics, and preset tests
  passed. The static build generated eleven application files.
- Desktop layout inspected at 1280 × 900. Calculator mobile layout inspected at
  390 × 844 and 320 × 844. Monitor navigation fits all four items at 320 px;
  page content has no horizontal overflow. Internal tables retain scrolling.
- The selected-result strip correctly shows 988.9 kHz, 8.83 µH, and 978 pF for
  the reference solves. Missing C26 gives a local field error and disables
  export. Invalid series resistance preserves focus and opens advanced inputs.
- Positive R produces the normalized-current response. Calculator JSON was
  downloaded and verified with the edited 50 Ω input and source assumptions.
- A synthetic monitor session retained 147 samples and six command/ack events,
  including ON, OFF, and SET VSET 29. Its downloaded JSON was verified and the
  saved session remained available after reload.
- Keyboard checks passed for the first-focus skip link, workspace focus,
  active Sessions semantics, and the mobile output-controls destination.
- Selected essential notes and labels measured 4.66:1–9.92:1 contrast. This is
  a targeted check, not a claim of complete accessibility conformance.
- No captured browser warnings or errors in the exercised flows. Real USB and
  electrical behavior were not exercised by this presentation change.

Evidence is retained in `qa/skills-ui-*` screenshots and verification records.
The release payload excludes firmware, PDFs, recorded sessions, credentials,
tests, and QA files. The firmware release on GitHub is unchanged.

## Production

Deployment `dpl_A7MtyB1g2BG2ez49kqRLsKCHqAtD` reached READY and owns
`thesis-power-lab.vercel.app`. All eleven public application files returned
HTTP 200 and matched the fourteen-file source manifest's SHA-256 hashes.
The public calculator returned 988.9 kHz, 8.83 µH, and 978 pF in its three
solve modes. At 320 px, its answer strip remained visible and the document
had no horizontal overflow. The public monitor displayed synthetic readings;
the simulator was stopped after inspection. No browser warnings or errors
were captured. Navigation was checked for Sessions, Connection, and returning
to the top, including sections clamped to the same desktop scroll position.

Evidence: `qa/skills-ui-deployment-check.json`,
`qa/skills-ui-live-browser-check.json`, and `qa/skills-ui-live-*.png`.
