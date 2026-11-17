# Chapters 04–06 passive-voice review

Reviewed: 35 assigned `.tex` files. Changed: 35 files (12 in Chapter 04, 11 in Chapter 05, 12 in Chapter 06). All assigned files were read in full and reviewed again after rewriting. Only the assigned prose was changed; headings were left for the root agent.

The wording was changed to factual passive or impersonal reporting while retaining direct, plain engineering English. Personal actions and naturally passive technical processes were rewritten. Static definitions, equations described in prose, physical relationships, and essential signal actors were retained in neutral active form where forced passives would obscure the meaning.

Examples:

- “I implemented the reference LED converter's separate pump and isolated resonant paths” became “The reference LED converter's separate pump and isolated resonant paths … were implemented in this work.” The reference-topology attribution was preserved.
- “I would set the model to the measured input and secondary demand, then compare …” became “The model would be set to the measured input and secondary demand, and … would then be compared.” The proposed work remains conditional.
- “I used the supplied values … because I did not remeasure inductance after installation or keep a detailed magnetic rework log” became “The supplied values … were used because inductance was not remeasured after installation and a detailed magnetic rework log was not kept.” The evidence limitation remains explicit.
- The inherited cores, windings, magnetic design, and component measurements remain distinguished from the electrical and mechanical integration performed in this thesis. Bima Nugraha Sanusi, the DTU Power Electronics group, and M'ani Gautason retain their existing attributions.

Preserved limits and ambiguities:

- Model calibration, startup/load/no-load comparisons, convergence checks, added loss/thermal paths, and the stepped output-power tests remain proposed or unfinished. They were not rewritten as completed work.
- The reported output-power gap remains distinct from measured dissipation. Installed magnetic identity, post-installation inductance, component-specific thermal limits, isolation margin, and standardized dielectric verification remain unresolved as stated in the source.
- The existing resonant-inductance scope ambiguity was left untouched: Chapter 04 uses `\LRES` for the summed discrete and leakage contributions, while Chapter 06's installed-resonance relationship contains `L_{\mathrm{RES}}+L_{\mathrm{lk}}+L_{\mathrm{int}}`. No symbol, equation, numerical value, or engineering interpretation was corrected.
- No later firmware features or new engineering claims were introduced.

Validation against `/workspace/tooling/thesis-passive-review/before` passed for all 35 files:

- Exact numeric-literal sequence per file.
- Exact LaTeX command and balanced argument sequence, including citations, labels, references, source-file paths, and headings.
- Exact inline math and all 50 protected environment blocks, including nested tabular environments, figures, tables, and equations.
- Exact raw newline sequence per file, retaining the source CRLF/LF styles without newline conversion.
- No first- or second-person pronouns in prose. The personal headings in `06_Magnetics_Integration/01_Provenance.tex` and `06_Magnetics_Integration/11_Limitations.tex` were intentionally left unchanged for the root agent.

No compilation, Git commands, commits, pushes, deployment, publication, or changes outside the owned `.tex` files and this note were performed.
