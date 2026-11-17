from pathlib import Path
import json

root=Path('/workspace/thesis/Chapters')
edits={
'02_Background/01_Offline_ACDC_PFC.tex':[
('A numerical comparison requires matched operating points and power boundaries, measured device stress, and complete assembly volumes at verified continuous output.', 'A numerical comparison needs the same operating conditions and measurement points, measured device stress, and complete assembly volumes at verified continuous output.'),
('Only the charge-pump supply was tested; a matched boost-PFC benchmark remains outstanding.', 'Only the charge-pump supply was tested; boost-PFC comparison tests remain to be done.')],
'02_Background/03_ClassDE_Resonant.tex':[
('The series approximation is used for initial sizing; the magnetizing branch and burst dynamics are retained when interpreting prototype switching and transients.', 'The series approximation is used for initial sizing; magnetizing current and burst dynamics are also considered when analyzing prototype switching and transients.')],
'02_Background/04_Soft_Switching_GaN.tex':[
('They establish operating principles; measurements establish switching behavior in the assembled stage.', 'These models describe the operating principle, but the assembled stage needs its own switching measurements.'),
('A ZVS assessment requires switch-node voltage aligned with the incoming gate command or device turn-on time, with adequate bandwidth and controlled probe loading, loop area, and common-mode error.', 'ZVS must be checked from switch-node voltage and the incoming gate command or device turn-on time on the same time base, with adequate bandwidth and controlled probe loading, loop area, and common-mode error.')],
'02_Background/05_Reference_2020.tex':[
('These results establish a working example of the principle and provide a starting point for the design calculations.', 'These results demonstrate the principle and provide a starting point for the design calculations.'),
('The prototype adds different magnetics, isolation, a downstream regulator, and sampled burst control; its complete-system performance is therefore measured independently.', 'The prototype uses different magnetics, isolation, a downstream regulator, and sampled burst control, so the reference efficiency cannot be assumed for this supply.')],
'02_Background/06_Reference_2021.tex':[
('Relationship between the reference converters and the present project.', 'Reference converters and the USB-C prototype.'),
('Work & Principal architecture & Relevance', 'Work & Circuit & Use in this project'),
('Closest circuit and burst-control precedent', 'Circuit and burst-control starting point')],
'03_Requirements_Architecture/chapter.tex':[
('These states define the hardware interfaces and verification requirements. Power targets are distinguished from implemented controller settings and measured capability.', 'These operating states determine the hardware interfaces and tests. The following sections give the power targets, controller settings, and measurements needed to check the supply.')],
'03_Requirements_Architecture/01_Use_Case.tex':[
('A short capture at a nominal load only establishes that operating point.', 'A short capture shows operation at that load, but not continuous performance.'),
('Residual resonant and capacitive energy after removal makes no-load control and overvoltage response explicit design requirements.', 'Residual resonant and capacitive energy after load removal must be handled by no-load control and overvoltage protection.')],
'03_Requirements_Architecture/02_Electrical_Specifications.tex':[
('distinguishes power criteria from the original MCU timing and feedback parameters.', 'lists the power targets and the original MCU timing and feedback settings.'),
('Principal targets and parameters of the laboratory converter.', 'Converter targets and controller settings.'),
('Quantity & Target or implemented value & Assessment', 'Parameter & Target or setting & Check'),
('Matched electrical, duration, and thermal records', 'Output power, run time, and temperature'),
('Power actuator & PA10 enables bursts of carrier cycles', 'Burst-enable pin & PA10 enables bursts of carrier cycles'),
('Quantities used to characterize performance.', 'Performance measurements.'),
('Quantity & Required interpretation', 'Quantity & Measurements and test conditions'),
('Mean VBUS and its deviation from the selected setting; ripple identified by capture conditions', 'Mean VBUS, deviation from the selected setting, and ripple with the capture conditions stated'),
('Corresponding input/output power values and the stated power boundary', 'Input and output power under the same conditions, with included stages and auxiliaries stated'),
('Measured node, time scale, probe arrangement, and evidence relevant to commutation', 'Switch-node and gate waveforms, time scale, and probe arrangement'),
('Section~\\ref{sec:revised-plan-criteria} gives those criteria and their status. These are requirements for the next tests, rather than demonstrated capabilities of the tested baseline.', 'Section~\\ref{sec:revised-plan-criteria} lists the work still needed. These tests have not all been completed on the baseline prototype.')],
'03_Requirements_Architecture/03_Functional_Requirements.tex':[
('Requirement identifiers connect the implemented control functions and measured performance to the results assessment.', 'The FR labels identify control functions, and the PR labels identify performance tests in the results chapter.'),
('Controller interfaces are introduced in \\cref{sec:intro-controller-basics}. On the original prototype, PA10 gates switching bursts, PA1 senses secondary bulk voltage, PA0 senses primary voltage, and PA2 senses half-bridge current.', 'MCU pin assignments are listed in \\cref{sec:intro-controller-basics}. On the original prototype, pin PA10 controls switching bursts, PA1 senses secondary bulk voltage, PA0 senses primary voltage, and PA2 senses half-bridge current.'),
('Direct memory access (DMA) buffers the ADC scan; the universal asynchronous receiver-transmitter (UART) carries commands and status.', 'DMA transfers ADC readings to memory, and UART carries commands and status.'),
('Performance and reporting requirements.', 'Performance tests and measurement conditions.'),
('ID & Required assessment', 'ID & Measurement or test'),
('Calculate efficiency only from corresponding input/output power records with a defined boundary.', 'Calculate efficiency from input and output power measured under the same conditions, with the included circuit stages stated.'),
('Interpret temperature observations together with load, duration, ambient condition, and airflow information.', 'Report temperature together with load, run time, ambient condition, and airflow information.'),
('Associate numerical results with their assembly, firmware, operating condition, and measurement source.', 'Record the assembly, firmware, operating conditions, and source measurements for each numerical result.'),
('assigns AP identifiers to the additional V2/V3 development criteria, separate from the baseline functions.', 'lists the additional V2/V3 design and test tasks under AP labels.')],
'03_Requirements_Architecture/04_USBC_Interface.tex':[
('USB-C Interface and Voltage Nodes', 'USB-C Output Stage')],
'03_Requirements_Architecture/05_Safety_Protection.tex':[
('The protection assessment covers laboratory behavior. Product qualification remains separate work.', 'The completed checks cover supervised laboratory operation, not product qualification.')],
'03_Requirements_Architecture/06_System_Architecture.tex':[
(' The power and sensing barriers serve different functions.', ''),
('On the original prototype, PA8 and PA9 generate complementary carrier commands and PA10 gates average transfer through burst enable.', 'On the original prototype, MCU pins PA8 and PA9 generate complementary carrier commands, while PA10 enables switching bursts.'),
('Bring-up therefore establishes these rails and the inhibited carrier before feedback calibration and low-power transfer. Closed-loop operation follows once isolated feedback is valid.', 'These rails must be checked with the carrier inhibited before feedback calibration and low-power transfer. Closed-loop regulation requires valid isolated feedback.'),
('Functional architecture of the tested V1.0 assembly, interpreted with the V1.1 schematic corrections. Charge-pump transfer and resonant transfer use the shared GaN stage. PA1 senses the secondary bulk bus before the USB-C output stage; PA0 and PA2 indicate primary voltage and half-bridge current. The transformer and AMC0330 blocks span their functional isolation boundary.', 'Power and control architecture of the V1.0 prototype with the V1.1 circuit corrections. The transformer carries power across the isolation barrier, and the AMC0330 returns secondary-bulk feedback to the MCU. PA1 measures this feedback; PA0 and PA2 measure primary voltage and half-bridge current.')],
'03_Requirements_Architecture/07_Operating_Modes.tex':[
('The original prototype uses PA10 as the active-high burst-enable GPIO.', 'The original prototype uses MCU pin PA10 as the active-high burst-enable output.'),
('Applies a limited burst command to establish secondary power and valid feedback before normal regulation.', 'Applies limited bursts to power the secondary-side feedback circuit before normal regulation.'),
('Full-demand escape &', 'Load-recovery override &'),
('The resulting low-frequency envelope depends on load state and settings, including line feed-forward and \\texttt{MAXRATE}. Each waveform is interpreted with the applicable configuration.', 'The burst envelope depends on load state and settings, including line feed-forward and \\texttt{MAXRATE}.'),
('Reaching the attempt limit ends precharge without guaranteeing valid feedback.', 'The attempt limit can be reached before feedback becomes valid.')],
'03_Requirements_Architecture/08_Verification_Matrix.tex':[
('connect each requirement to an assessment. The behavior implemented in the firmware is checked against the electrical measurements.', 'list the tests and measurements needed to check each requirement.'),
('Assessment of functional requirements.', 'Checks for the functional requirements.'),
('Assessment of performance and reporting requirements.', 'Checks for the performance requirements.'),
('ID & Assessment & Results section', 'ID & Test or measurement & Results section'),
('Consistent input/output power and measurement boundary', 'Input/output power measured under the same conditions and at stated circuit points'),
('Consistency of test identity and source records', 'Hardware, firmware, and source measurements for each result'),
('Firmware implementation establishes the commanded function, while measurements establish its electrical response.', 'Source code shows which functions were implemented; measurements show how the circuit responded.')],
'03_Requirements_Architecture/09_Revised_Plan_Criteria.tex':[
('The criteria below cover V2 baseline repetition, diagnosis of the output-power limit, controlled design changes, and readiness for final evaluation.', 'The plan calls for repeating the V2 tests, finding the output-power limit, testing controlled design changes, and preparing the final evaluation.'),
('Table~\\ref{tab:req-revised-plan-criteria} defines the additional design and test criteria, including thermal, stability, and volume measurements required beyond output power.', 'Table~\\ref{tab:req-revised-plan-criteria} lists the additional design work and tests, including temperature, stability, and volume measurements.'),
('Revised-plan acceptance and reporting criteria.', 'Tests and design work in the revised plan.'),
('Acceptance and reporting criteria carried forward from the revised project plan.', 'Tests and design work in the revised project plan.'),
('Required work and acceptance record', 'Planned test or design work'),
('using matched electrical measurements and defined-duration thermal/stability records.', 'using simultaneous electrical measurements and defined-duration thermal and stability runs.'),
('A single thermal image does not close this criterion.', 'A thermal image alone does not show thermal equilibrium or long-term stability.'),
('using the same stated volume convention and supported power basis.', 'using the same volume calculation and output-power test conditions.'),
('Record the V3 readiness decision and resulting test scope.', 'Decide whether V3 is ready for testing and list the tests that can be completed.'),
('a completed V3 readiness decision, and the paired full-system density comparison remain open.', 'a decision on V3 testing, and the full-system power-density comparison remain open.'),
('Original electromagnetic design is attributed in Section~\\ref{sec:intro-contributions}.', 'The original electromagnetic design came from the earlier work described in Section~\\ref{sec:intro-contributions}.')],
'04_Topology_Analysis/01_Topology_Overview.tex':[
('Throughout the analysis, \\(V_{\\mathrm{sec}}\\) denotes bulk voltage and VBUS denotes connector voltage.', '\\(V_{\\mathrm{sec}}\\) is the secondary bulk voltage, and VBUS is the USB-C output voltage.')],
'04_Topology_Analysis/02_Switching_Cycle.tex':[
('Ideal pump-branch intervals in the modified charge-pump topology. Device names refer to functional paths in the reference analysis.', 'Ideal charge-pump intervals during one switching cycle.'),
('Burst restart begins from the inductor currents and capacitor voltages left by the idle interval. It therefore requires separate assessment from the periodic sequence, particularly during sparse no-load packets.', 'Each burst restarts with the inductor currents and capacitor voltages left by the idle interval. The first cycles can therefore differ from steady switching, particularly during sparse no-load packets.')],
'04_Topology_Analysis/03_Line_Cycle_PFC.tex':[
('Power quality must therefore be assessed with the final controller.', 'PF and current THD must therefore be measured with the final controller.')],
'04_Topology_Analysis/05_Pump_Inductor.tex':[
('in-circuit current and clamp timing determine agreement with the assumed sequence.', 'in-circuit current waveforms and clamp timing are needed to check the triangular-current assumption.')],
'04_Topology_Analysis/11_Design_Summary.tex':[
('Table~\\ref{tab:analysis-design-summary} lists the values used to connect the reference equations to the prototype. It separates nominal circuit values, supplied magnetic measurements, and calculated estimates.', 'Table~\\ref{tab:analysis-design-summary} summarizes the prototype parameters used in the calculations.'),
('Quantity & Value & Interpretation', 'Parameter & Value & Notes'),
('Nominal implementation value', 'Nominal circuit value'),
('Inherited A/B measurements', 'Supplied measurements for inductors A and B'),
('Final discrete series contribution', 'External series inductance'),
('Inherited primary-referred measurement', 'Supplied primary-referred leakage measurement'),
('Sum if the stated contributions act in series', 'Discrete inductance plus leakage, assuming series connection'),
('Inherited transformer-variant range', 'Range of supplied transformer measurements'),
('Primary-to-secondary step-down convention', 'Primary-to-secondary turns ratio')],
}

changes=[]
for rel, replacements in edits.items():
 p=root/rel
 data=p.read_bytes()
 original=data
 rows=[]
 for a,b in replacements:
  left,right=a.encode(),b.encode()
  count=data.count(left)
  assert count>0,(rel,a)
  data=data.replace(left,right)
  rows.append({'before':a,'after':b,'occurrences':count})
 assert data!=original,rel
 p.write_bytes(data)
 changes.append({'path':'Chapters/'+rel,'replacements':rows})

out=Path('/workspace/tooling/thesis-direct-language')
(out/'early-edits.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Edited',len(changes),'files with',sum(sum(r['occurrences'] for r in c['replacements']) for c in changes),'local replacements')
