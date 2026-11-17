# Choose the right manual

Use only the parts the current product and audience need. These are planning aids, not mandatory chapter lists.

## Quick start or operator guide

Make the first successful use easy to follow:

1. Say what the product does and what the reader needs.
2. Show the product and the important connections with numbered callouts.
3. Explain setup and startup in the order the reader will actually do them.
4. Show the useful screen, expected result, and main controls.
5. Explain a normal task, saving/exporting results, and how to finish.
6. Give concise fixes for the most likely symptoms.

For an assembled working kit, avoid assembly, calibration, address-strap investigations, and speculative faults in the first-use path. Do not invent successful measurements for a photographed unit; state what the reader should expect according to verified product behavior.

Place the right screenshot beside the relevant steps. Explain a stopped capture if its button has changed back to Start, and a routing control whose label now means it is already enabled. Distinguish selecting an option from applying it, a requested source from a measured rail, and closing the browser from turning hardware off.

## Engineering/user reference

Provide the details needed at a bench:

- Product/revision identification, function, supported operating modes, and actual limits.
- Connector table: designator, purpose, mating connection, signal names, pins, direction, units/voltage domain, and ground where supported by evidence.
- Explicit pin-numbering viewpoint: top/bottom, pin 1 mark, connector face, and whether the board picture is mirrored.
- Physical switches, jumpers, fitted options, and left/right or on/off meanings in the stated viewpoint.
- Power routing, expected behavior during transitions, status indications, and measurement meaning.
- Normal use, manual override, shutdown, and specific recovery steps.

Separate supply input from a test point or logic pin. A regulator target is not proof of a measured or loaded output. A BOM value is not proof of what was fitted. Do not copy stock components over a user's confirmed assembly change. Use the smallest clarification necessary when an unknown would make the wiring instructions unreliable.

## Software integration guide

Ground the guide in the current implementation, not the feature wish list:

- System overview: UI, local service, USB bridge, device bus, and where data is stored.
- Supported OS/runtime, driver/native-library setup, startup, and device selection.
- Transport details: mode, address convention (for example 7-bit I2C), units, endianness, supported rates, and ownership of the native interface.
- Actual API routes, request/response examples, tokens/origins as applicable, command ordering, and observable completion.
- Telemetry/register fields, scaling formulas, signed values, validity flags, sample timestamps, and averaging/conversion timing.
- Power/SIM/other output commands, confirmation or preparation behavior, and error handling.
- Logging/export schema, retention, stop/clear semantics, and a minimal integration example.
- Recovery and limitations. Label extensions and unimplemented features as planned rather than working.

Keep UI display smoothing distinct from native ADC averaging and raw recording samples. Do not present a configured bus rate as scope-measured throughput. Keep HTTP command examples separate from hardware register examples. Avoid blind automatic replay of a timed-out output command; document the implementation's actual state-check/retry behavior.

## Evidence ledger

Keep a small internal table while drafting:

| Fact | Current evidence | Status |
| --- | --- | --- |
| Critical voltage, connector pin, switch direction, default, or command effect | User correction, current code, board marking, observed UI, or supplied source | Confirmed, superseded, unknown, or not physically measured |

Use source evidence internally without adding unwanted schematic citations to a finished operator manual. Keep uncertainties attached to the exact claim instead of padding every page with warnings. A user correction can supersede a stock design; avoid silently resolving a safety-critical conflict without acknowledging the particular uncertainty.

## Updates

Read the existing manual before editing. Preserve its useful structure, filename, audience, and brand. Update the source and rendered deliverable together when changing that document. Refresh screenshots when the controls or labels they illustrate changed. Label the actual UI/firmware/bridge versions separately if they differ.
