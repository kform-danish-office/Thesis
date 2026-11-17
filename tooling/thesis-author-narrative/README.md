# Author-centred V2 narrative correction

The user identified inappropriate wording about the date on which material was supplied. Removed file-handoff dates, archive-delivery explanations, chat references, export-history descriptions and administrative source-retention notes from the V2 introduction, hardware description and appendix captions. The narrative now describes the author's board design, integration, test changes and results. Genuine attribution to earlier DTU work is retained. Actual project schedules and original engineering documents are unchanged.

Persistent source: /workspace/thesis. Voice preferences are recorded in /workspace/tooling/thesis-voice-guide.md and /workspace/AGENTS.md, including an explicit rule to keep assistant/file-handoff history out of the thesis.

Six source files edited; 477 files unchanged. No original image, PDF schematic/PCB print, raw measurement, firmware or bibliography file changed. Numerical quantities, math, labels, citations and included graphics remain identical. All four current schematic sheets and 31 PCB pages remain in the compiled document. Original source-file names and provenance metadata remain available separately from the printed narrative.

Validation:
- python3 /workspace/tooling/thesis-author-narrative/audit.py
- bash /workspace/tooling/build-thesis.sh
- python3 /workspace/tooling/thesis-author-narrative/check-pdf.py
- python3 /workspace/tooling/verify-sources.py
- python3 /workspace/tooling/thesis-author-narrative/package.py

Full build: 430 A4 pages; all 12 chapters, References and appendices A–J. No missing glyphs, undefined references/citations, overfull boxes or text outside physical pages. Existing math-font substitutions and 92 nonfatal underfull horizontal messages remain. The corrected V2 introduction and appendix overview were visually checked. Source ZIP CRC and every member hash verified. No GitHub or publication action.

Current outputs: Thesis_Corrected_Narrative.pdf, Thesis_Corrected_Source.zip, Introduction_Preview.pdf. Hashes and byte counts: artifacts.json / SHA256SUMS. Source audit and exact diff: source-audit.json / wording.diff.
