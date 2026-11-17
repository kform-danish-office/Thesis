# Direct engineering language and colour V2 schematics

Current editable source: `/workspace/thesis`. Current complete PDF and editable source ZIP: `Thesis_V1_V2_V3.pdf` and `Thesis_V1_V2_V3_Source.zip` in this directory. These supersede earlier current-artifact pointers.

The wording pass includes headings, captions, qualitative table text and generated documentation, as well as paragraphs. MCU connections are called pins. Table 1.1 now reads “MCU pin assignments for the original controller and V2.” Table 4.2 is introduced as the prototype calculation parameters. Chapter 5 opens with charge-transfer, resonant-gain/phase and sensitivity calculations. Section 8.5 explains each firmware stage through the problem, change and functional improvement: manual bring-up, automatic voltage feedback, removal of blocking ADC waits, corrected bulk-voltage feedback, and startup/no-load/loaded control. It does not claim unmeasured quantitative gains.

Repeated organizing/disclaimer language was shortened across the thesis. Necessary measurement uncertainty remains beside the measurements it affects. The author's factual, practical engineering voice and APEC-style technical density are preserved. Model identifiers remain where they identify actual parts/comparisons; firmware versions remain in the introduced version and run records.

## Colour schematics

Approved source: `/workspace/source-archives/_SCH DWG NO__SCH.PDF`, copied byte-for-byte to `Pictures/Thesis/07_Hardware/Schematic_V2_Colour.pdf`. SHA-256: `7af67969cea32d270498dacdd244b937c2496f113b85038893dbc88260f8d031` (1,072,022 bytes, four pages). Page dimensions and functional text match the previous current V2 master; only off-circuit title hash/refresh strings differ. Original grey masters remain unchanged as historical source records.

All four current main-text crop PDFs were regenerated from the colour source with identical rectangles and dimensions, retaining vectors and circuit labels. The five main V2 figures and four current appendix sheets visibly render in colour. The complete source/region/raster comparisons are recorded in `colour-source-comparison.json`, `colour-crop-manifest.json`, `colour-assets-notes.md` and `colour-and-wording-pdf-check.json`.

## Preservation and review

- 142 existing files edited, including 136 TeX files; 348 unchanged; one colour master added; 491 current source files.
- Mathematical expressions, SI quantities, all seven original/V2 pin-assignment data rows, original drawings and raw measurements remain intact. Firmware and web source files are unchanged.
- Twelve generated table files changed only in approved captions and two qualitative headers. Eleven presentation string constants in their generator were updated; restoring those constants makes its Python AST identical to the original. Calculation logic, numerical rows, test IDs and stored exclusion/status strings are unchanged.
- Only the SHA-256 and size fields for those twelve generated tables were refreshed in the output checksum ledger. Other entries are identical.
- All wording changes have exact replayable maps. Root, early, hardware/control, results and appendix reviews found no remaining meaning regressions. The final firmware-stage explanation has its own read-only review. See `*-notes.md`, `*-independent-review.md`, `stage-rationale-review.md`, `source-audit.json` and `all-wording.diff`.

## Validation

```sh
python3 /workspace/tooling/thesis-direct-language/audit.py
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/thesis-direct-language/check-pdf.py
python3 /workspace/tooling/thesis-direct-language/check-colour-wording.py
python3 /workspace/tooling/verify-sources.py
python3 /workspace/tooling/thesis-direct-language/package.py
```

Full build: 424 A4 pages, all 12 chapters, references, appendices A–J, all four current V2 schematic sheets and 31 PCB pages. The main pin table, calculation table, model opening, firmware development and colour diagrams were rendered and inspected. The firmware-stage table uses left-aligned columns to avoid stretched spacing and split stage names. Symmetric 30 mm body side margins remain unchanged. No missing references/citations/glyphs, overfull boxes or text outside physical page bounds. Existing 81 underfull horizontal messages and math-font size substitutions remain nonfatal.

Tools: XeTeX 0.999996 (TeX Live 2025/dev/Debian), latexmk 4.86, pdfinfo 26.05.0, PyMuPDF 1.26.6. Manual bibliography, no Biber. Original archive hashes/CRCs, imported skills, retained assets and current source hashes pass. Source ZIP CRC and all member hashes pass; artifact hashes are in `artifacts.json` and `SHA256SUMS.txt`.

Source paths remain `/workspace/thesis` and `/workspace/working-source`. The selected `/workspace/Thesis` checkout remains clean at `e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`. No firmware/hardware setting, branch commit/push, or environment sharing/publication change. The existing authorized GitHub thesis download release is refreshed; remote verification is recorded in `github-release/`.

## GitHub verification

Existing authorized GitHub thesis downloads refreshed at https://github.com/kform-danish-office/Thesis/releases/tag/thesis-v1-v2-v3-review. All three remote SHA-256 digests/sizes and downloaded bytes match local artifacts. Downloaded source ZIP CRC, 491 entries and approved colour master SHA-256 pass. Evidence: /workspace/tooling/thesis-direct-language/github-release/published-state.json and download-verification.json. Selected reference checkout remains clean/unchanged; no branch commit/push or environment sharing/publication change.
