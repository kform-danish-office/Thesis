# Uniform thesis margins

Current editable source: `/workspace/thesis`. Current complete PDF and source ZIP: `Thesis_V1_V2_V3.pdf` and `Thesis_V1_V2_V3_Source.zip` in this directory. These supersede earlier current-artifact pointers.

The inherited two-sided report layout used inner=35 mm and outer=25 mm. That shifted the body text by 10 mm on consecutive pages. The body geometry in `main.tex` now uses equal 30 mm left and right margins. The 150 mm text width, text height, top/bottom dimensions and two-sided pagination remain unchanged. The intentional front/back cover layouts and landscape engineering sheets remain intact.

## Checks

Only `main.tex` changed among all 486 source files. The exact change is the body-geometry declaration plus its comment. All prose, mathematical expressions, measurements, code, diagrams and original assets are unchanged. Source archive hashes, current source manifests and clean reference checkout pass `verify-sources.py`.

The complete PDF remains 424 A4 pages with unchanged bookmarks, page numbering, word sequence and physical line breaks. Across portrait pages every body word moves by the expected 5 mm toward the center, with unchanged vertical coordinates. Both cover raster renders are pixel-identical to the previous PDF. Sample odd/even body pages now start at 30 mm from the same left edge. One PDF extraction grouping difference in the List of Tables separates dot leaders from caption text; word sequence and coordinates prove there is no rendered line-wrap change. Detailed results are in `layout-audit.json` and `independent-diagnosis.md`.

All 12 chapters, references, appendices A–J, four current V2 schematic sheets and 31 PCB pages are retained. No missing glyphs/references/citations, overfull boxes or text outside page bounds. Existing 106 underfull horizontal box messages and math-font size substitutions remain nonfatal. Adjacent odd/even pages were rendered and inspected.

Tested commands:

```sh
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/thesis-margin-review/audit-layout.py
python3 /workspace/tooling/thesis-margin-review/check-pdf.py
python3 /workspace/tooling/verify-sources.py
python3 /workspace/tooling/thesis-margin-review/package.py
```

The source ZIP CRC and every packaged member SHA-256 pass. Toolchain unchanged: XeTeX 0.999996 (TeX Live 2025/dev/Debian), latexmk 4.86, pdfinfo 26.05.0; manual bibliography, no Biber. No firmware/web/hardware changes. Selected `/workspace/Thesis` reference checkout stays clean at `e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`. The already-authorized GitHub thesis download release is refreshed; remote verification is recorded in `github-release/`. No branch commit/push or environment sharing/publication change.

## GitHub verification

Existing authorized GitHub thesis review downloads refreshed at https://github.com/kform-danish-office/Thesis/releases/tag/thesis-v1-v2-v3-review. All three remote asset SHA-256 digests/sizes and downloaded bytes match local files. Downloaded source ZIP CRC and486entries pass. Evidence: /workspace/tooling/thesis-margin-review/github-release/published-state.json and download-verification.json. Reference checkout clean/unchanged; no branch commit/push or environment sharing/publication change.
