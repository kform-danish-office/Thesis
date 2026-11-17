# Passive, factual thesis revision — 2026-10-25

The latest user request was to keep the author's voice while rewriting the
thesis in passive voice with factual wording. This supersedes the earlier
first-person preference. The direct American engineering style is retained:
methods, results and project actions are reported passively or impersonally;
definitions and static relationships are kept plain and grammatical. Proposed
work remains conditional and missing checks remain requirements.

## Current files

- Editable source: `/workspace/thesis`, all 467 paths retained.
- Normal build: `/workspace/thesis-build/main.pdf` and `main.txt`.
- Stable PDF: `Richard_Xu_Thesis_Passive_Factual_2026-10-25.pdf` in this directory.
- Full editable source ZIP: `Thesis_Passive_Factual_2026-10-25.zip`.
- Before-passive source backup: `before/`, all 467 files.
- Before-passive PDF: `thesis-before.pdf`, 384 pages.
- Final artifact sizes/hashes: `artifacts.json` and `SHA256SUMS`.

All 140 chapter files, ten descriptive appendix files, Abstract, Approval and
Acknowledgments were revised. The README voice/build guidance was updated.
There are **154 edited files** and **313 byte-identical files** relative to this
task's backup. Seven personal headings were made impersonal through eight
explicit heading/ToC edits, with label keys retained. The changes are listed in
`heading-edits.json`. Examples include “My Work and the Earlier Designs” →
“Project Contributions and Earlier Designs” and “What I Still Need to Measure” →
“Remaining Measurements.”

Examples of the prose:

- “I built and tested a USB-C laboratory power supply…” → “A USB-C laboratory
  power supply was built and tested…”
- “I used the supplied planar inductor and transformer…” → passive reporting
  of the supplied components and their use, retaining their inherited origin.
- Planned repeats and follow-up measurements retain “would” or “is required”;
  they are not presented as completed work.

Inherited topology and planar-magnetic design credit remain explicit. Author
responsibility and the AI-assistance disclosure are retained. The frozen
PWR-2.0.1 software record was not replaced with the later working-source
PWR-2.0.4 release. Tables, figures, captions, source listings, measurements,
equations, bibliography, metadata and layout were preserved. The original wording
inside technical tables, figures and frozen source remains; this is a narrative
rewrite, not a modification of quoted/reference material or program code.

## Preservation and factual review

`audit-prose-revision.py` compares the current tree with `before/` and the complete
baseline manifest. It checks:

- The original numeric-literal sequence in every edited file.
- All inline/display math and complete protected technical environments.
- Every LaTeX command and argument, except the eight explicit heading/ToC edits.
- Original newline conventions and all non-prose file hashes.
- A reporting scan for personal/reader pronouns outside math and protected syntax.

All checks passed. No personal/reader pronoun candidates remain in the scanned
narrative. `prose-audit.json` and `passive.diff` record the exact revision.
These checks protect content and structure; they do not independently establish
the correctness of the underlying research.

Three independent read-only reviews cover Chapters 1–8, Chapters 9–12/front
matter, and Appendices A–J. No unresolved introduced findings remain. Two
wording regressions were corrected and rechecked: a screening power difference
is described as assessed from measurements rather than independently measured
loss, and original source files are distinguished from their checksums in the
manifest. The abstract also distinguishes derived output power from directly
recorded readings. Review notes and source hashes are in `engineering-review.md`,
`claims-review.md` and `appendix-review.md`; section-level notes are beside them.
The later heading-only edits are allowlisted and audited separately.

The existing L_RES notation-scope question between Chapters 4 and 6 remains
unchanged. Existing calibration, synchronization, fitted-component, waveform
and thermal-duration limits remain in the text. Continuous ratings, conformity,
V2 powered characterization and V3 comparisons remain unestablished where they
were unestablished before this rewrite.

## Compilation and PDF checks

```bash
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/thesis-passive-review/audit-prose-revision.py
python3 /workspace/tooling/thesis-passive-review/check-pdf.py
python3 /workspace/tooling/verify-sources.py
```

The existing helper runs XeLaTeX through latexmk, sets the retained siunitx
package path, writes chapter auxiliaries to the separate build tree and verifies
PDF metadata/text. The bibliography is manual; no Biber is required. The build
completed successfully after all prose corrections and heading changes.

Final output: **388 A4 pages**, **16,805,852 bytes**, **1,057,258 extracted text
characters**. All 12 chapters, References and appendices A–J are present. No
missing characters, undefined citations/references or multiply defined labels
were reported. There are no overfull horizontal boxes or text beyond physical
page bounds. The log retains 85 nonfatal underfull-box messages and the existing
small math-font size-substitution warnings.

`pdf-audit.json` records coverage, renamed headings and rotated-coordinate text
bounds. Twelve representative pages were rendered under `page-previews/`;
the abstract and conclusion were visually inspected. This is representative
visual QA, not a visual proofread of all 388 pages. The original fonts, margins,
figure assets, tables and code listing configuration remain unchanged.

Tools retain XeTeX 0.999996 / TeX Live 2025/dev/Debian, latexmk 4.86 and Poppler
26.05.0. The retained verified texlive-science package provides siunitx. PDF
inspection uses Python 3.12.14 and PyMuPDF 1.26.6. No new package or service was
needed for the rewrite.

## Artifacts and persistence

PDF SHA-256:
`09945866c3256ff058a19e9422eea9d0fd029250139fc53306a5ced88b265ab3`.

The full source ZIP contains exactly 467 files with original relative paths,
including the previously prepared V2 photo/results-entry additions. It is
80,498,947 bytes; SHA-256:
`cb7ccce6013b1e18a6dcdf4cb6595dbd410f0960511a3776b6f3e01c2eb9056b`.
ZIP CRCs and every member's bytes/hash match the current source tree.

Current hashes are recorded separately from the approved import in
`/workspace/tooling/thesis-change-manifest.json` (154 entries). Original approved
ZIPs/import manifests and earlier thesis artifacts remain intact. Source checks
also pass for the current firmware/web, V2 assets, imported skills and unchanged
clean `/workspace/Thesis` reference checkout.

The older `thesis-tone-review` audit and artifacts describe the earlier
first-person revision. Its stricter heading/README scope is historical; use this
revision's audit for current work. No assertion was removed to accept a failed
check; the new heading changes are explicitly recorded under the latest user
request. Future edits should retain user work and record authorized hashes
rather than restoring older prose to satisfy a historical manifest.

No Git commits, pushes, release updates, deployments, hardware changes or sharing
changes occurred in this task. The private environment's startup instructions
now describe the passive revision and current artifacts. Review/save environment
settings and publish with Only me to snapshot the current source, backups and
tooling. Saving the draft is not environment publication or fresh-task
restoration. The author should review the revised prose before submission.
