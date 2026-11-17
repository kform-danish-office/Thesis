from pathlib import Path
import json

root=Path('/workspace/thesis/Chapters')
changes=[]
pending={}

def edit(rel, rows):
    p=root/rel
    data=pending.get(p,p.read_bytes())
    eol='\r\n' if b'\r\n' in data else '\n'
    for old,new in rows:
        a=old.replace('\n',eol).encode()
        b=new.replace('\n',eol).encode()
        assert data.count(a)==1,(rel,old)
        data=data.replace(a,b)
        changes.append({'path':'Chapters/'+rel,'before':old,'after':new})
    pending[p]=data

edit('05_Modeling_Simulation/01_Objectives.tex',[
('Each inherited model is used within this scope.','The calculations below use the inherited models for these purposes.'),
('For the USB-C circuit and voltage-control firmware, the comparison framework considers bus ripple, turn-on current, packet energy, and the response to component or command changes. Matched turn-on-current and packet-energy measurements remain required.','A prototype model must predict bus ripple, turn-on current, packet energy, and the response to component or command changes. Matched turn-on-current and packet-energy measurements are still needed to check it.')])
edit('05_Modeling_Simulation/02_Uploaded_LTspice_Files.tex',[
('Parameters visible in the inherited LTspice schematics compared with the prototype analysis values.','Inherited simulation parameters and prototype calculation values.'),
('Test condition stated per record','Input conditions listed with each test'),
('Downstream interface and variable load','USB-C PD stage and variable load'),
('Prototype efficiency is estimated from measured input and output power, subject to the measurement-boundary and timing limitations stated in the results.','Prototype efficiency is estimated from measured input and output power. The measurement locations and timing uncertainties are described with the results.')])
edit('05_Modeling_Simulation/03_GaN_Model.tex',[
("A fitted-stage switching model requires voltage-dependent output charge, gate/enable timing, reverse conduction, and interconnect impedance.","A switching model of the assembled stage requires voltage-dependent output charge, gate/enable timing, reverse conduction, and interconnect impedance.")])
edit('05_Modeling_Simulation/04_Simulation_Setup.tex',[
('The retained logs and RAW files are inherited results; a matching final-board model was not rerun.','The saved logs and RAW files are results from the inherited circuits. No simulation of the final board was completed.'),
('Time-step convergence and energy balance must be established before comparison with measured waveforms.','Time-step convergence and energy balance must be checked before comparison with measured waveforms.')])
edit('05_Modeling_Simulation/05_Simulation_Cases.tex',[
('Established-burst operation at a known load provides the initial calibration point, followed by line-cycle buffering, load transients, and high-impedance operation. This final-hardware simulation remains unfinished; the following calculations provide analytical expectations for measurement.','Model calibration should start with steady bursts at a known load, followed by line-cycle buffering, load transients, and high-impedance operation. The prototype simulation remains unfinished; the following calculations predict trends to check in testing.')])
edit('05_Modeling_Simulation/06_Steady_State.tex',[
('Resolving one scale does not establish behavior at the others.','The model must resolve all three time scales.')])
edit('05_Modeling_Simulation/07_Startup_NoLoad.tex',[
('Their margins require a switched model with the measured circuit and timing.','Checking the resulting peak voltage requires a switched model with the measured circuit and timing.')])
edit('05_Modeling_Simulation/08_Parameter_Sweeps.tex',[
('These calculated sensitivities are illustrative, rather than measured or simulated results.','These are first-order calculations, not measured or simulated results.'),
('First-order sensitivities and their interpretation.','Calculated effects of changing circuit values and burst density.'),
('More startup energy and a different transient trajectory','More startup energy and a different transient response'),
('frequency and dead-time experiments require a separately identified configuration.','frequency and dead-time experiments require their own recorded configuration.')])
edit('05_Modeling_Simulation/09_Loss_Estimation.tex',[
('Burst-dependent active loss and persistent auxiliary/idle consumption require stated power boundaries and burst state.','Active-cycle loss depends on burst operation, while auxiliary and idle circuits continue to draw power. Loss calculations must state which supplies are included and the burst operating state.'),
('Paired input/output readings at the Chapter~\\ref{ch:results} boundaries provide preliminary efficiency estimates and an input--output power difference, subject to synchronization, calibration, and auxiliary-power uncertainty.','Paired input/output readings in Chapter~\\ref{ch:results} provide preliminary efficiency estimates and an input--output power difference. Their accuracy is limited by synchronization, calibration, and uncertainty about included auxiliary power.'),
('Thermal images locate investigation areas; surface temperature alone does not quantify component loss.','Thermal images show where heating occurs; surface temperature alone does not quantify component loss.'),
('Diagnosis must distinguish dissipation from the mechanism preventing further load increase.','Finding the output limit requires more than a loss calculation.'),
('Temperature and controller-state observations identify follow-up measurements but do not individually establish the limiting mechanism.','Hotspots and controller states help choose the next measurements, but neither identifies the limiting mechanism on its own.')])
edit('05_Modeling_Simulation/10_Data_Limitations.tex',[
('DC-link ripple, magnetizing current, burst timing, and residual tank energy provide a framework for interpreting bench behavior.','DC-link ripple, magnetizing current, burst timing, and residual tank energy help explain the bench results.'),
('Laboratory tests establish progress toward the power and thermal targets.','Laboratory tests show how closely the converter approaches the power and thermal targets.')])
edit('05_Modeling_Simulation/chapter.tex',[
('Complete-system performance is therefore established by laboratory measurements rather than a calibrated final-board model.','The assembled supply is therefore evaluated through laboratory measurements; a calibrated final-board model is not available.')])

edit('06_Magnetics_Integration/01_Provenance.tex',[
('The component measurements are attributed to M\\\'ani Gautason.','The components were measured by M\\\'ani Gautason.'),
('The supplied cores and windings were retained; this thesis covers electrical connection, mechanical integration, and converter analysis using the supplied values. The table distinguishes these contributions.','The supplied cores and windings were used for the electrical connection, mechanical integration, and converter analysis in this thesis.'),
('Attribution of the magnetic-component work.','Supplied magnetic designs and the integration work in this thesis.'),
('Use of the supplied values in analysis and interpretation of prototype tests','Use of the supplied values in calculations and prototype testing')])
edit('06_Magnetics_Integration/02_Inherited_Specifications.tex',[
('Standalone planar-magnetics measurements supplied by M\\\'ani Gautason.','Planar-magnetics measurements by M\\\'ani Gautason.'),
('The installed A/B combination is unidentified, so calculations use the supplied range or a stated nominal value with the \\cref{eq:app-turns-ratio} convention.','The fitted A/B combination was not recorded, so calculations use the supplied range or a stated nominal value with the \\cref{eq:app-turns-ratio} convention.')])
edit('06_Magnetics_Integration/03_Integration_Requirements.tex',[
('Isolation assessment therefore covers the complete assembly.','The complete assembly must therefore be checked for insulation spacing.'),
('Requirements governing the installed magnetic interfaces.','Electrical and mechanical requirements for mounting the magnetics.'),
('Engineering requirement','Requirement'),
('A component-specific terminal drawing is still required for reproducible assembly.','A terminal drawing for each component is still needed to reproduce the assembly.')])
edit('06_Magnetics_Integration/04_Mounting_Concept.tex',[
('The photographed arrangement requires a defined fastening procedure and post-mounting air-gap check to establish repeatability.','A repeatable assembly requires a fastening procedure and an air-gap check after mounting.')])
edit('06_Magnetics_Integration/05_Footprint_Interconnection.tex',[
('Reproduction requires terminal and polarity verification in addition to the gain estimate from turns ratio.','The terminals and winding polarity must be checked before the assembly can be reproduced; turns ratio alone is insufficient.')])
edit('06_Magnetics_Integration/06_Mechanical_Assembly.tex',[
('Values in \\cref{tab:mag-inherited-measurements} were retained because inductance was not remeasured after installation and no detailed rework log was kept.','Calculations use the values in \\cref{tab:mag-inherited-measurements} because inductance was not remeasured after installation and no detailed rework log was kept.')])
edit('06_Magnetics_Integration/07_Isolation_Clearance.tex',[
('Winding-board spacing alone does not establish the complete isolation path.','Checking winding-board spacing alone is insufficient.'),
('Full insulation assessment additionally requires documented transformer spacing, material group, and standardized dielectric testing.','A full insulation check also requires the transformer spacing, material group, and standardized dielectric tests.')])
edit('06_Magnetics_Integration/08_Parasitics.tex',[
('Parasitic effects associated with the installed magnetics.','Parasitic effects in the installed magnetics.'),
('Numerical attribution requires installed-assembly impedance and capacitance measurements.','Quantifying these effects requires impedance and capacitance measurements on the assembled converter.')])
edit('06_Magnetics_Integration/09_Thermal_Integration.tex',[
('Inductance and turns ratio do not establish an installed thermal limit.','The thermal limit cannot be predicted from inductance and turns ratio alone.'),
('A continuous rating requires a timed thermal record on the identified assembly.','Continuous output must be checked by recording temperature over time on the tested assembly.')])
edit('06_Magnetics_Integration/10_Verification.tex',[
('The table below lists the measurements needed to resolve the remaining questions.','The remaining measurements are listed below.'),
('Evidence available for the magnetic integration.','Measurements and checks for the installed magnetics.'),
('Question & Evidence and interpretation','Check & Result'),
('Standalone electrical values & Supplied A/B measurements establish the component reference range.','Component measurements & Supplied A/B measurements give the starting electrical values.'),
('Installed identity and terminals & The final A/B assignment and part-specific terminal/polarity map were not retained.','Fitted variants and terminals & The fitted A/B combination and its terminal/polarity map are not documented.'),
('Installed parameters & No post-assembly inductance, ratio, or interwinding-capacitance extraction is available.','Installed parameters & No post-assembly measurements of inductance, turns ratio, or interwinding capacitance are available.'),
('Mechanical and isolation margin & Overall hardware documentation is available; detailed retention, spacing, and magnetic dielectric-test records are incomplete.','Mounting and insulation & Fastening details, magnetic spacing, and dielectric-test results are not fully documented.'),
('Operating temperature & Board thermal images are available, with limited component-specific and steady-state metadata.','Operating temperature & Board thermal images show surface heating; component temperatures and thermal settling times are not fully documented.'),
('System operation & The test results demonstrate power transfer through the installed assembly at the reported operating points.','Power transfer & Converter tests show power transfer through the installed magnetics at the reported loads.')])
edit('06_Magnetics_Integration/11_Limitations.tex',[
('These measurements support reproducible assembly and loss-driven revision.','These measurements are needed to reproduce the assembly and reduce its losses.'),
('The smaller V3 layout therefore establishes neither reduced magnetic loss nor increased continuous output.','No reduction in magnetic loss or increase in continuous output was demonstrated with the smaller V3 layout.')])

edit('07_Hardware/01_Prototype_Overview.tex',[
('The voltage-control firmware used for the identified final tests is described in Chapter~\\ref{ch:control}.','The voltage-control firmware used for the final tests is described in Chapter~\\ref{ch:control}.'),
('Hardware identity used to interpret the thesis measurements.','Hardware used for the prototype tests.'),
('Record & Physical status & Role in this thesis','Hardware & Build status & Use'),
('Anchor for prototype photographs, layout, and measurements','Board shown in the photographs, layout, and measurements'),
('Final fitted state','Final resonant branch'),
('Configuration used for the final results','Used for the final tests'),
('Documentation revision; no separate measured board','Drawing revision; no separate test board'),
('Bring-up correction record and revision comparison','Documents the bring-up corrections'),
('The earlier matched measurements remain associated with the modified V1.0 board.','The earlier matched measurements were taken on the modified V1.0 board.'),
('Assembled V1.0 laboratory prototype in the final fitted test configuration.','Assembled V1.0 prototype used for the final tests.')])
edit('07_Hardware/04_GaN_Half_Bridge.tex',[
('LMG2652 data-sheet quantities relevant to the prototype \\cite{tiLMG2652}. Values apply at the specified data-sheet conditions.','LMG2652 ratings and characteristics \\cite{tiLMG2652}, under the data-sheet test conditions.'),
('Quantity & Value & Engineering implication','Parameter & Value & Design consideration'),
('Current and temperature must be assessed together.','Check current and temperature together.'),
('Capacitive commutation contributes to the ZVS requirement.','The tank must supply the charge needed for commutation.'),
('Device limiting is distinct from PA2 firmware thresholds.','This device limit is separate from PA2 firmware thresholds.'),
('Package metrics require the corresponding thermal boundary conditions.','These values depend on the specified mounting and cooling conditions.'),
('These delays must be included when interpreting the switch node. The transistor dead time cannot be established from the timer registers alone.','These delays affect the switch-node timing. Actual transistor dead time must be measured; timer settings alone are insufficient.'),
("Soft turn-on must be assessed from the incoming switch's voltage/current relationship at the stated input and load, using the probing method in \\cref{sec:method-probing}.","Soft turn-on must be checked from the incoming switch's voltage and current at the stated input and load, using the probing method in \\cref{sec:method-probing}.")])
edit('07_Hardware/05_Gate_Drive.tex',[
('carrier at PA8/PA9.','carrier on MCU pins PA8/PA9.'),
('matched gate-timing and commutation-current captures are required to establish effective dead time and ZVS','matched gate-timing and commutation-current captures are needed to measure effective dead time and check ZVS')])
edit('07_Hardware/06_Resonant_Output.tex',[
('Resonant-inductor arrangements examined during prototype bring-up.','Resonant-inductor arrangements tested during bring-up.'),
('The actual inductor arrangement is therefore stated for each waveform comparison. The installed path must be measured before a model is used to select another change.','Waveform comparisons therefore need the fitted inductor arrangement. The installed path must be measured before the model is used to select another change.')])
edit('07_Hardware/07_USBC_Interface.tex',[
('Page borders and the title block are omitted to improve legibility.',''),
('USB-PD negotiation and interoperability still need separate protocol tests before broader compliance can be claimed.','USB-PD negotiation and interoperability still need protocol testing.')])
edit('07_Hardware/08_Sensing.tex',[
('Analog Feedback and Measurement Nodes','Analog Feedback and MCU Inputs'),
('V2 retains these measurement functions with direct ADC connections','V2 uses the same measurements with direct ADC connections'),
('V2 sheet 4 MCU and signal interface. Feedback enters PA0--PA2 directly; PA8/PB13 provide carrier commands and PA11 provides burst enable. The controller is referenced to the primary-side domain.','V2 sheet 4 MCU connections. Feedback enters pins PA0--PA2 directly; PA8/PB13 provide carrier commands and PA11 provides burst enable. The MCU uses the primary-side ground reference.'),
('Meaning of the three firmware acquisition channels.','MCU feedback pins and their functions.'),
('Channel & Physical signal & Use in the baseline firmware','MCU pin & Input & Firmware function'),
('Primary-voltage indication','Primary-voltage feedback'),
('Active voltage regulation and overvoltage decisions','Voltage regulation and overvoltage protection'),
('Half-bridge-current-related signal','Half-bridge current sensing'),
('Loaded/no-load classification, diagnostics, and enabled current protection','Load detection, diagnostics, and optional current protection'),
('The settings used to identify a test configuration are given in \\Cref{sec:ctrl-feedback}.','The calibration settings are given in \\Cref{sec:ctrl-feedback}.')])
edit('07_Hardware/09_Protection.tex',[
('Redundancy and single-fault response would also need to be assessed for a product-safety claim.','Product qualification would also require checks of redundancy and single-fault response.')])
edit('07_Hardware/11_PCB_Layout.tex',[
('The reference drawing locates the AC input, high-frequency power stage, magnetic interface, and output/control circuits.','The AC input, high-frequency power stage, magnetics, and output/control circuits are marked.'),
('Annotated views of the manufactured V1.0 layout. The board geometry provides the baseline for interpreting the final assembly and its rework.','V1.0 top and bottom copper, showing component regions and return paths.'),
('a signal name on the drawing must match a working timer output on the selected MCU.','the MCU pin on the drawing must support the required timer output.')])
edit('07_Hardware/13_Thermal.tex',[
('An enclosure or dedicated heat sink would change these paths and would need a separate assessment before a thermal rating could be assigned.','An enclosure or dedicated heat sink would change these paths, so continuous output would need to be retested.'),
('Thermal images are compared by their labeled loads and visible surfaces.','Thermal images are compared at the labeled loads and measured surfaces.'),
('Component temperatures still need to be recorded over time to assess sustained operation.','Component temperatures still need to be recorded over time to check sustained operation.')])
edit('07_Hardware/14_BOM_Manufacturing.tex',[
('The tested assembly is described by the component list in \\Cref{tab:hw-bom-provenance}, board photographs, and schematic changes. The fitted parts are identified in the list, while the photographs show changes to the resonant branch that are not captured by the revision name alone.','The fitted components are listed in \\Cref{tab:hw-bom-provenance}. The board photographs show the resonant-branch changes made during bring-up.'),
('Principal components identified in the fitted hardware record.','Main components fitted to the prototype.'),
('Recorded value or role','Value or function'),
('windings in V1.0 record','windings on V1.0'),
('in fitted record','fitted to the prototype'),
('Connector-side power conversion and USB-C interface','USB-C PD voltage regulation and interface'),
('V1.0 top-side assembly reference from the PCB export.','V1.0 top-side assembly drawing.'),
('Changes and interpretation corrections established during bring-up.','Circuit and feedback corrections made during bring-up.'),
('Resulting implementation or interpretation','Correction'),
('V1.1 records the corrected assignment.','The corrected pins are shown in V1.1.'),
('V1.1 corrects the recorded diode connection and also includes component substitutions.','V1.1 shows the corrected diode connection and component substitutions.'),
('Half-bridge-current indication is used for load classification rather than treated as connector output current.','The half-bridge-current signal is used for load detection; it is not the USB-C output current.'),
('Fitted components, calibration, and runtime settings define this configuration more precisely than the PCB revision alone.','The fitted components, calibration, and runtime settings must be reproduced along with the PCB revision.')])
edit('07_Hardware/15_Unmanufactured_Revisions.tex',[
('Status of the later design revisions.','Later circuit and layout revisions.'),
('Documentation corrections and component changes; no separate manufactured test board','Drawing corrections and component changes; no separate test board was built'),
('Compact layout continuation; not built or experimentally assessed','More compact layout; not built or tested')])
edit('07_Hardware/16_V2_F410.tex',[
('The common source supports both MCU targets; test results must identify the target, fitted assembly, and software configuration.','The common source supports both MCUs. Each test needs the MCU, fitted parts, and firmware settings recorded together.'),
('Both layers are shown in the same projection. These layout views describe the board design; fitted changes made during testing are described separately.','Both layers use the same view. Changes made during testing are described in the text.'),
('\\Cref{tab:hw-v2-pinmap} gives the assignments from MCU sheet 4 and the corresponding package pins.','\\Cref{tab:hw-v2-pinmap} lists the MCU pins from sheet 4 and their package pin numbers.'),
('Controller connections for the G071 test platform and V2 F410 drawing. Package pin numbers in the last column refer to the F410CBU6.','MCU pins on the G071 controller and V2 F410. Package pin numbers in the V2 column apply to the F410CBU6.'),
('G071 assignment & V2 F410 assignment','G071 pins & V2 F410 pins'),
('The fitted parts must be confirmed on the assembled V2 before test results are interpreted.','The parts fitted to the assembled V2 still need to be checked against the drawing.'),
('The final V1.0 arrangement with two \\SI{4.7}{\\micro\\henry} series inductors does not establish the missing V2 values.','The final V1.0 arrangement used two \\SI{4.7}{\\micro\\henry} series inductors; this does not give the missing V2 values.'),
('The installed branch and transformer must be identified before calculating resonance or comparing switching waveforms.','The fitted branch and transformer must be checked before calculating resonance or comparing switching waveforms.'),
('Displayed control and voltage-protection thresholds cannot be interpreted reliably until the firmware conversion scales match the measured circuit.','Displayed voltages and voltage-protection thresholds are reliable only when the firmware conversion scales match the measured circuit.'),
('The assembled power path and USB-PD behavior still need dedicated checks beyond the preliminary powered observations in \\cref{sec:res-v2-testing}.','Further power-path and USB-PD tests are still needed after the preliminary powered tests in \\cref{sec:res-v2-testing}.'),
('A complete test record linking these conditions is not available. The reported \\SI{85}{\\watt} remains a point to reconstruct and is not included in the measured curves.','These conditions were not recorded together. The reported \\SI{85}{\\watt} point still needs to be repeated and is not included in the measured curves.'),
('The V1.0 \\SI{202.77}{\\milli\\metre} by \\SI{72.77}{\\milli\\metre} outline does not establish V2 dimensions, so power density requires measurement of the fitted V2 assembly.','The V1.0 outline is \\SI{202.77}{\\milli\\metre} by \\SI{72.77}{\\milli\\metre}; V2 assembly dimensions must be measured separately before calculating its power density.'),
('Neither the reported \\SI{85}{\\watt} point nor the matched \\SI{79.89}{\\watt} point establishes defined-duration operation at the \\SI{100}{\\watt} target.','The reported \\SI{85}{\\watt} point and matched \\SI{79.89}{\\watt} point do not demonstrate sustained operation at the \\SI{100}{\\watt} target.')])
edit('07_Hardware/17_V3_Edge_Card_Plan.tex',[
('the estimate therefore does not establish a reduction\nfor equal system functionality.','the complete supply must be compared with those parts included.'),
('V3 design requirements to close before release; these are planned checks.','V3 design checks needed before manufacture.'),
('Required design decision and check','Design work and check'),
('before assigning a released revision.','before sending the design for manufacture.'),
('The smaller layout does not establish connector ratings, insulation\nspacing, assembled fit, or readiness for manufacture. These checks remain\nnecessary before the design can be released and evaluated as hardware.','Connector ratings, insulation spacing, and assembled fit must still be\nchecked before manufacture and hardware testing.'),
('the complete power path,\ncontrol, thermal design, and external USB-PD output stage to be assessed.','the complete power path,\ncontrol, thermal design, and external USB-PD output stage to be checked.'),
('the\nschematic/layout, design-rule, BOM, and manufacturing reviews must be\nclosed.','the\nschematic, layout, design rules, BOM, and manufacturing details must be\nchecked.'),
('V3 remains a layout estimate;\noperating evidence is limited to the V1 measurements and V2 bench\nobservations.','V3 remains an untested layout;\noperating results come from the V1 measurements and V2 bench tests.')])
edit('07_Hardware/chapter.tex',[
('The following sections distinguish the tested assembly, subsequent circuit revisions, and the V3 layout.','The following sections describe the tested assembly, later circuit revisions, and V3 layout.')])

edit('08_Control_Firmware/02_Architecture_Timing.tex',[
('Control and timing paths in the baseline firmware. The controller uses secondary-bulk voltage feedback at PA1 for regulation and the primary-current signal at PA2 for load classification. PA10 enables power-stage bursts while PA8/PA9 retain the fixed carrier. OFF/fault forces PA10 low; soft holdoff requests \\texttt{BLOW}, default zero.','Baseline control loop and timing. PA1 provides secondary-bulk voltage feedback; PA2 provides primary-current feedback for load detection. PA10 enables bursts and PA8/PA9 generate the fixed carrier. OFF/fault drives PA10 low; soft holdoff requests \\texttt{BLOW}, which is zero by default.'),
('Hardware resources used by the baseline firmware.','Timers, ADC, and UART used by the baseline firmware.'),
('Resource & Assignment & Function','Peripheral & MCU pins & Function'),
('Fixed carrier and enable-edge synchronization','Fixed carrier and attempts to align enable edges'),
('Continuous three-channel acquisition','Continuous sampling of the three inputs'),
('external timing captures are required to establish their jitter distribution.','external timing captures are needed to measure their jitter.')])
edit('08_Control_Firmware/03_Feedback_Calibration.tex',[
('The reference changes between drawings in \\cref{sec:hw-sensing} require a measured node-to-pin check.','The reference changes between drawings in \\cref{sec:hw-sensing} must be checked by measuring the circuit voltage and corresponding ADC-pin voltage.'),
('Calibration fields exported with the controller configuration.','ADC calibration settings in the configuration export.'),
('Channel & Principal fields & Interpretation','MCU pin & Settings & Purpose'),
('Primary-voltage reconstruction','Primary-voltage conversion'),
('Secondary-bulk reconstruction','Secondary-bulk voltage conversion')])
edit('08_Control_Firmware/06_Blocking_Limitations.tex',[
('Matched timing tests were not performed, so a measured improvement in update jitter or stability cannot be assigned to this change alone.','Matched timing tests were not performed, so the change in update jitter or stability was not measured separately.')])
edit('08_Control_Firmware/07_V2_DMA.tex',[
('Acquisition, feedback interpretation, operating states, and burst scheduling were revised at separate stages. The available measurements do not isolate a performance gain from DMA alone.','Acquisition, feedback scaling, operating states, and burst scheduling changed at different stages. The tests do not isolate the effect of DMA alone.')])
edit('08_Control_Firmware/08_Control_Law.tex',[
('Functional summary of the baseline voltage-control path. Protection details are specified separately in Section~\\ref{sec:ctrl-faults}.','Baseline voltage-control sequence. Fault handling is described in Section~\\ref{sec:ctrl-faults}.')])
edit('08_Control_Firmware/09_Limits_Antiwindup.tex',[
('Requested duty, scheduled burst width, and effective average duty must be recorded separately for waveform comparisons.','Waveform comparisons need the requested duty, scheduled burst width, and effective average duty.')])
edit('08_Control_Firmware/10_Open_Circuit_Safety.tex',[
('These are controller defaults, not connector-voltage limits for every test.','These defaults apply to the secondary bulk supply; the USB-C output has its own voltage setting.'),
('Peak markers and a firmware-state trace are still needed to assess its worst-case margin.','Peak-voltage measurements and a firmware-state trace are still needed to check the worst case.')])
edit('08_Control_Firmware/11_State_Machine.tex',[
('Operating flow in the baseline firmware. Mode commands select OPEN manual duty or voltage control, whose branches include loaded/no-load operation and eligible soft holdoff at \\texttt{BLOW} (default zero). OFF and latched faults inhibit PA10 globally.','Baseline firmware states. OPEN selects manual duty; voltage control switches between loaded and no-load operation and can enter soft holdoff at \\texttt{BLOW} (default zero). OFF and latched faults force PA10 low.'),
('Main operating states and exit conditions.','Firmware states, actions, and exit conditions.'),
('Configure resources and hold PA10 low','Configure peripherals and hold PA10 low')])
edit('08_Control_Firmware/12_Fault_Handling.tex',[
('this does not establish detection of every conversion or transfer error.','the flag alone does not detect every conversion or transfer error.'),
('This extended threshold must be included when assessing voltage margin.','This higher threshold must be included when checking voltage stress.'),
('These firmware functions do not provide a protection channel independent of the controller.','There is no separate hardware protection channel in these firmware checks.')])
edit('08_Control_Firmware/13_Timing_Resources.tex',[
('Each test therefore needs its source and runtime \\texttt{VER} response recorded together with its \\texttt{EXPORT}.','Each test therefore needs the source version, runtime \\texttt{VER} response, and \\texttt{EXPORT} saved together.')])
edit('08_Control_Firmware/14_Version_Comparison.tex',[
('Bring-up exposed limitations in acquisition timing, feedback interpretation, and burst control. \\Cref{tab:ctrl-version-identity} summarizes the resulting development stages, independently of the V1, V2, and V3 hardware revisions.','Bring-up exposed limitations in acquisition timing, feedback scaling, and burst control. \\Cref{tab:ctrl-version-identity} summarizes the firmware development; V1, V2, and V3 refer to hardware revisions.'),
('Continuous ADC DMA and revised feedback interpretation','Continuous ADC DMA and corrected feedback scaling'),
('Final control used with the documented prototype','Final control used for the prototype tests')])
edit('08_Control_Firmware/15_PWR_2_Port.tex',[
('Changes from the measured-baseline controller to the V2 controller port.','MCU pin and peripheral changes from the baseline controller to V2.'),
('Same analog pins and signal meanings','Same feedback inputs on the same MCU pins'),
('Command IDs and acknowledgments distinguish requested changes from accepted ones.','Command IDs and acknowledgments show whether the MCU accepted a change.'),
('The browser uses the same physical channel meanings.','The browser displays the same measured quantities as the firmware.'),
('Powered validation requires confirmation of the fitted configuration, sensing gains, and switching timing, followed by matched electrical and thermal tests toward','Further powered tests require the fitted parts, sensing gains, and switching timing to be checked, followed by matched electrical and thermal tests toward'),
('remain distinct (Section~\\ref{sec:hw-v2}).','come from different tests (Section~\\ref{sec:hw-v2}).')])
edit('08_Control_Firmware/chapter.tex',[
('Development Stages and Software Identification','Firmware Development and Versions'),
('identified final tests','final tests with a recorded firmware version'),
('Table~\\ref{tab:ctrl-software-identities} identifies the two archived\ncontrollers. The \\texttt{PWR} software identifiers are distinct from the\nV1, V2, and V3 hardware names; exact software identification is retained\nwhere needed to reproduce a test.','Table~\\ref{tab:ctrl-software-identities} lists the two firmware programs\nincluded with this thesis. The \\texttt{PWR} labels are software versions;\nV1, V2, and V3 refer to the boards.'),
('Names used for the two archived controller programs.','Firmware versions included with this thesis.'),
('Development stage & Software identifier & Role in this thesis','Firmware & Version & Use'),
('Controller associated with the identified final V1.0 test records','Used in the main V1.0 test series; individual run versions are listed with the results'),
('Hardware port with browser commands and logging; not an identification of the later bench-run firmware','MCU port with browser commands and logging. The later bench-run version was not recorded.'),
('The following sections use descriptive development stages. Software\nhistory and source-file details are given in Appendix~\\ref{app:firmware}.','The software history and source-file details are given in\nAppendix~\\ref{app:firmware}.'),
('Further validation requires synchronized control-state, enable-timing, electrical, and thermal measurements to separate control limits from power-stage limits.','Further tests need synchronized controller-state, enable-timing, electrical, and thermal measurements to determine whether the controller or power stage limits output.')])

for p,data in pending.items():p.write_bytes(data)

out=Path('/workspace/tooling/thesis-direct-language/control-edits.json')
out.write_text(json.dumps(changes,indent=2)+'\n')
print('Applied',len(changes),'prose/caption/table replacements in',len(set(r['path'] for r in changes)),'files')
