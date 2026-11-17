# Source integrity audit

Result: PASS. Compared the complete current thesis tree against `/workspace/tooling/thesis-terra-rewrite/Thesis_V1_V2_V3_Source.zip` by SHA-256, including every original file, not only selected extensions.

Baseline: 541 files. Current: 566. Unchanged byte-for-byte: 521. Changed: 20. Added: 25. Deleted: 0.

All 20 modified baseline paths are LaTeX files present in the lead judgement records. The 25 additions comprise the new results subsection and its 24 dataset files. No unexpected paths changed.

All 367 existing Data/, Pictures/, Code/, and Firmware/ files are byte-identical to the baseline. Other unchanged paths, including additional source/code locations, are listed with hashes in the JSON. No historical data, photographs, schematic PDFs, or embedded code was replaced.

All seven new raw CSVs match the import-manifest hashes, the dataset source-manifest hashes, and their still-accessible original attachment files. All eight retained thermal JPEGs match the import-manifest hashes and original ZIP member bytes. The ZIP hash also matches its recorded import hash. The eight members contain seven unique hashes: the two Capture 022 files are byte-identical. No imported original has been modified.

## Changed paths

- `Backmatter/Appendices/E_Experimental_Data.tex`
- `Chapters/01_Introduction/03_Aim_Objectives.tex`
- `Chapters/01_Introduction/09_V3_Development.tex`
- `Chapters/07_Hardware/16_V2_F410.tex`
- `Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex`
- `Chapters/09_Experimental_Methods/09_Efficiency.tex`
- `Chapters/09_Experimental_Methods/10_Thermal.tex`
- `Chapters/10_Results/12_Compliance_Table.tex`
- `Chapters/10_Results/14_Revised_Plan_Status.tex`
- `Chapters/10_Results/15_V2_Testing_Update.tex`
- `Chapters/10_Results/16_V3_Design_Outcome.tex`
- `Chapters/10_Results/chapter.tex`
- `Chapters/11_Discussion/01_Key_Findings.tex`
- `Chapters/11_Discussion/05_Magnetics_Integration.tex`
- `Chapters/11_Discussion/07_Limitations.tex`
- `Chapters/11_Discussion/09_Future_Improvements.tex`
- `Chapters/11_Discussion/10_Plan_Gap_Diagnosis.tex`
- `Chapters/12_Conclusion/01_Project_Summary.tex`
- `Chapters/12_Conclusion/02_Research_Questions.tex`
- `Frontmatter/Abstract.tex`

## Added paths

- `Chapters/10_Results/17_V2_Secondary_Load_Tests.tex`
- `Data/measurements/v2_load_thermal/README.md`
- `Data/measurements/v2_load_thermal/load_performance.pdf`
- `Data/measurements/v2_load_thermal/load_performance.png`
- `Data/measurements/v2_load_thermal/load_table.tex`
- `Data/measurements/v2_load_thermal/process.py`
- `Data/measurements/v2_load_thermal/raw/Capture 015.csv`
- `Data/measurements/v2_load_thermal/raw/Capture 017.csv`
- `Data/measurements/v2_load_thermal/raw/Capture 018.csv`
- `Data/measurements/v2_load_thermal/raw/Capture 019.csv`
- `Data/measurements/v2_load_thermal/raw/Capture 020.csv`
- `Data/measurements/v2_load_thermal/raw/Capture 021.csv`
- `Data/measurements/v2_load_thermal/raw/Capture 022 (2).csv`
- `Data/measurements/v2_load_thermal/source_manifest.json`
- `Data/measurements/v2_load_thermal/summary.csv`
- `Data/measurements/v2_load_thermal/summary.json`
- `Data/measurements/v2_load_thermal/thermal/Capture 015-thermal.jpg`
- `Data/measurements/v2_load_thermal/thermal/Capture 017-thermal.jpg`
- `Data/measurements/v2_load_thermal/thermal/Capture 018-thermal.jpg`
- `Data/measurements/v2_load_thermal/thermal/Capture 019-thermal.jpg`
- `Data/measurements/v2_load_thermal/thermal/Capture 020-thermal.jpg`
- `Data/measurements/v2_load_thermal/thermal/Capture 021-thermal.jpg`
- `Data/measurements/v2_load_thermal/thermal/Capture 022-thermal (1).jpg`
- `Data/measurements/v2_load_thermal/thermal/Capture 022-thermal.jpg`
- `Data/measurements/v2_load_thermal/thermal_figures.tex`

## Deleted or unexpected paths

None.

Audit was read-only for the thesis and archives. No build, source edit, or publication was performed. Only these two requested audit outputs were written.
