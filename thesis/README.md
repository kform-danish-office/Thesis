# Charge-pump PFC USB-C thesis — rewritten October 2026

This is the editable source of Richard Xu's thesis. The complete text, result
figures, measurement appendix, V1.0/V1.1 schematics, and the V2 F410 drawing
are included. The thesis also reproduces both complete firmware versions and
the complete supporting software source in line-numbered appendices.

The text builds on the October 20 revision. It follows the engineering work
from the original DTU converter and supplied magnetics through hardware
integration, feedback and timing changes, detachable-load control, measured
results, and the later V2/V3 work. Direct, factual American English and passive
reporting are used. Technical equations, figures, tables, citations, source code,
attribution, and the distinction between measured and planned work are preserved.

## Compile

Upload the source ZIP to Overleaf, select `main.tex`, and use **XeLaTeX**.
The reference list uses `thebibliography`; Biber is not required. The complete
project has been compiled with XeLaTeX and latexmk in the cloud environment. Author and submission metadata are
in `Setup/Statics.tex`. The current date reflects the October submission plan.

## Measurement data and figures

- Original workbooks and instrument images: `Data/measurements`.
- Completed electrical, AC-detail, harmonic, thermal, and transient tables:
  Appendix E and `Data/measurements/processed_rewrite`.
- Original waveform copies and their SHA-256 register: `processed_rewrite/raw_waveforms`
  and `raw_waveform_index.csv`.
- Eight rebuilt figures, each as vector PDF and PNG:
  `Pictures/Thesis/10_Results/Rebuilt`.
- Four vector schematic excerpts: `Pictures/Thesis/07_Hardware/Rebuilt`.
- Full V1.0 and V1.1 schematic PDFs: `Pictures/Thesis/07_Hardware`, also reproduced
  in Appendix B.
- Final firmware snapshot: `Code/thesi_power_control_PWR_1_9_20.ino`.

`Data/analysis/rebuild_results.py` regenerates the charts and data tables with
Python, NumPy, and Matplotlib. Run it from any directory:

```text
python Data/analysis/rebuild_results.py
```

The included raw copies are used when the original local acquisition folders
are unavailable. They retain the exported samples and offsets. No waveform is
rescaled to force a target line voltage or input power. Detailed processing
choices are recorded in `processing_provenance.txt` and `figure_manifest.json`.

## Interpretation

The measured assembly is the V1.0 PCB with rework, not a separately manufactured
V1.1 board. The thesis separates drawing changes, fitted hardware, supplied
magnetic design, and original integration/control work. Inconsistent input-power
records, AC statistic ranges, unverified raw-channel calibration, and absent
thermal endurance measurements are identified in the results and appendix.
Planned test rows are retained in the CSV register but are not measurements.

## Language

Use direct American English throughout the thesis and defense materials.
Methods, results, and project actions are reported in natural passive or
impersonal form. Use short, concrete sentences and familiar engineering terms.
Keep definitions and circuit behavior direct; avoid forced passive sentences,
vague claims, and repeated statements about what the document contains.
Proposed tests retain conditional wording, and estimates remain distinct from
measurements. Quotations and frozen source listings retain their original text.

## V2 and complete source

Project V2 is the development described in the October plan and the later
STM32F410 schematic. Its full four-sheet drawing is in Appendix B. The plan's
reported approximately 85 W baseline is kept separate from the matched
79.89 W result on the earlier V1.0 assembly. Neither establishes the 100 W
continuous target.

Preliminary powered V2 observations are recorded in
`Chapters/10_Results/15_V2_Testing_Update.tex`. An earlier load observation used
a 100 W constant-power setpoint. The latest note reports approximately 60 ns
software dead time; its firmware version and association with that earlier run
were not recorded. Matched input--output measurements and
thermal-endurance testing are still needed; no new continuous rating is established.

- Controller implementation and commands: Appendix C.
- Browser, build, test, and analysis documentation: Appendix G.
- Complete PWR-1.9.20 and current V2 firmware: Appendix H.
- Complete supporting software, test, and analysis files: Appendix I.
- Current V2 software: `Code/PWR_2_0_4`; historical V2 snapshot: `Code/PWR_2_0_1`.
- File identities, physical line counts, and SHA-256 checksums:
  `Code/source_manifest.json`.

The full listings read the frozen files directly, without selecting line
ranges. Generated build products, third-party libraries, and intermediate
historical duplicates are not separate source implementations. The current calculator is included in the application build and local server, with its UI module, magnetic presets, tests and fonts.

The current F410 source builds as PWR-2.0.4; G071 remains PWR-2.0.3 with fixed carrier timing. The F410 HEX passed the vector, checksum and reserved-settings-sector checks. All 76 browser tests, 131 protocol frames and storage tests including 122 interrupted-append boundaries passed. The current firmware adds browser calibration, reference-load/setup controls and output-OFF carrier/dead-time adjustment. Powered validation remains pending. Earlier measured results retain their original test configurations.

## Revised July–October plan

The revised July 27–October 27, 2026 plan is incorporated into the introduction,
requirements, modeling, hardware, methods, results, discussion, and conclusions.
Chapter 3 defines criteria AP-01–AP-08; Chapter 10 assesses them against the
available records. Appendix J connects the planned milestones to the chapters.
The original plan source and its 14-page PDF remain in `Data/project_records`.
The earlier working draft is retained there as `Original_Project_Definition.tex`.

The current plan sets a 65 W continuous minimum and a 100 W continuous target.
The 75 W figure is retained as an earlier validation milestone. The reported
approximately 85 W V2 baseline needs its own repeatable, matched test record;
the reconstructed measured result remains 79.89 W on the modified V1.0 assembly.
The 15 W planning shortfall, 20.11 W shortfall from that matched result, and
24.53 W screening input–output difference are separate quantities.

The V3 edge-card design brief, release checks, V2/V3 volume method, PDO/PPS tests,
and extended thermal/stability work are documented with their current evidence
status. Scheduled dates do not establish completion. No V3 build, continuous
rating, or numeric V2/V3 power-density improvement is inferred from the plan.

Latest V2 photo clarification: the thermal image is from a user-reported 95 W run.
Its earlier association with the 100 W setting is superseded; whether 95 W is
a setpoint or measured output is unspecified. Three original board/setup photos
are included in Section 10.15 and retained with the V2 evidence.

Current development narrative: V1 establishes the measured baseline; V2 adds integrated control and tank/thermal observations; V3 is a slimmed edge-card layout with the USB-PD section removed and secondary rectifiers retained. Approximately 8% net volume reduction is a design estimate for the reduced-function layout, not a measured complete-system power-density gain. New planar magnetics were not installed. The 3.3–3.6 A secondary-output region, suspected transformer limit and possible input via bottleneck remain qualitative bench findings. The project target remains 100 W. The question of higher-load operation, including 240 W USB-PD EPR, arose from feedback on the APEC digest.
