# Chapters 07–08 prose review

Reviewed all 34 `.tex` files in `Chapters/07_Hardware` and `Chapters/08_Control_Firmware` in full. Revised 32 files. Kept the existing first-person account of the author's work and neutral explanations of circuit and controller behavior. Left already clear passages alone. No technical design, source-code, measurement, or firmware-version updates were made.

Changed files in `07_Hardware`: all 18 `.tex` files (`01_Prototype_Overview.tex` through `17_V3_Edge_Card_Plan.tex`, plus `chapter.tex`).

Changed files in `08_Control_Firmware`: `01_Control_Objectives.tex`, `02_Architecture_Timing.tex`, `03_Feedback_Calibration.tex`, `05_V1_Blocking_Closed_Loop.tex`, `06_Blocking_Limitations.tex`, `08_Control_Law.tex`, `09_Limits_Antiwindup.tex`, `10_Open_Circuit_Safety.tex`, `11_State_Machine.tex`, `12_Fault_Handling.tex`, `13_Timing_Resources.tex`, `14_Version_Comparison.tex`, `15_PWR_2_Port.tex`, and `chapter.tex`. Reviewed but left unchanged: `04_V0_Open_Loop.tex` and `07_V2_DMA.tex`.

Examples:

- Replaced the dense pump-margin list ending in “link ripple/peak voltage” with a direct description of the required current, voltage-ripple, peak-voltage, and overshoot measurements, followed by the comparison with part ratings.
- Split the integrated-driver paragraph into the reduced connection count and the remaining board requirements. Kept device delays separate from programmed timer dead time.
- Replaced “The remaining auxiliary checks are operation over the input range and a timed thermal test” with “I still need to check auxiliary operation over the input range and run a timed thermal test.”
- Split the blocking-ADC explanation into the conversion wait, its execution-time cost, and the reason to remove the wait.
- Removed the formulaic “The exit condition is important” lead-in while retaining the readiness-or-attempt-limit startup behavior.
- Split the flash-journal wear distribution and interrupted-erase limitation into separate sentences.

Preserved the modified V1.0 measured assembly, unmanufactured V1.1/V1.2 revisions, frozen PWR-2.0.1 software port, reported V2 power point, and planned V3 work as separate evidence states. Requirements for future measurements remain requirements, rather than claims of completed validation.

Checks against `/workspace/tooling/thesis-tone-review/original-source` passed for all 34 files: the complete numeric-literal sequence, LaTeX command sequence and adjacent arguments, inline/display math, protected figure/table/tabular/equation/align/listing/verbatim/TikZ environments, and exact per-file LF/CRLF newline sequence are unchanged. No protected-content differences were found. No compilation was run by this delegated task.

Existing technical questions retained without correction:

- V2 divider labels still disagree with the firmware conversion assumptions; fitted resistor values and measured node-to-pin gain are needed. Direct ADC loading and settling also remain to be checked.
- V2 resonant component and transformer definitions remain incomplete; the final V1.0 series-inductor arrangement cannot supply those missing values.
- Effective gate/enable timing, commutation current, and jitter still need hardware captures. No matched timing comparison isolates the DMA change.
- The reported V2 power point still needs an identified assembly and a matched power/temperature/duration/settings record. No continuous rating or numeric V2/V3 power-density improvement was inferred.
- V3 connector geometry, interface definitions, spacing assumptions, fabrication, and readiness checks remain planned work.
