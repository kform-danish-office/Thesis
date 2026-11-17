# USB-C power-supply framing and restored opening

Current editable source: `/workspace/thesis`. Current complete PDF and source ZIP: `Thesis_V1_V2_V3.pdf` and `Thesis_V1_V2_V3_Source.zip` in this directory. These supersede earlier current-artifact pointers.

The project is a USB-C power supply, as stated in its thesis title. The opening now returns to the original source's focus on the supplied DTU converter/magnetics and the changing USB-C load: no load at startup, variable power demand and disconnection with stored energy. It uses the established impersonal voice and the corrected project name. The current section inputs are retained, including the approved MCU-pin, V2 and V3 material.

The laboratory-supply classification was removed from the opening, abstract, preface, problem statement, aim and conclusion. The input-condition table now names the external AC source at the same recorded voltage/frequency. Nine exact text replacements were made; no broader prose rewrite. The latest explicit project-type correction governs the terminology when consulting old source versions.

## Checks

- 9 TeX files edited; 482 byte-identical files; all 491 source paths retained.
- Math, numerical/SI values, labels/citations, source inclusions, code, raw data and figures are unchanged. Exact edits and full diff: `edits.json`, `source-audit.json`, `framing.diff`.
- Independent original-source and final-diff reviews passed. Original ZIP text and restoration rationale: `original-intro-review.md`; final review: `final-review.md`.
- Full PDF text scan finds no laboratory/lab/bench-supply classification. The original load-focused opening is confirmed in the PDF and rendered for visual review.
- Complete XeLaTeX/latexmk build: 424 A4 pages, all 12 chapters, references, appendices A–J, four current V2 schematic sheets and 31 PCB pages. The colour schematics, direct captions, firmware-development explanation and equal 30 mm side margins remain.
- No missing references/citations/glyphs, overfull boxes or physical-page text overflow. Existing 81 underfull messages and math-font substitutions remain nonfatal.

```sh
python3 /workspace/tooling/thesis-project-framing/audit.py
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/thesis-project-framing/check-pdf.py
python3 /workspace/tooling/verify-sources.py
python3 /workspace/tooling/thesis-project-framing/package.py
```

Toolchain unchanged: XeTeX 0.999996 (TeX Live 2025/dev/Debian), latexmk 4.86, pdfinfo 26.05.0; manual bibliography, no Biber. Original archives/current source integrity and ZIP CRC/member hashes pass. Artifact hashes are in `artifacts.json` and `SHA256SUMS.txt`.

Project-framing guidance is saved in AGENTS.md and thesis-voice-guide.md. No firmware/web/hardware setting changes. The selected `/workspace/Thesis` checkout remains clean at `e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`. The existing authorized GitHub thesis download release is refreshed; no branch commit/push or environment sharing/publication change. Remote verification is recorded in `github-release/`.

## GitHub verification

Existing authorized GitHub thesis downloads refreshed at https://github.com/kform-danish-office/Thesis/releases/tag/thesis-v1-v2-v3-review. All three server SHA-256 digests/sizes and downloaded bytes match local artifacts. Downloaded source ZIP CRC and 491 entries pass. Evidence: /workspace/tooling/thesis-project-framing/github-release/published-state.json and download-verification.json. Selected reference checkout remains clean/unchanged; no branch commit/push or environment sharing/publication change.
