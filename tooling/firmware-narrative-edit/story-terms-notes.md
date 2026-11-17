# Firmware identifiers in the early narrative

Edited 13 files in the assigned front matter and Chapters 1–7/9. Casual PWR identifiers were replaced with descriptive terms tied to their role: voltage-control firmware, baseline firmware, ported controller, or archived V2 controller source. The hardware-development sequence remains V1/V2/V3 and is not treated as a firmware numbering scheme.

The hardware section describes peripheral adaptation and the addition of browser telemetry as changes rather than dropping software identifiers into the account. The introductory timing table now identifies the archived V2 controller code. Its nominal 40 ns timing remains distinct from the later reported 60 ns bench setting with unknown firmware identity. The methods section points to the parent's explicit code-identity mapping at sec:ctrl-firmware-identities.

No PWR identifiers remain in the assigned routine prose. Literal source names, code, pin assignments, electrical settings, quantities, equations, labels and citations are unchanged. Byte replacement preserved original newline styles. Checks comparing physical quantities, math, labels, citations and literal source paths against the task snapshot all passed.

Changed files:
- Frontmatter/Abstract.tex
- Chapters/01_Introduction/05_Contributions_Attribution.tex
- Chapters/01_Introduction/06_Scope_Limitations.tex
- Chapters/01_Introduction/08_V2_Prototype.tex
- Chapters/02_Background/08_Research_Gap.tex
- Chapters/03_Requirements_Architecture/07_Operating_Modes.tex
- Chapters/03_Requirements_Architecture/09_Revised_Plan_Criteria.tex
- Chapters/05_Modeling_Simulation/01_Objectives.tex
- Chapters/07_Hardware/01_Prototype_Overview.tex
- Chapters/07_Hardware/08_Sensing.tex
- Chapters/07_Hardware/16_V2_F410.tex
- Chapters/09_Experimental_Methods/01_Objectives.tex
- Chapters/09_Experimental_Methods/07_Control_Tests.tex

No builds, manifests or GitHub actions performed. Source edits are frozen.
