from pathlib import Path
r=Path('/workspace/thesis')
def replace(name,a,b):
 p=r/name;raw=p.read_bytes();x=a.encode();y=b.encode()
 if x not in raw:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
 elif b'\n' not in x and b'\r\n' in raw:y=y.replace(b'\n',b'\r\n')
 assert raw.count(x)==1,(name,a[:90],raw.count(x));p.write_bytes(raw.replace(x,y))

text=r'''\section{Circuit and Controller Basics}
\label{sec:intro-controller-basics}

\subsection{Voltage, Current, and the Power Path}

A power supply transfers electrical energy from a source to a load. The
load is the equipment receiving that energy. Voltage is the electrical
potential difference between two points, measured in volts (V). Current
is the rate at which electric charge flows, measured in amperes (A).
Power is the rate of energy transfer, measured in watts (W). For a steady
DC output, power is found by multiplying voltage by current at the same
output. Measurements from different circuit paths cannot be multiplied
to obtain that output power.

The mains input is alternating current (AC), where voltage and current
change direction during each line cycle. The output is direct current
(DC), with a fixed polarity. Rectifier diodes allow current primarily in
one direction and are used to convert AC to DC. Switching transistors
then turn rapidly on and off to control energy transfer. A capacitor
stores energy in an electric field; an inductor stores energy in a
magnetic field. These parts form the resonant tank used in this supply.

The transformer has an input winding, called the primary, and an output
winding, called the secondary. Energy is transferred magnetically between
them. There is no direct conductive connection between these windings.
The rectified secondary output forms the secondary bulk bus: the DC
supply feeding the final USB-C regulator. A bus is a shared electrical
connection. The final regulator adjusts that voltage for the USB-C
connector, whose power line is named VBUS. Secondary-bulk voltage and
connector VBUS are therefore measured at different points.

A ground label identifies a voltage reference and return connection; it
does not automatically mean protective earth. Primary ground and isolated
secondary ground are separate references in this design. Voltage-sensing
circuits reduce or isolate the power-stage signals before they reach the
low-voltage controller.

\subsection{What the Microcontroller and Its Pins Do}

A microcontroller unit (MCU) is a small programmable computer built into
an electronic chip. Its program is called firmware. In this supply, the
MCU reads voltage and current indications, decides whether more energy is
needed, and sends switching commands to the power stage. STM32G071 and
STM32F410 identify the two MCU models used during development.

The chip is connected to the board through electrical terminals called
pins. A pin configured as an input receives a signal; an output sends a
signal to another circuit. Analog inputs accept a voltage that can vary
continuously. Digital signals represent logic states called high and low,
usually near the MCU's supply voltage and ground respectively. A logic-high
command is a low-voltage control signal, not the mains or output voltage.
The MCU pins carry sensing and command signals, rather than the load power.

STM32 signal names combine a port letter and a line number. For example,
PA1 means line 1 in port A. PB13 means line 13 in port B. These are signal
identifiers, not physical package-terminal numbers. The physical terminal
and the available functions depend on the MCU and its package. A pin can
serve different functions when configured differently, so the name alone
does not identify its purpose.

The sensing inputs used here are listed in
Table~\ref{tab:intro-controller-signals}. The primary-voltage input receives
a reduced voltage from the high-voltage circuit. The secondary-bulk input
receives a scaled signal through an isolated sensing circuit. The current
input receives a voltage representing current in the primary half bridge;
it does not carry or directly measure USB-C load current. A half bridge
is a pair of switching transistors. Its driver receives the MCU commands
and operates the transistor control terminals, called gates.

\begin{table}[htbp]
\centering
\small
\caption{MCU signal functions before and after the V2 controller change. Input and output directions are stated from the MCU's perspective.}
\label{tab:intro-controller-signals}
\begin{tabularx}{\textwidth}{@{}L{0.57\textwidth}L{0.15\textwidth}Y@{}}
\toprule
Signal function & G071 & F410 (V2)\\
\midrule
Primary-voltage measurement, analog input & PA0 & PA0\\
Secondary-bulk voltage feedback, analog input & PA1 & PA1\\
Primary half-bridge current indication, analog input & PA2 & PA2\\
Two fast switching commands, digital outputs & PA8 / PA9 & PA8 / PB13\\
Burst enable, digital output & PA10 & PA11\\
Serial transmit (TX), digital output & PC4 & PA9\\
Serial receive (RX), digital input & PC5 & PA10\\
\bottomrule
\end{tabularx}
\end{table}

The board version matters. For example, PA10 sends the burst-enable command
on the G071 platform but receives serial commands on the F410 board. Later
pin references use the function assigned on the stated board.

\subsection{Measuring, Timing, and Communicating}

The MCU contains built-in hardware blocks called peripherals. An
analog-to-digital converter (ADC) turns an input voltage into a numerical
reading. ADC1 identifies an ADC block, while an ADC channel identifies one
of its selectable signal paths. Calibration converts the reading back to
the physical quantity represented by the sensing circuit.

A timer is a hardware counter used to generate or schedule events. Names
such as TIM1, TIM3, and TIM5 identify timer blocks, not board pins. Timer
outputs generate the fast on/off pattern called the carrier. Two opposing,
or complementary, commands operate the half bridge. Dead time is the short
interval during which both commands are inactive between transitions.
A separate enable signal allows groups of carrier cycles, called bursts.
Changing how long those bursts are allowed controls average energy transfer.
A timer channel, such as CH1, is an output function within a timer; the
CH1N name identifies its complementary output.

Pulse-width modulation (PWM) describes control through the on-time of a
repeated pulse. Duty is the fraction of a period spent active. The carrier
and burst-enable duty refer to different time scales in this converter.
General-purpose input/output (GPIO) describes pins used for software-controlled
digital signals rather than a dedicated peripheral output.

Direct memory access (DMA) transfers ADC readings into memory automatically,
so the main program does not have to wait for each individual conversion.
It does not by itself synchronize sampling to switching. The serial
interface, called a universal asynchronous receiver-transmitter (UART),
sends commands and logged readings between the MCU and a computer-side
adapter. TX means transmit and RX means receive. This communication link
is separate from the USB-C power output.
'''
(r/'Chapters/01_Introduction/10_Controller_Basics.tex').write_bytes(text.replace('\n','\r\n').encode())
replace('Chapters/01_Introduction/chapter.tex',r'\input{Chapters/01_Introduction/01_Motivation}',r'''\input{Chapters/01_Introduction/10_Controller_Basics}
\input{Chapters/01_Introduction/01_Motivation}''')
replace('Chapters/01_Introduction/chapter.tex','V1 was used for bring-up and G071 controller development.','V1 was used for bring-up and development of the microcontroller, a programmable chip that reads signals and controls switching.')
replace('Chapters/01_Introduction/08_V2_Prototype.tex','Feedback & Primary voltage on PA0, isolated secondary-bulk voltage on PA1 through AMC0330, and half-bridge-current signal on PA2', 'Feedback & Scaled primary-voltage input (PA0), isolated secondary-bulk voltage feedback through AMC0330 (PA1), and primary half-bridge-current indication (PA2)')
replace('Chapters/01_Introduction/08_V2_Prototype.tex',r'''The controller connections were changed for the F410. Complementary
carrier commands use PA8 and PB13, enable uses PA11, and PA9/PA10 are used
for the command UART. The secondary-bulk voltage remains the regulated
feedback quantity. Connector voltage is set downstream, so the two voltage
measurements describe different parts of the supply.''',r'''The controller connections were changed for the F410. The two fast
switching-command outputs use PA8 and PB13. A separate enable output, PA11,
allows or blocks bursts. The UART serial link uses PA9 to transmit and
PA10 to receive commands and readings. These roles are introduced in
\cref{sec:intro-controller-basics}. The secondary-bulk voltage remains the
feedback quantity used for regulation. Connector voltage is set downstream,
so the two voltage measurements describe different parts of the supply.''')
replace('Frontmatter/Abstract.tex','GaN half-bridge bursts with the STM32G071.','gallium-nitride (GaN) half-bridge bursts with the STM32G071 microcontroller.')
replace('Frontmatter/Abstract.tex','Feedback was acquired through circular direct memory access (DMA) to avoid blocking the control loop with analog reads.', 'Voltage feedback was converted into digital readings and transferred automatically to memory using direct memory access (DMA), avoiding repeated processor waits for individual measurements.')
replace('Frontmatter/Nomenclature.tex','Isolated secondary-bus voltage before the output stage; PA1 feedback variable','Isolated secondary-bus voltage before the output stage; voltage-control feedback')
replace('Frontmatter/Nomenclature.tex','ADC & Analog-to-digital converter', 'MCU & Microcontroller unit; a programmable control chip\\\\\nADC & Analog-to-digital converter; converts an input voltage to a number')
replace('Frontmatter/Nomenclature.tex','DMA & Direct memory access', 'DMA & Direct memory access; automatic transfer of readings into memory')
replace('Frontmatter/Nomenclature.tex','GaN & Gallium nitride', 'GaN & Gallium nitride\\\\\nGPIO & General-purpose input/output; programmable digital signal connections')
replace('Frontmatter/Nomenclature.tex','PF / PFC & Power factor / power-factor correction','PF / PFC & Power factor / power-factor correction\\\\\nPWM & Pulse-width modulation; control through pulse on-time\\\\\nPAx / PBx & STM32 port A / B signal names; x identifies a line, not a package terminal\\\\\nTIMx & STM32 timer hardware block; x identifies the timer')
replace('Frontmatter/Nomenclature.tex','UART & Universal asynchronous receiver-transmitter', 'UART & Universal asynchronous receiver-transmitter; serial command/data link\\\\\nTX / RX & Transmit / receive directions of a communication signal')
print('Early reader primer, first-use wording and glossary added')
