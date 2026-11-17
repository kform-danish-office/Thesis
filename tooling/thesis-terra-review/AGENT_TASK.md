# Terra agent task

1. Read `/workspace/tooling/thesis-agent-voice-checklist.md`, `/workspace/AGENTS.md`, and `/workspace/tooling/thesis-voice-guide.md`.
2. Read every authored TeX file in your assigned scope. Inspect captions/tables in context. Do not change source files.
3. Identify material prose/voice problems using the checklist, not a banned-word replacement sweep. Keep good passages, especially the original introduction's framing.
4. Write exact, non-overlapping proposals to `proposals/<assignment>.json` as a JSON array with the schema from the checklist.
5. Write `proposals/<assignment>-review.md` listing files reviewed, what was retained, problems addressed and unresolved questions.
6. Send the root agent a concise summary. Root independently judges and applies proposals.

Work only in your assigned output files. Read references elsewhere when needed, but never modify them. No builds or network actions. The current thesis is the version after the direct-results pass; do not review an older PDF or backup as if current.
