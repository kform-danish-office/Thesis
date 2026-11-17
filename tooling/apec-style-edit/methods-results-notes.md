# Chapters 09–10: concise technical prose pass

Applied the user’s latest APEC digest-style preference: direct engineering prose, concise methods/results, and explicit evidence limits. No specific APEC manuscript was available, so this is a general conference-prose treatment rather than an asserted exact style match.

## Scope and counts

- Edited 28 subsection files in Chapters 09 and 10 only.
- Source-token word count: 11,699 → 9,582; 2,117 removed (18.1%). Counts include unchanged LaTeX tables, figures, and equations.
- No changes to chapter include files, other thesis directories, builds, manifests, or GitHub.

## Main changes

- Replaced tutorial explanations of instruments, ADC/DMA, channels, and signal identifiers with compact function-first descriptions.
- Condensed repeated “next capture needs…” passages into concrete measurement limitations and required follow-up methods.
- Shortened the revised validation campaign while retaining power sequence, test boundaries, stop criteria, protocol validation, and matched volume convention.
- Preserved the V1 numerical baseline and the qualitative V2 account. Leakage-only operation, reduced half-bridge heating, unresolved rectifier heating, and suspected copper/via or winding limits retain their evidence strength.
- Retained the secondary 3.3–3.6 A current region without inventing a corresponding output voltage or power.
- Kept the V3 reduction as an approximately 8% reduced-function design estimate, with absent replacement magnetics and matched continuous testing explicit.

## Representative changes

- “Direct memory access (DMA) copied those readings to memory without making the controller wait for each conversion” → “acquired secondary-bulk voltage at PA1 through continuous ADC DMA.”
- Thermal-method tutorial and repeated future-test cautions → a surface-hotspot statement and one paragraph identifying the missing ambient, airflow, warm-up, and setup records.
- V2 layout explanation now identifies limited copper and a possible single-via bottleneck as unconfirmed mechanisms; it no longer repeats a general copper-pour tutorial.
- Final results retain the numerical findings first, followed by the specific unresolved measurement or thermal constraint.

## Preservation verification

- Compared all assigned files against `/workspace/tooling/apec-style-edit/before`.
- SI quantity macro sequences and literal `\texttt{}` content are unchanged.
- All equation/align blocks, inline/display math, table blocks, figure blocks, citations, reference/label targets, source paths, and include/input paths are preserved.
- Existing LF/CRLF convention is retained per file.
- Verification output: `methods-results-validation.json` (zero failures).
- No build was run in this delegated task; the parent owns compilation and document-level checks.

## Existing issue passed to parent

- `10_Results/12_Compliance_Table.tex`, FR-04, still references “development burst photographs” after the earlier removal of the paired no-load photographs. The table was preserved in this pass; parent/root was notified for final consistency review.

## Edited files

| File | Before | After |
|---|---:|---:|
| `09_Experimental_Methods/01_Objectives.tex` | 261 | 224 |
| `09_Experimental_Methods/02_Safety_Arrangements.tex` | 267 | 197 |
| `09_Experimental_Methods/03_Test_Bench.tex` | 370 | 342 |
| `09_Experimental_Methods/04_Instrumentation.tex` | 349 | 301 |
| `09_Experimental_Methods/05_Probing.tex` | 297 | 248 |
| `09_Experimental_Methods/06_Test_Matrix.tex` | 272 | 226 |
| `09_Experimental_Methods/07_Control_Tests.tex` | 276 | 198 |
| `09_Experimental_Methods/08_Power_Quality.tex` | 201 | 141 |
| `09_Experimental_Methods/09_Efficiency.tex` | 183 | 146 |
| `09_Experimental_Methods/10_Thermal.tex` | 115 | 76 |
| `09_Experimental_Methods/11_Uncertainty.tex` | 287 | 229 |
| `09_Experimental_Methods/12_Revised_Plan_Validation.tex` | 1242 | 882 |
| `10_Results/01_Prototype_Verification.tex` | 460 | 369 |
| `10_Results/02_Startup_Shutdown.tex` | 99 | 54 |
| `10_Results/03_Steady_State.tex` | 922 | 839 |
| `10_Results/04_Load_Transients.tex` | 404 | 341 |
| `10_Results/05_Open_Circuit.tex` | 273 | 229 |
| `10_Results/06_ZVS.tex` | 409 | 358 |
| `10_Results/07_Input_Power_Quality.tex` | 722 | 635 |
| `10_Results/08_Efficiency.tex` | 487 | 415 |
| `10_Results/09_Thermal.tex` | 432 | 360 |
| `10_Results/10_Firmware_Comparison.tex` | 332 | 258 |
| `10_Results/11_Simulation_Hardware.tex` | 214 | 191 |
| `10_Results/12_Compliance_Table.tex` | 485 | 471 |
| `10_Results/13_Failures_Lessons.tex` | 396 | 319 |
| `10_Results/14_Revised_Plan_Status.tex` | 665 | 605 |
| `10_Results/15_V2_Testing_Update.tex` | 967 | 693 |
| `10_Results/16_V3_Design_Outcome.tex` | 312 | 235 |
