# Calculator model clarity and magnetizing branch — 2026-10-25

The user's measurement table matches the imported thesis Chapter 6. The earlier calculator deliberately calculated only the series-path LC/RLC reference, but did not expose the magnetizing branch clearly. This revision adds that context and bounded optional calculations while preserving the original series solver and plot.

Applied skills: web-design-engineer, frontend-design and better-ui, retaining the Power Lab typography/palette and native HTML/JS stack. A read-only engineering review checked the equivalent-circuit interpretation and implementation. A separate UI pass informed diagram placement and small-screen behavior.

## Result

- Equivalent circuit beside the result: Cr and Lr feed Lm in parallel with the primary-referred load; Lr is external plus leakage inductance. Readable alternate text diagram replaces the SVG in narrow containers, with accessible descriptions.
- Optional Lm field and paired transformer A/B reference selector. Default remains unknown; the explicit A preset loads A. Changing either Lm or leakage detaches the selected measured identity; loading another preset clears stale Lm/reference data.
- Series resonance clearly named; existing series-RLC response remains independent of Lm.
- Separate results for Xm at fs, Lm/Lr and an ideal open-secondary LC estimate. A visible note limits the last estimate to a linear, primary-referred, nonconducting-rectifier model; it is not loaded operating frequency, converter gain or ZVS. No branch current is inferred without voltage/waveform.
- Supplied A/B values and measured turns ratios are available in a reference disclosure. The 34.26/33.09 µH inductors and Rac2.05/2.17 Ω are identified as separate pump measurements, not silently used as resonant L or tank loss.
- Full calculation records and detailed sources use native disclosures to reduce page length; export controls and primary model limitations stay visible.
- JSON/CSV records include Lm, paired-reference provenance, optional branch results and assumptions. Existing v1 fields and series solve remain intact.

## Reference values

With external L9.4 µH, Cr1 nF, fs1 MHz:

| Reference | Leakage | Lm | Series fr | Ideal open-secondary frequency | Xm | Lm/Lr |
| --- | --- | --- | --- | --- | --- | --- |
| A | 16.42 µH | 150.78 µH | 990.472 kHz | 378.726 kHz | 947.379 Ω | 5.83966 |
| B | 16.50 µH | 139.89 µH | 988.941 kHz | 390.878 kHz | 878.955 Ω | 5.40116 |

These are comparison scenarios. Installed A/B identity is not established.

## Validation

- npm test: 51 passed, 0 failed/skipped. Five new math/reference tests cover A/B values, scaling/monotonic behavior, missing operating frequency, invalid/overflow input, and paired-source data. Original series tests still pass.
- npm run build: 15 app/font/license files; no new dependencies.
- check.cjs: default blank Lm leaves base calculation valid; A/B values apply together; edited Lm leaves series fr unchanged and detaches reference; invalid Lm gets associated local error and disables stale exports; blank recovers; JSON contains correct provenance/results; drawing preset clears stale branch values; explicit A preset loads A; widths320/390/768/1440 have no document overflow or page errors.
- final-capture.cjs: keyboard selection of A, keyboard reference/record/source disclosures, missing fs leaves Xm unknown without suppressing open-secondary estimate. Desktop/mobile evidence captured.
- mobile-anchor.cjs: Full result link places focused heading below sticky navigation and answer strip (observed y236px at390px viewport).
- Existing monitor/demo recording/export/persistence and calculator math/validation browser regression flows pass; no physical USB connection.
- 200% text stress and zoom-equivalent reflow pass for calculator; only harmless heading glyph-vs-linebox metric difference, no clipping ancestor. Literal native zoom and screen-reader output remain unverified.
- Rendered desktop diagram/result and full desktop/mobile layouts inspected. Source review found no actionable numerical/provenance/reset/stale-output defect.
- verify-sources.py passes: original ZIPs and thesis preserved; authorized current source revision recorded separately; selected GitHub checkout clean and unchanged; imported skills unchanged.

Useful evidence: model-desktop.png, model-mobile-viewport.png, calculator-1440.png, calculator-390.png, results.json, export-a.json. The model-mobile.png element screenshot includes normal sticky-chrome overlap caused by auto-scrolling the element for capture; use the viewport capture to assess the actual Full result navigation.

Full derivation/model boundary: /workspace/working-source/docs/calculator-evidence.md. Original archives and firmware/hardware settings were untouched. No commit, push, deployment, sharing change or publication was performed.
