# V2 secondary-output load and thermal results

Current editable thesis: `/workspace/thesis`. Current firmware/browser source: `/workspace/working-source`. The selected reference checkout remains `/workspace/Thesis` at `e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`.

The V2 results now include seven secondary-load readings, a numerical table, a voltage/temperature plot and all seven unique original thermal images. Only AC-supply and electronic-load rows are used from the new CSV captures. Their scope rows are excluded. Original V1 measurements and waveform figures are preserved.

Calculated secondary power reaches 137.08 W at 13.69 V and 10.01 A, with voltage droop. None of these load points reached thermal equilibrium. R3 covers the input bridge and R1 the secondary area. Capture 017's inconsistent input power/current/voltage readings remain flagged locally. Diode and thermal-path work is discussed without assigning a confirmed cause.

Four Terra agents proposed the initial data/results/methods/narrative integration. The lead accepted 15 proposals, revised nine, rejected one and made two connecting edits. Astra independently verified the final calculations and interpretation; Terra reviewed the final prose. Their six proposals were judged individually: three accepted and three revised. Exact proposals, judgments and source backups are retained here; the voice checklist is `../thesis-agent-voice-checklist.md`. Final Terra review found no further concrete defect.

## Validation

- Full XeLaTeX/latexmk build: 496 pages; manual bibliography, no Biber.
- All 12 chapters, references and appendices A–J; four current V2 schematic sheets and 31 PCB sheets present.
- No missing glyphs, undefined references/citations, overfull horizontal/vertical boxes or text outside physical pages. Existing 81 underfull horizontal boxes and math-font size substitutions remain.
- New V2 section: PDF pages 120–125, printed pages 98–103. The lead inspected the table, plot, first image plate and last image plate. All seven original JPEG streams are embedded unchanged exactly once.
- Compared with the previous complete source archive: 20 intended LaTeX files changed, 25 files added, 521 files unchanged and no deletions. All 367 historical data/image/code assets are byte-identical.
- Seven CSVs match their attachments and manifests. Eight thermal files match the original ZIP; the Capture 022 duplicate is retained in the source but displayed once.
- Original source ZIPs, imported skills, current firmware/web revision and the selected clean GitHub checkout passed the existing source integrity checks.
- The 566-file thesis source ZIP passed CRC and per-member SHA-256 checks.

## Commands and artifacts

```bash
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/thesis-v2-load-thermal/check-pdf.py
python3 /workspace/tooling/thesis-v2-load-thermal/check-v2-pdf.py
python3 /workspace/tooling/verify-sources.py
python3 /workspace/tooling/thesis-v2-load-thermal/package.py
python3 /workspace/local-handoff/package.py
```

Derived data can be regenerated with `MPLCONFIGDIR=/tmp/thesis-mpl python3 /workspace/thesis/Data/measurements/v2_load_thermal/process.py`. `tool-versions.json` records the tested versions. In particular, XeTeX is 0.999996 (TeX Live 2025/dev/Debian), latexmk 4.86, Python 3.12.14, PyMuPDF 1.26.6 and matplotlib 3.10.8.

Current artifacts are `Thesis_V1_V2_V3.pdf`, `Thesis_V1_V2_V3_Source.zip` and `SHA256SUMS.txt` in this directory. The complete local-work bundle is `/workspace/local-handoff/Thesis_Local_Handoff.zip`, with firmware/web sources, skills, original archives and tooling records. Its `LOCAL_START.md` explains local tool installation and adapting `/workspace` paths. Toolchains and dependency caches must be installed locally; no credentials are included.

Publication uses the existing user-authorized `thesis-v1-v2-v3-review` release. The release remains a prerelease and the reference branch is unchanged. Publication and SHA-256 verification records are kept separately in `release-*.json` and `asset-verification.json`.
