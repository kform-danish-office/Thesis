# Results, discussion and conclusion: APEC-style prose pass

The requested direction was concise technical conference prose. No APEC digest manuscript was present locally, so this pass follows the general style rather than claiming an exact match. The current request supersedes the earlier beginner-oriented explanation preference.

## Chapters 11–12 and Appendix C/G

Counts are whitespace-delimited source words, including retained LaTeX material; they are not rendered-PDF word counts.

| Scope | Files | Before | After | Reduction |
|---|---:|---:|---:|---:|
| Chapters/11_Discussion | 11 | 3358 | 2300 | 31.5% |
| Chapters/12_Conclusion | 5 | 1678 | 1168 | 30.4% |
| Backmatter/Appendices/C_Firmware_Documentation.tex | 1 | 5496 | 5406 | 1.6% |
| Backmatter/Appendices/G_Software_Tools.tex | 1 | 2294 | 2186 | 4.7% |

The discussion and conclusion now state operating conditions, measured results, likely mechanisms, and unresolved limits directly. Tutorial definitions of basic MCU peripherals and USB/UART conversion were condensed in the appendices; function context before pin IDs and operational reference details remain. Section names were tightened where useful (for example, “Experimental Limitations” and “Power-Shortfall Diagnosis”).

Examples:

- “Blocking conversion waits were replaced by circular DMA, which transfers new sensor readings automatically into a memory buffer” became “Circular DMA replaced blocking ADC conversion waits.” Its consequence—an acquisition delay can admit another energy packet before inhibition—remains.
- The repeated explanation that a reduced hotspot does not establish more output was condensed to separate hotspot relocation, estimated design volume, and sustained power.
- Repeated future-test instructions were combined into matched current/power/temperature measurements, controlled individual changes, and defined-duration validation.

Preserved evidence boundaries:

- V1 provides the matched numeric baseline; V2 observations remain preliminary and separate.
- The 3.3–3.6 A region refers to secondary output current.
- The 8% V3 reduction is an estimated reduced-function layout result, with external USB-PD hardware required for equivalent functionality.
- The transformer and single-via restriction remain suspected limitations. Lower half-bridge heating is reported without using it as proof of ZVS.
- 100 W remains the immediate objective; 240 W EPR remains a future goal.

Verification compared all edited files with `/workspace/tooling/apec-style-edit/before`. SI quantity sequences, inline/display mathematics, citations, labels, cross-references, source paths, and complete table/longtable, figure, equation/align, and listing blocks are unchanged. LaTeX brace balance is unchanged. No code, measurement data, builds, manifests, commits, pushes, deployments or publication were performed by this agent.

## Chapters 9–10

Completed and frozen by `methods_results_compress`: 28 subsection files, 11,699 → 9,582 source words (18.1% reduction). The pass tightened methods, revised validation procedures, result summaries, and V2/V3 interpretation while preserving all numeric and evidence distinctions. Its notes are in `methods-results-notes.md`; `methods-results-validation.json` records zero preservation failures. I also reviewed the revised V2/V3 result sections for consistency with the user’s observations.

The stale FR-04 evidence phrase was flagged for root review. Our edits leave that table untouched; root will replace the obsolete photograph description with an evidence-supported phrase and record the exception separately.

All 46 edited thesis files in this assigned scope are frozen for root’s compilation and final document review. No source edits remain in progress.
