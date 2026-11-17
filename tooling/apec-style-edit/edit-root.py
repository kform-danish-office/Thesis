from pathlib import Path
r=Path('/workspace/thesis')
def put(name,text):
 p=r/name;b=p.read_bytes();nl='\r\n' if b'\r\n' in b else '\n';p.write_bytes(text.replace('\r\n','\n').replace('\n',nl).encode())
def replace(name,a,b):
 p=r/name;raw=p.read_bytes();x=a.encode();y=b.encode()
 if x not in raw:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
 elif b'\n' not in x and b'\r\n' in raw:y=y.replace(b'\n',b'\r\n')
 assert raw.count(x)==1,(name,a[:100],raw.count(x));p.write_bytes(raw.replace(x,y))
def paragraph(name,starts,new):
 s=(r/name).read_text();old=next(x for x in s.split('\n\n') if x.startswith(starts));replace(name,old,new)

name='Chapters/01_Introduction/10_Controller_Basics.tex';s=(r/name).read_text();table=s[s.index('\\begin{table}'):s.index('\\end{table}')+len('\\end{table}')]
put(name,r'''\section{Control Architecture and Signal Definitions}
\label{sec:intro-controller-basics}

The microcontroller (MCU) regulates the isolated secondary bulk bus through
burst modulation of the fixed-frequency half bridge. The downstream USB-C
stage regulates connector VBUS independently. These nodes are distinguished
throughout the analysis and measurements.

The feedback inputs are the scaled primary voltage at PA0, isolated
secondary-bulk voltage at PA1, and primary half-bridge-current indication
at PA2. The current signal supports load classification and optional
protection; it is not a measurement of connector output current. ADC
acquisition operates through circular DMA independently of carrier phase.
Carrier commands, burst enable, and UART communication use separate MCU
signal paths.

Table~\ref{tab:intro-controller-signals} compares the assignments on the
original STM32G071 platform and the STM32F410 V2 board. Port identifiers
denote logical MCU signals; package-terminal numbers are given in the
hardware pin map. The PA10 reassignment from burst enable to UART receive
is therefore interpreted with the board revision.

'''+table+r'''
\FloatBarrier
''')
put('Frontmatter/Abstract.tex',r'''\section*{Abstract}
\addcontentsline{toc}{section}{Abstract}

A digitally controlled USB-C laboratory supply was implemented using an inherited charge-pump power-factor-correction (PFC) resonant topology and planar magnetics. Secondary-bulk voltage regulation was extended to startup, loaded operation, and load removal by controlling the energy admitted to the resonant stage.

The nominal \SI{1}{\mega\hertz} carrier was retained, while average transfer was regulated through gallium-nitride (GaN) half-bridge burst enable. Circular direct memory access (DMA) provided nonblocking feedback acquisition. Startup precharge and separate loaded/no-load duty limits were implemented. A downstream output stage provided the tested \SI{5}{\volt}, \SI{9}{\volt}, \SI{15}{\volt}, and \SI{20}{\volt} USB-C settings.

At \SI{240}{\volt}, \SI{50}{\hertz} input, matched measurements at the \SI{20}{\volt} setting yielded \SIrange{73.97}{79.89}{\watt} at the load. Average output voltage was \SIrange{19.973}{19.991}{\volt}, with \SIrange{0.416}{0.452}{\volt} recorded peak-to-peak ripple. Logged power factor was 0.97--0.99 and current total harmonic distortion was \SIrange{2.23}{3.98}{\percent}. Paired input/output readings gave preliminary efficiency estimates of \SIrange{76.5}{77.1}{\percent}, limited by acquisition timing and calibration uncertainty. No-load and load-removal operation were recorded. A thermal image labeled \SI{20}{\volt}, \SI{4}{\ampere} showed a \SI{90.4}{\celsius} surface maximum, motivating further loss and thermal characterization.

V2 integrated the MCU, GaN stage, isolated feedback, and USB-C circuit on a four-layer PCB. Tank and timing changes reduced half-bridge heating, while input-bridge heating remained unresolved (\cref{sec:res-v2-testing}). Bench performance remained comparable to the first prototype; secondary-winding loss and a restricted input current path were not isolated quantitatively. The V3 edge-card layout retained secondary rectification and omitted the USB-PD output section, giving an estimated net volume reduction of approximately \SI{8}{\percent}. Replacement planar magnetics were not installed. A complete-system density comparison must include the external regulated USB-PD stage.

Digitally controlled operation near \SI{80}{\watt} was demonstrated. The \SI{100}{\watt} continuous target and \SI{65}{\watt} continuous minimum require defined-duration thermal and stability validation. Full-range zero-voltage switching, USB-PD conformance, safety, and EMC remain unverified. Operation toward \SI{240}{\watt} USB-PD Extended Power Range (EPR) is a longer-term development objective.
''')
paragraph('Chapters/01_Introduction/chapter.tex','The starting point was',r'''A charge-pump PFC resonant converter was adapted to a digitally controlled USB-C laboratory supply using inherited planar magnetics. V1 established the power stage and burst-control implementation. Control, sensing, and interface functions were integrated in V2, where tank and timing changes reduced local heating without establishing higher sustained output. The V3 edge-card design addressed occupied volume, while the remaining winding and input-path losses motivated further magnetic and thermal development.''')
paragraph('Chapters/01_Introduction/01_Motivation.tex','Increasing the switching frequency',r'''MHz switching permits reduced passive-component size but increases sensitivity to commutation time, winding loss, and parasitic impedance. Magnetic integration, gate timing, layout, and control must therefore be evaluated at the installed operating point.''')
paragraph('Chapters/01_Introduction/01_Motivation.tex','The LED load used',r'''USB-C operation introduces startup without a load, delayed attachment, load removal, and multiple output-voltage settings. These conditions alter the demand on the resonant stage and require control of both secondary stored energy and average transferred power.''')
paragraph('Chapters/01_Introduction/02_Problem_Statement.tex','The difficulty is',r'''The charge-pump and isolated resonant paths share one half bridge, coupling input-current shaping to secondary power transfer. The DC link buffers the pulsating mains power, while burst control must supply the load and limit residual excitation during startup, light load, and load removal.''')
paragraph('Chapters/01_Introduction/03_Aim_Objectives.tex','The component and control requirements',r'''The analytical component and control requirements are evaluated against the assembled hardware and measured operating points. The resulting electrical and thermal limits guide the V2 and V3 changes.''')
print('Technical introduction and abstract written; elementary primer removed')
