# Frontmatter and Chapters 1–4 wording review

Read the assigned frontmatter and chapter prose. Edited 26 files, focusing on sentences that sounded like source-audit notes, vague design jargon, or forced passive conversions. All numerical values, math, headings, citations, labels, figure/table environments, and technical distinctions were left intact. Original newline style and final-newline status were preserved through byte-based replacements. No source-data, firmware, or cover-image edits.

Representative changes:

- Abstract: "The main control problem was managing the energy remaining ..." became a direct explanation of regulating under load and limiting further charging after disconnection because energy remains stored.
- Introduction: "the load ... could disappear" became "be disconnected while energy remained in the converter."
- Design analysis: "capacitor trajectory" became "capacitor-voltage waveform."
- Background: "component scale" became "component values" where that was the intended meaning.
- USB-C adaptation: "output-power actuator" became a direct explanation of how output power is controlled through enabled intervals.
- Requirements: "two measurements answer different questions" became the concrete requirement to measure and report the two voltages separately.

Original input/output node distinctions, unverified continuous ratings, inherited-design attribution, baseline/V2 separation, and model limitations remain explicit. Existing clear physical descriptions were retained in natural active voice; work performed remains mostly passive/impersonal, with no first-person narrative.

The full replacement list is retained temporarily at /tmp/natural_intro.py for parent review. Changed scope comprises Frontmatter/Abstract.tex, Frontmatter/Approval.tex, and 24 chapter files within Chapters 1–4. No builds or manifest edits were made by this agent.
