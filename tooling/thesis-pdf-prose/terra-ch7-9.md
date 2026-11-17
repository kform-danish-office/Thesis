# Chapters 7–9 prose review

Reviewed files:

- `Chapters/07_Hardware/01_Prototype_Overview.tex`
- `Chapters/07_Hardware/02_Input_Filter_Bridge.tex`
- `Chapters/07_Hardware/03_Charge_Pump_Network.tex`
- `Chapters/07_Hardware/04_GaN_Half_Bridge.tex`
- `Chapters/07_Hardware/05_Gate_Drive.tex`
- `Chapters/07_Hardware/06_Resonant_Output.tex`
- `Chapters/07_Hardware/07_USBC_Interface.tex`
- `Chapters/07_Hardware/08_Sensing.tex`
- `Chapters/07_Hardware/09_Protection.tex`
- `Chapters/07_Hardware/10_Auxiliary_Power.tex`
- `Chapters/07_Hardware/11_PCB_Layout.tex`
- `Chapters/07_Hardware/12_EMI.tex`
- `Chapters/07_Hardware/13_Thermal.tex`
- `Chapters/07_Hardware/14_BOM_Manufacturing.tex`
- `Chapters/07_Hardware/15_Unmanufactured_Revisions.tex`
- `Chapters/07_Hardware/16_V2_F410.tex`
- `Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex`
- `Chapters/07_Hardware/chapter.tex`
- `Chapters/08_Control_Firmware/01_Control_Objectives.tex`
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
- `Chapters/09_Experimental_Methods/01_Objectives.tex`
- `Chapters/09_Experimental_Methods/02_Safety_Arrangements.tex`
- `Chapters/09_Experimental_Methods/03_Test_Bench.tex`
- `Chapters/09_Experimental_Methods/04_Instrumentation.tex`
- `Chapters/09_Experimental_Methods/05_Probing.tex`
- `Chapters/09_Experimental_Methods/06_Test_Matrix.tex`
- `Chapters/09_Experimental_Methods/07_Control_Tests.tex`
- `Chapters/09_Experimental_Methods/08_Power_Quality.tex`
- `Chapters/09_Experimental_Methods/09_Efficiency.tex`
- `Chapters/09_Experimental_Methods/10_Thermal.tex`
- `Chapters/09_Experimental_Methods/11_Uncertainty.tex`
- `Chapters/09_Experimental_Methods/12_Revised_Plan_Validation.tex`
- `Chapters/09_Experimental_Methods/chapter.tex`

Deliberate keeps: circuit descriptions, component ratings, schematic captions and pin assignments; firmware stage and version comparison, flash journal and browser protocol details; test configuration, probing, power calculations and local thermal limitations. These explain engineering operation or reproduce the test. LaTeX paths, labels, citations and equations remain untouched.

Uncertainty for lead review: the timing proposal removes a conflicting note about baseline revision; preserve any run-specific attribution where needed in the results or source history. The V2 baseline proposal retains configuration identification without listing export commands. No changes to technical data are proposed.

Second pass: all 47 assigned files were read in full, including the portions omitted from the initial truncated tool output. The source appendix reference in the chapter introduction is deliberately retained; later repeated navigation is reduced. The checksummed flash journal is technical behavior and is retained. V2 timing, fitted-part uncertainty, divider calibration and the reported 85 W operating point remain qualified.

## Section-by-section editorial judgement

### 07_Hardware

- 01 Prototype: board identity, changes and insulation check are clear; retain revision table and photo.
- 02 Input: combine repeated attenuation requirement; retain parts, filter revisions and V2 caption.
- 03 Pump: retain branch function, fitted values, ratings and local stress measurements.
- 04 Half bridge: retain data-sheet conditions, ratings table and need to measure commutation.
- 05 Gate drive: retain board-specific pins and unverified ZVS condition.
- 06 Resonant path: connect waveform comparison to fitted branch; retain calculated resonance and inductor photographs.
- 07 USB-C: retain stage role, tested voltages and qualification of 100 W.
- 08 Sensing: connect scale check to physical causes; retain pin map and distinction between primary current and connector power.
- 09 Protection: retain hardware/firmware layers and specific fault limitations.
- 10 Auxiliary: remove repeated sensing-power explanation; retain startup sequence.
- 11 Layout: retain loop, return and insulation rationale and captions.
- 12 EMI: retain coupling mechanisms and measurement gap.
- 13 Thermal: retain heat paths and temperature-history requirement.
- 14 Components: retain fitted parts and bring-up corrections tables.
- 15 Revisions: retain unmanufactured status and applicability of V1 results.
- 16 V2: remove repeated navigation and 85 W repetition; retain actual timing, divider mismatch and fitted-component uncertainty.
- 17 V3: retain removal of PD, estimated volume reduction, uninstalled magnetics and required checks.
- Chapter introduction: retain chapter structure and labels.

### 08_Control_Firmware

- 01 Objectives: retain regulated node and board-specific signals.
- 02 Timing: retain architecture, synchronization limitations, diagram and resource table.
- 03 Calibration: link recorded settings to response; retain equations, reference values and calibration table.
- 04 Open loop: retain motivation and its no-load limitation.
- 05 Blocking control: retain conversion-wait rationale.
- 06 Blocking limitations: retain DMA explanation of the actual change.
- 07 DMA: retain feedback correction and functional benefits.
- 08 Control law: retain hysteresis, thresholds, load classification and code summary.
- 09 Duty limits: retain minimum-pulse rationale and antiwindup distinction.
- 10 No-load: retain hysteresis, recovery and required peak measurement.
- 11 States: retain precharge, fault logic, state diagram and attempt-limit behavior.
- 12 Faults: retain actual detection and limitations, OVP thresholds and recovery.
- 13 Timing: make test settings and version the focus; retain external jitter measurement.
- 14 Development: retain staged comparison and functional benefits.
- 15 V2 port: reduce repeated source inventory; retain timer, journal checksum, calibration, protocol, software tests and unpowered validation status.
- Chapter introduction: retain source appendix and concise firmware history table.

### 09_Experimental_Methods

- 01 Objectives: retain test purposes, configuration and measurement table.
- 02 Safety: retain electrical setup and shutdown specifics.
- 03 Bench: retain instrument identities, calibration qualification and measurement boundary.
- 04 Instrumentation: retain channels, scaling and instrument role tables.
- 05 Probing: retain bandwidth constraint and ZVS measurement conditions.
- 06 Matrix: remove data inventory; retain test program and interpretation limits.
- 07 Control tests: retain actual loaded and load-removal observations and missing startup measurements.
- 08 Power quality: retain PF/THD definitions and integration conditions.
- 09 Efficiency: retain boundaries, V2 load terminals and averaging limitations.
- 10 Thermal: retain R1/R3 locations, emissivity and limited setup information.
- 11 Uncertainty: remove workbook processing detail; retain lack of error bars and measurement requirements.
- 12 Remaining tests: connect V2 baseline conditions and retain target, firmware version, uncertainty and density boundary.
- Chapter introduction: retain test purpose and measurement distinctions.

