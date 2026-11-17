from pathlib import Path
root=Path('/workspace/thesis/Chapters')
changed=[]
def replace(folder,name,old,new):
 p=root/folder/(name+'.tex');raw=p.read_bytes();crlf=b'\r\n' in raw;s=raw.decode().replace('\r\n','\n')
 assert old in s,(name,old[:60]);s=s.replace(old,new,1);p.write_bytes(s.replace('\n','\r\n').encode() if crlf else s.encode())
 if p not in changed:changed.append(p)
M='09_Experimental_Methods';R='10_Results'
replace(M,'12_Revised_Plan_Validation',r'''The next test campaign must establish a repeatable V2 baseline, identify the
cause of the power gap, and allow a fair V3 comparison \cite{projectOctoberPlan}. The
remaining tests are described below.
Section~\ref{sec:revised-plan-criteria} defines AP-01--AP-08, and
Section~\ref{sec:res-revised-plan} shows which results are currently available.''',r'''The remaining campaign targets a repeatable V2 baseline, power-limit diagnosis,
and a matched V3 comparison \cite{projectOctoberPlan}. AP-01--AP-08 are defined
in Section~\ref{sec:revised-plan-criteria}; current results are summarized in
Section~\ref{sec:res-revised-plan}.''')
replace(M,'12_Revised_Plan_Validation',r'''Testing would begin with the approximately \SI{85}{\watt} V2 point reported
in the plan. A repeat needs the actual board, fitted parts and rework,
magnetics, resonant values, controller target, firmware source/version, saved
settings, and live mode. The record for a software-controlled run should
include the version, status, and validated configuration export. Successful compilation checks that the software can be built; a powered
baseline test is still required.

The setup record needs the AC input, output setting, negotiated PDO or APDO,
load and cable, auxiliary supplies, cooling arrangement, ambient temperature,
and duration. Voltage/current scaling and probe zero would be checked before
comparison. If the earlier \SI{85}{\watt} setup cannot be reconstructed, a new repeatable
baseline should be reported, together with the known differences from the
earlier setup.

Real AC input power and power quality come from the identified analyzer;
external connector voltage and load current give output power. The saved
setup needs instrument ranges and accuracy information, probe positions,
bandwidth, averaging intervals, and oscilloscope timing. Temperature records
need the observed surface, emissivity or contact-sensor method, and cooling
conditions. Protocol tests also need the advertised source capability and
the settings requested and accepted by the sink.''',r'''The reported approximately \SI{85}{\watt} V2 point must be repeated with
identified hardware, rework, magnetics, resonant values, controller target,
firmware source, saved settings, and live mode. Version, status, and validated
configuration exports are required; a successful build does not verify powered
operation.

The baseline record must identify AC input, output setting and negotiation,
load/cable, auxiliary supplies, cooling, ambient, and duration. Probe scaling
and zero must be checked. If the original \SI{85}{\watt} configuration cannot
be reconstructed, a new baseline must state the known differences.

The measurement record must include analyzer identity, ranges and accuracy,
probe positions, bandwidth, averaging and timing, and thermal sensing method.
Protocol tests must identify advertised capabilities and requested/accepted
sink settings.''')
replace(M,'12_Revised_Plan_Validation',r'''Input and output power must cover the same steady interval. Real AC input
power, connector voltage, and load current would be recorded together and
used in the calculation in Section~\ref{sec:method-efficiency}. Secondary
bulk and connector VBUS are separate nodes. PA2 and the firmware
voltage--current product describe control behavior. Output power still needs
external connector measurements.

Auxiliary power must be included in the same accounting. Internally supplied
control and driver power is already included at the AC input. The measured
power from any external supply must also be included in the stated total.
Any exclusion must be stated before comparison with a complete supply.

Instrument ranges, probe scaling, calibration information, and the method in
Section~\ref{sec:method-uncertainty} determine the uncertainty. Separate averaging windows, a changing load, or unmeasured auxiliary power
can make the input and output readings unsuitable for an efficiency
calculation.

Before a continuous-power test, the test sheet needs a duration, a criterion
for thermal stability, and stop limits. The record also needs the initial
condition, elapsed time, ambient temperature, airflow or fan setting,
orientation, heat sinks, and temperature history. The exact duration and numeric limits must be specified when the revised
plan is turned into a bench test. One
electrical capture and one thermal image cannot establish that history.''',r'''Real AC input power, external connector voltage, and load current must be
measured over the same steady interval for the calculation in
Section~\ref{sec:method-efficiency}. Secondary-bulk measurements and the
primary-current input PA2 describe upstream control rather than connector
output power. The boundary must include internally supplied auxiliaries and
measured external supply power, with any exclusions stated.

Instrument ranges, scaling, calibration, and the propagation method in
Section~\ref{sec:method-uncertainty} define the uncertainty. Unmatched
averaging windows, changing load, or omitted auxiliary power invalidate a
matched efficiency estimate.

Continuous-power tests require a specified duration, thermal-stability
criterion, and numerical stop limits. Initial condition, elapsed time,
ambient, airflow, orientation, heat sinks, and temperature histories must be
recorded; isolated electrical and thermal captures are insufficient.''')
replace(M,'12_Revised_Plan_Validation',r'''Table~\ref{tab:method-revised-load-sequence} gives the planned load sequence.
The selected PDO/APDO, cable, connector, load, and converter ratings determine
which points can actually be applied. A target requiring too much current
at the selected voltage must be omitted or tested with a suitable supported
configuration.''',r'''The planned sequence in Table~\ref{tab:method-revised-load-sequence} is limited
by the selected PDO/APDO and cable, connector, load, and converter ratings.
Unsupported voltage/current combinations must be omitted or reconfigured.''')
replace(M,'12_Revised_Plan_Validation',r'''Before increasing power, numeric stop limits would be set from component
ratings, expected waveforms, sensing range, and thermal assumptions. The run
must stop at a limit, loss of regulation or feedback, an unexplained protection
event, or abnormal switching. The stopping condition and raw trace must be
saved. Surface and junction limits must remain distinct.

One controlled item should be changed per retest, with the rest of the setup
kept the same. The change log needs the exact part or setting, reason, expected
effect, and before/after files. Candidate changes in the plan include sensing
calibration, control limits, switching timing, resonant and charge-pump values,
gate behavior, conduction paths, rectification, and local cooling.
For a calibration change, both scales and the raw readings are needed to
distinguish a corrected display from an electrical improvement.''',r'''Stop limits must follow component ratings, expected stress, sensing range,
and thermal assumptions, with surface and junction limits treated separately.
Limit crossings, loss of regulation/feedback, unexplained protection, or
abnormal switching require termination and a saved event trace.

Controlled retests must change one item while retaining the remaining setup.
The log must identify the part or setting, rationale, expected effect, and
before/after records. Candidates include sensing calibration, control limits,
switching timing, resonant and charge-pump values, gate behavior, conduction
paths, rectification, and cooling. Calibration changes require raw readings
and both scales to separate display correction from electrical improvement.''')
replace(M,'12_Revised_Plan_Validation',r'''For each supported fixed PDO, the advertised capability, negotiated
voltage/current, regulation, applicable load range, and attach and detach
behavior would be recorded. PPS testing applies only when the actual source
advertises an APDO. It needs requested and accepted settings, measured
connector output, transitions, and supported-limit behavior. Fixed-voltage
captures do not replace that protocol sequence.

Dynamic tests need startup, shutdown, load steps and removal, no-load
recovery, and mode changes. Connector VBUS, the relevant bulk/control
signals, and the load event need a shared time reference. For protection,
the test must define the trigger, applied condition, observed response, and
recovery within the approved bench limits. Fault-injection results cannot
be inferred from ordinary operation.

At the final accepted power, the remaining measurements are efficiency,
PF/THD, ripple, transients, component stress, and extended thermal stability.
The run record should include drift, protection events, interruptions, and
cooldown/restart behavior. Completing that duration establishes behavior
under those conditions; lifetime reliability needs a broader assessment.''',r'''Fixed-PDO tests must record advertised and negotiated voltage/current,
regulation, load range, and attach/detach behavior. PPS tests require an
advertised APDO, requested/accepted settings, measured connector output,
transitions, and limit behavior; fixed-voltage records do not verify PPS.

Startup, shutdown, load steps/removal, no-load recovery, and mode transitions
require synchronized connector VBUS, relevant bulk/control signals, and event
markers. Protection tests must define the applied fault, trigger, response,
and recovery within the bench limits.

At the final accepted power, efficiency, PF/THD, ripple, transients, stress,
and extended thermal stability must be assessed. Drift, protection,
interruptions, and cooldown/restart behavior belong in the run record.
A defined-duration result applies to those conditions rather than lifetime
reliability.''')
replace(M,'12_Revised_Plan_Validation',r'''The envelope includes installed parts on both PCB sides, required
daughterboards and connectors, and onboard heat sinks. The same axes must be
used for both assemblies, with the treatment of any enclosure, external
cooling, or support hardware stated. Bench probes and instruments are excluded
in both cases. Hardware required for operation must still be included if it is moved
off-board.

The continuous output power in the numerator must be verified externally,
with its duration, ambient, airflow, input, output setting, and thermal condition. Density
should be reported alongside efficiency, temperature, and remaining margin.
Using nominal \SI{100}{\watt} for one board and a short measured peak for
the other would defeat the comparison required by AP-07.''',r'''The envelope includes both PCB sides, required daughterboards/connectors,
heat sinks, and functional hardware moved off-board. Both assemblies must
use the same axes and treatment of enclosure, cooling, and supports; bench
instrumentation is excluded.

The numerator requires externally verified continuous output under stated
duration, ambient, airflow, input, output setting, and thermal conditions.
Density must be reported with efficiency, temperature, and margin. A nominal
\SI{100}{\watt} rating and a short measured peak are not comparable under AP-07.''')
replace(M,'12_Revised_Plan_Validation',r'''The approximately \SI{8}{\percent} net reduction described for the slimmed
V3 layout is a design-volume estimate. The USB-PD section was removed, so
that estimate does not compare two complete supplies with the same output
function. Any external regulator, PD controller, connector, and necessary
cooling would need to be included in the system volume.

Verified assembled dimensions and matched continuous-power runs are still
needed for both boards, so there is no V2/V3 density result yet. If V3 does
not pass readiness, AP-08 calls for the completed V2 tests as the final
hardware results and a clear statement of the V3 work remaining.''',r'''The approximately \SI{8}{\percent} V3 reduction is a design-volume estimate
with USB-PD omitted, not a complete-supply comparison. External regulation,
PD control, connectors, and required cooling must enter the system volume.
Verified dimensions and matched continuous-power tests remain unavailable,
so no V2/V3 density result is reported. AP-08 specifies completed V2 testing
as the fallback if V3 is not ready.''')
Path('/workspace/tooling/apec-style-edit/methods-results-changed.txt').open('a').write('\n'.join(str(p) for p in changed)+'\n')
