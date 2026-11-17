# Chapters 07–08 passive-voice revision

All 34 assigned `.tex` files were read in full and revised. Chapter 07 contains 18 changed files and 65 changed prose lines; Chapter 08 contains 16 changed files and 60 changed prose lines. Each source paragraph occupies one line, so these are 125 revised prose paragraphs/lead-ins. The 75 original prose lines containing personal pronouns now contain none. Static definitions and circuit relationships were retained where natural.

Representative changes:

- “I assembled one V1.0 PCB” → “One V1.0 PCB was assembled.”
- “I added …” → “… were added in this project,” preserving the distinction between this project's additions and inherited circuits/magnetics.
- “I moved acquisition to DMA” → “Acquisition was moved to DMA.”
- “Before reducing area, I would review …” → “Before area is reduced, … would be reviewed,” preserving the proposed status.
- “I still need …” → “… are still needed” or “… must be checked,” retaining missing measurements as missing.

Evidence boundaries retained:

- Modified manufactured V1.0 remains the measured assembly, including its final series-inductor arrangement. V1.1 and V1.2 remain unmanufactured drawing/layout revisions.
- Nominal F410 timing calculations remain source definitions requiring driver-input/switch-node captures. Compilation and software descriptions were not turned into powered verification. The frozen PWR-2.0.1 scope was retained; no PWR-2.0.4 working-source features were introduced.
- The reported V2 85 W point remains separate from the matched V1.0 79.89 W dataset. Missing assembly, settings, duration, sensing, thermal, and calibration information remains explicit.
- V3 interface design, loss measurements, reviews, manufacturing, and bring-up remain pending or planned. Conditional review/comparison statements remain conditional.
- Supplied planar cores/windings and the inherited charge-pump resonant circuit remain identified as inherited. The project-specific PCB, additions, bring-up corrections, and firmware work retain their contribution context.
- No new photograph or hardware evidence was added.

Local comparisons against `/workspace/tooling/thesis-passive-review/before` passed for every assigned file: exact per-file numeric sequence, all inline/display math, all 45 protected environments (including nested environments), the entire LaTeX command/balanced-argument sequence, and the full raw LF/CRLF newline sequence. All headings, labels, references, citations, paths, tables, figures, equations, listings, and TikZ content remain unchanged. Personal-pronoun scanning found no remaining prose candidates in these chapters.

Only the 34 owned thesis sources and this note were edited. No compilation, Git action, deployment, publication, or hardware operation was performed. Root-managed heading edits and the final full-thesis audit are outside this subtask.
