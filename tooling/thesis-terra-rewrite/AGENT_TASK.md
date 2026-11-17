# Terra thesis rewrite assignment

The author has now asked for a rewrite using the same supervised Terra process. Read `/workspace/tooling/thesis-agent-voice-checklist.md`, `/workspace/AGENTS.md`, and `/workspace/tooling/thesis-voice-guide.md` before working. Current source is `/workspace/thesis`, after the previous supervised review. Your file list is `<scope>-files.json` beside this assignment.

Read all assigned files and propose paragraph-level rewrites where the flow or voice is still awkward. This is a prose rewrite, not just a search for repeated caveats. Improve sentence structure, connect reasoning, explain actual design changes through their function, and make results read as engineering work. Keep the original load-focused opening and useful passages. No quota and no synonym-only churn: do not force edits where the existing prose is better. Do not replace precise technical content with generic summaries.

Write factual, mostly passive or impersonal prose at APEC technical density. Natural active descriptions of circuit functions are welcome. Keep the author's plain engineering voice. Avoid administrative narration, repeated defensive claims, artificial passives, elementary tutorials and a new polished-but-generic academic voice. Preserve local scientific uncertainty and attribution; do not invent performance or causation. Read the surrounding paragraphs so a rewrite does not repeat the same qualification elsewhere.

All source files are read-only for proposing agents. Write only:

- `proposals/<scope>.json`: non-overlapping exact replacements, using the checklist schema (`id`, `path`, `old`, `new`, `reason`, `facts_preserved`, `checklist`). Capture `old` from bytes decoded as UTF-8, preserving CRLF/LF. Every `old` must occur exactly once in the current source. Keep equations, quantities, labels and citation/reference commands unchanged. Use a paragraph-sized replacement to improve connected prose, where warranted; do not silently delete substantive facts.
- `proposals/<scope>-review.md`: complete file inventory, main rewrites, good passages kept and any actual technical uncertainty for the lead.

Do not edit firmware/code, raw data, schematic/photographic assets, generated measurement tables or formatting settings. Read references/code if needed to check meaning. Do not run builds, commit, push, publish, deploy, use the network or modify another agent's outputs. Send the lead a concise result when finished. The lead independently judges every proposed replacement before applying it.
