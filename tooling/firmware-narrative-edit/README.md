# Firmware stages explained instead of scattered revision labels

Routine prose and captions now describe the control-development stage: open-loop checks, blocking voltage feedback, DMA-based feedback, baseline voltage-control firmware and the archived V2 port. The control chapter introduces exact software identifiers in a short explanation and mapping table before they are used. Hardware V1/V2/V3 names are kept separate from software revisions.

Exact revisions remain in the clearly introduced test-configuration table and in software-history/source records. The high-load record's PWR-1.9.10 identity remains distinct from the identified final PWR-1.9.20 records; missing versions are not filled in. Archived V2 source remains distinct from the unidentified later bench-run firmware, preserving the nominal40ns/programmed60ns distinction. Code files, literal source/build paths and original listing contents are unchanged.

The control-development comparison table now uses Open loop, Blocking feedback, DMA feedback and Final baseline rather than ambiguous V0/V1/V2 software labels. A leftover hardware paragraph referring to a software stage called V2 was changed to refer to DMA-based controller development. No file-handoff dates or chat narrative were added.

Persistent source: /workspace/thesis, 486 files. 36 existing files edited, 450 unchanged. Current local PDF/source: Thesis_V1_V2_V3.pdf and Thesis_V1_V2_V3_Source.zip in this directory; hashes: artifacts.json and SHA256SUMS.txt. Source snapshot and diff: before/ and firmware-terms.diff. Review: final-review.md and the three editing reports. Preferences saved in AGENTS.md and thesis-voice-guide.md.

Validation: audit.py; /workspace/tooling/build-thesis.sh; check-pdf.py; /workspace/tooling/verify-sources.py; package.py. Full PDF has 434 A4 pages, all12chapters, References and appendices A–J. All4currentV2schematic sheets and31PCB print pages are still embedded. The removed scope-photo figure stays removed and raw C2 plots remain included. No missing references/citations/glyphs, overfull boxes or text outside physical pages. Routine96underfull horizontal messages and existing math-font substitutions remain. The new software-identification section was visually inspected. Source ZIP CRC and every member hash passed.

The existing authorized GitHub thesis downloads are refreshed at the same URLs. Before/after state and hash/download verification are under github-release/. Selected reference checkout remains unchanged; no branch commit/push or environment sharing change.
