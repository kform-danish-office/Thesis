# V2 schematics in the main thesis

Current editable source: `/workspace/thesis`. Current full PDF and source archive: `Thesis_V1_V2_V3.pdf` and `Thesis_V1_V2_V3_Source.zip` in this directory. These supersede previous current-artifact pointers.

All five main-text schematic figures (six graphic inclusions) now use the latest V2 drawings: topology overview, input/filter bridge, charge-pump/resonant stage, USB-C output and MCU/signal interface. Original vector content was cropped with PyMuPDF; circuit symbols, nets, reference labels and values were not redrawn or altered. Four new display PDFs contain five source-region pages. The original master PDFs and earlier V1 source records remain unchanged and included in Appendix B.

Captions and references match V2. Four internal figure labels were renamed without a revision suffix, with dependent references updated. The original buffered V1 controller and fitted/tested component history remain identified separately from V2 direct feedback and PA8/PB13/PA11 commands. No blanket component/netlist equivalence claim was added. The common circuit explanation uses the cleaner V2 drawings without changing measured results or historical configurations.

## Source and visual checks

- 8 TeX files edited, 4 new vector PDFs added; 478 existing files unchanged; 490 files total.
- Mathematical expressions, numerical SI quantities, citations, code, raw measurements and original graphics/documents unchanged. Existing tables retained except the V1.1 role cell changed from circuit reference to bring-up correction record.
- Original V2 master SHA-256 remains `c2623551c7094d2caa60efbbd3dab674b49553c6a3e39d8407afe83cb36c8ad2`.
- `crop-manifest.json` records source rectangles, hashes and original-region render comparisons. Three crops are pixel-identical; two have only subpixel antialias differences (mean channel error below 0.001 on a 0–255 scale). The source Altium-logo resource remains inherited outside the crop; no raster imagery is visible in the diagram regions.
- All five main schematic figures were found in the compiled main chapters and rendered for visual review. Full width landscape views keep the power/USB circuit context; small component labels remain sharp when zoomed. `main-schematic-pages.json` records the pages.
- Independent mapping and final reviews found no remaining caption, pin or fitted-history inconsistency. See `mapping-review.md` and `final-review.md`.

## Build and integrity

Full XeLaTeX/latexmk build: 424 A4 pages, all 12 chapters, References and appendices A–J. All 4 current V2 schematic sheets and 31 PCB pages remain in Appendix B. No missing references/citations/glyphs, overfull boxes or text outside physical page bounds. Symmetric 30 mm body side margins and 150 mm text width are unchanged. Existing 105 underfull horizontal messages and math-font size substitutions remain nonfatal.

Tested commands:

```sh
python3 /workspace/tooling/v2-main-schematics/generate-crops.py
python3 /workspace/tooling/v2-main-schematics/audit.py
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/v2-main-schematics/check-pdf.py
python3 /workspace/tooling/verify-sources.py
python3 /workspace/tooling/v2-main-schematics/package.py
```

Toolchain unchanged: XeTeX 0.999996 (TeX Live 2025/dev/Debian), latexmk 4.86, pdfinfo 26.05.0, PyMuPDF 1.26.6 for vector crops. Manual bibliography; no Biber. Source ZIP CRC and every member hash pass. Original archives/imported skills/current source integrity pass. No firmware/web/hardware settings changed. Selected `/workspace/Thesis` checkout remains clean at `e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`. The existing authorized GitHub thesis download release is refreshed; no branch commit/push or environment sharing/publication change.

## GitHub verification

Existing authorized GitHub thesis review downloads refreshed at https://github.com/kform-danish-office/Thesis/releases/tag/thesis-v1-v2-v3-review. All three remote SHA-256 digests/sizes and downloaded bytes match local files. Downloaded source ZIP CRC and 490 entries pass. Evidence: /workspace/tooling/v2-main-schematics/github-release/published-state.json and download-verification.json. Reference checkout clean/unchanged; no branch commit/push or environment sharing/publication change.
