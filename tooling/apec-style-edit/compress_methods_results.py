from pathlib import Path
root=Path('/workspace/thesis/Chapters')
changed=[]
def replace(folder,name,old,new):
 p=root/folder/(name+'.tex')
 raw=p.read_bytes(); crlf=b'\r\n' in raw
 s=raw.decode().replace('\r\n','\n')
 assert old in s, (name,old[:70])
 s=s.replace(old,new,1)
 p.write_bytes(s.replace('\n','\r\n').encode() if crlf else s.encode())
 if p not in changed: changed.append(p)
M='09_Experimental_Methods'
R='10_Results'
replace(M,'01_Objectives',r'''The assembled converter was first tested to check whether the selected output
voltage could be maintained as load increased. Startup, load removal, and
no-load operation were then examined, since energy transfer must also be
controlled when there is no steady load to absorb it. Input power quality,
efficiency, switching waveforms, and temperature were assessed to identify
losses and guide further design changes.''',r'''The test campaign assessed loaded regulation, startup, load removal, and
no-load energy control. Input power quality, efficiency, switching waveforms,
and surface temperatures were measured to identify operating limits and
priorities for the next revision.''')
replace(M,'01_Objectives',r'''active version, mode, calibration, and thresholds. These settings matter when
tests are compared because they can change the burst pattern.''',r'''active version, mode, calibration, and thresholds for comparisons of burst
operation.''')
replace(M,'02_Safety_Arrangements',r'''The tests were run with a controlled source, current limiting during bring-up,
rated probes, physical separation from the exposed board, and an external
input-power disconnect. Operating conditions could then be changed without
reaching into an energized circuit.

With PA10 inhibited, the hardware, source setting, load, and probe references
were checked. The UART and oscilloscope were set up before the board was
energized so that startup could be observed without moving live connections.

Both differential and common-mode voltage had to remain within the probe
ratings. A grounded passive-probe clip could not be connected to an
AC-line-referenced node. Source isolation did not remove the need to check
the references shared by the circuit and instruments.

For shutdown, input power and the enable command were removed. The charge
remaining in the DC link and output capacitors was then checked before the
board was handled. With PA10 low, commanded transfer stops, but stored charge remains until the
capacitors discharge through an available path. The external source
disconnect provided an emergency stop independent of UART communication.''',r'''Bring-up used a controlled, current-limited source, rated probes, separation
from exposed conductors, and an external input disconnect. Hardware, source,
load, and probe references were checked with the burst-enable output PA10
inhibited; UART and oscilloscope connections were completed before energizing.
Probe differential and common-mode ratings were observed, and grounded
passive-probe clips were excluded from line-referenced nodes. Source isolation
did not remove shared-reference constraints.

Shutdown removed input power and the enable command. Residual DC-link and
output-capacitor voltages were checked before handling. PA10 inhibition stops
commanded transfer but does not discharge stored energy. The external
disconnect provided an emergency stop independent of UART communication.''')
replace(M,'03_Test_Bench',r'''and collect its diagnostic output. The applied load was therefore set independently of the operating state
estimated by the controller.''',r'''and collect diagnostics. Load demand was set independently of the controller's
load estimate.''')
replace(M,'03_Test_Bench',r'''Where practical, input power was measured at the DUT terminals to include
internally supplied auxiliary power. On the output side, the secondary bulk bus, connector VBUS, and load sense
point are separate measurement locations. The measurement
location is stated with each result because a reading beyond the cable
includes its voltage drop and loss.''',r'''Where practical, input power was measured at the DUT terminals, including
internally supplied auxiliaries. Output results identify the secondary-bulk,
connector-VBUS, or load-sense location; measurements beyond the cable include
its voltage drop and loss.''')
replace(M,'04_Instrumentation',r'''Delivered voltage, current, and power were assessed with external instruments.
The controller's converted sensor readings and serial status messages were
used to check sensing and commands. These ADC readings and UART messages
were not treated as independent measurements of connector output.''',r'''External instruments measured delivered voltage, current, and power.
Controller ADC and UART data were used for sensing and command diagnostics,
rather than independent connector-output measurements.''')
replace(M,'04_Instrumentation',r'''In Table~\ref{tab:channel-definitions}, CH1--CH4 identify oscilloscope input
channels. These labels belong to the measuring instrument; they are not
MCU port names or physical chip-pin numbers.''',r'''In Table~\ref{tab:channel-definitions}, CH1--CH4 denote oscilloscope channels,
independent of MCU port or package-pin identifiers.''')
replace(M,'04_Instrumentation',r'''The capture and test notes give node names, attenuation, range, coupling,
bandwidth, trigger, and timebase where available. These settings are needed
to interpret a channel; its color or number alone does not identify the signal
or its scale.''',r'''Capture-specific node assignments, attenuation, range, coupling, bandwidth,
trigger, and timebase take precedence over channel color or number.''')
replace(M,'05_Probing',r'''Fast GaN edges make the physical probe connection part of the measurement.
Short connections to the local return reduce pickup and added loop inductance.
Gate-source voltage must be referenced to that transistor's source, while a
primary switch-node probe must tolerate the full common-mode voltage.

The current probe was zeroed and its polarity noted before measurement.
Voltage and current channels also need deskew before their relative timing
can be used to calculate switching energy or power. The CP2100A bandwidth is
\SI{800}{\kilo\hertz}, below the nominal \SI{1}{\mega\hertz} carrier. It
can measure input-current behavior but cannot resolve the full fast
resonant-current transition.''',r'''Short local-return connections limited probe pickup and loop inductance.
Gate-source measurements require a source-referenced probe; switch-node
measurements require the full primary common-mode rating. Current-probe zero
and polarity were checked before acquisition. Voltage/current deskew is
required for switching-energy calculations. The CP2100A bandwidth of
\SI{800}{\kilo\hertz} is below the nominal \SI{1}{\mega\hertz} carrier,
limiting its use to input-current behavior rather than fast resonant-current
transitions.''')
replace(M,'05_Probing',r'''The MCU burst-enable output PA10 on the original prototype marks the interval in which switching
cycles are allowed. An individual transistor turns on within
that envelope, so the enable or switch-node trace alone cannot locate the ZVS
measurement instant.''',r'''The original prototype's burst-enable output PA10 marks the switching envelope,
not individual gate transitions. Enable and switch-node traces alone therefore
do not locate the ZVS measurement instant.''')
replace(M,'06_Test_Matrix',r'''Bring-up was followed by tests under load and at no load. Each stage addressed
a practical question: whether the circuit switched, whether the selected
output was delivered, and how operation changed with demand. The numerical
data for the results and plots came from workbook rows and instrument captures.''',r'''Bring-up established switching and power transfer, followed by loaded and
no-load characterization. Workbook rows and instrument captures supplied the
numerical results and plots.''')
replace(M,'06_Test_Matrix',r'''The test records include workbook entries, screenshots, waveform files,
firmware, and photographs. Numerical exports are used where available at
their original precision. Missing setup details or peak markers limit the
calculations possible from some captures; \cref{sec:method-uncertainty}
explains these limits.

The graphs were rebuilt from the measured points. Connecting lines indicate
the trend between tested loads; no intermediate measurements or fitted
converter model are implied.''',r'''Workbook entries, screenshots, waveform exports, firmware, and photographs
were retained. Numerical exports preserve their original precision; missing
setup details and peak markers limit derived quantities as discussed in
\cref{sec:method-uncertainty}. Plot lines connect measured points without
implying intermediate measurements or a fitted converter model.''')
replace(M,'07_Control_Tests',r'''During the final baseline-control tests, the conditioned secondary-bulk-voltage signal
at input PA1 was read continuously by the analog-to-digital converter
(ADC). Direct memory access (DMA) copied those readings to memory without
making the controller wait for each conversion. The burst-enable output
PA10 set the intervals in which switching cycles were allowed. Where
available, settings saved through the UART serial link were used to
interpret the response instead of source-code defaults.

Under load, delivered voltage and the burst pattern were checked at a fixed
output setting. The saved measurements begin after startup. To assess startup and shutdown, the initial output and load condition,
precharge, output rise, peak voltage, PA10 transitions, inhibition, output
decay, and any fault still need to be recorded on a shared time base.

For load removal, output voltage and switching activity were examined around
disconnection. A follow-up capture needs to span both the immediate rise from
stored energy and the later no-load cycling. The active threshold, latch state, and recovery action also need to be
recorded so that normal holdoff can be distinguished from a hard fault when
the burst-enable signal at PA10 is low.''',r'''The final baseline controller acquired secondary-bulk voltage at PA1 through
continuous ADC DMA and controlled switching intervals through burst-enable
output PA10. Saved UART settings, where available, identified the active
configuration rather than source-code defaults.

Loaded tests checked delivered voltage and burst structure at a fixed output
setting. The records begin after startup; synchronized initial conditions,
precharge, output rise/peak, PA10, inhibition, decay, and fault status remain
necessary to quantify startup and shutdown.

Load-removal captures covered output voltage and switching around disconnection.
A complete assessment requires both the immediate stored-energy response and
later no-load cycling, with thresholds, latch state, and recovery recorded to
distinguish holdoff from a latched fault.''')
replace(M,'08_Power_Quality',r'''Input-current shaping was checked alongside output regulation because burst
operation changes when energy is drawn from the line. With the
SDS824X HD, DP10013, and CP2100A, RMS voltage, RMS current, real input power,
true power factor, and input-current THD were measured:''',r'''Input-current shaping under burst control was assessed using the SDS824X HD,
DP10013, and CP2100A. The recorded quantities were RMS voltage/current, real
input power, true power factor, and input-current THD:''')
replace(M,'08_Power_Quality',r'''A representative steady-state reading must cover several AC line cycles
and enough burst activity within the integration window. Startup and load transitions are
excluded when steady-state readings are interpreted. Source isolation and any input-path
current limiting remain part of the stated setup.

True PF includes displacement and distortion, so a current waveform that
looks sinusoidal is not enough to assess it. PF, the current waveform, and THD are therefore compared at the same
operating condition. Harmonics-standard qualification would also
require selecting the applicable equipment class and following its test
procedure; that was outside this campaign.''',r'''Steady-state integration must cover several line cycles and representative
burst activity, excluding startup and load transitions. Source isolation and
input current limiting remain part of the test configuration. PF, current
waveform, and THD were compared at the same operating condition; no
harmonics-standard qualification was performed.''')
replace(M,'09_Efficiency',r'''A steady output voltage does not show how much input power is needed.
System efficiency is calculated from real AC input power and DC power
at the stated output measurement point:''',r'''System efficiency was calculated from real AC input power and DC power at the
stated output measurement point:''')
replace(M,'09_Efficiency',r'''Input and output entries are paired at the same operating condition. A DUT
input measurement includes internally supplied auxiliary circuits. The output
sense point determines whether cable loss is included. That loss can only be
subtracted if the voltage drop has been measured.

A synchronized, repeated efficiency sweep with a complete uncertainty budget
was not performed at every setting and load. The paired calculations in
Chapter~\ref{ch:results} therefore give initial estimates, with the source
readings identified. Unmatched input and output observations are excluded.''',r'''Paired entries use the same operating condition. DUT input measurements include
internal auxiliaries; the stated output sense point determines cable-loss
inclusion. No cable-loss correction was made without a measured voltage drop.
The results in Chapter~\ref{ch:results} are initial estimates because a
synchronized, repeated sweep with a complete uncertainty budget was not
available at every point. Unmatched observations were excluded.''')
replace(M,'10_Thermal',r'''Thermal images were taken to locate heating as load increased. The stated
voltage and current were recorded with each image, along with maximum, cursor,
and reference-marker temperatures. The emissivity setting was 0.95.

The camera measures visible surface temperature. Viewing angle, emissivity,
reflections, focus, and component visibility affect the apparent hotspot.
It cannot directly give semiconductor junction temperature or separate
copper, winding, and core losses.

The images indicate where temperatures should be monitored in further
tests.
The high-power captures lack complete records of ambient conditions, airflow,
warm-up duration, camera setup, and thermal steady state. An instrumented run
is still needed before a continuous thermal power rating can be assigned.''',r'''Thermal images recorded labeled voltage/current conditions and maximum,
cursor, and reference-marker temperatures at emissivity 0.95. The images
locate apparent surface hotspots; viewing angle, reflections, focus, and
component visibility affect the readings. Junction temperature and individual
copper, winding, and core losses cannot be extracted.

Incomplete ambient, airflow, warm-up, and camera-setup records prevent a
thermal steady-state assessment. The images guide instrumented monitoring
but do not establish a continuous power rating.''')
replace(M,'11_Uncertainty',r'''A difference between tests may come from the measurement itself. Instrument
accuracy, probe attenuation and zero, voltage/current phase error, channel
timing, output sense-point placement, cable drop, emissivity, and repeatability
must be considered before that difference is interpreted. ADC scaling and
controller thresholds can also change the bursts and operating point.''',r'''Relevant uncertainties include instrument accuracy, probe attenuation and
zero, voltage/current phase error, channel timing, output sense location,
cable drop, emissivity, and repeatability. ADC scaling and thresholds can
also shift burst operation and the operating point.''')
replace(M,'11_Uncertainty',r'''The setup records and repeat measurements are insufficient for a complete
numerical uncertainty budget at every point. The original workbook precision is preserved so the calculations can be
reproduced. The last displayed digits should not be interpreted as measured
accuracy, and error bars are not added without sufficient uncertainty data.

A single screenshot records one event. Worst-case transient behavior must
be assessed from repeated events against a defined acceptance band. Thermal
equilibrium requires a temperature history, while timing jitter must be
measured rather than inferred from a firmware setting. These limits are
applied to the results in Chapter~\ref{ch:results}.''',r'''Incomplete setup records and repeat measurements prevent a numerical
uncertainty budget at every point. Workbook precision is preserved for
reproducibility rather than claimed accuracy; unsupported error bars are
omitted. Worst-case transients require repeated events and a defined
acceptance band, thermal equilibrium requires a temperature history, and
jitter requires measured timing. These limits apply throughout
Chapter~\ref{ch:results}.''')
# Record the changed paths for the later reporting pass.
Path('/workspace/tooling/apec-style-edit/methods-results-changed.txt').write_text('\n'.join(str(p) for p in changed)+'\n')
