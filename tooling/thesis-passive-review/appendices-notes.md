# Appendices A–J passive-voice review

Reviewed and changed all ten owned appendix files, from A_Analytical_Equations.tex through J_Revised_Plan_Integration.tex. Descriptive prose was rewritten in factual passive or impersonal engineering English; static definitions and numerical relations retain neutral direct wording. No files outside these appendices and this note were edited by this agent.

Examples:

- “I calculate screening efficiency” became “Screening efficiency is calculated,” with every original acquisition requirement retained.
- Firmware startup, ADC acquisition/calibration, fault handling, settings writes, UART framing, lease expiry, browser logging, build checks, and analysis processing were rewritten around the actions and values involved.
- “I rebuilt both PWR-2.0.1 targets” became “Both PWR-2.0.1 targets were rebuilt,” with the historical date and the distinction from powered V2 testing retained.
- The contribution appendix still attributes the charge-pump topology and planar magnetics to earlier work, while converter implementation, STM32 development, bring-up, and testing remain identified as thesis work.
- Planned V2 repeats, unfinished prototype modeling, and V3 release/testing/density work remain required or conditional, rather than reported as completed.

Uncertainties and boundaries retained:

- Measured modified V1.0 results remain separate from the frozen PWR-2.0.1 software checks and reported V2 point.
- Missing test settings, calibration limits, disagreeing readings, unmeasured physical timing, missing calculator UI integration, and unfinished modeling remain explicit.
- No PWR-2.0.4 material, photographs, hardware results, or new performance claims were added.
- Personal headings in B and F were left unchanged by this agent; they were subsequently updated by the root agent’s explicit heading allowlist.
- Protected tables and listing content retain their original wording, including active technical descriptions and quoted command identifiers.

Before the root agent’s separate heading updates, verification against /workspace/tooling/thesis-passive-review/before passed for every owned file: identical digit sequence, inline/display math strings, 53 protected environment blocks, 2,121 LaTeX command/argument strings, and the exact per-file CRLF/LF newline sequence. No first- or second-person narrative pronouns remain after protected syntax is excluded. No compilation, Git mutation, publishing, or hardware test was performed.

Cross-review by passive_04_06 found one introduced ambiguity in H: originals and checksums had been grouped as if both were inside the manifest. The root-approved correction now states that the original UTF-8 files are included in the editable package and their SHA-256 checksums are recorded in the manifest. H was rechecked after this correction: numeric literals, all commands/arguments, and exact newline sequences still match the baseline. No other actionable appendix drift was found. Appendix source is frozen pending final root validation.
