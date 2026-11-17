from pathlib import Path
r=Path('/workspace/thesis')
def replace(name,a,b):
 p=r/name;raw=p.read_bytes();x=a.encode();y=b.encode()
 if x not in raw:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
 elif b'\n' not in x and b'\r\n' in raw:y=y.replace(b'\n',b'\r\n')
 assert raw.count(x)==1,(name,a[:110],raw.count(x));p.write_bytes(raw.replace(x,y))
def paragraph(name,starts,new):
 s=(r/name).read_text();old=next(x for x in s.split('\n\n') if x.startswith(starts));replace(name,old,new)
def append(name,new):
 p=r/name;b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';p.write_bytes(b.rstrip()+nl+nl+new.replace('\r\n','\n').replace('\n',nl.decode()).encode()+nl)

paragraph('Frontmatter/Abstract.tex','Development continued with V2,',r'''Development continued with an F410-based V2 board integrating the controller, GaN stage, isolated feedback, and USB-C circuit on a four-layer PCB. Lower half-bridge heating was observed after the tank and timing changes, but input-bridge heating remained unresolved (\cref{sec:res-v2-testing}). Bench performance was broadly comparable to the first prototype. Secondary-winding loss and a restricted input current path were suspected limitations, but neither was isolated quantitatively.

A slimmer V3 edge-card design was prepared without the USB-PD output section, leaving secondary rectification. Its estimated net volume reduction was about \SI{8}{\percent}. New planar magnetics were not installed within the available time, so higher sustained power was not demonstrated. A complete USB-C supply would also require an external regulated USB-PD stage.''')
replace('Frontmatter/Abstract.tex','The next step is to identify what limits sustained output, measure the effect of each controlled change, and use those findings to guide V3.',r'The next work is to resolve the magnetic and current-path limits, then evaluate the complete V3 arrangement. Operation toward \SI{240}{\watt} USB-PD Extended Power Range (EPR) remains a longer-term goal.')
paragraph('Frontmatter/Approval.tex','The next stage is set out',r'''The work progressed from converter bring-up and G071 control to the integrated F410 V2 board and a reduced V3 edge-card layout. Secondary-winding heating and the later input-bridge hotspot guided the remaining magnetic and layout work. The V3 USB-PD section was removed to reduce volume, but new magnetics were not installed within the project time. Appendix~\ref{app:revised-plan} links the original milestones to the design, test results, and work still needed.''')
replace('Frontmatter/Approval.tex','The new schematic and PCB print set are included','The schematic and PCB print set are included')

paragraph('Chapters/01_Introduction/chapter.tex','The starting point was',r'''The starting point was a DTU charge-pump converter and supplied planar magnetics. The hardware and controller were developed around those parts for a USB-C laboratory supply. V1 was used for bring-up and G071 controller development. The control and interface functions were then integrated into the F410-based V2 board. Tank and timing changes reduced some local heating, but did not establish a higher sustained power capability. Those findings led to a slimmer V3 edge-card design and further work on the magnetic and thermal limits.''')
append('Chapters/01_Introduction/03_Aim_Objectives.tex',r'''A reduced V3 layout was prepared from these findings. The USB-PD section was removed from the converter card to reduce volume, while the secondary rectifiers were retained. Installation of new planar magnetics and matched V3 tests remained unfinished. The design outcome is described in \cref{sec:hw-v3-plan,sec:res-v3-design}.''')
replace('Chapters/01_Introduction/05_Contributions_Attribution.tex','The complete converter was developed from these supplied designs; the conversion principle and magnetics were not redesigned.','The operating prototypes were developed from these supplied designs. Their conversion principle and fitted magnetic assemblies came from the earlier work; a replacement planar-magnetic set was not installed.')
replace('Chapters/01_Introduction/05_Contributions_Attribution.tex','The new schematic and PCB documentation are included','The schematic and PCB documentation are included')
append('Chapters/01_Introduction/05_Contributions_Attribution.tex',r'''The V3 contribution was a slimmed edge-card layout with the USB-PD output section removed and secondary rectification retained. The resulting volume reduction was estimated at the design stage. Further magnetic optimization was identified, but no new magnetic set was installed or validated within the project.''')
replace('Chapters/01_Introduction/06_Scope_Limitations.tex','The thesis covers the development from the first open-frame laboratory prototype to the integrated V2 board.','The thesis covers development from the first open-frame laboratory prototype through the integrated V2 board and the reduced V3 edge-card design.')
replace('Chapters/01_Introduction/06_Scope_Limitations.tex','Section~\\ref{sec:revised-plan-criteria} also tracks the planned V3 edge-card design, its release checks, and the matched V2--V3 comparison.',r'Section~\ref{sec:revised-plan-criteria} also tracks the V3 layout work, its remaining release checks, and the matched V2--V3 comparison.')
replace('Chapters/01_Introduction/07_Thesis_Structure.tex','how the hardware developed from the first prototype to V2.','how the hardware developed from the first prototype through V2 and the reduced V3 layout.')

# Keep the original plan requirements, while bringing the completion narrative up to date.
paragraph('Chapters/03_Requirements_Architecture/09_Revised_Plan_Criteria.tex','The schedule sets V2 testing',r'''The completed work includes the measured first-prototype baseline, integrated V2 circuit and firmware, powered tank changes, and a reduced V3 layout. Replacement planar magnetics were not installed. A matched repeat near \SI{85}{\watt}, the full PPS and extended-load tests, a completed V3 readiness decision, and the paired full-system density comparison remain open. Chapter~\ref{ch:results} presents the measurements and design estimate; Chapters~\ref{ch:discussion} and \ref{ch:conclusion} connect them to the next steps.''')
append('Chapters/06_Magnetics_Integration/11_Limitations.tex',r'''Secondary-winding heating and limited power increase at higher load made transformer optimization a priority for the later revisions. The operating prototypes retained the inherited magnetic assemblies. New planar magnetics were not installed within the project time, so a smaller V3 layout did not establish improved magnetic loss or higher continuous output.''')
replace('Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex','The layout work was therefore completed as a design variant without','A slimmed design variant was therefore prepared without')

name='Chapters/09_Experimental_Methods/12_Revised_Plan_Validation.tex'
replace(name,'Verified assembled dimensions and matched continuous-power runs are still',r'''The approximately \SI{8}{\percent} net reduction described for the slimmed
V3 layout is a design-volume estimate. The USB-PD section was removed, so
that estimate does not compare two complete supplies with the same output
function. Any external regulator, PD controller, connector, and necessary
cooling would need to be included in the system volume.

Verified assembled dimensions and matched continuous-power runs are still''')

# Revise only the status rows affected by the new development account.
name='Chapters/10_Results/14_Revised_Plan_Status.tex'
replace(name,'Earlier screening, switching, and thermal records; preliminary V2 observations of lower half-bridge heating and persistent input-bridge heating','Earlier screening and thermal records; secondary-winding heating and limited power increase; later V2 input-bridge heating with a suspected interlayer bottleneck')
replace(name,'The plan defines an edge-card revision and its design/release work','A slimmed edge-card layout was prepared with the USB-PD section removed and secondary rectification retained')
replace(name,'A schedule entry or drawing alone does not establish completed release reviews, manufacture, or assembly','Release reviews, manufacturing/assembly readiness, and replacement-magnetics validation remain incomplete')
replace(name,'The measured operating points and design material are retained',r'Approximately \SI{8}{\percent} net volume reduction was estimated for the reduced-function V3 layout')
replace(name,'Older tests and preliminary powered V2 observations remain separate from the planned V3 work; wider copper and input-bridge relocation are planned','V1 and V2 supply the operating results; V3 reached a slimmed layout, with new magnetics not installed')
replace(name,'No matched V3 readiness/test report or completed V2 baseline repeat establishes this decision here','A V3 readiness decision and matched power/thermal tests remain open')
replace(name,'Section~\\ref{sec:method-plan-validation} defines the follow-up tests,',r'''The V3 design estimate is reported in \cref{sec:res-v3-design}; it does
not close the complete-system power-density comparison.
Section~\ref{sec:method-plan-validation} defines the follow-up tests,''')

paragraph('Chapters/11_Discussion/chapter.tex','The inherited converter was adapted',r'''The revisions addressed different limitations of the same converter. V1 established operation and control, V2 integrated the hardware and allowed the tank changes to be tested, and V3 reduced the layout by removing the USB-PD section. The remaining question is whether the magnetic and current-path losses can be reduced enough to sustain more output. The discussion connects the observed heating, unchanged practical power limit, and smaller V3 design to the work still needed.''')
append('Chapters/11_Discussion/01_Key_Findings.tex',r'''The V2 bench comparison did not establish a clear increase in available output over V1. Instead, the dominant heating concern shifted toward the input bridge after the tank changes. V3 then addressed occupied volume by removing the USB-PD section. These are distinct outcomes: a change in hotspot location, an estimated reduction in design volume, and an increase in sustained output are not interchangeable measures of improvement.''')
append('Chapters/11_Discussion/05_Magnetics_Integration.tex',r'''During prototype development, secondary-winding heating was encountered and the highest-power operating region was observed around \SIrange{3.3}{3.6}{\ampere} at the secondary output. This made the transformer a candidate limitation. Winding resistance, current distribution, leakage, and output headroom need to be measured together before one cause is assigned. Increasing the load without obtaining more useful power does not identify the loss mechanism by itself.

The reduced V3 layout retained the inherited magnetic constraints. New planar magnetics were not installed within the available time. Further winding and transformer optimization may help the \SI{100}{\watt} objective, but the longer-term \SI{240}{\watt} EPR goal would also require review of the pump, switches, tank, rectifiers, control, cooling, and USB-PD output stage.''')
name='Chapters/11_Discussion/08_Lessons_Learned.tex'
replace(name,'The complete test configuration also needs to be saved',r'''The thermal path has to be reviewed as a complete current path. The V2
input hotspot remained even after the diode replacement. A suspected
single-via connection showed why a large copper pour alone cannot be
assumed to remove a bottleneck. Copper area, pad connections, interlayer
paths, and the actual current need to be considered together.

The magnetic assemblies also set practical limits on both power and
size. Secondary-winding heating motivated transformer optimization, but
the project did not reach an installed replacement magnetic set. A new
board outline alone could not demonstrate that improvement.

The V3 reduction also showed why the included functions must be stated
when comparing size. Removing the USB-PD section reduced the converter
layout, but a complete USB-C supply would still need those functions
elsewhere. The complete system must be compared before a power-density
gain can be claimed.

The complete test configuration also needs to be saved''')
paragraph('Chapters/11_Discussion/09_Future_Improvements.tex','The powered V2 trials',r'''The powered V2 trials established operation with the leakage-only resonant tank, but did not establish more available output than V1. Input-bridge heating remained unresolved, and the earlier secondary-winding observations still need a separate loss assessment. The next measurements should track current paths, winding and rectifier temperatures, and corresponding input/output power under the same conditions.''')
paragraph('Chapters/11_Discussion/09_Future_Improvements.tex','The V3 edge card should',r'''The prepared V3 edge-card layout removes the USB-PD section and retains secondary rectification. Its estimated size reduction should be checked after the full output function and assembly volume are defined. Transformer optimization and a verified interlayer current path should guide the next revision. Release review, assembly inspection, gradual power-up, and a readiness decision remain necessary before the slimmed design can be assessed as working hardware.''')
replace('Chapters/11_Discussion/09_Future_Improvements.tex','V2--V3 improvement. Supported fixed PDOs and PPS then need protocol tests,','V2--V3 improvement. Any external USB-PD stage must be included. Supported fixed PDOs and PPS then need protocol tests,')
# Add the new diagnostic questions without changing the existing calculations or diagnostic table.
name='Chapters/11_Discussion/10_Plan_Gap_Diagnosis.tex'
replace(name,'The original \\SI{85}{\\watt} files should first be recovered,',r'''The later bench observations add two candidate limitations: secondary-
winding heating near the high-power operating region and the V2 input
hotspot, where a single-via current path was suspected. The former calls
for winding-current, resistance, and temperature measurements; the latter
calls for checking the actual interlayer path and voltage drop. Neither
has yet been isolated as the cause of the power ceiling.

The original \SI{85}{\watt} files should first be recovered,''')
print('Abstract, intro, methods, status and discussion integrated')
