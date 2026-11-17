from pathlib import Path
r=Path('/workspace/thesis')
def replace(name,a,b):
 p=r/name;raw=p.read_bytes();x=a.encode();y=b.encode()
 if x not in raw:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
 elif b'\n' not in x and b'\r\n' in raw:y=y.replace(b'\n',b'\r\n')
 assert raw.count(x)==1,(name,a[:100],raw.count(x));p.write_bytes(raw.replace(x,y))
def paragraph(name,starts,new):
 s=(r/name).read_text();old=next(x for x in s.split('\n\n') if x.startswith(starts));replace(name,old,new)
def append(name,new):
 p=r/name;b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';p.write_bytes(b.rstrip()+nl+nl+new.replace('\r\n','\n').replace('\n',nl.decode()).encode()+nl)

name='Chapters/12_Conclusion/01_Project_Summary.tex'
replace(name,'from the \\SI{79.89}{\\watt} result above. V3 remains a planned revision;\nreadiness checks and a matched V2--V3 density comparison are still needed.',r'''from the \SI{79.89}{\watt} result above.

V3 was prepared as a slimmer edge-card layout. The USB-PD output section
was removed, leaving secondary rectification, with an estimated net
volume reduction of approximately \SI{8}{\percent}. A new planar-magnetic
set was not installed within the available time. V3 therefore demonstrates
layout development, while the loss, thermal, and continuous-power
improvements remain to be tested. A complete USB-C comparison must include
the external output stage as well.''')
append(name,r'''The main outcome is the development path across the revisions. Converter operation and control were established with V1. V2 integrated those functions and allowed the tank changes to be tested, but its bench behavior did not establish a higher output capability. V3 reduced the layout while exposing how much further reduction depended on the magnetics and on the functions included in the system.''')

name='Chapters/12_Conclusion/02_Research_Questions.tex'
replace(name,'of this thesis. Fields and windings were not redesigned.', 'of this thesis. Secondary-winding heating identified a need for further transformer work, but no replacement magnetic set was installed.')
paragraph(name,r'\paragraph{RQ5:',r'''\paragraph{RQ5: Further development.}
V2 is operational, but its bench performance did not establish more available output than V1. Secondary-winding heating, the limited power increase around \SIrange{3.3}{3.6}{\ampere} at the secondary output, and the later input hotspot identify the next measurements. The transformer and a possible single-via restriction remain suspected limitations, rather than confirmed loss allocations. The slimmed V3 layout gives an estimated \SI{8}{\percent} net reduction by removing the USB-PD section, but needs external output hardware for a complete USB-C function. Replacement magnetics, readiness checks, and matched power/thermal tests remain unfinished. The immediate target is \SI{100}{\watt}; \SI{240}{\watt} EPR remains a longer-term goal.''')
append('Chapters/12_Conclusion/03_Contributions.tex',r'''A reduced V3 edge-card layout was also prepared. The USB-PD section was removed from the converter card, while the secondary rectifiers were retained. This provided a design-level volume reduction and a basis for the next magnetic and thermal work. It did not establish improved continuous power or a validated replacement transformer.''')
replace('Chapters/12_Conclusion/03_Contributions.tex','The four-layer PCB and circuit are documented in the new\nprint set.','The four-layer PCB and circuit are documented in the\nschematic and PCB prints.')
paragraph('Chapters/12_Conclusion/chapter.tex','The inherited converter was built',r'''The inherited converter was built into a working laboratory supply with a detachable output. Development progressed from G071 control and V1 testing to the integrated F410 V2 board, then to a slimmed V3 edge-card layout. The revisions established operation and reduced the occupied design volume, but secondary-winding heating and the later input hotspot remained unresolved. The conclusions distinguish those completed design and test steps from the sustained-power and magnetic improvements still needed.''')

name='Chapters/12_Conclusion/04_Future_Work.tex'
paragraph(name,'The immediate V2 task',r'''The immediate task is to separate the magnetic limitation from the input-path heating. Secondary current, winding temperature, rectifier temperature, voltage drops, and corresponding input/output power should be recorded under the same load conditions. The suspected single-via path needs to be checked directly before additional copper or a diode relocation is treated as a solution. Synchronized switching waveforms are also needed to confirm the inferred ZVS behavior.''')
paragraph(name,'The V3 edge-card design',r'''The prepared V3 layout needs to be completed around the selected magnetics and the required external output stage. The reduced layout should then be reviewed, assembled, and brought up gradually. Both sides of the comparison need the same included functions, volume convention, supported power basis, cooling, and electrical conditions. The estimated size reduction alone does not establish increased power density or improved thermal margin.''')
append(name,r'''Reaching the longer-term \SI{240}{\watt} USB-PD EPR goal would require more than a smaller board or a transformer change. The pump charge transfer, switch and capacitor stress, rectification, magnetic current capability, control range, isolation, cooling, and USB-PD output stage would all need to support that operating point. The present work does not demonstrate EPR power delivery.''')

name='Backmatter/Appendices/J_Revised_Plan_Integration.tex'
replace(name,'Section~\\ref{sec:hw-v3-plan} defines the interface, mechanical, thermal, spacing, manufacturing, and release work. It does not assign unverified dimensions or present a planned board as a completed build.',r'Section~\ref{sec:hw-v3-plan} describes the reduced edge-card layout, removal of the USB-PD section, and the replacement magnetics and hardware checks still needed. Section~\ref{sec:res-v3-design} reports the design outcome.')
replace(name,'Section~\\ref{sec:res-revised-plan} reports the missing V2/V3 comparison and the evidence needed for the planned V3 readiness decision.',r'Section~\ref{sec:res-revised-plan} distinguishes the V3 design-volume estimate from the outstanding complete-system power-density comparison and readiness decision.')
replace(name,'For this October 20 revision, completion is assessed', 'Completion is assessed')
paragraph(name,'The measurements are from the earlier prototype,',r'''The matched numerical measurements are from the earlier prototype. V2 adds the integrated circuit, software, and later tank and thermal observations. V3 adds a slimmed layout with secondary rectification retained and the USB-PD section removed. A replacement magnetic set was not installed, and a matched complete-system V2--V3 power-density comparison remains unfinished.''')

append('README.md','Current development narrative: V1 establishes the measured baseline; V2 adds integrated control and tank/thermal observations; V3 is a slimmed edge-card layout with the USB-PD section removed and secondary rectifiers retained. Approximately 8% net volume reduction is a design estimate for the reduced-function layout, not a measured complete-system power-density gain. New planar magnetics were not installed. The 3.3–3.6 A secondary-output region, suspected transformer limit and possible input via bottleneck remain qualitative bench findings. The 100 W target and longer-term 240 W EPR goal are not continuous ratings.')
print('Conclusions, plan mapping and source summary updated')
