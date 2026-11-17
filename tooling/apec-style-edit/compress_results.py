from pathlib import Path
root=Path('/workspace/thesis/Chapters/10_Results');changed=[]
def rep(name,old,new):
 p=root/(name+'.tex');raw=p.read_bytes();crlf=b'\r\n' in raw;s=raw.decode().replace('\r\n','\n')
 assert old in s,(name,old[:60]);s=s.replace(old,new,1);p.write_bytes(s.replace('\n','\r\n').encode() if crlf else s.encode())
 if p not in changed:changed.append(p)
rep('01_Prototype_Verification',r'''fixed settings with a \SI{240}{\volt}, \SI{50}{\hertz} input. The selected output voltage was obtained at the tested loads. The voltage, switching,
power-quality, and temperature results below show how the supply operated
and what still needs to be checked before a continuous rating can be assigned.''',r'''fixed settings with a \SI{240}{\volt}, \SI{50}{\hertz} input. Regulation was
obtained at the tested loads; the electrical and thermal records below
characterize these points without establishing a continuous rating.''')
rep('01_Prototype_Verification',r'''The electrical calculations are based on the \texttt{Load Data} sheet in
\sourcefile{Data/measurements/Thesis_USB_PDO_3A_Limited_Test_Plan.xlsx}.
Test identifiers link each worksheet row to its oscilloscope and analyzer
screenshots. Only completed rows are used; \emph{Planned} rows remain planned
even if provisional values were entered. The appendix contains the full
numerical tables and source rows. The processed CSV files contain the original
readings alongside the calculated values.

The captures were interpreted according to their measurement setup.
DC-coupled captures provide the absolute average output, while AC-coupled
captures show variations around that level and acquisition statistics. Thermal images locate surface heating at the labeled
loads. The additional raw oscilloscope exports show their original samples,
but their load identification and probe calibration are less complete than
those of the main workbook tests.

Only measured points are shown in the graphs; results are not assigned to
untested loads. Error bars
were not added because the setup and instrument records are insufficient for
a numerical uncertainty budget. Instrument disagreements and differences
between scope fields are explained with each affected result.''',r'''Calculations use completed rows of the \texttt{Load Data} sheet in
\sourcefile{Data/measurements/Thesis_USB_PDO_3A_Limited_Test_Plan.xlsx}.
Test identifiers link rows to oscilloscope and analyzer screenshots;
\emph{Planned} rows are excluded. The appendix retains complete tables and
source rows, and processed CSVs retain original and calculated values.

DC-coupled captures establish absolute mean output; AC-coupled captures
provide detail and acquisition statistics. Thermal images locate labeled
surface heating. Additional raw waveform exports preserve original samples
but have incomplete load identification and probe calibration. Graphs show
measured points only. Insufficient uncertainty records preclude error bars;
instrument and measurement-field discrepancies are stated with the results.''')
rep('02_Startup_Shutdown',r'''The converter started and reached regulation at all four tested settings,
but the saved measurements begin after the loaded operating condition was
reached. The command, PA10, output voltage, and firmware state were not
recorded together. These signals are needed to calculate startup delay,
inrush, overshoot, shutdown delay, and discharge time.

The precharge and shutdown sequences implemented in this work are described
in Chapter~\ref{ch:control}. Both sequences still need to be captured from the initial condition through
regulation or inhibition so that measured timing can be compared with the
intended behavior.''',r'''The converter reached regulation at all four tested settings. The retained
records begin after startup and lack synchronized command, burst-enable
PA10, output-voltage, and firmware-state traces. Startup delay, inrush,
overshoot, shutdown delay, and discharge time therefore remain unquantified.
The implemented sequences are described in Chapter~\ref{ch:control}.''')
rep('03_Steady_State',r'''where \(V_\mathrm{BUS,avg}\) is the scope average at the USB-C connector.
This is a measurement of the downstream output. The intermediate secondary
bus is a separate node regulated by the upstream controller.''',r'''where \(V_\mathrm{BUS,avg}\) is the USB-C connector mean. The upstream
controller regulates the separate secondary intermediate bus.''')
rep('03_Steady_State',r'''\SI{14.9835}{\volt}. The mean was kept close to the setpoint by the downstream stage. This does
not limit the magnitude of ripple or transient excursions.''',r'''\SI{14.9835}{\volt}. These means establish downstream regulation rather than
ripple or transient limits.''')
rep('03_Steady_State',r'''exceeds \SI{75}{\watt} electrically. Performance is compared using the
calculated output. The original test names are kept so the records can be
located.''',r'''exceeds \SI{75}{\watt} electrically. Comparisons use calculated output;
original test names retain traceability.''')
rep('03_Steady_State',r'''The ripple fields from the longer acquisition windows are less clear. At \SI{20}{\volt} and
\SI{0.25}{\ampere}, the VBUS entry is \SI{12.6564}{\volt}, described
as ``amplitude/ripple.'' Other rows also have unusually large pp values.
The saved probe settings, measurement selections, and windows do not explain
the large values, so there is no basis for correcting the entries. They remain
in the table. A new acquisition is needed for a reliable ripple measurement.''',r'''Long-window ripple fields remain unresolved. At \SI{20}{\volt} and
\SI{0.25}{\ampere}, VBUS is listed as \SI{12.6564}{\volt}
``amplitude/ripple.'' Several other pp entries are anomalously large.
Incomplete probe, measurement-selection, and window records preclude a
correction; the entries are retained but require remeasurement.''')
rep('03_Steady_State',r'''The later captures used AC coupling and a changed probe setup. Their VBUS
detail fields span about \SI{25}{\milli\volt} to \SI{83}{\milli\volt}.
On several screens, the quantity is \emph{Range (Max--Min)} of
\emph{V avg} across acquisitions. For example, the \SI{5}{\volt},
\SI{3}{\ampere} capture gives \SI{29.6924}{\milli\volt} for the spread
of VBUS-average statistics. This is the spread between average readings,
not \SI{29.7}{\milli\volt} of instantaneous peak-to-peak ripple.''',r'''The later AC-coupled captures used a different probe setup and report VBUS
detail fields of approximately \SI{25}{\milli\volt} to \SI{83}{\milli\volt}.
Several fields are the acquisition-to-acquisition \emph{Range (Max--Min)} of
\emph{V avg}. At \SI{5}{\volt}, \SI{3}{\ampere}, the reported
\SI{29.6924}{\milli\volt} is this statistical spread, rather than
\SI{29.7}{\milli\volt} instantaneous peak-to-peak ripple.''')
rep('04_Load_Transients',r'''The no-load control was examined during load removal. Energy remaining in
the resonant network can continue charging the secondary bus after the load
is disconnected.
The four captures below show switching and output-voltage response around
disconnection at the tested settings.''',r'''Load-removal tests examined secondary-bus charging by residual resonant
energy. The four captures below show switching and output-voltage response
around disconnection.''')
rep('04_Load_Transients',r'''with a measured pre-step average and a synchronized load-event marker.
Recovery time would end when voltage returned to a declared regulation band.
The captures lack a consistent event marker and band, so their
acquisition-wide pp values cannot supply either result.

The traces show the transition from load to no load, but PA10 and UART state
were not saved together. The internal \texttt{LBOOST}, voltage-window, or
no-load-guard sequence cannot be identified from these events. Capturing those
signals during repeated removals, load-increase steps, and controlled slew
rates could show which control decision governs the peak and recovery.''',r'''using the pre-step mean and a synchronized event marker. Recovery requires
a declared regulation band. Neither result can be derived from the retained
acquisition-wide pp fields. Missing synchronized burst-enable PA10 and UART
state also prevent attribution to \texttt{LBOOST}, voltage-window, or no-load
guarding. Repeated, event-marked steps are required to separate these responses.''')
rep('05_Open_Circuit',r'''\SI{0.358}{\percent} above their targets. Transfer could therefore be reduced while the average output voltage was
maintained close to the selected value at these points.''',r'''\SI{0.358}{\percent} above their targets. Reduced transfer maintained the
mean output near the selected setting.''')
rep('05_Open_Circuit',r'''A reliable steady-state no-load input-power value cannot be calculated
from the paired screenshots. The \SI{5}{\volt} and \SI{9}{\volt} screens retain transient
or statistical history, and the \SI{15}{\volt} capture lacks settled
input power. At \SI{20}{\volt}, AC-coupled output channels also leave the
absolute output level unknown.



The no-load voltage measurements above and the load-removal captures in
Section~\ref{sec:res-transient} show unloaded operation at the tested points. The next capture needs absolute peak voltage,
the active OVP threshold, and firmware state from the same event to assess
the protection margin.''',r'''Steady-state no-load input power remains undetermined: the \SI{5}{\volt}
and \SI{9}{\volt} screens include transient or statistical history, and the
\SI{15}{\volt} record lacks settled input power. At \SI{20}{\volt}, AC coupling
also prevents an absolute-output measurement. These records and
Section~\ref{sec:res-transient} establish unloaded operation, but protection
margin requires synchronized absolute peak voltage, active OVP threshold,
and firmware state.''')
rep('06_ZVS',r'''The switching captures show how the MCU burst-enable signal at PA10 selects
groups of the nominal
\SI{1}{\mega\hertz} carrier into bursts. Figure~\ref{fig:pdo20-high-power-scope}
shows the switch node and both output-side voltages at the main high-power
points. The additional raw C2 exports show the burst structure and individual
carrier transitions in greater detail.''',r'''The MCU burst-enable output PA10 groups the nominal \SI{1}{\mega\hertz}
carrier into packets. Figure~\ref{fig:pdo20-high-power-scope} records the
switch node and output-side voltages at identified high-power points; the
raw C2 exports resolve burst structure and carrier transitions.''')
rep('06_ZVS',r'''The processed data include the
thresholds and source checksums. This frequency applies to the exported
waveforms; it does not establish the exact timer clock used in the main
campaign.''',r'''Detection thresholds and source checksums are retained. This frequency
characterizes the exports rather than the main campaign's timer clock.''')
rep('06_ZVS',r'''The plots show bursts and ringing. A ZVS test also needs to resolve turn-on,
especially at burst starts and ends, where the resonant state differs from
that inside the packet. Probe loading, ground inductance, deskew, and amplitude
calibration must be known before those transitions can be classified.''',r'''ZVS remains unverified, particularly at packet boundaries. Classification
requires gate-referenced turn-on captures with known probe loading, return
inductance, deskew, and amplitude calibration.''')
rep('07_Input_Power_Quality',r'''The best input-power-quality readings were recorded at the high-power
\SI{20}{\volt} points.
Between \SI{3.7}{\ampere} and \SI{4}{\ampere}, logged PF approaches
unity and current-THD entries are much smaller than at several low-power
settings. Figure~\ref{fig:rebuilt-pq} shows how these readings change across
the loaded dataset.''',r'''The high-power \SI{20}{\volt} records gave the best logged input power quality.
Between \SI{3.7}{\ampere} and \SI{4}{\ampere}, PF approached unity and
current THD was lower than at several low-power points
(Figure~\ref{fig:rebuilt-pq}).''')
rep('07_Input_Power_Quality',r'''The spectra show which harmonics dominate at each load. At \SI{3.8}{\ampere},''',r'''At \SI{3.8}{\ampere},''')
rep('07_Input_Power_Quality',r'''of the fundamental. After the tables were checked against the screenshots,
the components through order 40 were summed by root-sum-square. The results are''',r'''of the fundamental. Screenshot-checked components through order 40 give
root-sum-square THD values of''')
rep('07_Input_Power_Quality',r'''Both results are reported because the difference cannot be resolved from
the saved records. A synchronized repeat is needed to identify its cause.''',r'''The discrepancy remains unresolved; both values are retained pending a
synchronized repeat.''')
rep('07_Input_Power_Quality',r'''The raw line-timescale exports show waveform shape at the original amplitudes
and offsets. They were not scaled to a target voltage or power. They lack test
identifiers linking them to the June workbook rows, and their probe calibration
is incomplete. These files were therefore not used to calculate new
calibrated PF or real-power values.

Earlier charge-pump work reported favorable PF and distortion under its own
conditions \cite{ammar2020chargepump,ammar2021led}. Here, the input filter,
magnetics, output setting, and burst pattern all change the operating
condition. Comparing against a standard requires defined acquisition,
averaging, and harmonic classification beyond these tests.
Table~\ref{tab:pq-results} retains all power-quality readings and identifiers.''',r'''Raw line-timescale exports retain original amplitudes and offsets. Missing
workbook test links and incomplete probe calibration preclude additional
calibrated PF or real-power calculations.

Earlier charge-pump results \cite{ammar2020chargepump,ammar2021led} used
different operating conditions. Input filtering, magnetics, output setting,
and burst structure limit direct comparison; these tests also do not establish
harmonics-standard compliance. Table~\ref{tab:pq-results} retains the full
readings and identifiers.''')
rep('08_Efficiency',r'''The input--output power difference was substantial at high load, even with
the output regulated. Output power, an initial efficiency estimate, and the
power difference were calculated for the usable steady-state rows as''',r'''Usable steady-state rows give output power, initial efficiency estimates,
and input--output power difference as''')
rep('08_Efficiency',r'''The different instruments and operating histories mean that these groups
do not form one calibrated efficiency map.''',r'''Different instruments and operating histories prevent interpretation as one
calibrated efficiency map.''')
rep('08_Efficiency',r'''calculated output. Measuring power at the intermediate stages and improving
heat removal are the next priorities. The total difference does not show how
much is dissipated in the GaN stage, inductors, charge pump, output interface,
or auxiliary supply.''',r'''calculated output. The total difference does not allocate loss among the GaN
stage, inductors, charge pump, output interface, and auxiliary supply;
intermediate-stage power measurements are required.''')
rep('08_Efficiency',r'''Siglent and ITECH readings still
differ in several selected groups. Using the workbook value allows the
calculation to be reproduced, but does not resolve that disagreement.

For a repeated efficiency sweep, input and output power should be measured
together after settling. Auxiliary power, cable drop, temperature history,
and propagated uncertainty should be included so the results can be compared
on the same basis. Measurements at the intermediate stages would then help
locate the losses.''',r'''Siglent/ITECH disagreement remains in several selected groups; the workbook
choice preserves reproducibility rather than resolving instrument error.
A matched sweep must synchronize settled input/output readings and account
for auxiliaries, cable drop, temperature, and propagated uncertainty.''')
rep('09_Thermal',r'''\SI{102.9}{\celsius}, the highest saved value. These surfaces need closer
temperature monitoring before raising the load or reducing the assembly size.''',r'''\SI{102.9}{\celsius}, the highest retained surface reading.''')
rep('09_Thermal',r'''The ten images use emissivity 0.95 and cover open-load and loaded conditions.
The graph uses the maximum marker rather than the cursor or lower reference.
That distinction matters at \SI{9}{\volt}, \SI{2}{\ampere}: the maximum
is \SI{56.8}{\celsius}, while the cursor and workbook give
\SI{39.7}{\celsius}.''',r'''The ten open-load and loaded images use emissivity 0.95. The plot uses camera
maxima rather than cursor/reference values: at \SI{9}{\volt},
\SI{2}{\ampere}, these are \SI{56.8}{\celsius} and
\SI{39.7}{\celsius}, respectively, with the workbook retaining the latter.''')
rep('09_Thermal',r'''Surface temperatures are shown by the camera. The component at each maximum
is not always identified, and junction temperature is not measured. The
lower reference marker was not recorded as an ambient-temperature reading. Duration, airflow,
camera distance, and a criterion for a temperature plateau were not recorded.
The \SI{4.7}{\ampere} electrical capture also lacks DC output voltage,
so its image label cannot establish a regulated \SI{94}{\watt} output.

The electrical results reach approximately \SIrange{74}{80}{\watt}.
A stabilized run is still needed to determine how long that power can be
sustained. It needs identified component hotspots, controlled ambient and
airflow, and acceptance limits for the devices and insulation system. The images identify areas for further investigation; the stabilized run
would be used to establish thermal margin.''',r'''Hotspot components are incompletely identified, junction temperatures were
not measured, and lower reference markers are not ambient readings. Missing
duration, airflow, camera-distance, and plateau criteria preclude a thermal
steady-state result. The \SI{4.7}{\ampere} record also lacks DC output
voltage, so its label does not establish regulated \SI{94}{\watt} output.

The matched electrical results reach approximately \SIrange{74}{80}{\watt}.
Continuous capability requires a stabilized run with identified hotspots,
controlled ambient/airflow, and device and insulation acceptance limits.''')
rep('10_Firmware_Comparison',r'''The final controller uses each sensed quantity for a specific task. The
secondary-bulk-voltage measurement at input PA1 is used for regulation.
The primary-current signal at PA2 is used to classify load, while the
burst-enable output at PA10 controls average energy transfer. The carrier
commands at PA8/PA9 keep the nominal switching frequency. Reaching this
arrangement required changes to acquisition timing as well as the feedback
calculation.''',r'''The final controller regulates secondary-bulk voltage through PA1, classifies
load from primary current at PA2, and controls average energy transfer through
burst-enable output PA10. Carrier outputs PA8/PA9 retain nominal switching
frequency. Both acquisition timing and feedback interpretation were revised.''')
rep('10_Firmware_Comparison',r'''The main correction was the interpretation of PA2 as half-bridge current.
Its product with PA1 could not be used as USB-C output power, so that
calculation was removed from the control approach. The
voltage loop was closed around PA1, and PA2 was used for load classification
and diagnostics. Optional PA0 feed-forward can further cap the allowed PA10
duty.''',r'''The key correction was to identify PA2 as half-bridge current rather than
output current. PA1--PA2 product-based output-power control was replaced by
PA1 voltage regulation, with PA2 retained for load classification and
diagnostics. Optional PA0 feed-forward caps PA10 duty.''')
rep('10_Firmware_Comparison',r'''The loaded and load-removal tests show the combined controller operating. Several features were changed together, and not all
revisions were tested with identical loads, probes, complete exports, and
timing logs. The contribution of each change has not been measured separately.
For example, \texttt{MAXRATE} requests a \SI{20}{\micro\second} control
period; only a timing capture could confirm the achieved period and jitter.''',r'''Loaded and load-removal records demonstrate the combined controller, but
unmatched configurations prevent attribution to individual changes. For
example, \texttt{MAXRATE} requests a \SI{20}{\micro\second} period;
the achieved period and jitter require measured timing.''')
rep('11_Simulation_Hardware',r'''The prototype is therefore assessed against its requirements under the actual
test conditions. A predictive comparison would need measured magnetic
parameters, component and layout parasitics, the implemented controller, and
the same input and load. Otherwise, a difference could come from an omitted
circuit feature rather than the hardware behavior being studied.''',r'''Hardware is assessed against requirements at the recorded test conditions.
A predictive model comparison requires measured magnetics, component/layout
parasitics, the implemented controller, and matched input and load.''')
rep('12_Compliance_Table',r'''Section~\ref{sec:revised-plan-criteria} explains these criteria. The table
uses the identifiers from Chapter~\ref{ch:requirements} to distinguish
implemented functions, observed behavior, and tests still needed.
``Demonstrated'' applies only to the points tested.''',r'''Section~\ref{sec:revised-plan-criteria} defines these criteria. The requirement
identifiers from Chapter~\ref{ch:requirements} distinguish implementation,
measured behavior at tested points, and remaining validation.''')
rep('12_Compliance_Table',r'''Average-voltage regulation is the clearest completed performance result.
Establishing an operating range also requires synchronized power and ripple
measurements, thermal endurance, transient and protection timing, and
gate-referenced switching captures. USB-PD protocol, safety, harmonic-standard,
and EMI certification remain separate qualification work.''',r'''Average-voltage regulation is established at the logged points. A rated
operating range still requires synchronized power/ripple measurements,
thermal endurance, transient/protection timing, and gate-referenced switching
captures. USB-PD, safety, harmonic-standard, and EMI qualification remain open.''')
rep('13_Failures_Lessons',r'''Voltage regulation and load classification were adopted in this work, then
minimum carrier-cycle handling and no-load guarding were revised. These
changes addressed the irregular pulses and excess charging seen during
development. They also clarified how each sensed signal was used by the
controller.

The instrument's measurement field also had to be checked before its value
could be interpreted. The plots use original samples and readings without
imposed power targets, and keep waveform ripple separate from the spread of
average readings. The highest calculated output from these measurements is \SI{79.89}{\watt}.
A continuous rating and the \SI{100}{\watt} objective still require the
next test campaign.

In that campaign, input and output power should be measured together, and
ripple captured with known coupling and bandwidth. Temperatures at identified
locations should be followed to stabilization, with firmware state recorded
at load and protection events. Each remaining design choice could then be
checked against a loss, thermal margin, or control response.''',r'''Voltage regulation, load classification, complete-cycle scheduling, and
no-load guarding addressed incorrect sensing interpretation, irregular pulses,
and excess charging. Measurement review also separated waveform ripple from
the spread of acquisition averages. Original readings give a maximum
calculated output of \SI{79.89}{\watt}; neither a continuous rating nor the
\SI{100}{\watt} objective is established.

The remaining campaign must pair input/output power, capture ripple with
known coupling and bandwidth, follow identified temperatures to stabilization,
and record controller state during load and protection events.''')
rep('14_Revised_Plan_Status',r'''The starting point matters. Here, \sourcefile{PDO20-80W-40A-001}, row 27,
gives \SI{19.9732}{\volt} at \SI{4}{\ampere}, or
\SI{79.8928}{\watt}, on the V1.0 assembly with the baseline voltage-control firmware. The
reported \SI{85}{\watt} V2 point needs its own board, firmware, settings,
and measurement files. The V2 name alone does not establish that the earlier result came from this
assembly or the later integrated V2 design and its controller port. The earlier
setup must be reconstructed before the reported \SI{85}{\watt}
value can be used as a baseline for changes.''',r'''The retained V1.0 baseline, \sourcefile{PDO20-80W-40A-001}, row 27,
gives \SI{19.9732}{\volt} at \SI{4}{\ampere}, or
\SI{79.8928}{\watt}, with the baseline voltage-control firmware. The
reported \SI{85}{\watt} V2 point requires separate board, firmware,
settings, and measurement identification. The revision name does not establish
which assembly was tested; the earlier configuration must be reconstructed
before the reported \SI{85}{\watt} serves as a change baseline.''')
rep('14_Revised_Plan_Status',r'''The next step is to repeat the identified baseline, then measure duration,
temperature, stress, and dynamic behavior against declared limits. Average
regulation alone cannot answer those questions.
The V3 design estimate is reported in \cref{sec:res-v3-design}; it does
not close the complete-system power-density comparison.
Section~\ref{sec:method-plan-validation} defines the follow-up tests, and
Section~\ref{sec:disc-plan-gap} connects them to controlled changes. These
tests are needed to assign a continuous rating and compare revisions; the
schedule itself is not a test record.''',r'''Continuous rating and revision comparison require an identified baseline
followed by duration, temperature, stress, and dynamic tests against declared
limits. The V3 estimate in \cref{sec:res-v3-design} does not establish
complete-system density. Follow-up methods and controlled changes are given
in Sections~\ref{sec:method-plan-validation} and~\ref{sec:disc-plan-gap}.''')
Path('/workspace/tooling/apec-style-edit/methods-results-changed.txt').open('a').write('\n'.join(str(p) for p in changed)+'\n')
