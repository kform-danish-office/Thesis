from pathlib import Path
import json
root=Path('/workspace/thesis')
changes={
'Chapters/09_Experimental_Methods/01_Objectives.tex':[
('Experimental questions and their primary observations.','Measurements used to evaluate the prototype.'),
('The baseline firmware used for the identified final runs is described in Section~\\ref{sec:ctrl-firmware-identities}. Where available,','The baseline firmware used for the final runs is described in Section~\\ref{sec:ctrl-firmware-identities}. Where available,')],
'Chapters/09_Experimental_Methods/02_Safety_Arrangements.tex':[
('Safety and connection metadata relevant to an energized test.','Connections and settings needed for powered tests.'),
('Item & Information required to interpret the test','Item & Settings and connections')],
'Chapters/09_Experimental_Methods/03_Test_Bench.tex':[
('Principal experimental equipment.','Test equipment.'),
('Serial numbers and certificate identifiers\nare missing from the thesis files.','Instrument serial numbers and calibration certificates\nwere not recorded.')],
'Chapters/09_Experimental_Methods/04_Instrumentation.tex':[
('Instrument roles and retained outputs.','Instruments and recorded measurements.'),
('Quantity & Instrument & Evidence','Quantity & Instrument & Recorded output'),
('Typical channel assignments in the time-domain tests. The capture-specific assignment takes precedence.','Typical oscilloscope channel assignments.'),
('100:1 high-voltage channel with the declared local reference','100:1 high-voltage channel referenced to the measured circuit'),
('Input power-analysis channel definitions.','Oscilloscope channels for input-power measurements.'),
('Capture-specific node assignments, attenuation, range, coupling, bandwidth,\ntrigger, and timebase take precedence over channel color or number.','Waveform interpretation requires the node assignments, probe attenuation,\nrange, coupling, bandwidth, trigger, and timebase for each capture. Channel\ncolor and number alone do not identify the measurement.')],
'Chapters/09_Experimental_Methods/05_Probing.tex':[
('Setup information needed for waveform interpretation.','Probe and trigger settings needed for each test.'),
('Waveform class & Relevant metadata','Test & Probe and acquisition settings')],
'Chapters/09_Experimental_Methods/06_Test_Matrix.tex':[
('Test classes used to characterize the prototype.','Prototype test program.'),
('Workbook entries, screenshots, waveform exports, firmware, and photographs\nwere retained. Numerical exports preserve their original precision; missing\nsetup details and peak markers limit derived quantities as discussed in\n\\cref{sec:method-uncertainty}. Plot lines connect measured points without\nimplying intermediate measurements or a fitted converter model.','Workbook entries, screenshots, waveform exports, firmware, and photographs\nare included with the test data. Numerical exports keep the original\nprecision. Missing setup details and peak markers limit the calculations,\nas discussed in \\cref{sec:method-uncertainty}. Plot lines connect measured\npoints; they are not fitted converter characteristics.')],
'Chapters/09_Experimental_Methods/07_Control_Tests.tex':[
('through burst-enable\noutput PA10.','through the MCU burst-enable\npin PA10.'),
('Observations used in control-response assessment.','Signals recorded during control tests.')],
'Chapters/09_Experimental_Methods/11_Uncertainty.tex':[
('Workbook precision is preserved for\nreproducibility rather than claimed accuracy; unsupported error bars are\nomitted.','The workbook values are shown at their original precision,\nwhich exceeds the known measurement accuracy. Error bars are omitted\nbecause the required uncertainty data are incomplete.')],
'Chapters/09_Experimental_Methods/12_Revised_Plan_Validation.tex':[
('\\subsection{Identify and Repeat the V2 Baseline}','\\subsection{Repeat the V2 Baseline}'),
('The measurement record must include analyzer identity, ranges and accuracy,','The measurements must identify the analyzer, ranges and accuracy,'),
('\\caption[Planned power sequence for validation.]{Planned power sequence from the revised project plan. No row adds a measured result.}','\\caption[Planned load sequence.]{Planned load sequence for the remaining tests.}'),
('Stage & Purpose and condition for proceeding','Stage & Test and condition for increasing load')],
'Chapters/10_Results/01_Prototype_Verification.tex':[
('The identified final records used the baseline voltage-control firmware.','The final test records used the baseline voltage-control firmware.'),
('Hardware and control configuration of the final measurement campaign.','Hardware and firmware used in the final tests.'),
('Item & Recorded configuration','Item & Test configuration'),
('V1.0 PCB; V1.1 is the corrected schematic reference, not a second manufactured PCB','V1.0 PCB with rework; V1.1 documents the corrected circuit'),
('The appendix retains complete tables and\nsource rows, and processed CSVs retain original and calculated values.','Complete tables and\nsource rows are included in the appendix; processed CSVs include both\noriginal readings and calculated values.'),
('DC-coupled captures establish absolute mean output; AC-coupled captures\nprovide detail and acquisition statistics. Thermal images locate labeled\nsurface heating. Additional raw waveform exports preserve original samples\nbut have incomplete load identification and probe calibration. Graphs show\nmeasured points only. Insufficient uncertainty records preclude error bars;\ninstrument and measurement-field discrepancies are stated with the results.','DC-coupled captures show mean output voltage; AC-coupled captures show\nsmall-signal detail and acquisition statistics. Thermal images show surface\nhotspots. The raw waveform exports include the original samples, but some\nlack load and probe-calibration details. Graphs show measured points only.\nError bars are omitted because the uncertainty data are incomplete.\nInstrument disagreements and ambiguous measurement fields are discussed\nwith the affected results.')],
'Chapters/10_Results/02_Startup_Shutdown.tex':[
('The retained\nrecords begin after startup','The available\ncaptures begin after startup')],
'Chapters/10_Results/03_Steady_State.tex':[
('Output regulation and original scope entries from the completed DC-coupled records. The right panel uses a logarithmic axis and reproduces the workbook VBUS peak-to-peak field, including anomalous values. It does not combine these values with AC-detail statistics.','Measured output-voltage error and the workbook VBUS peak-to-peak readings. The right panel uses a logarithmic scale and includes the anomalous workbook values. AC-coupled statistics are plotted separately.'),
('Representative maximum-load and high-power DC records. Output power is calculated from the recorded average VBUS and load current; the pp column reproduces the original workbook field.','Maximum-load and high-power measurements. Output power is calculated from average VBUS and load current. The pp column contains the original workbook readings.'),
('Comparisons use calculated output;\noriginal test names retain traceability.','Comparisons use calculated output;\nthe original test names are kept so each point can be found in the workbook.'),
('Representative original DC-coupled screenshots. Yellow is the switch node, green is the secondary intermediate bus, and blue is USB-C VBUS according to the source notes. The complete screenshot groups remain in the measurement archive.','DC-coupled voltage captures. The source notes identify yellow as the switch node, green as the secondary bulk voltage, and blue as USB-C VBUS. The complete capture groups are included with the test data.'),
('Incomplete probe, measurement-selection, and window records preclude a\ncorrection; the entries are retained but require remeasurement.','The probe, selected measurement, and acquisition window were not fully\nrecorded, so these values cannot be corrected reliably and must be remeasured.'),
("Logged output-channel detail ranges from the AC-coupled captures. Several numbers represent the range of the oscilloscope's averaged-voltage statistics across acquisitions. They are not validated instantaneous peak-to-peak output ripple.","Output-channel statistics from the AC-coupled captures. Several readings are the range of average voltage across acquisitions, rather than instantaneous peak-to-peak ripple."),
('Original AC-coupled detail screenshots. CH1 remains DC-coupled; CH2 and CH3 cannot establish absolute secondary-bus or VBUS voltage.','AC-coupled output-detail captures. CH1 is DC-coupled; CH2 and CH3 do not show absolute secondary-bus or VBUS voltage.')],
'Chapters/10_Results/04_Load_Transients.tex':[
('Retained load-removal screenshots. The traces document the response around the event, but do not include a simultaneous terminal-current measurement and firmware-state log.','Voltage response during load removal. Load current and firmware state were not recorded simultaneously with these traces.'),
('Numerical fields retained for load-removal events. The acquisition-wide average and pp field are not the overshoot relative to the pre-step output.','Load-removal voltage readings. Average and peak-to-peak values cover the full acquisition and do not give the overshoot from the pre-step voltage.'),
('a declared regulation band. Neither result can be derived from the retained\nacquisition-wide pp fields. Missing synchronized burst-enable PA10 and UART\nstate also prevent attribution to \\texttt{LBOOST}, voltage-window, or no-load\nguarding. Repeated, event-marked steps are required to separate these responses.','a specified regulation band. Neither result can be calculated from the\nacquisition-wide pp readings. Burst-enable PA10 and UART state were not\nrecorded at the same time, so the response cannot be assigned to\n\\texttt{LBOOST}, the voltage window, or no-load guarding. Repeated steps\nwith event markers are needed to measure each response.')],
'Chapters/10_Results/05_Open_Circuit.tex':[
('Completed no-load observations. The pp column retains the original workbook field; the \\SI{20}{\\volt} detail entry is a different measurement category.','No-load voltage readings. The pp column contains the workbook values; the \\SI{20}{\\volt} entry instead gives AC-coupled statistics.'),
('Record & VBUS avg (V) & Logged pp/detail (V) & Evidence type','Test & VBUS avg (V) & Logged pp/detail (V) & Capture type')],
'Chapters/10_Results/06_ZVS.tex':[
('The MCU burst-enable output PA10','The MCU burst-enable pin PA10'),
('Replotted raw C2 exports: overview records 00006 and 00008, and carrier-detail records 00007 and 00010 from \\sourcefile{Waveforms_Richard}. Samples retain their original amplitude and time scale. The records illustrate different burst activity, but are not assigned to a workbook load point because matched operating metadata are incomplete.','Raw C2 waveforms: overview records 00006 and 00008, and carrier-detail records 00007 and 00010 from \\sourcefile{Waveforms_Richard}. The original amplitude and time scales are unchanged. Load and setup details are incomplete, so these captures cannot be linked to individual workbook tests.'),
('What the retained switching evidence establishes.','Switching-waveform observations and missing measurements.'),
('Evidence & Supported interpretation','Capture & Observation or missing measurement'),
('Main DC-coupled screenshots','Main DC-coupled captures'),
('Missing gate-source/deskew data & Residual turn-on voltage and actual dead time cannot be quantified','Gate-source timing and deskew missing & Residual turn-on voltage and actual dead time cannot be measured from these captures')],
'Chapters/10_Results/07_Input_Power_Quality.tex':[
('Logged input PF and current THD versus load. Filled markers identify DC output records; the open marker identifies the \\SI{4.7}{\\ampere} high-load record with AC-coupled output channels. PF and THD originate from different instruments in some rows. No line is drawn through unmeasured loads.','Measured input PF and current THD versus load. Filled markers use DC-coupled output measurements; the open marker is the \\SI{4.7}{\\ampere} test with AC-coupled output channels. Some PF and THD readings come from different instruments. Only measured points are shown.'),
('Original LeCroy line-timescale exports from captures 7 and 8. Channels retain their recorded offset and amplitude scale. The two C3 source files are byte-identical and do not constitute independent bus measurements. Undocumented probe scaling prevents quantitative input-power or PF extraction.','LeCroy line-timescale waveforms from captures 7 and 8, with the original offsets and amplitude scales. The two C3 files contain identical data. Probe scaling was not recorded, so input power and PF cannot be calculated from these traces.')],
'Chapters/10_Results/08_Efficiency.tex':[
('Row-level efficiency and input-minus-output power calculated from eleven selected records. The marker shape identifies the fixed output voltage. The figures retain discrete observations and do not imply an interpolated efficiency characteristic or a separated power-stage loss model.','Initial efficiency estimates and input-minus-output power from eleven tests. Marker shapes identify the fixed output voltage. The points are not an efficiency curve or a breakdown of individual stage losses.'),
('Different instruments and operating histories prevent interpretation as one\ncalibrated efficiency map.','The tests used different instruments and operating histories, so these\nvalues do not form a calibrated efficiency map.'),
('the workbook\nchoice preserves reproducibility rather than resolving instrument error.','the selected\nworkbook entries are used consistently, but the instrument error remains unresolved.')],
'Chapters/10_Results/09_Thermal.tex':[
('the highest retained surface reading.','the highest recorded surface reading.'),
('Maximum surface-temperature readings from the ten labeled thermal screenshots. The conditions follow the image labels. The markers do not establish a stabilized temperature-versus-load characteristic because dwell time and airflow were not recorded.','Maximum surface temperatures in the ten thermal images, using the load conditions written on each image. Run duration and airflow were not recorded, so the points are not steady-state temperatures.'),
('Representative original thermal images, preserving the visible marker readings and supplied operating labels.','Thermal images with their camera readings and test labels.'),
('duration, airflow, camera-distance, and plateau criteria preclude a thermal\nsteady-state result.','duration, airflow, camera distance, and temperature histories prevent a\nsteady-state thermal comparison.')],
'Chapters/10_Results/10_Firmware_Comparison.tex':[
('through\nburst-enable output PA10.','through\nthe MCU burst-enable pin PA10.'),
('Control-development stages and their experimental role.','Firmware changes during development.'),
('Final documented control family used in the identified main \\SI{5}{\\volt} and \\SI{20}{\\volt} rows','Controller used in the main identified \\SI{5}{\\volt} and \\SI{20}{\\volt} tests'),
('Loaded and load-removal records demonstrate the combined controller, but\nunmatched configurations prevent attribution to individual changes.','Loaded and load-removal tests show the combined controller response.\nThe tests did not hold all other settings fixed while changing one feature,\nso the contribution of each change was not measured.')],
'Chapters/10_Results/11_Simulation_Hardware.tex':[
('Scope of the comparison between inherited simulation and hardware.','Comparison of the inherited models with the prototype measurements.'),
('Quantity & Experimental evidence & Comparison supported','Quantity & Measurements & Model comparison'),
('Identified scope captures and additional raw exports & Qualitative topology-level interpretation','Oscilloscope captures and raw waveform exports & Shows circuit operation; no numerical match'),
('Hardware is assessed against requirements at the recorded test conditions.','The prototype results are compared with the requirements at the tested loads.')],
'Chapters/10_Results/12_Compliance_Table.tex':[
('The requirement\nidentifiers from Chapter~\\ref{ch:requirements} distinguish implementation,\nmeasured behavior at tested points, and remaining validation.','The table uses the requirement\nnumbers from Chapter~\\ref{ch:requirements} and lists the completed work\nand measurements still needed.'),
('Evidence-based assessment of the prototype requirements.','Prototype requirements and test results.'),
('ID & Requirement & Experimental or implementation basis & Assessment','ID & Requirement & Measurements or implementation & Status'),
('Partly assessed','Incomplete'),
('Demonstrated at logged points','Met at tested points'),
('Retained load-removal screenshots; recovery band and timing absent & Qualitative evidence','Load-removal captures; recovery band and timing missing & Response recorded'),
('Function present in source; controlled trip event absent & Not experimentally verified','Implemented in firmware; no measured trip event & Trip not measured'),
('Mean established; pp/statistic ambiguity and transient timing gaps identified','Average voltage measured; ripple definitions and transient timing incomplete'),
('Recorded; no standards determination','Measured; standard compliance not tested'),
('Efficiency with stated boundary & Eleven transparent screening calculations; boundary uncertainty retained & Screening result','Efficiency at defined input/output points & Eleven initial estimates; included supplies and timing remain uncertain & Initial estimate'),
('Traceable; metadata incomplete','Linked; setup details incomplete'),
('No controlled isolation of limiting mechanism','The component or control action limiting power was not isolated')],
'Chapters/10_Results/13_Failures_Lessons.tex':[
('Issues that shaped the final implementation and interpretation.','Bring-up problems, corrections, and design lessons.'),
('Preserved source entries and used qualified screening calculations','Kept the original readings and calculated initial efficiency estimates'),
('Retained camera maxima and their labeled conditions','Recorded camera maxima and the stated test conditions')],
'Chapters/10_Results/14_Revised_Plan_Status.tex':[
('The retained V1.0 baseline,','The V1.0 reference test,'),
('settings, and measurement identification. The revision name does not establish\nwhich assembly was tested; the earlier configuration must be reconstructed\nbefore the reported \\SI{85}{\\watt} serves as a change baseline.','settings, and measurements. The hardware and settings used for that test\nmust be recovered before the reported \\SI{85}{\\watt} point can be repeated.'),
('\\caption[Status of revised-plan deliverables.]{Revised-plan deliverables and their status in the results reported here. Scheduled dates are not completion records.}','\\caption[Progress against the revised plan.]{Progress against the revised project plan and remaining tests.}'),
('ID & Required deliverable & Available result & Remaining assessment','ID & Planned work & Result & Remaining work'),
('Baseline identity, original run, and matched repeat remain unverified here','Original hardware/settings and a repeat test are still needed'),
('Release reviews, manufacturing/assembly readiness, and replacement-magnetics validation remain incomplete','Design review, fabrication/assembly checks, and replacement-magnetics tests remain incomplete')],
'Chapters/10_Results/15_V2_Testing_Update.tex':[
('Firmware\nidentity, timing readback, and effective switch dead time were not recorded;','The firmware\nversion, timing readback, and effective switch dead time were not recorded;'),
('No corresponding\nvoltage was retained,','No corresponding\nvoltage was recorded,'),
('Matched efficiency and temperature equivalence was not established.','Efficiency and temperature were not compared under the same conditions.'),
('V2 thermal image from a run reported as \\SI{95}{\\watt}. The camera reports a regional surface maximum of \\SI{70.0}{\\celsius} in R3 and \\SI{61.5}{\\celsius} in R1. These are displayed surface-region values, not diode-junction temperatures. The image was not mapped to individual diodes or to a specific stage of the later diode-replacement and timing changes.','V2 thermal image during the reported \\SI{95}{\\watt} run. The displayed surface maxima are \\SI{70.0}{\\celsius} in R3 and \\SI{61.5}{\\celsius} in R1. The image does not identify individual diode junctions or show which diode and timing changes were fitted.'),
('\\subsection{Next Layout Changes and Test Status}','\\subsection{Next Layout Changes}'),
('V2 assembly overview (upper left), thermal-camera bench arrangement (upper right), and component-side detail (lower). The photographs show the V2 hardware and test setup; a common test configuration across all images has not been verified.','V2 assembly overview (upper left), thermal-camera setup (upper right), and component-side detail (lower).')],
'Chapters/10_Results/16_V3_Design_Outcome.tex':[
('Development outcomes across the prototype revisions.','Main changes and results for each prototype.'),
('Revision & Main development & Outcome and remaining limit','Revision & Main change & Result and remaining work')],
'Chapters/11_Discussion/01_Key_Findings.tex':[
('Measured Performance and Revision Outcomes','Measured Performance and Prototype Changes'),
('V2 did not establish greater available output than V1.','Higher output from V2 than V1 was not demonstrated.'),
('Hotspot\nrelocation, estimated design-volume reduction, and sustained-power\nimprovement therefore remain separate outcomes.','Moving the hotspot does not show that total loss fell. The smaller layout\nalso needs power and thermal tests before sustained-power improvement\ncan be claimed.')],
'Chapters/11_Discussion/03_Control_Contribution.tex':[
('while the burst-enable output PA10 controls transfer intervals.','while the MCU burst-enable pin PA10 controls transfer intervals.'),
('Loaded demand is initialized from retained average duty','Loaded demand is initialized from the stored average duty')],
'Chapters/11_Discussion/06_Reference_Comparison.tex':[
('System & Operating context & Reported performance','System & Test conditions & Reported performance')],
'Chapters/11_Discussion/08_Lessons_Learned.tex':[
('Board identity, settings, raw waveforms, power readings, and temperature\nrecords must be retained together. Screenshots alone can omit coupling,\naveraging, and firmware state; the data appendix and rebuilt plots show\nwhere these differences affect interpretation.','Each test needs the board version, settings, waveforms, power readings,\nand temperatures recorded together. Screenshots can omit coupling,\naveraging, and firmware state, which limits what can be calculated from\nthem. The data appendix and replotted measurements show these gaps.')],
'Chapters/11_Discussion/09_Future_Improvements.tex':[
('requires its original records and an identified\nrepeat before comparison with the older assembly\'s','needs to be repeated with its hardware and settings recorded\nbefore comparison with the older assembly\'s'),
('with identified temperatures tracked\nto equilibrium.','with component temperatures followed\nto equilibrium.'),
('Its estimated volume reduction must be checked with the\nexternal output function and complete assembly defined.','Its estimated volume reduction must be checked after including the\nexternal output stage and all hardware needed by the complete supply.')],
'Chapters/11_Discussion/10_Plan_Gap_Diagnosis.tex':[
('Each hardware or MCU-port change requires\na matched baseline and test identity.','Each hardware or MCU-port change requires\na comparison test with the board and settings recorded.'),
('\\caption[Measurements for controlled converter changes.]{Measurements needed before and after a controlled converter change. The existing observations define questions, rather than a ranked component-loss result.}','\\caption[Measurements for diagnosing the power limit.]{Measurements needed before and after each change to diagnose the power limit.}'),
('Question & Existing indication & Matched baseline/retest record and resulting decision','Question & Current result & Measurements needed'),
('Power boundary and instrument agreement','Power readings and measurement points'),
('A reduced hotspot is useful only if regulation and all\nother stress limits remain acceptable. The existing records do not yet\nsupport a ranked component-loss allocation.','Lower temperature at one hotspot is useful only if regulation and all\nother stress limits remain acceptable. Individual component losses have\nnot yet been separated.')],
'Chapters/12_Conclusion/01_Project_Summary.tex':[
('The thermal image was identified as a\n\\SI{95}{\\watt} run without a continuous-rating record. These qualitative\nV2 observations remain separate from the matched V1.0 measurements.','The thermal image was reported as a\n\\SI{95}{\\watt} run, with no duration or thermal-equilibrium record. These\nV2 observations cannot be compared quantitatively with the V1.0 measurements.'),
('Neither is established by a stabilized, defined-duration run, including\nthe earlier','No stabilized run of defined duration has verified these levels or\nthe earlier'),
('V3 therefore establishes layout\ndevelopment; its loss, thermal, and continuous-power performance remain\nuntested.','V3 reached the layout stage; its losses, temperatures,\nand continuous output were not tested.')],
'Chapters/12_Conclusion/03_Contributions.tex':[
('the bench firmware identity was not recorded, and matched power and\nthermal-endurance tests remain outstanding.','the firmware version used on the bench was not recorded, and comparable\npower and thermal-endurance tests are still needed.')],
'Chapters/12_Conclusion/04_Future_Work.tex':[
('The approximately \\SI{85}{\\watt} V2 result requires recovery of the\noriginal records and an identified repeat','The approximately \\SI{85}{\\watt} V2 result needs to be repeated using the\noriginal hardware and settings')]
}
rows=[]
for rel,replacements in changes.items():
 p=root/rel;data=p.read_bytes();eol='\r\n' if b'\r\n' in data else '\n'
 for a,b in replacements:
  aa=a.replace('\n',eol).encode();bb=b.replace('\n',eol).encode()
  count=data.count(aa)
  if count==0 and bb in data:
   rows.append({'path':rel,'before':a,'after':b,'already_applied':True});continue
  expected=(Path('/workspace/tooling/thesis-direct-language/before')/rel).read_bytes().count(aa)
  if count!=expected:raise RuntimeError((rel,a,count))
  data=data.replace(aa,bb)
  rows.append({'path':rel,'before':a,'after':b,'occurrences':count})
 p.write_bytes(data)
Path('/workspace/tooling/thesis-direct-language/results-edits.json').write_text(json.dumps(rows,indent=2)+'\n')
print(len(rows),'replacements in',len(changes),'files')
