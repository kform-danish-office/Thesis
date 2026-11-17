# Results, discussion and appendix wording check

Scope reviewed: all explanatory prose in Chapters 9–12 and Appendices A/B/D/E/F/J. Tables, figures, captions, math, source records and raw data were preserved. This was a targeted follow-up to the user's objection to vague USB-C stage regulation and bare unit-symbol prose, not another broad thesis rewrite.

Thirteen files received sixteen small prose replacements. Undefined “downstream” references now identify the USB-C PD output stage. The measured USB-C output voltage and MCU-regulated secondary bulk supply are described directly. Generic wording about separating nodes or retaining an “equivalent-function volume” was replaced with the relevant measurement or complete-supply volume. No negotiation, dynamic-independence or conformance claim was added.

Two overstatements of burst timing were qualified: the firmware attempts carrier-boundary alignment, and the contribution is fixed-carrier burst scheduling. The code's bounded polling cannot guarantee that every physical enable edge is synchronized. This matches existing controller limitations elsewhere in the thesis.

No bare “MHz” prose was found in the assigned chapters or explanatory appendices. Numerical quantities such as `\SI{1}{\mega\hertz}` remain unchanged. Mathematical independence in uncertainty propagation, independent hardware protection, and independent safety assessment remain because they state actual technical requirements. Measurement-boundary and provenance wording in data/provenance appendices was retained where it affects interpretation.

All invariance checks pass: mathematical expressions, SI quantities, numeric tokens, citations/references/source paths, complete protected environments and original line-ending styles. See `results-invariance.json` and machine-readable replacements in `results-edits.json`. No build, source manifest, publication, firmware, hardware or GitHub changes were performed by this task.

## Replacements

### Chapters/09_Experimental_Methods/chapter.tex

Before: The setup had to separate secondary-bulk regulation from connector output, and controller telemetry from external measurements.

After: The setup monitored both secondary-bulk and USB-C output voltage. External instruments supplied the output-power measurements; controller telemetry was used for diagnostics.

### Chapters/09_Experimental_Methods/04_Instrumentation.tex

Before: Controller ADC and UART data were used for sensing and command diagnostics, rather than independent connector-output measurements.

After: ADC readings and UART data were used to diagnose controller sensing and command handling.

### Chapters/09_Experimental_Methods/04_Instrumentation.tex

Before: In Table~\ref{tab:channel-definitions}, CH1--CH4 denote oscilloscope channels, independent of MCU port or package-pin identifiers.

After: In Table~\ref{tab:channel-definitions}, CH1--CH4 label the oscilloscope inputs.

### Chapters/10_Results/03_Steady_State.tex

Before: where \(V_\mathrm{BUS,avg}\) is the USB-C connector mean. The upstream controller regulates the separate secondary intermediate bus.

After: where \(V_\mathrm{BUS,avg}\) is the mean USB-C output voltage. The MCU regulates the secondary bulk supply feeding the USB-C PD stage.

### Chapters/10_Results/03_Steady_State.tex

Before: These means establish downstream regulation rather than ripple or transient limits.

After: These averages show that the USB-C PD output remained close to its selected voltage; ripple and transient limits require separate measurements.

### Chapters/11_Discussion/01_Key_Findings.tex

Before: The downstream stage maintained average connector voltage across these points.

After: Average USB-C output voltage was maintained across these points.

### Chapters/11_Discussion/02_Topology_Adaptation.tex

Before: The downstream stage regulates connector voltage, while the upstream loop maintains its secondary-bus headroom.

After: The USB-C PD stage regulates the output voltage to the selected PD level, while the MCU regulates the secondary bulk supply feeding it.

### Chapters/11_Discussion/02_Topology_Adaptation.tex

Before: across the charge pump, burst schedule, secondary-bus headroom, downstream stage, and thermal path.

After: across the charge pump, burst schedule, secondary bulk supply, USB-C PD output stage, and thermal path.

### Chapters/11_Discussion/03_Control_Contribution.tex

Before: Enable requests are aligned to carrier boundaries to limit partial intervals.

After: The firmware attempts to align enable requests with carrier boundaries to limit partial intervals.

### Chapters/11_Discussion/04_Open_Circuit_Safety.tex

Before: Discharge and downstream-stage dynamics modify this relationship.

After: Capacitor discharge and the response of the USB-C PD stage also affect the voltage rise.

### Chapters/11_Discussion/09_Future_Improvements.tex

Before: Measured magnetics, parasitics, downstream-stage behavior, and packet energy would then support validation of the installed converter model.

After: Measured magnetics, parasitics, USB-C PD stage behavior, and packet energy would then support validation of the installed converter model.

### Chapters/11_Discussion/chapter.tex

Before: The remaining limitations are magnetic and input-path heating, sustained output, and equivalent-function volume.

After: The remaining questions concern magnetic and input-path heating, sustained output, and the volume of a complete USB-C PD supply.

### Chapters/12_Conclusion/01_Project_Summary.tex

Before: sensing, auxiliaries, the downstream stage, and the MCU were integrated

After: sensing, auxiliaries, the USB-C PD output stage, and the MCU were integrated

### Chapters/12_Conclusion/02_Research_Questions.tex

Before: magnetics, downstream stage, sensing, and digital control were integrated

After: magnetics, USB-C PD output stage, sensing, and digital control were integrated

### Chapters/12_Conclusion/03_Contributions.tex

Before: synchronized fixed-carrier bursts, direct secondary-voltage regulation,

After: fixed-carrier burst scheduling, direct secondary-voltage regulation,

### Backmatter/Appendices/A_Analytical_Equations.tex

Before: \(V_{\mathrm{BUS}}\) the downstream USB-C output. These are separate circuit nodes. Load power is calculated from the connector voltage. The controller's bulk-voltage measurement is upstream of the output stage.

After: \(V_{\mathrm{BUS}}\) the USB-C PD output voltage. The MCU measures secondary bulk voltage upstream of the USB-C PD stage. Load power is calculated from connector voltage and external load current.

## Independent meaning review

Read-only review of all sixteen replacements and their surrounding source found no actionable issues. Stage roles remain accurate, regulation remains limited to recorded averages, and attempted carrier alignment is correctly qualified. The dual-voltage setup description is supported by the unchanged CH2/CH3 assignments and retained captures. No open findings remain.
