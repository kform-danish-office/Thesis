# Lead judgement: second Terra rewrite

Four GPT-6.1 Terra agents read 162 authored TeX files. The final proposals contain 31 rewrites: 18 accepted, 12 rewritten by the lead, and 1 rejected. Scores are editorial judgements, not a language metric. Each accepted final passage was checked for voice, technical fidelity and flow.

The first pass was returned for deeper paragraph work. A punctuation-only thermal edit and a synonym-only results edit were withdrawn. The second pass connects design changes to their reasons and results, while preserving the original introduction and useful existing explanations.

| Proposal | Decision | Proposed V/T/F | Lead judgement |
|---|---|---|---|
| opening-01 | Accept | 2/2/2 | Removes repeated V1 attribution while keeping the reported V2 point separate from the measured V1 result. |
| opening-02 | Accept | 2/2/2 | Connects the V2 tank change to series-inductor heating, as described in the testing section. |
| opening-03 | Accept | 2/2/2 | Explains the power path once, in circuit order, with the two regulators and PA1 feedback correctly assigned. |
| opening-04 | Accept | 2/2/2 | States the continuous-test conditions directly and gives the load-removal controls their physical purpose. |
| opening-05 | Revise | 2/2/1 | The proposed sentence can attach loaded/no-load operation to startup precharge as well as duty limits. Separate those functions. |
| opening-06 | Accept | 2/2/2 | Organizes hardware and firmware work by development stage and explains the tank-change trigger. |
| opening-07 | Accept | 2/2/2 | Separates the repeat test, later tank tests and volume comparison without dropping requirements. |
| circuit-01 | Accept | 2/2/2 | Links heat paths and thermal images to the longer temperature measurements needed for sustained operation. |
| circuit-02 | Accept | 2/2/2 | Keeps the V1 and V2 fitted-component distinction while removing a redundant explanatory aside. |
| circuit-03 | Accept | 2/2/2 | Combines repeated statements about the reported 85 W point into its test conditions and planned repeat. |
| circuit-04 | Revise | 1/1/2 | Some thermal behavior has already been observed. Describe the remaining checks without implying that no thermal measurements exist, and retain the pre-installation origin of the given values. |
| circuit-05 | Accept | 2/2/2 | Groups the available calculations and inputs before the switched-model and calibration work still needed. |
| circuit-06 | Revise | 2/1/2 | Waveform comparisons are planned model checks. Keep that prospective status instead of implying that bulk ripple and commutation have already been checked. |
| circuit-07 | Accept | 2/2/2 | Connects heat generation, transfer and removal to what the surface images show and the temperature histories needed. |
| control-01 | Accept | 2/2/2 | Explains DMA through the removed foreground wait, retaining the exact ADC sample setting. |
| control-02 | Reject | 2/2/1 | The original already explains the calibration search and browser interface clearly. The rearrangement adds little and does not justify another edit. |
| control-03 | Accept | 2/2/2 | Expands the ambiguous interval shorthand and distinguishes software diagnostics from measured jitter. |
| control-04 | Revise | 1/2/2 | The measurement list is useful, but PA10 should be identified by its burst-enable function in the rewritten sentence. |
| control-06 | Revise | 2/1/2 | Keep the original possibility of delayed duty adjustment; the prose should not imply a separately measured timing effect. |
| control-07 | Revise | 2/1/2 | Minimum scheduled burst duration does not guarantee complete physical carrier cycles. The baseline polling can time out; describe the intended reduction in partial cycles. |
| control-08 | Accept | 2/2/2 | Groups programming recovery and erase recovery by operation, preserving the remaining erase-interruption failure and output-OFF fallback. |
| control-09 | Revise | 1/1/1 | The proposed where-clause suggests selective error bars, whereas the source omits them. State the missing uncertainty inputs directly and retain the actual presentation choice. |
| results-open | Accept | 2/2/2 | Maps each mean voltage to its error and removes a duplicate conclusion without changing values. |
| results-v2-secondary | Accept | 2/2/2 | Separates the comparable output observation from the heating sequence and keeps the winding cause suspected. |
| results-v3 | Revise | 1/2/2 | Replace the vague ending about assessment with the concrete layout and build status. Keep the external USB-PD stage in the complete-supply comparison. |
| results-summary-v3 | Accept | 2/2/2 | Corrects the ambiguous grammar that could read as removal of secondary rectification. The layout-only status stays explicit. |
| results-firmware-development | Revise | 2/1/2 | The source confirms bounded optional PA0 feed-forward in particular control branches. Use can cap rather than an unconditional duty relationship and name pins by function. |
| results-failures | Revise | 2/2/1 | The problem-to-change sequence is stronger, but retain the original load-classification contribution and identify its PA2 role. |
| results-contribution-firmware | Accept | 2/2/2 | Groups control features by operating role and explains why V2 needed timer and ADC remapping. |
| results-lessons-hotspot | Revise | 1/2/2 | The causal sequence is useful. Replace remains suspect with a direct description of the possible restriction. |
| results-summary-v2-target | Revise | 1/2/2 | The new conclusion still repeats a broad comparison disclaimer. State the V2 change and result directly, retain the missing temperature history beside the 95 W run, and make the repeat-test work concrete. Routine component model names are unnecessary here. |

## Lead rewrites

### opening-05

> The gallium-nitride (GaN) half bridge operated at a nominal \SI{1}{\mega\hertz}, with average power controlled by bursts of switching cycles. Feedback samples were supplied through a circular direct memory access (DMA) buffer. Startup precharge was implemented alongside separate burst-duty limits for loaded and no-load operation. The USB-C PD stage provided the tested \SI{5}{\volt}, \SI{9}{\volt}, \SI{15}{\volt}, and \SI{20}{\volt} USB-C settings.

### circuit-04

> The given electrical measurements were taken before installation and used in the converter calculations. Power was transferred through the installed magnetics during converter tests. The remaining checks on installed parameters, temperature, and isolation are listed in \Cref{tab:mag-verification-actions}.

### circuit-06

> The model must resolve carrier-scale phase, clamp timing, and energy per active cycle, as well as average transfer over each burst and the line-cycle energy imbalance in the DC link and secondary capacitors. Nominal series resonance is near \SI{0.989}{\mega\hertz}, but turn-on phase also depends on magnetizing current, pump current, and rectifier state.  Calibration requires matched input and secondary demand, followed by separate comparisons of voltage envelopes and switching waveforms. Both comparisons are needed to assess bulk ripple and commutation current as well as mean VBUS. Chapter~\ref{ch:results} reports these quantities separately.

### control-04

> Loaded tests checked delivered voltage and burst structure at a fixed output setting. Because the records begin after startup, synchronized measurements of initial conditions, precharge, output rise and peak, the burst-enable signal (PA10), inhibition, decay, and fault status are still needed to quantify startup and shutdown.

### control-06

> Voltage feedback allowed the burst command to increase or reduce energy transfer as the sensed voltage changed under load, replacing manual adjustment. The first implementation waited for each ADC conversion before updating the command. These conversion waits shared the foreground execution path with UART handling and other work, which could delay the next duty adjustment.

### control-07

> After load removal, limited discharge through the connector allows continued bursts to raise the bulk voltage. The no-load guard uses the primary-current indication at PA2 and configured reference conditions to select a narrower voltage band and lower high-duty cap. Average transfer is thereby limited while the minimum burst duration is retained to reduce partial carrier cycles. The defaults are \(V_{\mathrm{set}}=\SI{28}{\volt}\), \(V_{\mathrm{NLdrop}}=\SI{5}{\volt}\), and \(d_{\mathrm{NL}}=\SI{5}{\percent}\), giving approximately \SI{23}{\volt} to \SI{28}{\volt} at the secondary bulk. The USB-C output has its own voltage setting.

### control-09

> The setup information and repeated measurements needed for a numerical uncertainty budget are incomplete. Values are therefore kept at the workbook precision, and no error bars are given. Characterizing worst-case transients requires repeated events with a defined acceptance band; thermal equilibrium requires a temperature history, and jitter requires timing measurements. These limits apply throughout Chapter~\ref{ch:results}.

### results-v3

> The V3 edge-card layout retained secondary rectification and removed the USB-PD section, giving an estimated net volume reduction of approximately \SI{8}{\percent}. External regulation and USB-PD remain necessary for a complete USB-C supply. Replacement planar magnetics were not installed, and the smaller layout still needs to be built and tested.

### results-firmware-development

> The current-sense pin PA2 measures half-bridge current, so multiplying its current indication by secondary voltage was not a suitable output-power feedback signal. The product-based control was replaced by secondary-voltage regulation using PA1, while PA2 was retained for load classification and diagnostics. Optional feed-forward from the primary-voltage input PA0 can cap the burst-enable duty requested at PA10 as primary voltage rises.  Loaded and load-removal tests show the combined controller response. The individual changes were not tested at fixed settings, so their separate contributions remain unmeasured. For example, \texttt{MAXRATE} requests a \SI{20}{\micro\second} period; the achieved period and jitter require measured timing.

### results-failures

> The control changes addressed the problems found during bring-up. PA1 voltage regulation replaced the incorrect power feedback, with PA2 retained for load classification. Complete-cycle scheduling addressed irregular pulses, and no-load guarding limited charging after load removal. Measurement review separated waveform ripple from the spread of acquisition averages. The original readings give a maximum calculated output of \SI{79.89}{\watt}; further loading toward the \SI{100}{\watt} objective requires temperature histories alongside the electrical readings.  The remaining tests must pair input and output power, capture ripple with known coupling and bandwidth, follow identified temperatures to stabilization, and record controller state during load and protection events.

### results-lessons-hotspot

> The V2 input hotspot persisted after diode replacement, so the current and thermal paths around the bridge need further investigation. One possible restriction is a single-via connection between layers: narrow pad connections and interlayer paths can restrict current and heat flow despite a large copper pour.  Secondary-winding heating motivated transformer optimization, but a replacement set was not installed. The V3 layout reduced volume by removing the USB-PD section, so a complete-system power-density comparison must also include the equivalent external output functions.

### results-summary-v2-target

> V2 integrated the MCU, GaN stage, isolated sensing, and USB-C PD circuit on a four-layer PCB, documented in \cref{sec:app-v2-oct27}. The external series inductor was removed after excessive heating, and the tank was changed to use transformer leakage with approximately \SI{1.66}{\nano\farad}. Half-bridge heating decreased after the tank and timing changes, while input-bridge heating persisted. The thermal image shows surface heating during a \SI{95}{\watt} run; a temperature history is still needed to assess continuous operation.  The revised plan retains \SI{100}{\watt} continuous as the target and \SI{65}{\watt} continuous as the minimum \cite{projectOctoberPlan}. Defined-duration tests with temperature histories are still needed at these levels and at the earlier \SI{75}{\watt} milestone. The reported approximately \SI{85}{\watt} V2 point should be repeated with the board, firmware, settings, power readings, and temperatures recorded together. This earlier V2 point is separate from the calculated \SI{79.89}{\watt} V1.0 result above.

## Technical checks

The optional PA0 feed-forward relationship was checked against the baseline source at `Code/thesi_power_control_PWR_1_9_20.ino`: the bounded reference/primary-voltage scale is calculated near line 2444 and applied in the relevant control branches near line 2704. Carrier-boundary polling can time out near lines 1131–1161; the rewrite therefore describes minimum burst duration as reducing partial cycles, not guaranteeing measured full cycles.

The [voice checklist](/workspace/tooling/thesis-agent-voice-checklist.md), [assignment](/workspace/tooling/thesis-terra-rewrite/AGENT_TASK.md), complete inventories and original agent proposals are retained. The final checks are recorded below.

## Final verification

The 30 approved rewrites affect 28 source files. The other 513 files are byte-for-byte unchanged from the previous source archive. Quantities, SI ranges, inline and displayed equations, existing labels and references are preserved. One explicit reference to the existing magnetic-check table was added. Firmware, measurements, pictures, schematics and layout settings are unchanged.

The full thesis compiles to 490 pages with all 12 chapters, references and appendices A–J, four current V2 schematic sheets and 31 PCB sheets. There are no undefined references/citations, missing glyphs, overfull boxes or text outside a page. Existing warnings remain: 81 underfull horizontal boxes and math-font size substitutions. The USB-C power-path, modelling, no-load control and conclusion pages were inspected visually.

The final prose review raised two precise wording issues; both were corrected before the final build. PA2 now refers to its current indication, and the 79.89 W result is explicitly calculated. The original source archives and selected GitHub checkout pass integrity checks.

Commands: `bash /workspace/tooling/build-thesis.sh`; `python3 check-pdf.py`, `python3 audit.py`, `python3 package.py` in this review directory; `python3 /workspace/tooling/verify-sources.py`. Exact changes, quantities, build output and PDF checks are retained alongside this report.

The source ZIP contains 541 current files; ZIP CRC and member hashes pass. The existing [GitHub review release](https://github.com/kform-danish-office/Thesis/releases/tag/thesis-v1-v2-v3-review) was refreshed, and all three remote asset digests and sizes match local files.
