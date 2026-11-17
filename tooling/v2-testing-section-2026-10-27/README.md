# V2 testing section added to the thesis

The user's dictated V2 update was rewritten in direct, factual passive prose and added as **Section 10.15, V2 Testing and Resonant-Tank Changes**. The source is `Chapters/10_Results/15_V2_Testing_Update.tex` under `/workspace/thesis`.

The section records original-state testing, heating in the reported approximately 9.4 µH external series inductor, its removal, a roughly 1.66 nF leakage-only tank, lower half-bridge heating, persistent input-bridge heating after diode replacement, and proposed copper/placement changes. The later correction “60 Ms dead time for software” was interpreted in context as **60 ns programmed dead time**, replacing the earlier 16 ns statement; that interpretation was stated to the user. The firmware version and effective measured interval remain unrecorded.

Copper area is described as a likely contributor, not a proven loss allocation. Lower half-bridge heating is retained as an observation and the user's ZVS inference is distinguished from waveform verification. The earlier 100 W constant-power setting is not presented as a verified continuous rating. The reported bench inductor value is not silently equated with the schematic's nominal 10 µH L4 or the earlier V1.0 assembly. The frozen PWR-2.0.1 source and its 40 ns timing description remain historical.

## Files and artifacts

- Current source: `/workspace/thesis`, **471 files**, retaining every preceding path.
- Backup: `before/`, all **467** preceding files; `thesis-before.pdf`, the preceding **384-page** version.
- V2 excerpt: `V2_Testing_Section.pdf`, **2 pages**, copied from physical PDF pages 119–120 (printed pages 97–98). It includes the preceding section's short closing paragraph on its first page.
- Full PDF: `Richard_Xu_Thesis_V2_Testing_Update.pdf`, **386 A4 pages**, 16,864,169 bytes.
- Full editable source ZIP: `Thesis_V2_Testing_Update.zip`, **471 entries**, 80,564,465 bytes.
- Full PDF SHA-256: `d1c86f57b49847792c62ef835583fed0ef4b412965d783e624f409f52c62c858`.
- Source ZIP SHA-256: `70948a852fb22fee3b7b9bc2cec54067815c42e8ac1a897a17325a1b6bebca9b`.
- Excerpt SHA-256: `93b5fc099b6b933689dd56f10aca2194e2481a3e90940e1761a40e2f7969db66`.

`artifacts.json` and `SHA256SUMS` record the final sizes and hashes. The source ZIP's CRCs, paths, and every member hash were verified against the audited source.

Seven existing files were updated: the Results chapter input, its revised-plan status, the V2 hardware discussion, Abstract, Preface, Contributions, and README. Four files were added: the new section, the verbatim bench note, the original thermal photo, and its provenance JSON. The other **460** existing files remain byte-identical to the backup.

The original dictation and timing correction are retained in `Data/project_records/V2_Testing_Update.txt`. The documentary thermal image is retained unchanged at `Data/measurements/v2_results/evidence/v2_bridge_thermal_original.jpg`, alongside its provenance. Its displayed R3/R1 maxima are 70.0/61.5 °C. Region emissivity is 0.95; the global display is 0.97. The image is not used as a junction-temperature measurement, an identified diode-temperature map, or a matched before/after comparison. Its association with the later diode swap or timing change is unknown. The earlier user description of unstable operation was clarified to mean continued thermal rise with steady output voltage.

The V2 workbook and six header-only CSV templates remain unchanged. No synthetic measurements or invented waveform data were entered. The old quantitative V1.0/G071 figures, results, raw workbooks, equations, bibliography and frozen software remain unchanged. Only three qualitative status-table rows (AP-03, AP-05, AP-08) were updated to acknowledge the new observations.

## Validation and review

Completed successfully:

```bash
python3 /workspace/tooling/v2-testing-section-2026-10-27/audit-update.py
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/v2-testing-section-2026-10-27/check-pdf.py
python3 /workspace/tooling/verify-sources.py
python3 /workspace/tooling/v2-testing-section-2026-10-27/package-artifacts.py
```

The source audit checks the exact change/addition sets, all backup hashes, original numeric sequences, equations, command/argument sequences, protected environments, and existing newline styles. It explicitly allows only the three reviewed status-row replacements. Every other existing table, figure, caption and listing is preserved. The retained photo matches its original bytes/hash. The new section uses passive/impersonal prose. The exact original dictation and correction were independently checked against the user's supplied text.

The PDF contains all 12 chapters, References and appendices A–J, with 1,052,723 extracted text characters. There are no undefined citations/references, missing characters, multiply defined labels, overfull horizontal boxes or text outside physical page bounds. There are 90 nonfatal underfull-box messages and the existing small math-font substitutions. The status-table page and both V2 pages were visually inspected. A float barrier keeps the thermal figure from splitting the final paragraph. This is not a visual review of every page.

Independent technical review is recorded in `technical-review.md`; no findings remain. A README statement that initially combined the earlier load setting with the later timing note was corrected, preserving the unknown run association. Minor consistency edits retained the F410 identity and the distinction from planned V3 work. Final review hashes were refreshed after the layout-only float barrier.

The existing XeLaTeX/latexmk helper uses `main.tex`, sets the retained siunitx TEXINPUTS path, and writes auxiliary/PDF output to `/workspace/thesis-build`. Bibliography is manual; Biber is not required. No dependencies or tool activation changed. The cumulative source-change manifest now has **158 entries** (154 edited imported files and four new testing files); the separate prior 16-file V2 asset manifest is unchanged. Original source archives/import manifests and the selected clean GitHub reference remain unchanged.

This task recorded the user's bench observations; the agent did not operate or verify hardware. Switching frequency, exact fitted transformer/rectifier identities, measured timing, matched input/output power, thermal history and continuous capability remain incomplete. No firmware/web change, commit, push, release update, deployment, sharing change or environment publication occurred. Keep access Only me when the user reviews/saves and publishes the private snapshot. Draft saving does not establish publication, sharing state or restoration in a fresh task.
