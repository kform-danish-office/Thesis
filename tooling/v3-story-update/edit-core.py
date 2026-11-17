from pathlib import Path
r=Path('/workspace/thesis')
def put(name,text):
 p=r/name; old=p.read_bytes() if p.exists() else b''
 nl='\r\n' if b'\r\n' in old else '\n'
 p.write_bytes(text.replace('\r\n','\n').replace('\n',nl).encode())
def replace(name,a,b):
 p=r/name; raw=p.read_bytes(); old=a.encode();new=b.encode()
 if old not in raw:old=old.replace(b'\n',b'\r\n');new=new.replace(b'\n',b'\r\n')
 elif b'\n' not in old and b'\r\n' in raw:new=new.replace(b'\n',b'\r\n')
 assert raw.count(old)==1,(name,a[:90],raw.count(old));p.write_bytes(raw.replace(old,new))

p=r/'Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex';old=p.read_text();table=old[old.index('\\begin{table}'):old.index('\\end{table}')+len('\\end{table}')]
put('Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex',r'''\section{V3 Edge-Card Design}
\label{sec:hw-v3-plan}

V3 was developed as a slimmer edge-card design based on the V2 converter
\cite{projectOctoberPlan}. The purpose was to reduce the occupied volume
and improve the power-path layout while carrying forward the control work.
The earlier tests had shown that stable output voltage alone did not remove
the thermal limit. Secondary-winding heating and the later input-bridge
hotspot therefore became the main concerns for further development.

\subsection{Reduced Output Section and Volume}

The USB-PD output section was removed from the converter-card design,
leaving secondary rectification as its output. A net volume reduction of
approximately \SI{8}{\percent} was estimated for this slimmed arrangement.
A separate regulated output and USB-PD interface would be needed to form
a complete USB-C supply. The reduction therefore describes the smaller
converter design; it is not a measured reduction in the volume of a
functionally equivalent complete supply.

The inherited planar magnetics still constrained the available space.
Further reduction was expected from a revised planar-magnetic design,
but a new magnetic set was not installed within the available project time.
The layout work was therefore completed as a design variant without
establishing its sustained power or thermal performance. The distinction
between the layout estimate and a complete assembly comparison is explained
in \cref{sec:method-density,sec:res-v3-design}.

\subsection{Power Path and Edge Interface}

The V2 controller and circuit in Section~\ref{sec:hw-v2} formed the starting
point. The edge interface still needs a verified contact assignment,
signal reference, voltage/current requirement, and startup state. Primary
and isolated secondary connections must remain distinct. PA1 remains
secondary-bulk feedback and PA2 remains a primary half-bridge-current
signal. The F410 assignments do not by themselves define an edge-connector
pinout.

Removing the USB-PD section changes the system interface as well as its
size. The rectified secondary output must be matched to any external
regulator and its load. Power contacts, copper, and interlayer connections
must carry that current without creating another local thermal bottleneck.
The complete pump, half-bridge, resonant, and rectifier loops still need
to be checked together with the gate and sensing returns.

'''+table+r'''

The smaller layout does not establish connector ratings, insulation
spacing, assembled fit, or readiness for manufacture. These checks remain
necessary before the design can be released and evaluated as hardware.

\subsection{Magnetic and Thermal Development}

The high-power operating region was observed around
\SIrange{3.3}{3.6}{\ampere} at the secondary output. Secondary-winding
heating was encountered, and greater loading did not give a clear increase
in available power. Transformer optimization was therefore identified as
a priority. Winding loss, interconnect loss, resonant behavior, and output
headroom still need to be separated before the transformer can be assigned
as the limiting component.

The immediate objective remains \SI{100}{\watt}. Operation toward the
\SI{240}{\watt} USB-PD Extended Power Range (EPR) level is a longer-term
development goal. That increase would require the complete power path,
control, thermal design, and external USB-PD output stage to be assessed.
It is not a capability demonstrated by the reduced V3 layout.

\subsection{Release and Bring-Up Status}

A slimmed layout was prepared, but the replacement magnetics and matched
V3 power and thermal tests were not completed. Before manufacture, the
schematic/layout, design-rule, BOM, and manufacturing reviews must be
closed. After assembly, the planned sequence remains optical inspection,
continuity and isolation checks, low-voltage subsystem checks,
current-limited startup, control/interface verification, and gradual
loading \cite{projectOctoberPlan}.

Section~\ref{sec:revised-plan-criteria} gives the acceptance criteria.
AP-06 and AP-08 require release, assembly, and readiness checks. The V1
measurements and V2 bench observations remain the operating results;
the V3 reduction remains a design estimate until the complete arrangement
has been built and tested.
''')

put('Chapters/01_Introduction/09_V3_Development.tex',r'''\section{From the V2 Findings to V3}
\label{sec:intro-v3}

The revisions were used to address different parts of the same problem.
V1 established converter operation and the burst-control method. V2
integrated the controller and interface functions on the power board and
allowed the resonant tank to be changed. Comparable output behavior was
observed on the bench, but the dominant heating in the modified V2
arrangement was concentrated near the input bridge. A clear increase in
available output power was not established by the board revision alone.

Secondary-winding heating and the difficulty of increasing power around
the high-load operating region motivated further transformer work. The
V3 edge-card layout was then slimmed by removing the USB-PD output section
and retaining secondary rectification. A net volume reduction of about
\SI{8}{\percent} was estimated. The output function changed with that
reduction, so an external regulated USB-PD stage would have to be included
in a complete-system comparison.

New planar magnetics were not installed within the available time. V3
therefore represents layout development and an identified direction for
further work, rather than a demonstrated increase in continuous power.
The immediate objective remains \SI{100}{\watt}; operation toward
\SI{240}{\watt} USB-PD EPR is a longer-term goal. The design changes and
remaining checks are described in \cref{sec:hw-v3-plan}.
''')
replace('Chapters/01_Introduction/chapter.tex',r'\input{Chapters/01_Introduction/08_V2_Prototype}',r'''\input{Chapters/01_Introduction/08_V2_Prototype}
\input{Chapters/01_Introduction/09_V3_Development}''')
replace('Chapters/01_Introduction/08_V2_Prototype.tex','results to guide the planned V3 design.','results to develop and evaluate the V3 edge-card design.')

# Add the new operating observations without merging them into earlier numeric tables.
anchor=r'\subsection{Input-Bridge Heating}'
replace('Chapters/10_Results/15_V2_Testing_Update.tex',anchor,r'''\subsection{Secondary Output and Comparison with V1}

Secondary-winding heating was encountered during prototype development.
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
efficiency or temperature at matched operating points.

\subsection{Input-Bridge Heating}''')
replace('Chapters/10_Results/15_V2_Testing_Update.tex',
'''Insufficient copper around the input bridge was suspected as a cause of
the heating. Narrow traces can add resistive loss, while limited copper
area reduces heat spreading from the diode pads. This has not yet been
confirmed by current, voltage-drop, or thermal measurements. Replacing
the diodes did not resolve the problem.''',
'''Insufficient copper around the input bridge was suspected as a cause of
the heating. A connection concentrated through a single via was also
suspected in this area. A large copper pour cannot remove a bottleneck if
the current still passes through one restricted interlayer connection.
Narrow traces and vias can add resistive loss, while limited copper area
reduces heat spreading from the diode pads. The fitted current path and
its voltage drop still need to be checked before this explanation can be
confirmed. Replacing the diodes did not resolve the problem.''')

put('Chapters/10_Results/16_V3_Design_Outcome.tex',r'''\section{V3 Design Outcome and Revision Comparison}
\label{sec:res-v3-design}

The V3 edge-card layout was reduced by removing the USB-PD output section
and retaining the secondary rectifiers. The estimated net volume reduction
was approximately \SI{8}{\percent}. This is a design estimate for the
slimmed converter arrangement. It is not a measured power-density result
for a complete USB-C supply, because external regulation and USB-PD
functions would still be required.

A replacement planar-magnetic set was not installed within the project
time. Further reduction and higher sustained output were therefore not
demonstrated. The outcome is a smaller layout concept and a clearer set
of thermal and magnetic questions for the next prototype.

\begin{table}[htbp]
\centering
\small
\caption{Development outcomes across the prototype revisions.}
\label{tab:revision-development-outcomes}
\begin{tabularx}{\textwidth}{@{}L{0.14\textwidth}L{0.34\textwidth}Y@{}}
\toprule
Revision & Main development & Outcome and remaining limit\\
\midrule
V1.0/G071 & Converter integration and DMA-based burst control with the downstream USB-C stage & Matched electrical measurements and load-event records; thermal and loss limitations remained\\
V2/F410 & Integrated controller, browser interface, and leakage-only tank trial & Comparable qualitative bench performance; input-bridge heating remained, with copper and a possible via bottleneck under investigation\\
V3 edge card & Slimmed layout with USB-PD section removed and secondary rectification retained & Approximately \SI{8}{\percent} estimated net volume reduction; replacement magnetics and matched power/thermal validation remained incomplete\\
\bottomrule
\end{tabularx}
\end{table}
\FloatBarrier

The revisions show that changing the position of a hotspot is not by
itself a measured reduction in total loss. The available power and
component temperatures need to be compared together. The winding and
input-path observations guide the next measurements, while the V3 layout
shows what can be removed or rearranged before a new magnetic design is
installed. A complete V2--V3 comparison must include every output stage
needed to provide the same function, as defined in \cref{sec:method-density}.
''')
replace('Chapters/10_Results/chapter.tex',r'\input{Chapters/10_Results/15_V2_Testing_Update}',r'''\input{Chapters/10_Results/15_V2_Testing_Update}
\input{Chapters/10_Results/16_V3_Design_Outcome}''')
print('Core V1/V2/V3 story added')
