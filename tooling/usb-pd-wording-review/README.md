# Circuit-role and unit wording review

Current editable source: `/workspace/thesis`. Current complete PDF and editable archive: `Thesis_V1_V2_V3.pdf` and `Thesis_V1_V2_V3_Source.zip` in this directory. These supersede earlier current-artifact pointers.

The user objected to the sentence claiming the downstream stage regulates connector VBUS independently, the generic node-distinction wording, and bare “MHz switching” prose. The review was expanded to the full thesis for similar statements while retaining concise technical prose and the author's practical engineering voice.

The MCU is now described as regulating the secondary bulk supply feeding the USB-C PD stage. The PD stage regulates the USB-C output voltage to the selected PD level. Vague downstream/node/headroom wording was replaced where it obscured those roles. No dynamic independence, completed protocol validation or conformance claim was introduced. Externally measured output quantities remain distinguished from MCU feedback where it affects interpretation.

“Megahertz” is spelled out for frequency-range prose. Numerical SI quantities such as 1 MHz remain unchanged. The motivation explains shorter commutation time directly. Valid technical meanings of independent hardware protection, mathematical uncertainty assumptions and external checks were retained; this was not a global word replacement.

The pass also corrected overstated carrier-alignment language: bounded polling attempts alignment and may time out. Precharge wording states its purpose rather than guaranteeing feedback readiness after an attempt limit. ADC acquisition is described as free-running without carrier synchronization.

## Scope and preservation

38 TeX files received targeted prose corrections; 452 source files are unchanged. All 490 source paths remain. Every mathematical expression, numerical token, SI quantity, LaTeX command/argument, label/citation, source inclusion and protected table/figure/listing matches the frozen baseline. All code, evidence, raw data and engineering assets are unchanged. Details: `source-audit.json`, `wording.diff`, `root-review.md`, `control-notes.md`, `control-independent-review.md`, and `results-notes.md`. Independent reviews found no remaining meaning regressions. The last small motivation grammar refinement and repeated device-name removal were checked against the same constraints.

The concise APEC-style direction, V2 schematic figures, crop-only cover, removed scope photographs, contextual firmware names and symmetric 30 mm side margins remain intact. Source history and fitted V1/V2 differences were preserved. Writing preferences are recorded in `/workspace/AGENTS.md` and `/workspace/tooling/thesis-voice-guide.md`.

## Validation

```sh
python3 /workspace/tooling/usb-pd-wording-review/audit.py
bash /workspace/tooling/build-thesis.sh
python3 /workspace/tooling/usb-pd-wording-review/check-pdf.py
python3 /workspace/tooling/verify-sources.py
python3 /workspace/tooling/usb-pd-wording-review/package.py
```

Full build: 424 A4 pages, all 12 chapters, references and appendices A–J, all four current V2 schematic sheets and 31 PCB pages. Final PDF text checks confirm the corrected regulation paragraph and megahertz wording. Introduction pages were rendered for inspection. No missing references/citations/glyphs, overfull boxes or text outside physical page bounds. Existing 103 underfull horizontal messages and math-font size substitutions remain nonfatal.

Toolchain unchanged: XeTeX 0.999996 (TeX Live 2025/dev/Debian), latexmk 4.86, pdfinfo 26.05.0; manual bibliography, no Biber. Original archives, imported skills, retained assets and current source hashes pass. Source ZIP CRC and every packaged member hash pass. Artifact hashes are in `artifacts.json` and `SHA256SUMS.txt`.

No firmware, web app, code or hardware settings changed. The selected `/workspace/Thesis` checkout remains clean at `e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`. The existing authorized GitHub download release is refreshed; no branch commit/push or environment sharing/publication change. Remote verification is recorded in `github-release/`.

## GitHub verification

Existing authorized GitHub thesis review downloads refreshed at https://github.com/kform-danish-office/Thesis/releases/tag/thesis-v1-v2-v3-review. All three remote asset SHA-256 digests/sizes and downloaded bytes match local files. Downloaded source ZIP CRC and 490 entries pass. Evidence: /workspace/tooling/usb-pd-wording-review/github-release/published-state.json and download-verification.json. Selected reference checkout clean/unchanged; no branch commit/push or environment sharing/publication change.
