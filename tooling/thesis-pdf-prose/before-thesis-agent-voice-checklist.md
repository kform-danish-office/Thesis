# Thesis prose and voice checklist for GPT-6.1 Terra agents

## Assignment

Read `/workspace/AGENTS.md` and `/workspace/tooling/thesis-voice-guide.md` first. This checklist turns the author's repeated corrections into editing instructions. Read each assigned section in context, including its captions, tables, and nearby explanation. Preserve passages that already work. The lead agent judges every proposal before it enters `/workspace/thesis`.

## Intended voice

Write concise engineering prose for a power-electronics audience, at the density of an APEC digest. Describe what was built or changed, why, and what happened. Use factual, mostly passive or impersonal sentences, with active constructions where they explain a physical relationship naturally. Keep connected paragraphs. Do not imitate typing errors, spoken hesitations or swearing. Do not turn the thesis into a tutorial, a short digest, a project-management report, or a legal defence.

A useful model: “The series inductor became hot during loading. It was removed, and the resonant capacitance was changed so that the tank used transformer leakage alone. Heating then remained concentrated near the input bridge.” Only use each claim when supported by the section's actual facts.

## Checklist for every proposed edit

- [ ] The sentence describes the author's engineering work, a circuit function, a result, or a specific next step.
- [ ] Its point is clear on the first reading; the subject and physical action are concrete.
- [ ] The reason for a design/control change is explained through its function or observed benefit.
- [ ] The paragraph reads as connected prose, not a sequence of disclaimers or choppy slogans.
- [ ] Passive voice is natural. “The diodes were replaced, but the heating remained” is useful; “an establishment of operation was performed” is not.
- [ ] Necessary technical detail is retained; elementary MCU/electronics definitions are omitted.
- [ ] A figure caption describes what is visible. It does not add an unrelated claim about what the picture cannot prove.
- [ ] Table headings name the quantities, pins or functions. They do not narrate how evidence was classified.
- [ ] Missing information is mentioned only where it changes interpretation. State the actual missing quantity and consequence briefly, once in that context.
- [ ] Redundant “does not establish/prove/demonstrate/verify” clauses are removed, not exchanged for synonyms.
- [ ] Uncertainty stays scientifically honest: a suspected cause stays suspected; a temperature decrease is not proof of ZVS; a load setting is not a measured power result.
- [ ] No fact, measurement, cause, test, performance gain or completion status has been invented.
- [ ] Attribution remains accurate without repeating “inherited” or source-record language beside every result.
- [ ] The wording sounds like practical engineering English, not “evidence boundaries,” “identity,” “provenance,” “admissibility,” or “records establish” rhetoric. These are diagnostic cues, not a blind word blacklist.
- [ ] Numbers, units, equations, symbols, measured values, references, labels, source paths and hardware/firmware identities are preserved.
- [ ] No new handoff/upload date or chat history enters the thesis.
- [ ] The edit improves meaning or readability enough to justify changing already revised text.

## Examples from the author's corrections

| Avoid | Preferred treatment |
|---|---|
| “These views do not establish the exact fitted configuration…” | “The V2 board and thermal-camera setup are shown in Figure …” |
| “The inherited measurements …” | “The given component measurements …” or “The measured leakage values …”, with attribution retained where introduced. |
| “The table separates nominal circuit values, supplied measurements and calculated estimates.” | “The table summarizes the parameters used in the calculations.” |
| “Input and output directions are stated from the MCU's perspective.” | “MCU pin assignments for the original controller and V2.” |
| “Matched tests were not performed to isolate each development stage.” | Explain the functional change: “DMA removed the conversion waits from the control loop.” Do not invent a measured speed gain. |
| “The downstream stage regulates VBUS independently; the nodes are distinguished throughout…” | “The MCU regulates the secondary bulk supply. The USB-C PD stage regulates the selected USB-C output voltage.” |
| “The photos do not establish continuous capability.” | Describe the photos. Discuss a missing temperature history once in the thermal interpretation if needed. |
| “Zero-voltage switching was achieved because heating decreased.” | “Half-bridge heating decreased after the tank and timing changes. ZVS still needs to be checked from switch voltage and current at turn-on.” |
| “The 240 W EPR goal…” | Mention once in the discussion as a higher-load question raised in APEC digest feedback. |
| “USB-C laboratory supply” | “USB-C power supply.” |

## Project facts and terminology that must survive editing

- Product: a USB-C power supply based on a high-frequency charge-pump PFC resonant converter. Preserve the original load-focused introduction. Laboratory describes tests or instruments, not the product.
- Project target: 100 W continuous, with a 65 W minimum. The 240 W EPR point is a reviewer's question, not an objective. It appears once in the discussion.
- MCU: identify the device where needed, then use “the MCU.” Introduce project-specific pin roles briefly and name pins by function first. Board-specific assignments matter. Do not merge hardware V1/V2/V3 with firmware development stages.
- MCU regulation concerns secondary bulk voltage. USB-C PD controls the selected connector voltage. PA2 senses primary half-bridge current, not USB output current. Do not infer connector power from a diagnostic voltage-current product.
- Spell out “megahertz” for a general frequency range; retain “MHz” with numerical values.
- Current V2/F410 source is PWR-2.0.4; the shared source's G071 target remains PWR-2.0.3. Earlier powered measurements retain their original attribution. Routine prose uses descriptive firmware stages; exact IDs belong in introduced history, comparisons or build/test records.
- Carrier adjustment changes excitation frequency, not passive LC resonance. Browser calibration searches burst duty, not frequency. Reference-load entries describe physical loads connected by the operator; they do not switch or program a load.
- V2 removed the approximately 9.4 µH series inductor and used about 1.66 nF with transformer leakage. The reported bench software dead time was about 60 ns. Current source defaults are a separate matter.
- V2 winding heating and the 3.3–3.6 A secondary-output region do not supply a matched connector-power result. Copper/via restrictions remain suspected. Diode replacement did not remove the heating.
- The earlier V2 thermal image is from a 95 W run; the separate 100 W CP condition is a load setting. Output voltage was steady while the bridge temperature rose. Do not claim thermal equilibrium or a continuous rating.
- Later V2 load tests use only AC-supply and electronic-load readings from seven captures; exclude their scope rows. Secondary power reached 137.08 W at 13.69 V and 10.01 A, with voltage droop and no thermal equilibrium. This is not connector power or a continuous rating. R3 covers the input bridge; R1 covers the secondary area. The R3 maximum was 83.9 °C at the intermediate 70.75 W point, then lower at subsequent higher loads; R1 rose to 98.3 °C. Do not describe a monotonic input-bridge decrease or identify a region maximum as one diode junction. Capture 017 input power conflicts with voltage × current; retain its local warning and do not infer power factor.
- V3 is a reduced layout with the USB-PD stage removed and secondary rectifiers retained; about 8% estimated net volume reduction. New magnetics were not installed. Do not turn this into measured complete-system power density or improved power capability.
- Keysight traces: yellow = half-bridge switch-node voltage; green = secondary output voltage; blue = USB-C VBUS. State AC coupling when relevant. Do not apply this mapping to unrelated raw C2 records.
- Preserve the current colour V2 schematic views, the crop-only cover image, the removal of paired no-load photographs, and equal 30 mm body side margins.

## Required agent output

Do not edit the thesis directly. Write proposal JSON and a short review to your assigned output paths. Each proposal must contain:

- `id`: stable identifier within your assignment.
- `path`: file relative to `/workspace/thesis`.
- `old`: exact original text, including actual CRLF/LF characters; it must occur exactly once.
- `new`: complete replacement text, with valid LaTeX.
- `reason`: the concrete reading problem and how the change fixes it.
- `facts_preserved`: technical facts or uncertainty that matter to the edit.
- `checklist`: short list of checklist items addressed.

Read bytes and decode UTF-8 when capturing exact replacement text; universal newline conversion can break an otherwise valid patch. Make proposals non-overlapping. Keep equations, quantities, labels and citation commands unchanged. Do not edit generated data tables or archival code: flag a problem in those files separately for the lead. Record every assigned file you reviewed, acceptable passages you deliberately kept, and any uncertainty that needs lead review. Empty proposals are acceptable when the wording already works.

Do not run builds, change firmware, alter source data, commit, push, deploy, publish or write to another agent's output. All source files remain read-only for the proposing agents.

## Lead-agent judgement

The lead checks the complete surrounding passage, not just the replacement. Every proposal receives Accept, Revise or Reject with a specific reason. A fluent sentence that changes the science is rejected. A shorter sentence that obscures a pin, test condition or measured quantity is rejected or revised. A synonym-only change with no useful improvement is rejected.

Score each proposal 0–2 for voice, technical fidelity and flow. Technical fidelity must score 2, and the accepted wording must score at least 5/6 overall. Treat these as editorial scores, not an objective language metric. A hard factual or scope failure overrides the score. For Revise, the lead records its own final wording and checks it again.

After applying accepted/revised edits, the lead checks source integrity, compiles the full thesis, checks cross-references and page overflow, and inspects representative changed pages. Publish only within the user's existing authorization. Give the author the checklist, judgement record and current PDF.
