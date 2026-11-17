# V2 main-document schematic mapping review

Read-only assessment of the current main-text schematic inclusions and latest V2 source, `Pictures/Thesis/07_Hardware/Schematic_V2_F410_2026-10-27.pdf`. No thesis sources, assets, builds, repository or publication state were changed by this reviewer. Review-agent guidance was applied to technical consistency; this is a planned figure substitution, not a request to redesign the circuit.

## Required consistency changes

[P2] Scope the MCU figure to the actual V2 implementation — `Chapters/07_Hardware/08_Sensing.tex:9`

The existing caption describes TLV9064 analog buffers and PA8/PA9/PA10. V2 sheet 4 has no TLV9064 and directly connects the three feedback nets to PA0–PA2. Its carrier outputs use PA8/PB13 and its enable uses PA11. A file-only substitution would produce a false caption and an apparent contradiction with the unqualified buffer statement immediately above it. Keep that statement explicitly about the original test platform, identify the new figure as V2, and describe the direct feedback connections and V2 command assignments. The existing table of PA0/PA1/PA2 roles remains valid. Chapter 7's later V2 section already records the differences accurately.

[P2] Do not equate displayed V2 part labels with the fitted V1 test configuration — `Chapters/07_Hardware/03_Charge_Pump_Network.tex:14`

The current caption says component values follow this drawing. After swapping to V2, it must not make the preceding V1 fitted-part account appear to come from that image. V2 draws S4D02120T for D4/D5/D9/D10 and D6–D8, a 10 µF C25 link capacitor, SER1512-103MED at L4, and an unspecified C26. The original test account instead identifies PU1JLWH in its component list, a 22 µF V1.0 link and the fitted two-inductor resonant arrangement. Preserve those historical facts and caption V2 as the common circuit reference; distinguish fitted changes in the text. No power-stage numerical recalculation is needed for this display change.

## Figure mapping

| Main-text use | Current figure label | V2 source | Minimal prose/caption update |
| --- | --- | --- | --- |
| Ch4 power-stage structure | `fig:analysis-v11-power-stage` | Sheet 3, complete circuit-region crop | The overview sentence and caption should identify V2 and its common pump/resonant power paths. Retain PA10 specifically as the original prototype's enable; the power sheet uses functional port names, not those MCU pins. |
| Ch7 input filter/bridge | `fig:hw-input-schematic` | Sheet 3, separate input and bridge crops | Identify V2 sheet 3. Input chain and D4/D5/D9/D10 designators retain their roles. The existing V1.0 fitted choke history remains a historical comparison, not a V2 fitted claim. |
| Ch7 pump/DC link | `fig:schematic-v11-power-stage` | Sheet 3, complete circuit-region crop | Identify V2 sheet 3; change the first local “In V1.1” circuit-description reference to V2/common drawing. Preserve the V1.0/V1.1 C25 history and historical component-list evidence. Remove the unqualified statement that fitted values follow the displayed drawing. |
| Ch7 USB-C output | `fig:schematic-v11-usbc` | Sheet 2, complete USB-C circuit region | Caption V2 sheet 2. The U1 MPQ4242 stage, R3 current sensing, J1 connector, and `V_PW_OUTPUT_BULK`/`USB_PD_OUT` names still match the prose. |
| Ch7 analog feedback | `fig:schematic-v11-mcu` | Sheet 4, MCU/control-sense region | Apply the MCU finding above. Caption the V2 pins and direct feedback; preserve original buffered-platform history. |

The internal `v11` figure labels can remain stable without misleading the reader because labels do not print. If renamed for maintainability, update every reference together; avoid a stale-reference-only build failure. No figure in the listed main-text scope needs to keep an older schematic merely to preserve the circuit-operation explanation. Original V1.0/V1.1 full drawings should remain in the appendix as the historical source record.

## Confirmed shared designators and roles

- Input: F1 fuse, R13 inrush element, R14 varistor, L2 filter, C21–C23 capacitors, U11 CAP300DG discharge, D4/D5/D9/D10 bridge.
- Power stage: U3 LMG2652; C24 pump capacitor; L3 pump inductance; D6–D8 steering network; C25 pumped-link capacitance; C26/L4/T1 resonant branch; CR1–CR4 secondary rectifier.
- Feedback and supply: U5 AMC0330; U4/U6 LMR54410; `VSW`, `HVVCC`, `MCU_3_3V`, `SEC_3_3V`; functional `H_GATE`, `L_GATE`, `GAN EN`, `V_SENSE_P`, `V_SENSE_S`, `I_SENSE_P` ports.
- USB-C: U1 MPQ4242, R3 0.01 Ω connector-current resistor, J1 connector, separate secondary-bulk and connector-output net names.

## Document differences to keep scoped

These observations do not prevent using cleaner V2 drawings for the shared functional explanation. They do mean the prose should not add a blanket claim that every V1.1 and V2 component or controller connection is identical.

- Sheet 3 replaces input connector J2 (703W-00/52) with P3 (691322110003), preserving the mains-input role. Current local prose does not name that connector, so no new prose is required.
- Sheet 3 changes the diode family from PU1JLWH to S4D02120T and the L4 part from 74439346082 to SER1512-103MED. Existing Chapter 7 V2 detail already scopes these labels.
- Sheet 3 shows R50 returned to PGND rather than the old sheet's GND label and adds C7 1 nF between PGND and GND. Do not redraw or relabel these nets when making display crops. Existing new-source text describes R50 at primary ground.
- Sheet 2 changes L1 part label from 7443551470 to 744393665047, but main USB-C prose identifies only its function. U1, R3, connector and important bulk/output net names remain stable.
- Sheet 4 integrates the F410 MCU, eliminates U9 TLV9064 buffers, remaps carrier/enable/UART pins, and changes service-header details. Original G071 carrier/enable history and software target records must retain their own assignments.

No independent netlist/simulation equivalence proof was requested or performed. The figure substitution is supported for a common functional circuit explanation, with board-specific connections and fitted test configurations retained explicitly.
