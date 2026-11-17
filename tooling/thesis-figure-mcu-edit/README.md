# Removed scope photographs and reduced MCU naming

Removed the paired no-load development oscilloscope photographs identified by the user: the original figure label was fig:no-load-switching-quality-photos. Removed its direct references, photo-dependent prose and the stale photograph row in the ZVS evidence table. The raw C2 waveform plots and other switching evidence remain included. Original image assets and source archives are preserved, but those two pictures are no longer referenced by the thesis.

Routine prose now uses the MCU or the board version rather than repeating a model number. Actual device comparisons, component-identification entries, pin-map comparison headings, toolchain names, literal selectors, file names and archived code retain the specificity needed for reproduction. The MCU/pin introduction and variant-dependent pin assignments remain clear.

Final review findings were corrected: the leftover photo evidence row was removed, and the contribution statement identifies MCU firmware rather than implying the MCU chip was developed in this thesis. Review: final-review.md. Naming notes and source audit are in this directory.

Persistent source: /workspace/thesis, 486 files. 54 existing source files edited; 432 unchanged. Numerical quantities, mathematical expressions, remaining labels/graphics/citations, raw data, source code and engineering PDFs remain unchanged. Listing caption prose was simplified without modifying listing contents. Exact diff: wording.diff. Removed figure block retained externally as removed-figure.tex.

Validation: audit.py; /workspace/tooling/build-thesis.sh; check-pdf.py; /workspace/tooling/verify-sources.py; package.py. Full build: 434 A4 pages, all 12 chapters, References and appendices A–J. All four current V2 schematic sheets and 31 PCB pages remain included. No missing references/citations/glyphs, overfull boxes or text outside physical pages. 94 routine underfull horizontal messages and existing small math-font substitutions remain. The no-load/switching section was visually inspected. Source ZIP CRC and every member hash pass.

Current local PDF and editable source: Thesis_V1_V2_V3.pdf and Thesis_V1_V2_V3_Source.zip. Hashes: artifacts.json and SHA256SUMS.txt. The already-authorized GitHub download release is refreshed at the same URLs; before/after metadata and asset verification are in github-release/. Selected reference checkout remains unchanged, with no branch commit/push or environment sharing change.
