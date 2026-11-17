# Control, hardware and modeling wording check

Scope: Chapters 05–08 and Appendix C/G prose only. The latest request was to find statements similar to the unclear USB-C regulation/independence wording, while retaining concise technical prose and the user’s direct engineering voice. No broad stylistic rewrite was performed.

Nineteen local replacements were made in 15 TeX files. Source files are frozen. No builds, manifests, GitHub or hardware operations were performed by this agent.

## Changes

### Chapters/05_Modeling_Simulation/02_Uploaded_LTspice_Files.tex

Replaces generic node/power-boundary wording with the actual bulk-to-PD power path and concrete measurement/comparison conditions.

Before: The predecessor regulates a high-voltage output; the prototype has separate isolated bulk and connector VBUS nodes. Model comparison requires corresponding nodes and power boundaries.

After: The predecessor regulates a high-voltage output; in the prototype, the isolated secondary bulk supply feeds the USB-C PD output stage. Comparisons must state where voltages and powers are measured and which stages and auxiliary supplies are included.

### Chapters/05_Modeling_Simulation/03_GaN_Model.tex

Spells out a bare unit-symbol adjective in prose; numeric SI expressions remain unchanged.

Before: At MHz frequency, transition-energy error directly affects calculated loss, so device-name substitution is insufficient.

After: At megahertz switching frequencies, transition-energy error directly affects calculated loss, so device-name substitution is insufficient.

### Chapters/05_Modeling_Simulation/05_Simulation_Cases.tex

Names the PD stage input behavior that an output resistor alone cannot reproduce as voltage/load change.

Before: A fixed resistor at connector voltage does not reproduce the downstream regulator's bulk-bus demand.

After: An output resistor alone does not model the USB-C PD stage's input demand as its output voltage and load change.

### Chapters/05_Modeling_Simulation/07_Startup_NoLoad.tex

States the purpose of precharge without guaranteeing readiness before a timeout/attempt-limit exit.

Before: Limited precharge establishes power for isolated feedback before voltage control.

After: Limited precharge is used to power the isolated feedback circuit before normal voltage control begins.

### Chapters/06_Magnetics_Integration/07_Isolation_Clearance.tex

Names creepage, clearance and dielectric strength instead of referring vaguely to these margins.

Before: The functional isolation path does not establish these margins.

After: Functional isolation alone does not establish creepage, clearance, or dielectric strength.

### Chapters/06_Magnetics_Integration/10_Verification.tex

Replaces assembled-path shorthand with power transfer through the installed magnetics.

Before: Converter tests demonstrate assembled-path power transfer,

After: Converter tests demonstrate power transfer through the installed magnetics,

### Chapters/07_Hardware/06_Resonant_Output.tex

Removes a claim that the output stage separates the resonant transfer function from the voltage setting; states the actual regulation role.

Before: This separates the resonant transfer function from the final connector voltage setting.

After: The USB-C PD stage regulates the output voltage from this bulk supply.

### Chapters/07_Hardware/07_USBC_Interface.tex

States PD output regulation and input/output net roles directly; states MCU bulk regulation separately and locates cable drop at the load.

Before: The isolated bulk supply was connected to the USB-C connector through the MPQ4242GVE-0000-AEC1-P stage.

After: The MPQ4242GVE-0000-AEC1-P stage regulates the USB-C output voltage from the isolated bulk supply.

Before: The bulk and connector nodes are named separately as \texttt{V\_PW\_OUTPUT\_BULK} and \texttt{USB\_PD\_OUT} in \Cref{fig:schematic-usbc}.

After: In \Cref{fig:schematic-usbc}, \texttt{V\_PW\_OUTPUT\_BULK} feeds the stage and \texttt{USB\_PD\_OUT} supplies the USB-C output.

Before: The secondary bulk voltage is regulated by the front-end controller using the secondary-voltage feedback signal received at MCU input PA1. Connector VBUS also depends on the downstream power path and cable drop, so the measured node is stated with each result.

After: The MCU regulates the secondary bulk voltage using feedback at PA1. The USB-C PD stage regulates its output to the selected PD level. Voltage at the load can differ because of cable drop, so the measurement point is stated with each result.

### Chapters/07_Hardware/10_Auxiliary_Power.tex

States precharge intent without promising secondary-sensing readiness despite the configured attempt-limit exit.

Before: Bounded precharge bursts and settling intervals establish the secondary supply before normal control.

After: Bounded precharge bursts and settling intervals are used to power the secondary-side sensing before normal control.

### Chapters/07_Hardware/16_V2_F410.tex

Uses concrete no-carrier-synchronization phrasing for ADC acquisition and states the PD input/output net roles.

Before: ADC1 continuously scans primary voltage at PA0, secondary-bulk voltage at PA1, and half-bridge current at PA2 through DMA2 Stream0 Channel0, independently of carrier phase.

After: ADC1 continuously scans primary voltage at PA0, secondary-bulk voltage at PA1, and half-bridge current at PA2 through DMA2 Stream0 Channel0 without synchronization to the carrier.

Before: USB-PD sheet 2 includes the MPQ4242GVE-0000-AEC1-P output stage and separate \texttt{V\_PW\_OUTPUT\_BULK}/\texttt{USB\_PD\_OUT} nodes.

After: USB-PD sheet 2 includes the MPQ4242GVE-0000-AEC1-P output stage, fed from \texttt{V\_PW\_OUTPUT\_BULK} and supplying \texttt{USB\_PD\_OUT}.

### Chapters/08_Control_Firmware/01_Control_Objectives.tex

States that the PD stage regulates the output to the selected PD level instead of saying it sets connector VBUS.

Before: the downstream MPQ4242 sets connector VBUS.

After: the MPQ4242 USB-C PD stage regulates the output voltage to the selected PD level.

### Chapters/08_Control_Firmware/02_Architecture_Timing.tex

Explains free-running acquisition and foreground concurrency without an ambiguous independence claim.

Before: Acquisition is free-running and independent of both carrier phase and the foreground loop.

After: The scan is free-running without synchronization to the carrier, and DMA acquisition continues while the foreground loop runs.

### Chapters/08_Control_Firmware/15_PWR_2_Port.tex

Replaces scan retains / independent wording with actual sequential sampling without carrier synchronization.

Before: The free-running ADC scan retains primary voltage, secondary-bulk voltage, and primary current, sampled sequentially and independently of carrier phase.

After: The free-running ADC scan samples primary voltage, secondary-bulk voltage, and primary current sequentially, without synchronization to the carrier.

### Backmatter/Appendices/C_Firmware_Documentation.tex

Makes bounded carrier-alignment polling an attempt, including its timeout, rather than a guaranteed aligned request.

Before: The software request is aligned with a carrier boundary without an interrupt on every \SI{1}{\mega\hertz} cycle. Interrupt latency and GPIO execution still affect the physical edge.

After: Polling attempts to align the software request with a carrier boundary without an interrupt on every \SI{1}{\mega\hertz} cycle; it can time out without observing an update. Interrupt latency and GPIO execution still affect the physical edge.

### Backmatter/Appendices/G_Software_Tools.tex

States which external measurements feed the results and that the numerical module runs without the incomplete UI, instead of generic kept separate / works independently phrases.

Before: or delivered USB-C power. They are kept separate from the external
load-current and VBUS measurements used for Chapter~\ref{ch:results}.

After: or delivered USB-C power. The results in Chapter~\ref{ch:results} use external
load-current and VBUS measurements.

Before: The numerical module works independently.

After: The numerical module runs without the page interface.

## Preservation checks

`python3 /workspace/tooling/usb-pd-wording-review/validate-control.py` passes for all 15 files. Math occurrences, SI expressions, numeric tokens, labels, citations, references/source paths, complete protected environments, line-ending styles and final-newline status match the baseline. All tables, figures, code listings, equations, evidence and original assets are unchanged. Checks and diff are in `control-validation.json` and `control-prose.diff`.

One added repeat of the MPQ4242 name in the first draft was removed before finalization; numeric-token counts remain unchanged. A second read-only reviewer checked the complete final 19-edit set and found no remaining issues. The review also checked acquisition, bounded polling and numerical-module behavior against the archived source; see `control-independent-review.md`.

## Deliberately retained terminology

Technical distinctions such as independent hardware interlocks, external measurement checks, isolated voltage domains, model/measurement power boundaries and software tests that do not need the browser are retained where they have a concrete meaning. This was not a global replacement of independent, node, or boundary.

## Outside-scope items sent to the parent

- Chapter 04 / 10_USBC_Adaptation.tex: “OVP independently selects soft holdoff or hard inhibition” can wrongly suggest an independent protection channel; it is firmware in the same MCU.
- Chapter 02 / 07_USBC_Context.tex: “negotiates and regulates” should preserve the difference between intended USB-PD function and the fixed-output electrical tests actually demonstrated.

The parent confirmed both outside-scope items were corrected in the root-owned pass. No unresolved findings remain.
