# MCU signals introduced for a beginner reader

Added an early Circuit and Controller Basics section before the first detailed pin table. It explains voltage/current/power, AC/DC, rectification, stored energy, transformer primary/secondary, bulk voltage versus USB VBUS, ground references, MCU/firmware, signal versus supply pins, analog/digital inputs, port names versus package terminal numbers, and the sensing/command paths. ADC, timer/channel, PWM/duty/bursts, GPIO, DMA and UART/TX/RX are introduced before the signal-function map. The map identifies G071/F410 differences, particularly PA10 and PB13.

Later chapters now give the function before the identifier, explain local peripheral terms, and distinguish input measurements from control actions. The glossary no longer refers to an unexplained PA1 feedback variable. The appendix pin-map key distinguishes port labels, package pins, alternate functions, timer channels and ADC channels. Oscilloscope channel names are distinguished from MCU names.

Cross-reviews checked the explanations against the circuit and archived firmware. Corrections keep G071 SENSOR detection limited to the acquisition-running flag and polling-based enable alignment described as an attempt. They also distinguish the 1 MHz carrier from the timer clock. See agent notes and cross-review reports in this directory. No electronic settings, pin assignments, measurements or source code were changed.

Persistent thesis source: /workspace/thesis. Voice/reader preferences: /workspace/tooling/thesis-voice-guide.md and /workspace/AGENTS.md. Source snapshot: before/. Exact diff: reader-revision.diff. Audits: source-audit.json and pdf-audit.json. The source audit checks numerical quantities, mathematical expressions, labels, graphics and earlier protected tables/figures, apart from the specified explanatory glossary, feedback-row and architecture-caption changes.

Validation commands:
- python3 /workspace/tooling/mcu-reader-introduction/audit.py
- bash /workspace/tooling/build-thesis.sh
- python3 /workspace/tooling/mcu-reader-introduction/check-pdf.py
- python3 /workspace/tooling/verify-sources.py
- python3 /workspace/tooling/mcu-reader-introduction/package.py

Original V1/V2/V3 technical scope and uncertainty are retained. All four current V2 schematic sheets and 31 PCB prints remain included. No missing references/citations, missing glyphs, overfull boxes or physical-page overflow. Routine underfull spacing and math-font substitutions remain; exact counts are in pdf-audit.json. Source ZIP integrity and artifact hashes are recorded with the packaged outputs.

Final full thesis: 436 A4 pages; source project: 486 files (44 existing files edited, one primer added, 441 unchanged). The new primer is in Section 1.1 before the first detailed pin map. Numerical quantities, existing equations, data and pin assignments remain preserved. The final PDF has 94 nonfatal underfull horizontal messages and existing math-font size substitutions; no overfull boxes or missing references/glyphs.

Current local outputs: Thesis_V1_V2_V3.pdf and Thesis_V1_V2_V3_Source.zip in this directory. Hashes: artifacts.json and SHA256SUMS.txt. The earlier release files remain in /workspace/tooling/v3-story-update. Existing GitHub thesis-release assets were refreshed as a continuation of the authorized download workflow, preserving the public URLs. Before/after remote metadata, server hash checks and fresh download verification are under github-release/.
