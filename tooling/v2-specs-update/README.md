# V2 specifications and thesis narrative update

Persistent source: /workspace/thesis. The introduction now describes development from the G071 prototype to the integrated F410 V2 board, then the powered tank changes, bridge-heating limitation and planned V3 work. A new introduction section and specification table summarize the documented V2 circuit. The abstract, preface, hardware description, conclusion and future work follow the same progression in the user's direct, factual, mostly passive voice.

Appendix B includes every page of the new four-sheet schematic and 31-page PCB print set. The earlier schematic remains available. Selected top/bottom copper views also appear in the V2 hardware section. Original new vector PDFs are retained in Pictures/Thesis/07_Hardware together with V2_2026-10-27_provenance.json. The approved uploaded ZIP is retained in /workspace/source-archives; CRC passed and archive SHA-256 is 5814e9eb408b630bfc3a6bbb92dd899ee39f82236a5f90429ba9cd3f8c3be26d.

The new export confirms the F410/LMG2652/AMC0330/MPQ4242 circuit and four copper layers (Top, Int1 GND, Int2 PWR, Bottom). It does not resolve missing L3/T1/C26 values, divider-label discrepancies, fitted diode identity, V2 dimensions or copper weights. The original drawn external inductor remains separate from the reported leakage-only tank. The 79.89 W G071 results, archived 40 ns timing, reported 60 ns V2 setting and 95 W thermal run remain distinct. Continuous power and ZVS are not newly claimed.

The two inline 3D views were inspected to understand the design. Their original raster files were not included in the ZIP or made available as local attachments. The thesis therefore reproduces the exact vector PCB prints rather than generating replacements for those images. Exact 3D figures can be added if the raster files are attached separately.

Validation:
- python3 /workspace/tooling/v2-specs-update/audit.py
- bash /workspace/tooling/build-thesis.sh
- python3 /workspace/tooling/v2-specs-update/check-pdf.py
- python3 /workspace/tooling/verify-sources.py
- python3 /workspace/tooling/v2-specs-update/package.py

18 existing files edited and 4 files added; 461 earlier files unchanged. All original non-TeX assets, math, labels and earlier figures/tables preserved except the explicitly updated Appendix B revision register. Separate technical and narrative reviews completed; the RQ2 answer now explicitly describes transfer of the control law to F410 and the source of the G071 captures. The compiled PDF has 430 A4 pages, all 12 chapters, References and appendices A–J, and all 35 new source-document pages. No missing glyphs, references, citations, overfull boxes or text outside physical pages. 91 nonfatal underfull horizontal messages and existing math-font size substitutions remain. Representative new pages were visually inspected. The source ZIP was checked by CRC and every member hash.

Current outputs:
- Thesis_V2_Specifications_Update.pdf
- V2_Introduction_Excerpt.pdf
- Thesis_V2_Specifications_Source.zip

See artifacts.json and SHA256SUMS for hashes. No commit, push, deployment or publication; selected GitHub reference checkout remains unchanged.
