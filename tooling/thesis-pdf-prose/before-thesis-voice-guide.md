# Thesis voice preferences

User repeatedly requested the wording to stay close to their own voice. The V2 bench dictation in thesis/Data/project_records/V2_Testing_Update.txt provides a sample of how they explain their work. Use plain, practical engineering English: what was changed, why, what happened, and what remains unresolved. Keep factual, mostly passive prose and the existing impersonal voice. Avoid first-person narration, inflated vocabulary, bureaucratic expressions, and overly short fragments. Do not reproduce spoken hesitations or grammatical errors.

Use passive voice for work and observations where it reads naturally: “The diodes were replaced, but the heating remained.” Use ordinary grammar for physical relationships: “Narrow traces can add resistive loss.” Do not force every sentence into passive voice. Keep technical terms when they carry meaning.

Describe the experiment itself rather than the editing or record-keeping process. Preserve measured-versus-reported distinctions and uncertainty in plain language. Never turn lower temperature into proof of ZVS, a load setting into measured output, or a suspected layout cause into a confirmed diagnosis.

Keep numerical values, equations, figures, tables, labels and references intact during prose-only changes. Retain original evidence and the crop-only cover photograph. Verify the complete thesis build after edits.

Write from the author’s perspective within the existing impersonal/passive voice. The author designed and tested V2. Do not narrate file uploads, dates on which the author supplied material to an assistant, chat exchanges, archive deliveries or tool limitations inside the thesis. Describe the design, reason for a change, experiment and result. File hashes, export timestamps and assistant workflow belong in external setup/review notes. Keep dates only where they serve the actual scientific or project history. Preserve attribution for topology and magnetics that really originated in earlier DTU work.

Use concise technical prose at the density of an APEC digest. Assume an engineering audience; omit definitions of voltage, current, basic components, logic levels and general MCU operation. Introduce project-specific signals by function at first use and expand acronyms briefly where needed. Preserve quantitative detail and distinguish measurements from estimates without repeating procedural caveats.

Use “the MCU” in ordinary prose after identification. Repeat the specific MCU model only for a device/board comparison or where exact hardware identity or build instructions require it. Use the prototype version to preserve context when pin assignments differ. Do not repeat model names in every section or caption. The paired no-load development oscilloscope photographs (partial_switching_removed_scope_crop.png and no_load_clean_switching_scope_crop.png) were explicitly removed from the thesis figure sequence; do not reinsert them without a request.

Use descriptive firmware stages in ordinary prose: open-loop control, blocking feedback, DMA-based voltage control, baseline firmware and the archived V2 port. Introduce exact PWR revision IDs only in an explained software-identification/history table or a test/source record that needs them. Hardware V1/V2/V3 names and software revision numbers must remain distinct. Preserve exact code/file names and known versus unknown run-version attribution.


The APEC-style direction supersedes the earlier beginner-reader treatment. Organize technical prose around circuit operation, design rationale, implementation and measured results. Keep the thesis format and complete source/data appendices; do not turn the document into a short digest or invent a specific reference manuscript.

Explain the actual circuit and controller roles directly. The MCU regulates the secondary bulk supply feeding the USB-C PD stage; the PD stage regulates the USB-C output voltage to the selected PD level. Do not imply dynamic independence between these stages or pad the explanation with statements that nodes are distinguished throughout the document. Keep useful measurement locations and signal definitions. In ordinary prose, write “switching at megahertz frequencies” rather than “MHz switching”; use unit symbols alongside numerical values, such as “1 MHz”.

Captions, headings and table labels are part of the voice pass. Prefer “MCU pin assignments for the original controller and V2” to “signal functions ... directions stated from the MCU perspective.” Introduce a calculation table by naming the parameters, not explaining how nominal, measured and estimated values were sorted. Open a modeling chapter with the calculations and models used. For firmware development, explain the problem, change and practical benefit at each stage. Keep actual uncertainty once beside the result it affects; avoid repeated audit-like disclaimers and narration about evidence organization.

The project is a USB-C power supply based on a high-frequency charge-pump PFC resonant converter. Do not call it a laboratory supply or bench power supply. Laboratory describes the test setting or instruments only. Preserve the original introduction’s project framing and load-focused motivation; do not redefine the product while revising prose.

Describe the intended USB-C load as a device drawing power from the USB-C output; retain electronic/resistive load terminology for actual tests. Omit missing bench-run firmware-version commentary from summary tables without assigning an unconfirmed revision. For the Keysight three-channel captures, label yellow as half-bridge switch-node voltage, green as secondary output voltage, and blue as USB-C VBUS output voltage. State AC coupling where relevant; do not apply this colour mapping to unrelated raw C2 recordings.

The 240 W USB-PD EPR point was a question raised in feedback on the APEC digest about higher-load capability, not a project goal or development objective. Keep the actual 100 W target and 65 W minimum; mention the reviewer question once where discussing power limitations rather than repeating EPR checklists.

Use natural wording for attribution. Prefer “the given measurements” or “component measurements,” “the supplied models,” and “earlier DTU work” as appropriate. Avoid “inherited” as a repeated prose label. Keep the actual source and author of supplied designs and measurements clear.

Describe figures and observations directly. Do not attach repeated “does not establish/prove/demonstrate” caveats to photographs, tables, layout descriptions, or ordinary results. Remove empty defensive clauses rather than replacing them with a synonym. Keep necessary measurement limits concise and local, and state remaining work as concrete measurements or design changes.
