# V1, V2 and V3 thesis narrative

Updated the development story in the introduction, hardware, results, discussion, conclusion and plan-status sections. V1 establishes the measured baseline and control work. V2 integrates F410 control and allows the leakage-only tank and timing changes to be discussed alongside comparable bench performance and persistent input heating. V3 is a reduced edge-card layout with the USB-PD output section removed and secondary rectification retained.

The 3.3–3.6 A high-power operating region is described at the secondary output; no connector voltage or wattage is assumed. Secondary-winding loss and a possible single-via current-path bottleneck remain suspected limitations. The approximately 8% reduction is an estimated net volume change for the slimmed design, with the changed function made explicit. It is not a measured complete-system power-density gain. No new magnetic set was installed. The 100 W objective and longer-term 240 W EPR direction remain goals.

The user's direct, factual, mostly passive voice is retained. No upload dates or chat/file-handoff narrative was added. Original numerical results, firmware, schematic/PCB PDFs, photographs and raw data are unchanged. The complete V2 schematic and PCB print sets remain in the thesis.

Persistent source: /workspace/thesis (485 files). Full PDF: Thesis_V1_V2_V3.pdf, 432 A4 pages. Editable source: Thesis_V1_V2_V3_Source.zip. Integrity: artifacts.json and SHA256SUMS.txt. Original source preserved in before/. Exact diff: story.diff. Claim review: claim-review.md. Source audit: source-audit.json. PDF audit and page previews are retained here.

Validation commands:
- python3 /workspace/tooling/v3-story-update/audit.py
- bash /workspace/tooling/build-thesis.sh
- python3 /workspace/tooling/v3-story-update/check-pdf.py
- python3 /workspace/tooling/verify-sources.py
- python3 /workspace/tooling/v3-story-update/package.py

28 existing files edited, 2 new sections added, 455 earlier files unchanged. All earlier mathematical expressions, labels, source graphics and numerical baseline tables preserved. Only the revised-plan status and plan integration tables were updated to reflect the new account. Full build passed, with all 12 chapters, References and appendices A–J. All 35 current V2 document pages were verified present. No undefined references/citations, missing glyphs, overfull boxes or text outside physical pages. Existing small math-font substitutions and 92 nonfatal underfull horizontal messages remain. The abstract, V3 hardware opening and V3 result table were visually inspected. Source ZIP CRC and every member hash passed.

The user requested GitHub downloads before this narrative update. The dedicated thesis review release is published at https://github.com/kform-danish-office/Thesis/releases/tag/thesis-v1-v2-v3-review. All three public release downloads match local hashes and GitHub digests; the downloaded source ZIP also passed CRC and entry-count checks. The selected GitHub checkout remains unchanged; no branch commit or push was made. Published state and downloaded-asset verification are recorded under github-release/.
