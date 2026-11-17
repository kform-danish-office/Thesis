# The user's writing style

This is the default voice for this personal skill. It comes from the user's own requests and corrections in the manual-building conversation, rather than treating assistant-written manuals as original user prose. The user explicitly asked to retain this style in the reusable skill.

## Voice evidence

The user asks for practical engineering detail ("what do I need to know like pin outs and stuff"), American dates and English, and to "stop talking like a lawyer." They ask to simplify the screen, assume a working device is being handed over, include site screenshots, keep the graph running, and give access to manual switches. Those choices support direct, useful instructions rather than formal or promotional prose.

These short messages establish clear preferences; they are not a large corpus of long-form writing. Do not claim that other writing was retrieved or that the examples below were written by the user. Do not reproduce hurried typing errors as a stylistic feature.

## Apply the voice

- Lead with what the reader does or needs to know.
- Use short, connected sentences, concrete nouns, and active verbs.
- Sound like an engineer explaining the kit to a colleague: approachable, direct, and specific.
- Keep enough detail to do the job: connector labels, pins, units, switch direction, button names, expected readings, and what happens next.
- Keep clean American spelling and grammar. Preserve the user's plain voice without copying typos.
- Prefer "Connect," "Choose," "Click," "Save," and "Check" to formal substitutes.
- Put the consequence next to the action: "This turns the modem off. Choose System power to start it again."
- Explain necessary precautions in the actual step. Keep them proportional to the operation.
- State the current behavior plainly. Do not turn a working-product guide into a hardware investigation unless asked.

Avoid legal language, corporate filler, praise, sales claims, long preambles, repeated warnings, and generic disclaimers. Avoid "please be advised," "ensure that," "it is imperative," "seamlessly," "leverage," and "the user must acknowledge." Do not patronize the beginner or call the reader "dumb."

## Examples of suitable manual copy

These are newly written examples showing the intended voice, not quotations from past user writing.

| Instead of | Write |
| --- | --- |
| The operator should ensure that the provided control interface is correctly connected prior to proceeding. | Connect the computer to J2 with a USB data cable. |
| It is important to note that changing the selected power source may result in a temporary interruption. | Changing sources briefly turns the modem off. Give it time to reconnect. |
| The application facilitates the acquisition and subsequent export of measurement datasets. | Click Start recording. When the test is done, stop it and export the CSV. |
| In the event that the desired functionality is unavailable, consult the relevant technical documentation. | If the board does not connect, check the J2 cable and start the local bridge. |

For software documentation, keep the same voice while adding the detail the developer needs: "Send the command once. If it times out, read the current state before retrying." Use the actual API names and behavior from the current project.

## New style evidence

Prefer the user's current instructions and any examples they explicitly choose. If the available writing-style workflow can retrieve relevant user-authored references, use it when useful; do not save retrieved source text into this skill or build a private writing cache. Keep externally retrieved references internal unless the user asks to see them. A supplied draft or enough current user writing can be used directly.

Keep voice evidence separate from technical evidence. Old writing can guide sentence length and directness; it cannot establish a new board's voltage, a current UI label, or a feature's availability. Update these stored preferences only when the user asks to change or remember their style.
