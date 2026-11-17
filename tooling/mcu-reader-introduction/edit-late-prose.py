from pathlib import Path
root=Path('/workspace/thesis')
changed=[]
def edit(name, pairs):
    p=root/name; raw=p.read_bytes(); original=raw
    for old,new in pairs:
        a=old.encode(); b=new.encode()
        if a not in raw:
            a=a.replace(b'\n',b'\r\n'); b=b.replace(b'\n',b'\r\n')
        elif b'\n' not in a and b'\r\n' in raw:
            b=b.replace(b'\n',b'\r\n')
        assert raw.count(a)==1,(name,old[:100],raw.count(a))
        raw=raw.replace(a,b)
    if raw!=original:
        p.write_bytes(raw);changed.append(name)

edit('Chapters/04_Topology_Analysis/01_Topology_Overview.tex',[
(r'The carrier remains at \SI{1}{\mega\hertz} during enabled operation. The controller adjusts the PA10 burst command. PA1 measures \(V_{\mathrm{sec}}\), PA0 provides optional primary-voltage feed-forward, and PA2 provides load classification. The burst command changes average energy transfer at the selected carrier operating point and sets how often the pump transfers charge.',
 r'The carrier remains at \SI{1}{\mega\hertz} during enabled operation. The controller changes the switching-burst duration through its enable output, PA10 on the G071. The conditioned secondary-bulk voltage \(V_{\mathrm{sec}}\) is read at input PA1. The conditioned primary-voltage signal at PA0 provides optional feed-forward, while the primary-current signal at PA2 is used to distinguish loaded from no-load operation. The burst command changes average energy transfer at the selected carrier operating point and sets how often the pump transfers charge.')
])
edit('Chapters/04_Topology_Analysis/09_Device_Stress.tex',[
('PA2 indicates that primary-side current according to its circuit transfer relationship and calibration.',
 'The current-sense voltage at controller input PA2 represents that primary-side current according to the sensing circuit and its calibration.'),
('PA10 inhibition ends further commanded excitation,',
 'Holding the G071 burst-enable output PA10 low ends further commanded excitation,')
])
edit('Chapters/05_Modeling_Simulation/07_Startup_NoLoad.tex',[
('When PA10 is inhibited, no further excitation is commanded,',
 'When the G071 burst-enable output PA10 is held low, no further excitation is commanded,')
])
edit('Chapters/09_Experimental_Methods/04_Instrumentation.tex',[
('The ADC and UART readings were used to check the sensed values and controller\ncommands. They were not treated as independent measurements of connector\noutput.',
 'The controller\'s converted sensor readings and serial status messages were\nused to check sensing and commands. These ADC readings and UART messages\nwere not treated as independent measurements of connector output.'),
(r'''\begin{table}[htbp]
\centering
\caption{Typical channel assignments in the time-domain tests. The capture-specific assignment takes precedence.}''',
 r'''In Table~\ref{tab:channel-definitions}, CH1--CH4 identify oscilloscope input
channels. These labels belong to the measuring instrument; they are not
MCU port names or physical chip-pin numbers.

\begin{table}[htbp]
\centering
\caption{Typical channel assignments in the time-domain tests. The capture-specific assignment takes precedence.}''')
])
edit('Chapters/09_Experimental_Methods/05_Probing.tex',[
('PA10 identifies the burst envelope. An individual transistor turns on within',
 'The G071 burst-enable output PA10 marks the interval in which switching\ncycles are allowed. An individual transistor turns on within')
])
edit('Chapters/09_Experimental_Methods/07_Control_Tests.tex',[
('PA1 voltage feedback, continuous ADC DMA, and PA10 burst control in PWR-1.9.20\nwere used in the final control tests. Where available, saved UART settings were used to interpret\nthe response instead of source-code defaults.',
 'For the final PWR-1.9.20 tests, the conditioned secondary-bulk-voltage signal\nat input PA1 was read continuously by the analog-to-digital converter\n(ADC). Direct memory access (DMA) copied those readings to memory without\nmaking the controller wait for each conversion. The burst-enable output\nPA10 set the intervals in which switching cycles were allowed. Where\navailable, settings saved through the UART serial link were used to\ninterpret the response instead of source-code defaults.'),
('PA10 is low.', 'the burst-enable signal at PA10 is low.')
])
edit('Chapters/10_Results/06_ZVS.tex',[
('The switching captures show how PA10 groups the nominal\n',
 'The switching captures show how the G071 burst-enable signal at PA10 selects\ngroups of the nominal\n')
])
edit('Chapters/10_Results/10_Firmware_Comparison.tex',[
('The final controller uses each sensed quantity for a specific task. PA1\nsets the secondary-voltage demand, PA2 classifies load, and PA10 adjusts\naverage energy transfer. PA8/PA9 retain the nominal carrier. Reaching this\narrangement required changes to acquisition timing as well as the feedback\ncalculation.',
 'The final controller uses each sensed quantity for a specific task. The\nsecondary-bulk-voltage measurement at input PA1 is used for regulation.\nThe primary-current signal at PA2 is used to classify load, while the\nburst-enable output at PA10 controls average energy transfer. The carrier\ncommands at PA8/PA9 keep the nominal switching frequency. Reaching this\narrangement required changes to acquisition timing as well as the feedback\ncalculation.')
])
edit('Chapters/11_Discussion/03_Control_Contribution.tex',[
(r'''\SI{1}{\mega\hertz} carrier is generated by TIM1, and transfer intervals
are selected through PA10. Demand is updated in the control task from
continuously acquired ADC samples.''',
 r'''\SI{1}{\mega\hertz} carrier is generated by the MCU's carrier timer,
TIM1. The transfer intervals are selected through the burst-enable output
PA10. Demand is updated from sensor readings converted by the ADC.'''),
('Blocking conversion waits were replaced by circular DMA.',
 'Blocking conversion waits were replaced by circular DMA, which transfers\nnew sensor readings automatically into a memory buffer.')
])
edit('Chapters/11_Discussion/08_Lessons_Learned.tex',[
('The PA2 correction showed why the sensed quantity had to be identified',
 'The correction to the interpretation of the primary-current input PA2\nshowed why the sensed quantity had to be identified')
])
edit('Backmatter/Appendices/C_Firmware_Documentation.tex',[
(r'''\begin{longtable}{@{}L{0.19\linewidth}L{0.34\linewidth}L{0.37\linewidth}@{}}
\caption{Peripheral assignments. F410 package numbers refer to the UFQFPN48 device.}''',
 r'''The naming conventions are introduced in \cref{sec:intro-controller-basics}.
In the table below, PA/PB/PC names identify logical MCU port signals, while
``package'' identifies a physical terminal on the chip. TIM identifies a
timer block and CH one of its output channels. An ADC channel selects the
input to be converted. DMA channels and streams select a memory-transfer
path; they are not extra external pins. GPIO means general-purpose digital
input/output. AF selects an alternate pin function, such as connecting a
timer output instead of a software-controlled signal. RX and TX mean
receive and transmit on the serial connection.

\begin{longtable}{@{}L{0.19\linewidth}L{0.34\linewidth}L{0.37\linewidth}@{}}
\caption{Peripheral assignments. F410 package numbers refer to the UFQFPN48 device.}'''),
('With a \\SI{100}{\\mega\\hertz} timer clock, the F410 values are ARR',
 'The timer settings are held in registers, which are named hardware\nconfiguration locations written by the firmware. ARR sets the counter\nrange, CCR1 sets the output comparison point, and DTG sets the programmed\ndead time. With a \\SI{100}{\\mega\\hertz} timer clock, the F410 values are ARR')
])
edit('Backmatter/Appendices/G_Software_Tools.tex',[
('bench computer through a USB-to-UART adapter to the controller\'s command UART.\nFiles are served by the local server or static web host.',
 'bench computer through a USB-to-UART adapter to the controller\'s command UART.\nThe adapter converts between USB data and the controller\'s serial transmit\nand receive signals. This data conversion does not by itself provide\nelectrical isolation. Files are served by the local server or static web host.'),
('Telemetry fields follow the firmware definitions. PA1 senses the\nsecondary bus upstream of the USB-C output stage. PA2 is the\nhalf-bridge-current sensing path.',
 'Telemetry fields follow the firmware definitions. The secondary-bulk-voltage\ninput PA1 senses the bus upstream of the USB-C output stage. The\nprimary-current input PA2 carries the half-bridge-current sensing signal.')
])
print('\n'.join(changed))
Path('/workspace/tooling/mcu-reader-introduction/late-edited-files.txt').write_text('\n'.join(changed)+'\n')
