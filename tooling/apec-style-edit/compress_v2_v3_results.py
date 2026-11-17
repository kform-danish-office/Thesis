from pathlib import Path
root=Path('/workspace/thesis/Chapters/10_Results');changed=[]
def rep(name,old,new):
 p=root/(name+'.tex');raw=p.read_bytes();crlf=b'\r\n' in raw;s=raw.decode().replace('\r\n','\n')
 assert old in s,(name,old[:60]);s=s.replace(old,new,1);p.write_bytes(s.replace('\n','\r\n').encode() if crlf else s.encode())
 if p not in changed:changed.append(p)
rep('15_V2_Testing_Update',r'''The V2 prototype was first tested with the original resonant tank.
Excessive heating was observed in the external series inductor,
which was reported as approximately \SI{9.4}{\micro\henry}.
The tank was then modified to use only the transformer leakage
inductance. The external inductor was removed, and the resonant
capacitance was changed to approximately \SI{1.66}{\nano\farad}.
The prototype was operated with the modified tank. Removing the inductor
eliminated one source of heating, but the overall reduction in losses has
not yet been measured using matched input and output power readings.

The supplied leakage measurements in
Table~\ref{tab:mag-inherited-measurements} give an ideal series resonance
near \SI{0.96}{\mega\hertz} with this capacitance. This is a calculation
based on the supplied component values. The resonant frequency of the
installed V2 tank has not been measured. The fitted transformer and
switching waveforms under load still need to be recorded.''',r'''The original V2 tank showed excessive heating in the approximately
\SI{9.4}{\micro\henry} external series inductor. The inductor was removed
and the resonant capacitance changed to approximately
\SI{1.66}{\nano\farad}, allowing operation with transformer leakage alone.
This removed the hot component; total loss reduction remains unquantified
without matched input/output power measurements.

The inherited leakage values in Table~\ref{tab:mag-inherited-measurements}
give an ideal series resonance near \SI{0.96}{\mega\hertz}. Installed V2
resonance was not measured, and the fitted transformer and loaded switching
waveforms remain to be identified.''')
rep('15_V2_Testing_Update',r'''The software dead-time setting was reported as approximately
\SI{60}{\nano\second}. Lower half-bridge heating was observed after the
tank and timing changes. This was taken as an indication of ZVS, but
lower temperature alone is not enough to confirm it. Synchronized
switch-voltage and current waveforms are still needed. The firmware
version, timing readback, and effective dead time at the switches were not
recorded during these tests. The nominal timing in the archived controller
source is described separately
in Section~\ref{sec:hw-v2}.''',r'''The reported software dead-time setting was approximately
\SI{60}{\nano\second}. Half-bridge heating decreased after the tank and
timing changes, but this observation does not verify ZVS. Synchronized
switch-voltage, gate-command, and current captures are required. Firmware
identity, timing readback, and effective switch dead time were not recorded;
archived-source timing is described in Section~\ref{sec:hw-v2}.''')
rep('15_V2_Testing_Update',r'''Secondary-winding heating was encountered during prototype development.
The operating region associated with the highest available power was
observed around \SIrange{3.3}{3.6}{\ampere} at the secondary output.
Increasing the load further did not give the expected increase in power.
The corresponding voltage would be needed to express this current range
as a separate power result. It is not used to replace the matched
connector voltage/current measurements from the earlier campaign.

The transformer secondary was suspected as a limitation, but its winding
loss was not measured separately from interconnect, rectifier, resonant,
or control effects. V2 gave broadly comparable bench performance to V1.
With the modified V2 tank, the input section became the dominant heating
concern. This qualitative comparison does not establish identical
efficiency or temperature at matched operating points.''',r'''Secondary-winding heating and limited power increase were observed near
\SIrange{3.3}{3.6}{\ampere} at the secondary output. No corresponding
voltage was retained, so this range is not converted into a power result
or substituted for the earlier matched connector measurements.

The secondary winding was suspected as a limit, without separate loss
measurements to distinguish magnetic, interconnect, rectifier, resonant,
and control effects. V2 performance was qualitatively comparable to V1,
while the modified tank shifted the main heating concern to the input
section. Matched efficiency and temperature equivalence was not established.''')
rep('15_V2_Testing_Update',r'''The input full-bridge rectifier, D4, D5, D9, and D10, continued to heat up.
The diodes were replaced, but the heating remained. The fitted devices
were reported as SiC rectifiers. The original and replacement part numbers
still need to be recorded.''',r'''Heating persisted around input-bridge diodes D4, D5, D9, and D10 after
diode replacement. The devices were reported as SiC rectifiers; original
and replacement part numbers were not recorded.''')
rep('15_V2_Testing_Update',r'''An earlier load test was reported at \SI{240}{\volt} AC,
\SI{50}{\hertz}, with a \SI{100}{\watt} constant-power load setting.
Output voltage was reported to remain steady while bridge temperature
continued to rise. The surface temperature was reported to reach about
\SI{80}{\celsius} within a few seconds, then rise more slowly toward
\SI{90}{\celsius}, when the test was stopped. The load setting is not a
measurement of delivered power and does not establish a continuous rating.

The thermal image in Figure~\ref{fig:v2-bridge-thermal-observation}
was taken during a reported \SI{95}{\watt} run. It was
not specified whether this was a load setting or a measured output.
The earlier \SI{100}{\watt} load setting and temperature rise were
reported separately. It has not been confirmed whether they refer to the
same run as this image.''',r'''At \SI{240}{\volt} AC, \SI{50}{\hertz}, and a \SI{100}{\watt}
constant-power load setting, output voltage remained steady while bridge
surface temperature rose to approximately \SI{80}{\celsius} within seconds,
then more slowly toward \SI{90}{\celsius}, where testing was stopped.
The setpoint does not establish delivered power or continuous capability.

Figure~\ref{fig:v2-bridge-thermal-observation} is from a reported
\SI{95}{\watt} run, without identification as setpoint or measured output.
Its relationship to the separately reported \SI{100}{\watt} test and
temperature history is unconfirmed.''')
rep('15_V2_Testing_Update',r'''Insufficient copper around the input bridge was suspected as a cause of
the heating. A connection concentrated through a single via was also
suspected in this area. A large copper pour cannot remove a bottleneck if
the current still passes through one restricted interlayer connection.
Narrow traces and vias can add resistive loss, while limited copper area
reduces heat spreading from the diode pads. The fitted current path and
its voltage drop still need to be checked before this explanation can be
confirmed. Replacing the diodes did not resolve the problem.''',r'''Limited bridge copper and a possible single-via interlayer bottleneck were
suspected. Either could increase resistive heating or restrict heat spreading,
but the fitted path and voltage drop were not measured. Persistence after
diode replacement leaves the loss mechanism unresolved.''')
rep('15_V2_Testing_Update',r'''Wider current paths and more copper for heat spreading are planned for the
next layout. Moving the rectifier diodes to another side of the board is
also being considered. Their effect on temperature still needs to
be measured under the same test conditions.

V2 was operated successfully with the leakage-only resonant tank, but
continued heating of the input bridge remains unresolved. Temperature
measurements over a defined test duration, matched input and output power
readings, and switching waveforms are still needed to confirm the loss
reduction, ZVS, and continuous output capability.''',r'''The next layout will widen current paths and increase heat-spreading copper;
rectifier relocation is also under consideration. Matched tests are required
to assess these changes. V2 operation with the leakage-only tank was achieved,
but bridge heating, total loss reduction, ZVS, and continuous capability
remain to be resolved through synchronized electrical and thermal tests.''')
rep('16_V3_Design_Outcome',r'''The V3 edge-card layout was reduced by removing the USB-PD output section
and retaining the secondary rectifiers. The estimated net volume reduction
was approximately \SI{8}{\percent}. This is a design estimate for the
slimmed converter arrangement. It is not a measured power-density result
for a complete USB-C supply, because external regulation and USB-PD
functions would still be required.

A replacement planar-magnetic set was not installed within the project
time. Further reduction and higher sustained output were therefore not
demonstrated. The outcome is a smaller layout concept and a clearer set
of thermal and magnetic questions for the next prototype.''',r'''Removing the USB-PD section while retaining secondary rectification gave
the V3 edge-card layout an estimated net volume reduction of approximately
\SI{8}{\percent}. This reduced-function estimate is not a complete USB-C
power-density result; external regulation and USB-PD remain necessary.
Replacement planar magnetics were not installed within the project, so
further reduction and higher sustained output were not demonstrated.''')
rep('16_V3_Design_Outcome',r'''The revisions show that changing the position of a hotspot is not by
itself a measured reduction in total loss. The available power and
component temperatures need to be compared together. The winding and
input-path observations guide the next measurements, while the V3 layout
shows what can be removed or rearranged before a new magnetic design is
installed. A complete V2--V3 comparison must include every output stage
needed to provide the same function, as defined in \cref{sec:method-density}.''',r'''The winding and input-path observations identify priorities for the next
prototype, but hotspot relocation does not quantify total loss reduction.
A V2--V3 comparison must match continuous power and thermal conditions and
include all output hardware required for the same function, following
\cref{sec:method-density}.''')
Path('/workspace/tooling/apec-style-edit/methods-results-changed.txt').open('a').write('\n'.join(str(p) for p in changed)+'\n')
