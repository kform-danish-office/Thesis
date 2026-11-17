# Natural thesis voice revision

Revised prose throughout the front matter, chapters and appendix introductions to retain the user's plain, practical engineering voice. Work and observations remain mostly passive/impersonal; ordinary physical relationships use natural grammar. Compressed terms and wording about the editing process were replaced with concrete explanations. Technical uncertainty and measured-versus-reported distinctions remain explicit.

Persistent source: /workspace/thesis. Persistent voice guidance: /workspace/tooling/thesis-voice-guide.md, linked from /workspace/AGENTS.md.

Validation commands:
- python3 /workspace/tooling/thesis-natural-voice/audit.py
- bash /workspace/tooling/build-thesis.sh
- python3 /workspace/tooling/thesis-natural-voice/check-pdf.py
- python3 /workspace/tooling/verify-sources.py
- python3 /workspace/tooling/thesis-natural-voice/package.py

The source audit preserves numerical sequences, math, LaTeX command arguments, all protected environments (including tables and figures), newline conventions and every non-prose file. The crop-only cover and original measurement evidence are unchanged. Review notes and independent findings are retained here. Review fixes preserve telemetry queue behavior, distinguish missing supplied records from events never recorded, and distinguish logged readings from calculated results. The final diff is wording.diff.

Current outputs: Thesis_Natural_Voice.pdf and Thesis_Natural_Voice_Source.zip. Integrity values are in artifacts.json and SHA256SUMS. The PDF checks cover every physical page, all 12 chapters, References and appendices A–J. Existing underfull spacing and small math-font substitutions remain nonfatal. No publication or GitHub checkout changes.
