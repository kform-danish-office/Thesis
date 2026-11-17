# Chapters 07–08 voice polish

All assigned prose was reread against the new immutable baseline at `/workspace/tooling/thesis-voice-polish/before`. The pass changed 18 hardware files (62 prose lines) and 16 firmware files (58 prose lines). Each prose paragraph or equation lead-in occupies one source line.

The main correction was to remove forced passive grammar from descriptions of circuit behavior and simple references. Actual assembly, tests, changes, and calculations remain factual and impersonal, with natural passive wording where appropriate. Definitions and physical relationships use direct subjects and verbs. No first- or second-person prose was introduced.

Representative before/after changes:

- “Logic commands are sent to the integrated driver by the STM32. On PA8 and PA9, the fixed … carrier is generated” became “Logic commands are sent from the STM32 to the integrated driver. PA8 and PA9 carry the fixed … carrier.”
- “The MCU can therefore be started before enough supply voltage is available for a useful isolated-feedback reading” became “The MCU can therefore start before the isolated feedback has enough supply voltage for a useful reading.”
- “The required current must be carried by power contacts and copper” became “Power contacts and copper must carry the required current.” The following proposed review remains “would be reviewed.”
- “Through `STATUS`, … were inspected” became “`STATUS` was used to inspect …”.
- “Power could be transferred by the hardware” became “The hardware could transfer power.” The controller implementation still states that the carrier was kept fixed and enable bursts were used.
- “Carrier-update sync requests and low-time margin are also allowed for by the scheduler” became “The scheduler also allows for carrier-update sync requests and low-time margin.”

Preserved evidence and contribution boundaries:

- The modified manufactured V1.0 board remains the measured assembly. V1.1 and V1.2 remain unmanufactured revisions.
- The charge-pump resonant circuit and supplied planar magnetics remain inherited. This project's PCB, supporting circuits, control, and bring-up changes remain distinct additions.
- The F410 timing figures remain nominal calculations requiring captures. The frozen PWR-2.0.1 thesis source remains separate from current working-source features. No software check was changed into powered verification.
- The reported V2 point remains separate from the matched V1.0 results. Missing assembly, calibration, timing, duration, thermal, and power-density information remains missing.
- V3 design, interface work, reviews, manufacturing, and bring-up remain planned or unfinished. Conditional comparisons and reviews remain conditional.
- No new measurements, photographs, sources, or technical claims were added.

Final scoped checks passed against the new baseline for all 34 files: exact numeric sequence, all math, all 45 protected environment blocks, complete LaTeX command and balanced-argument sequence, and the full raw LF/CRLF newline sequence. This also preserves headings, tables, figures/captions, listings, TikZ, references, labels, citations, and paths. No prose personal-pronoun candidates remain. No wording fix was blocked by protected macro order.

Only the 34 owned thesis sources and this note were edited. No build, global manifest edit, Git action, deployment, publication, or hardware operation was performed. Sources are frozen for root review.
