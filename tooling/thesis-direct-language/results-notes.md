# Results and discussion: direct language pass

Scope reviewed: all prose, headings, captions and qualitative table wording in Chapters 9–12. The latest user request explicitly included table/caption text, which earlier prose-only passes had left unchanged. The revisions describe parts, tests and results directly while keeping the technical density and the author's factual, impersonal engineering voice.

Thirty-five TeX files were edited. The changes replace abstract evidence/identity/metadata/interpretation language where concrete terms are clearer. Captions identify the measurement or figure; tables use ordinary labels such as “Test configuration”, “Capture type”, “Measurements needed” and “Status”. Openings state the actual measured output, control behavior or development work rather than explaining how the thesis organizes evidence. Valid technical terms and actual test limitations remain where needed; this was not a blind word replacement.

## Examples

### Chapter 9 table caption

Before: Safety and connection metadata relevant to an energized test.

After: Connections and settings needed for powered tests.

### Chapter 10 requirement table

Before: Evidence-based assessment of the prototype requirements.

After: Prototype requirements and test results.

### Chapter 10 switching table

Before: Evidence & Supported interpretation

After: Capture & Observation or missing measurement

### Chapter 10 model table

Before: Scope of the comparison between inherited simulation and hardware.

After: Comparison of the inherited models with the prototype measurements.

### Chapter 10 no-load table

Before: Evidence type

After: Capture type

### Chapter 10 V2 photographs

Before: The photographs show the V2 hardware and test setup; a common test configuration across all images has not been verified.

After: The caption now simply names the three views. The surrounding prose still notes that the photos do not identify the exact fitted thermal-test setup.

### Chapter 11 diagnostic table

Before: Matched baseline/retest record and resulting decision

After: Measurements needed

### Chapter 12 opening

Before: The conclusions separate demonstrated operating points and layout changes from unresolved loss mechanisms and continuous-power performance.

After: The tests demonstrated output regulation and identified magnetic and input-path heating as priorities for further development.

## Scientific meaning preserved

- The main numerical dataset remains the V1 test assembly. Firmware identities in its table are unchanged, including the earlier high-load record and unidentified intermediate-voltage runs.
- Initial efficiency estimates still carry instrument, synchronization and auxiliary-power uncertainty.
- Thermal readings remain surface temperatures. Missing run duration/airflow means equilibrium cannot be checked; the language does not claim temperatures were definitively non-steady.
- The V2 thermal image remains a reported 95 W run, distinct from the separately reported 100 W load setting. The caption keeps the 70.0°C and 61.5°C readings and the unknown fitted diode/timing changes.
- The 3.3–3.6 A observation remains at the secondary output and is not converted to connector watts. V3's 8% remains an estimated volume reduction after omitting USB-PD; 240 W EPR remains future work.
- No startup capture, component-loss breakdown, continuous rating, ZVS proof or protocol conformance was invented. Future test tables remain plans rather than claimed completed measurements.

## Preservation checks

`python3 /workspace/tooling/thesis-direct-language/validate-results.py` passes. Math, SI expressions, table-row numerical content, labels/references/citations/source paths, complete equation and code environments, line-ending styles, pin assignments and measurement values match the frozen baseline. There is one deliberate nonmeasurement numeric-token exception: a redundant second “V2” was removed from the board-photo caption. All quantitative values remain unchanged.

No source data, code, firmware, graphics/assets, build settings, source manifest, GitHub or hardware operations were changed by this task. The parent agent owns the colour schematic replacement and final build/publication.

The exact edit list is `results-edits.json`; the complete baseline diff is `results-prose.diff`; checks are in `results-validation.json`.

## Edited files

- `Chapters/09_Experimental_Methods/01_Objectives.tex`
- `Chapters/09_Experimental_Methods/02_Safety_Arrangements.tex`
- `Chapters/09_Experimental_Methods/03_Test_Bench.tex`
- `Chapters/09_Experimental_Methods/04_Instrumentation.tex`
- `Chapters/09_Experimental_Methods/05_Probing.tex`
- `Chapters/09_Experimental_Methods/06_Test_Matrix.tex`
- `Chapters/09_Experimental_Methods/07_Control_Tests.tex`
- `Chapters/09_Experimental_Methods/11_Uncertainty.tex`
- `Chapters/09_Experimental_Methods/12_Revised_Plan_Validation.tex`
- `Chapters/10_Results/01_Prototype_Verification.tex`
- `Chapters/10_Results/02_Startup_Shutdown.tex`
- `Chapters/10_Results/03_Steady_State.tex`
- `Chapters/10_Results/04_Load_Transients.tex`
- `Chapters/10_Results/05_Open_Circuit.tex`
- `Chapters/10_Results/06_ZVS.tex`
- `Chapters/10_Results/07_Input_Power_Quality.tex`
- `Chapters/10_Results/08_Efficiency.tex`
- `Chapters/10_Results/09_Thermal.tex`
- `Chapters/10_Results/10_Firmware_Comparison.tex`
- `Chapters/10_Results/11_Simulation_Hardware.tex`
- `Chapters/10_Results/12_Compliance_Table.tex`
- `Chapters/10_Results/13_Failures_Lessons.tex`
- `Chapters/10_Results/14_Revised_Plan_Status.tex`
- `Chapters/10_Results/15_V2_Testing_Update.tex`
- `Chapters/10_Results/16_V3_Design_Outcome.tex`
- `Chapters/11_Discussion/01_Key_Findings.tex`
- `Chapters/11_Discussion/03_Control_Contribution.tex`
- `Chapters/11_Discussion/06_Reference_Comparison.tex`
- `Chapters/11_Discussion/08_Lessons_Learned.tex`
- `Chapters/11_Discussion/09_Future_Improvements.tex`
- `Chapters/11_Discussion/10_Plan_Gap_Diagnosis.tex`
- `Chapters/12_Conclusion/01_Project_Summary.tex`
- `Chapters/12_Conclusion/03_Contributions.tex`
- `Chapters/12_Conclusion/04_Future_Work.tex`
- `Chapters/12_Conclusion/chapter.tex`

## Review status

A separate read-only scientific-meaning review checked the complete 35-file diff and found no actionable issues. It independently verified SI/math/reference/source-path invariants and the startup, thermal, firmware and V1/V2/V3 qualifications. See `results-independent-review.md`. No findings remain. Sources are frozen.
