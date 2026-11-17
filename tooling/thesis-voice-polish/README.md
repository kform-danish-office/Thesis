# Thesis voice and wording polish — October 25, 2026

The user found the preceding passive revision awkward and asked for another pass that keeps their voice. The current thesis uses direct, practical engineering English: short concrete sentences, natural passive or impersonal reporting of methods and results, and ordinary grammar for definitions and circuit behavior. No first-person narrative was reintroduced. The acknowledgments use direct thanks without personal pronouns.

All 140 chapter files, ten descriptive appendices, Abstract, Approval, Acknowledgements, and the README were revised. This is 154 changed files and 313 byte-identical files against the 467-file backup. The edits remove forced passives, stacked clauses, abstract wording, and repeated statements about what is documented. Headings and layout were not changed.

Examples:

- “when demand disappeared” → “after the load was disconnected”
- “Power could be transferred by the hardware” → “The hardware could transfer power”
- In the scheduling explanation, “A complete carrier cycle cannot be contained in that interval” was shortened to say that the interval is too short for a complete cycle.
- “screening efficiency” → “initial efficiency estimate” in explanatory prose, with the calculation basis and uncertainty retained
- The empty preface sentence “The controller development is extended through this work” was removed.

## Current deliverables and backup

- Editable source: `/workspace/thesis` — all 467 original relative paths retained.
- Build: `/workspace/thesis-build/main.pdf` and `main.txt`.
- Stable PDF: `Richard_Xu_Thesis_Voice_Polished_2026-10-25.pdf` — 384 A4 pages, 16,793,768 bytes.
- Full editable source: `Thesis_Voice_Polished_2026-10-25.zip` — 467 files, 80,494,944 bytes; paths, CRCs and every member hash verified.
- Previous source: `before/` — all 467 files, with `before-manifest.json`.
- Previous PDF: `thesis-before.pdf` — the preceding 388-page passive revision.
- Artifact hashes: `artifacts.json` and `SHA256SUMS`.

PDF SHA-256: `6ecc403febcac78539d52d9c71af9079e54bdfd4c83b48aa48b3c39e7dd63899`.

Source ZIP SHA-256: `af6098af31f2cef025f01ddb046c672e389c6e97c5ae4dadb993e3830ed1579e`.

## Validation

These commands completed successfully:

```bash
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/thesis-voice-polish/audit-prose-revision.py
python3 /workspace/tooling/thesis-voice-polish/check-pdf.py
python3 /workspace/tooling/verify-sources.py
python3 /workspace/tooling/thesis-voice-polish/package-artifacts.py
```

The preservation audit checks every source path and baseline hash; all numeric literal sequences, math, complete protected technical environments, LaTeX commands and arguments, headings, newline style, and final-newline state are preserved. No heading exceptions were needed. The narrative scan reports zero personal/reader pronoun candidates. These checks protect literal content; editorial review is still needed to assess meaning.

All changed narrative was read against the preceding version. Six independent cross-reviews cover frontmatter/README, Chapters 01–03, 04–06, 07–08, 09–10, and Appendices A–J. The root agent reviewed all sixteen Discussion/Conclusion files and their diffs. All review findings were resolved and rechecked. Reports and final source hashes are retained in the corresponding `*-review.md` files.

The review corrected wording that implied complete metadata for every measurement, no-load transfer always stopping, precharge always waiting for valid feedback, multiple TLV9064 packages, and guaranteed outcomes from planned tests. Appendix C now distinguishes a software delay between reads from a precise acquisition interval, and commanded excitation being inhibited from stored energy disappearing. These are wording corrections supported by the existing source/evidence, not changes to hardware or firmware behavior. Attribution, author responsibility, the AI-assistance disclosure, and uncertainty/planned-work qualifiers remain.

The PDF contains all 12 chapters, References, and appendices A–J. It has 1,046,801 extracted text characters and no missing characters, undefined citations/references, multiply defined labels, overfull horizontal boxes, or text outside the physical page. There are 90 nonfatal underfull-box messages and the existing small math-font size substitutions. Twelve representative pages were rendered; the abstract and conclusion were visually inspected. This was not a visual inspection of every page.

The build uses `main.tex`, XeLaTeX/latexmk and the manual bibliography; no Biber is required. XeTeX 0.999996 (TeX Live 2025/dev/Debian), latexmk 4.86, Poppler 26.05.0, Python 3.12.14 and PyMuPDF 1.26.6 remain installed. The retained verified TeX package provides siunitx. No new dependencies were installed. The helper sets TEXINPUTS and keeps auxiliary/build files outside the source tree.

## Source boundaries and persistence

Original ZIPs/import manifests, all data/figures/tables/captions, frozen source listings and bibliography are unchanged. The sixteen V2 photo/results assets remain intact and the results-entry sheets remain blank. Frozen thesis PWR-2.0.1 was not replaced with the later working-source PWR-2.0.4. The existing L_RES notation-scope ambiguity in Chapters 04/06 was not changed. Research claims and measurements were not independently revalidated.

The cumulative authorized revision hashes in `/workspace/tooling/thesis-change-manifest.json` were updated; the preceding manifest is saved here as `before-revision-manifest.json`. `/workspace/tooling/verify-sources.py` passes for original archives, current thesis, V2 assets, firmware/web, skills, and the unchanged clean GitHub reference at `e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`.

Use this directory's current audit/PDF checks and artifacts. The older `thesis-tone-review` and `thesis-passive-review` directories retain historical versions and checks; do not restore old prose merely to satisfy a historical wording assertion. Editorial scripts in this directory record applied changes and are not routine startup commands.

The setup report and saved start instructions identify this revision. Installation, network, credentials, repositories and unrelated workflows were left unchanged. No Git commit/push, release update, deployment, physical hardware action, sharing change or environment publication was performed. The user can review/save environment settings and publish with Only me to snapshot the current source, tools and backups. Draft saving does not publish or verify restoration in a new task; sharing controls are not exposed here.
