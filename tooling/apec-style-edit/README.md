# Technical thesis prose revision

Current editable source: `/workspace/thesis`. Current full PDF and editable source ZIP: `Thesis_V1_V2_V3.pdf` and `Thesis_V1_V2_V3_Source.zip` in this directory. These supersede earlier current-artifact pointers.

The user requested the technical density of an APEC digest. The elementary electronics/MCU tutorial was replaced by a compact control-architecture and board-specific signal section. Main chapters and limited explanatory appendix prose were tightened around circuit operation, design rationale, implementation and measured results. The full thesis format remains. No separate APEC digest manuscript was available locally; the edit does not claim to reproduce one.

The user's direct, factual, mostly impersonal voice is retained. Project-specific signals remain introduced by function. MCU model and firmware identities remain where needed for actual comparison and test/source identification. Previous photo removals, crop-only cover and absence of handoff dates remain preserved.

## Scope and evidence

- 131 TeX files edited; 355 source files unchanged; all 486 source paths retained.
- Edited-file whitespace-delimited source counts: 47,690 before and 38,042 after (20.2% reduction). Counts include commands and unchanged tables/captions, and are not a manuscript word limit.
- Math occurrences, numerical SI expressions, labels, citations, graphics/source paths and protected figures/tables/listings match the baseline, except the explicitly documented FR-04 correction of a stale removed-photo evidence description. Repeated references to the superseded primer were removed. Original data, code, firmware, schematics and PCB PDFs are unchanged.
- Independent reviews covered the abstract/introduction, Chapters 2–6, Chapters 7–8, and Chapters 9–12/Appendices C/G. Findings about startup captures/attempt limits, efficiency uncertainty and loss attribution were corrected and verified; no open findings remain. See `*-review.md`.
- V1 numeric results remain separate from V2 qualitative observations. The 95 W thermal record is not a continuous rating; 60 ns is reported software dead time with unidentified bench firmware, distinct from archived 40 ns. Secondary current, suspected via/winding causes, the reduced-function V3 8% estimate, and future 240 W goal retain their qualifications.

## Validation

Commands run:

```sh
python3 /workspace/tooling/apec-style-edit/audit.py
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/apec-style-edit/check-pdf.py
python3 /workspace/tooling/verify-sources.py
python3 /workspace/tooling/apec-style-edit/package.py
```

Full XeLaTeX/latexmk build: 424 A4 pages, all 12 chapters, References and Appendices A–J. All four current V2 schematic sheets and 31 PCB pages remain embedded. No missing references, citations or glyphs, overfull boxes, or text outside physical page bounds. Selected introduction, control, modeling and conclusion pages were rendered and inspected. Nonfatal 106 underfull horizontal boxes and pre-existing math-font size substitutions remain. No Biber is used.

Tools: XeTeX 0.999996 (TeX Live 2025/dev/Debian), latexmk 4.86, pdfinfo 26.05.0. All original import archive hashes/CRCs, approved current source hashes, retained V2 assets and 118 imported skill files pass. Packaged ZIP CRC and every member hash pass; artifact hashes are in `artifacts.json` and `SHA256SUMS.txt`.

The selected `/workspace/Thesis` checkout remains clean at `e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`. Firmware/web workflows and hardware settings were not changed. No branch commit/push or environment sharing/publication change is part of this pass. GitHub release asset refresh continues the user's previously explicit request for downloadable thesis files; remote verification is stored in `github-release/`.

## GitHub verification

Existing authorized GitHub thesis review release refreshed at https://github.com/kform-danish-office/Thesis/releases/tag/thesis-v1-v2-v3-review, preserving PDF/source download URLs. All three GitHub asset SHA-256 digests and sizes match local files, and downloaded bytes independently match; downloaded source ZIP CRC and 486 entries pass. Evidence: /workspace/tooling/apec-style-edit/github-release/published-state.json and download-verification.json. Selected reference checkout remains clean/unchanged; no branch commit/push or environment sharing/publication change.
