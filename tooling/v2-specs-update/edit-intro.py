from pathlib import Path
root=Path('/workspace/thesis/Chapters/01_Introduction')
def edit(name, replacements):
 p=root/name; raw=p.read_bytes(); s=raw.decode()
 for a,b in replacements:
  assert s.count(a)==1,(name,a)
  s=s.replace(a,b)
 p.write_bytes(s.encode())
edit('chapter.tex', [
('The starting point was a DTU charge-pump converter and supplied planar magnetics. The hardware and controller were then built around those parts for a USB-C laboratory supply. The main change was the load. It could be absent at startup, draw different amounts of power, or be disconnected while energy remained in the converter. The circuit, burst controller, and tests were developed around these conditions.',
 'The starting point was a DTU charge-pump converter and supplied planar magnetics. The hardware and controller were developed around those parts for a USB-C laboratory supply. The first prototype was brought up with an STM32G071 controller. The control and interface functions were then integrated into the F410-based V2 board. In both stages, the load could be absent at startup, draw different amounts of power, or be disconnected while energy remained in the converter. The circuit, burst controller, and tests were developed around these conditions.'),
('\\input{Chapters/01_Introduction/03_Aim_Objectives}\r\n', '\\input{Chapters/01_Introduction/03_Aim_Objectives}\r\n\\input{Chapters/01_Introduction/08_V2_Prototype}\r\n')])
edit('01_Motivation.tex', [
('An LMG2652 GaN half bridge, an STM32G071 controller, and the USB-C output section were added around these parts. Average power is controlled by enabling groups of fixed-frequency switching cycles. The complete supply allowed the inherited conversion principle to be tested with a detachable, variable load.',
 'An LMG2652 GaN half bridge, an STM32G071 controller, and the USB-C output section were added around these parts in the first prototype. Average power was controlled by enabling groups of fixed-frequency switching cycles. The same approach was carried into V2, with the controller integrated onto the converter PCB. This allowed the inherited conversion principle to be tested with a detachable, variable load and then developed into a more integrated assembly.')])
edit('03_Aim_Objectives.tex', [
('The revised plan carries this work into V2 evaluation and a V3 edge-card design \\cite{projectOctoberPlan}. The next electrical step is to repeat the reported \\SI{85}{\\watt} V2 operating point and explain the \\SI{15}{\\watt} output shortfall to the \\SI{100}{\\watt} target before selecting converter changes. The plan also calls for fixed-PDO and PPS tests, thermal and stability tests of defined duration, and a V2--V3 power-density comparison using the same definition of assembly volume. Section~\\ref{sec:revised-plan-criteria} sets out these criteria and their current status.',
 'The revised plan carries this work into V2 evaluation and a V3 edge-card design \\cite{projectOctoberPlan}. It calls for the reported \\SI{85}{\\watt} V2 operating point to be repeated and the \\SI{15}{\\watt} shortfall to the \\SI{100}{\\watt} target to be investigated. V2 has since been operated with a modified resonant tank, as described in \\cref{sec:res-v2-testing}. Those preliminary observations still need matched power and thermal measurements. The plan also calls for fixed-PDO and PPS tests, thermal and stability tests of defined duration, and a V2--V3 power-density comparison using the same definition of assembly volume. Section~\\ref{sec:revised-plan-criteria} sets out these criteria and their current status.')])
edit('04_Research_Questions.tex', [
('How is secondary voltage controlled by the final firmware during startup, loaded operation, load attachment, load removal, and no load?',
 'How is secondary voltage controlled during startup, loaded operation, load attachment, load removal, and no load, and how is that control carried from the first prototype to V2?')])
edit('05_Contributions_Attribution.tex', [
('The assembled supply was tested to check its behavior in practice.',
 'The controller was then ported to the STM32F410CBU6 on V2. The revised board integrates the control, isolated feedback, local supplies, and USB-C output with the power stage. Browser control and logging were added, and the resonant tank was modified during powered testing. The new schematic and PCB documentation are included in Appendix~\\ref{app:hardware}.\r\n\r\nThe assembled supply was tested to check its behavior in practice.')])
edit('06_Scope_Limitations.tex', [
('The implementation and tests center on the open-frame laboratory prototype. The manufactured V1.0 board was tested after bring-up modifications. Later corrections and design changes appear in schematic V1.1. The hardware chapter separates the fitted circuit from that later drawing.',
 'The thesis covers the development from the first open-frame laboratory prototype to the integrated V2 board. The manufactured V1.0 board was tested after bring-up modifications, and later corrections were recorded in schematic V1.1. The F410-based V2 design and its preliminary powered tests form the next stage. The hardware chapter identifies the drawing and fitted configuration used at each stage.'),
('The revised plan identifies the F410 controller and PWR-2 firmware as the V2 development described here. It reports an earlier V2 result near \\SI{85}{\\watt}. In the matched measurements analyzed here, \\SI{79.89}{\\watt} was reached on the modified V1.0 assembly. This is a separate result. Section~\\ref{sec:revised-plan-criteria} also tracks the planned V3 edge-card design, its release checks, and the matched V2--V3 comparison.',
 'The revised plan identifies the F410 controller and PWR-2 firmware as the V2 development described here. It reports an earlier V2 result near \\SI{85}{\\watt}. In the matched measurements analyzed here, \\SI{79.89}{\\watt} was reached on the modified V1.0 assembly. That measured result is kept separate from the reported V2 point and the later tank and thermal observations. Section~\\ref{sec:revised-plan-criteria} also tracks the planned V3 edge-card design, its release checks, and the matched V2--V3 comparison.')])
edit('07_Thesis_Structure.tex', [
('Chapters~\\ref{ch:magnetics} and \\ref{ch:hardware} show how the supplied magnetic components were integrated and the converter was assembled. Chapter~\\ref{ch:control} follows the controller development and explains the operating states used in testing. Chapter~\\ref{ch:methods} defines the test setup and measurement methods.',
 'Chapters~\\ref{ch:magnetics} and \\ref{ch:hardware} show how the supplied magnetic components were integrated and how the hardware developed from the first prototype to V2. Chapter~\\ref{ch:control} follows the G071 controller development, the F410 port, and the operating states used in testing. Chapter~\\ref{ch:methods} defines the test setup and measurement methods.'),
('The appendices provide the equations, schematics, firmware documentation, and measurement tables needed to follow the work.',
 'The appendices provide the equations, complete schematics, V2 PCB prints, firmware documentation, and measurement tables needed to follow the work.')])
new=r'''\section{Development of the V2 Prototype}
\label{sec:intro-v2}

The first prototype was used to develop the power circuit and burst
controller. V2 was then designed with the STM32F410CBU6 controller on the
converter board in place of the separate G071 platform. The charge-pump
PFC and isolated resonant paths were retained, together with the supplied
planar magnetics and downstream USB-C output stage.

The V2 schematic and PCB export supplied on October 27, 2026 documents
this integrated design. The main specifications are summarized in
Table~\ref{tab:intro-v2-specs}. The circuit connections and controller
timing are described in \cref{sec:hw-v2}; the complete schematic and PCB
print set are included in \cref{sec:app-v2-oct27}.

\begin{table}[htbp]
\centering
\caption{V2 design summary from the schematic, PCB prints, and archived controller source. These are design specifications, rather than verified continuous-performance ratings.}
\label{tab:intro-v2-specs}
\small
\begin{tabularx}{\textwidth}{@{}p{0.25\textwidth}X@{}}
\toprule
Function & V2 implementation\\
\midrule
Controller & STM32F410CBU6 integrated on the converter PCB\\
Power stage & LMG2652RFBR GaN half bridge shared by the charge-pump and resonant paths\\
Feedback & Primary voltage on PA0, isolated secondary-bulk voltage on PA1 through AMC0330, and half-bridge-current signal on PA2\\
USB-C output & MPQ4242 output stage downstream of the isolated secondary bulk bus\\
Local supplies & BAC1S12SC bias supply and separate LMR54410 regulators for primary and secondary local supplies\\
PCB & Four copper layers; assembly dimensions, thickness, and copper weight are not specified in the supplied print set\\
Archived timing & Nominal \SI{1}{\mega\hertz} carrier and \SI{40}{\nano\second} programmed dead time in PWR-2.0.1\\
\bottomrule
\end{tabularx}
\end{table}

The controller connections were changed for the F410. Complementary
carrier commands use PA8 and PB13, enable uses PA11, and PA9/PA10 are used
for the command UART. The secondary-bulk voltage remains the regulated
feedback quantity. Connector voltage is set downstream, so the two voltage
measurements describe different parts of the supply.

During later powered V2 tests, heating was observed in the external
series resonant inductor. It was removed, and the tank was changed to use
transformer leakage with approximately \SI{1.66}{\nano\farad} resonant
capacitance. A software dead-time setting of approximately
\SI{60}{\nano\second} was reported. The input bridge continued to heat up,
including during the run identified as \SI{95}{\watt}. These observations
are discussed in \cref{sec:res-v2-testing}. They show that the modified V2
was operated, but they do not establish a continuous output rating or a
measured efficiency improvement.

The V2 drawings describe the original resonant branch. The fitted tank
changes must therefore be stated separately when interpreting a test.
Some component values and feedback scaling also remain unresolved in the
drawing, as discussed in \cref{sec:hw-v2}. The next work is to measure the
V2 configuration consistently, resolve the bridge heating, and use those
results to guide the planned V3 design.
'''
(root/'08_V2_Prototype.tex').write_bytes(new.replace('\n','\r\n').encode())
print('Updated introduction and added V2 design summary')
