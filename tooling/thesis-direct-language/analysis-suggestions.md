# Chapter 4 direct-language suggestions

Read-only review of all Chapter 4 prose, headings, captions and qualitative table text. No thesis source, equations, numerical values, diagrams or reference labels were changed. Most of the chapter is already direct technical analysis; the following are the clearest opportunities to remove abstract or administrative phrasing.

## Recommended replacements

### `01_Topology_Overview.tex`

Before:

> Throughout the analysis, \(V_{\mathrm{sec}}\) denotes bulk voltage and VBUS denotes connector voltage.

After:

> \(V_{\mathrm{sec}}\) is the secondary bulk voltage, and VBUS is the USB-C output voltage.

Reason: define the quantities directly, without explaining how the document refers to them. Preserve the existing inline math expression exactly.

### `02_Switching_Cycle.tex`

Before caption:

> Ideal pump-branch intervals in the modified charge-pump topology. Device names refer to functional paths in the reference analysis.

After caption:

> Ideal charge-pump intervals during one switching cycle.

Reason: the table describes low-side/high-side states, not revision-specific component designators. The preceding sentence and citation already identify the reference analysis; the second caption sentence reads like a defensive note and adds no useful circuit detail.

Before:

> Burst restart begins from the inductor currents and capacitor voltages left by the idle interval. It therefore requires separate assessment from the periodic sequence, particularly during sparse no-load packets.

After:

> Each burst restarts with the inductor currents and capacitor voltages left by the idle interval. The first cycles can therefore differ from steady switching, particularly during sparse no-load packets.

Reason: state the physical difference rather than requiring an unspecified assessment. “Can” preserves uncertainty and does not claim a measured transient result.

### `03_Line_Cycle_PFC.tex`

Before:

> Power quality must therefore be assessed with the final controller.

After:

> PF and current THD must therefore be measured with the final controller.

Reason: name the quantities being measured. This does not add numerical limits or claim the measurements have already been completed across the full operating range.

### `05_Pump_Inductor.tex`

Before phrase following the existing measured-inductance sentence:

> in-circuit current and clamp timing determine agreement with the assumed sequence.

After:

> in-circuit current waveforms and clamp timing are needed to check the triangular-current assumption.

Reason: names the waveform check and the assumption directly. Preserve the preceding SI quantities and section reference.

### `11_Design_Summary.tex`

Before:

> Table~\ref{tab:analysis-design-summary} lists the values used to connect the reference equations to the prototype. It separates nominal circuit values, supplied magnetic measurements, and calculated estimates.

After:

> Table~\ref{tab:analysis-design-summary} lists the nominal circuit values, supplied magnetic measurements, and estimates used in the calculations.

Reason: the original explains the table’s classification process instead of simply introducing its contents.

Suggested table wording (keep all value cells and mathematical expressions unchanged):

| Existing text | Direct replacement |
| --- | --- |
| `Quantity & Value & Interpretation` | `Parameter & Value & Notes` |
| `Nominal implementation value` | `Nominal circuit value` |
| `Inherited A/B measurements` | `Supplied measurements for inductors A and B` |
| `Final discrete series contribution` | `External series inductance` |
| `Inherited primary-referred measurement` | `Supplied primary-referred leakage measurement` |
| `Sum if the stated contributions act in series` | `Discrete inductance plus leakage, assuming series connection` |
| `Inherited transformer-variant range` | `Range of supplied transformer measurements` |
| `Primary-to-secondary step-down convention` | `Primary-to-secondary turns ratio` |

The conditional series assumption remains explicit. The supplied-measurement origin remains explicit where it matters. These edits do not turn estimates or inherited measurements into new fitted-board measurements.

## Wording that should remain technical

The ZVS charge-polarity, timing and missing-calibration qualifications are useful analysis, not legal disclaimers. Keep them. Likewise, the resonance/gain model limits and the distinction between primary current and USB-C output current affect the equations and must remain. The V2 power-figure caption’s named-net sentence explains the separated schematic boxes and can remain. I found no need to simplify the switching equations or add MCU/electronics tutorials.
