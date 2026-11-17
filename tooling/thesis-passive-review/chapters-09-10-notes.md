# Chapters 09–10 passive-voice review

Completed a factual passive/impersonal voice pass in all 28 assigned TeX files: 13 in Experimental Methods and 15 in Results. 65 narrative paragraphs were revised. A prose-only scan found 68 personal-pronoun occurrences in the baseline and 0 afterward (protected blocks and math excluded).

Examples:

- “I tested the V1.0 PCB” became “The V1.0 PCB was tested.”
- “I need a stabilized run” became “a stabilized run is required”; this remains missing work.
- “I would record” became “would be recorded”; planned tests remain conditional.
- Firmware changes implemented by the author retain “in this work,” while LTspice studies retain their inherited attribution.

Technical limits retained: completed/planned row separation; the highest matched DC output point; efficiency screening and unsynchronized acquisition; instrument disagreement; waveform ripple versus averaged-voltage acquisition statistics; raw-export calibration and load-identification gaps; gate-referenced/deskew requirements for ZVS; surface rather than junction temperature; missing duration, stabilization, ambient, and airflow records; unverified continuous ratings and qualification work. No data, code, citations, new results, or newer-firmware/photo material was added.

Verification against `/workspace/tooling/thesis-passive-review/before` passed in every file for all numeric literal sequences, every LaTeX command with its arguments, headings, inline/display math, and 49 full protected figure/table/equation/align blocks. 11 math fragments were byte-identical. Label/reference/citation/path contents were unchanged as part of the command checks. Raw-byte edits preserved CRLF/LF styles and original final newline bytes. Headings were left for the root agent. No compile, Git operation, publication, deployment, hardware action, or edits outside the assigned TeX files and this note were performed.

No unresolved factual or attribution questions were introduced. Neutral definitions, device relationships, and clear statements of evidence were retained where forcing a passive construction would make the text cumbersome.
