# Natural attribution wording

Replaced repeated “inherited” labels with contextual engineering wording: given/component measurements, supplied models or magnetics, and earlier DTU work. The component measurements retain their attribution to M’ani Gautason in Chapter 6 and its table caption. The author's assembled-converter measurements remain their own work.

43 exact substitutions in 33 files; 508 prior source files byte-identical. All 541 paths preserved. Numerical quantities, equations, labels, citations and source paths are unchanged. Historical source/data and current PWR-2.0.4 files are unchanged. Exact edits: edits.json and wording.diff. Byte/technical audit: audit.py and source-audit.json. Final independent review: final-review.md (no unresolved findings).

Commands:

- `python3 /workspace/tooling/thesis-natural-attribution/audit.py`
- `bash /workspace/tooling/build-thesis.sh`
- `python3 /workspace/tooling/thesis-natural-attribution/check-pdf.py`
- `python3 /workspace/tooling/thesis-natural-attribution/package.py`
- `python3 /workspace/tooling/verify-sources.py`

Full 492-page build passes, with all 12 chapters, references and appendices A–J. All four current V2 schematic sheets and 31 PCB pages remain. No missing glyphs, references or citations; no horizontal/vertical overfull boxes or physical-page text overflow. 82 nonfatal underfull horizontal messages and existing math-font substitutions remain. Main discussion page visually checked. Source ZIP CRC and all 541 member hashes pass. Original archives, approved current sources and selected reference checkout integrity pass. No firmware or hardware settings changed.

Toolchain unchanged: XeTeX 0.999996 / TeX Live 2025/dev/Debian; latexmk 4.86; Python 3.12.14.

The existing thesis review release is refreshed under the previous download-publication request. No commit or repository branch push is made. Private environment access remains Only me.
