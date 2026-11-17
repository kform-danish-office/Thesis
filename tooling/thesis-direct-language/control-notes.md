# Direct language pass: modeling, magnetics, hardware and control

Reviewed all prose, headings, captions, listing captions and table text in Chapters 5–8. The latest user instruction explicitly included these areas; this pass therefore changed the caption and table wording that earlier prose-only passes preserved.

The edits keep concise power-electronics prose, the user's practical factual voice, and the actual design/test limits. They do not add elementary explanations or turn missing measurements into validated results.

## Main changes

- Captions and table headings name their subject directly: “Hardware used for the prototype tests”, “MCU feedback pins and their functions”, and “Firmware versions included with this thesis”.
- Tables use “Check / Result”, “MCU pin / Input / Firmware function”, and “Firmware / Version / Use” instead of audit-style headings about evidence, interpretation or identity.
- MCU input, carrier and enable connections are called pins where appropriate. All pin assignments remain unchanged. The V2 comparison still includes actual package pin numbers where needed.
- Boilerplate about how excerpts were cropped or how records should be interpreted was removed from captions. Caption scope still matches the circuit shown. Diagram paths and assets were not edited by this task.
- Magnetic integration is described through mounting, winding terminals, parasitics and measurements rather than “integration evidence” or a “component reference range”. Inherited design/measurement attribution remains.
- Model limitations now state what was simulated, calculated or still needs measurement directly. Efficiency remains preliminary, with synchronization, calibration and auxiliary-power uncertainty intact.
- Firmware descriptions retain bounded alignment attempts, precharge attempt limits, acquisition-running-flag limits, optional/disabled current protection, and diagnostic rather than measured USB-C output power.
- The Chapter 8 title is now “Firmware Development and Versions”, replacing “Development Stages and Software Identification”. Its stable internal label remains unchanged. Exact software IDs are still introduced in this section and retained in the history/test records.

## Examples

Before: “Hardware identity used to interpret the thesis measurements.”

After: “Hardware used for the prototype tests.”

Before: “Meaning of the three firmware acquisition channels.”

After: “MCU feedback pins and their functions.”

Before: “Evidence available for the magnetic integration.” / “Question / Evidence and interpretation”

After: “Measurements and checks for the installed magnetics.” / “Check / Result”

Before: “Changes and interpretation corrections established during bring-up.”

After: “Circuit and feedback corrections made during bring-up.”

Before: “The component values follow this drawing” was already removed by the preceding V2 figure pass. This pass retains that distinction: the displayed V2 drawings do not silently replace fitted V1 component values or measured test configurations.

## Preservation

There are 190 local edit records across 52 TeX files. All checks in `control-validation.json` pass: SI expressions, math occurrences, numerical tokens (with the redundant hardware-version reminder exception below), MCU pin occurrences, labels, citations, references, source/graphic paths, complete equation/TikZ/verbatim environments, listing code bodies, original newline styles and final-newline status. Qualitative caption/table words are authorized changes; numerical/data cells are unchanged.

The archived 40 ns V2 setting and later reported 60 ns bench setting remain distinct, with the bench-run firmware version unrecorded. V1 matched data, V2 preliminary observations, secondary-current observations, the reduced-function V3 estimate, and future power targets retain their qualifications. All mathematical and source data remain unchanged.

Only Chapters 5–8 were edited. No figures/assets, code, hardware settings, manifests, build outputs, GitHub or environment publication operations were changed by this task. The parent owns the colour schematic replacement and full compilation.

## Final chapter-opening check

The user also singled out the Chapter 5 opening. It now states the technical work directly: “Charge transfer, resonant gain and phase, and component sensitivity are examined using the circuit equations and supplied LTspice models.” The first section is “Charge-Transfer and Resonant Models”. Relevant model differences and missing measurements remain in their technical sections instead of being repeated as a defensive chapter opening.

Redundant chapter-organizing closers were removed from Chapters 5–7. The Chapter 8 source pointer now names the baseline and V2 sources directly while preserving its appendix reference. A review finding in the Chapter 8 introduction was corrected: “main final test series” no longer implies that every recorded final-run software version was the baseline.

## Section 8.5: why the controller improved

The latest user request asked for each stage's functional benefit. Section 8.5 and its four input files now explain the problem, implementation change and resulting capability:

- Manual carrier/burst commands enabled timing and basic-transfer bring-up before automatic voltage control.
- Voltage feedback let the controller correct sensed-voltage changes rather than depend on manual burst settings.
- Blocking conversions delayed opportunities for foreground command handling and duty updates.
- Circular DMA removed conversion waits while acquisition, commands and control continued.
- Correcting the PA2 interpretation moved active regulation away from a diagnostic voltage--primary-current product and onto secondary bulk voltage.
- Startup precharge, no-load limits/soft holdoff and loaded duty trim controlled requested energy as operating conditions changed. Carrier alignment remains an attempt, not a guarantee.

The table now uses “Stage / Change / Improvement”. Repeated statements about unmatched tests and failure to isolate DMA-only gains were removed here because the section does not claim numerical jitter, stability, efficiency or ZVS improvements. The repeated Chapter 8 closing summary/disclaimer was also removed.

All mathematical expressions, SI values, software IDs, pin assignments, labels, references, and source inclusions remain. The only numerical-token exception is removal of the repeated “V1, V2, and V3” hardware-naming reminder from Section 8.5; those names are already introduced in Section 8.1. This is recorded explicitly in `control-validation.json`. No numerical data were changed.

The focused rationale is recorded in `stage-rationale-edits.json`. Final read-only review found no issues; see `stage-rationale-review.md`.

## Changed files

- `Chapters/05_Modeling_Simulation/01_Objectives.tex`
- `Chapters/05_Modeling_Simulation/02_Uploaded_LTspice_Files.tex`
- `Chapters/05_Modeling_Simulation/03_GaN_Model.tex`
- `Chapters/05_Modeling_Simulation/04_Simulation_Setup.tex`
- `Chapters/05_Modeling_Simulation/05_Simulation_Cases.tex`
- `Chapters/05_Modeling_Simulation/06_Steady_State.tex`
- `Chapters/05_Modeling_Simulation/07_Startup_NoLoad.tex`
- `Chapters/05_Modeling_Simulation/08_Parameter_Sweeps.tex`
- `Chapters/05_Modeling_Simulation/09_Loss_Estimation.tex`
- `Chapters/05_Modeling_Simulation/10_Data_Limitations.tex`
- `Chapters/05_Modeling_Simulation/chapter.tex`
- `Chapters/06_Magnetics_Integration/01_Provenance.tex`
- `Chapters/06_Magnetics_Integration/02_Inherited_Specifications.tex`
- `Chapters/06_Magnetics_Integration/03_Integration_Requirements.tex`
- `Chapters/06_Magnetics_Integration/04_Mounting_Concept.tex`
- `Chapters/06_Magnetics_Integration/05_Footprint_Interconnection.tex`
- `Chapters/06_Magnetics_Integration/06_Mechanical_Assembly.tex`
- `Chapters/06_Magnetics_Integration/07_Isolation_Clearance.tex`
- `Chapters/06_Magnetics_Integration/08_Parasitics.tex`
- `Chapters/06_Magnetics_Integration/09_Thermal_Integration.tex`
- `Chapters/06_Magnetics_Integration/10_Verification.tex`
- `Chapters/06_Magnetics_Integration/11_Limitations.tex`
- `Chapters/06_Magnetics_Integration/chapter.tex`
- `Chapters/07_Hardware/01_Prototype_Overview.tex`
- `Chapters/07_Hardware/04_GaN_Half_Bridge.tex`
- `Chapters/07_Hardware/05_Gate_Drive.tex`
- `Chapters/07_Hardware/06_Resonant_Output.tex`
- `Chapters/07_Hardware/07_USBC_Interface.tex`
- `Chapters/07_Hardware/08_Sensing.tex`
- `Chapters/07_Hardware/09_Protection.tex`
- `Chapters/07_Hardware/11_PCB_Layout.tex`
- `Chapters/07_Hardware/13_Thermal.tex`
- `Chapters/07_Hardware/14_BOM_Manufacturing.tex`
- `Chapters/07_Hardware/15_Unmanufactured_Revisions.tex`
- `Chapters/07_Hardware/16_V2_F410.tex`
- `Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex`
- `Chapters/07_Hardware/chapter.tex`
- `Chapters/08_Control_Firmware/02_Architecture_Timing.tex`
- `Chapters/08_Control_Firmware/03_Feedback_Calibration.tex`
- `Chapters/08_Control_Firmware/04_V0_Open_Loop.tex`
- `Chapters/08_Control_Firmware/05_V1_Blocking_Closed_Loop.tex`
- `Chapters/08_Control_Firmware/06_Blocking_Limitations.tex`
- `Chapters/08_Control_Firmware/07_V2_DMA.tex`
- `Chapters/08_Control_Firmware/08_Control_Law.tex`
- `Chapters/08_Control_Firmware/09_Limits_Antiwindup.tex`
- `Chapters/08_Control_Firmware/10_Open_Circuit_Safety.tex`
- `Chapters/08_Control_Firmware/11_State_Machine.tex`
- `Chapters/08_Control_Firmware/12_Fault_Handling.tex`
- `Chapters/08_Control_Firmware/13_Timing_Resources.tex`
- `Chapters/08_Control_Firmware/14_Version_Comparison.tex`
- `Chapters/08_Control_Firmware/15_PWR_2_Port.tex`
- `Chapters/08_Control_Firmware/chapter.tex`

Both independent reviews have no unresolved findings. All source edits are frozen.
