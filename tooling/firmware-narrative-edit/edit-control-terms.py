from pathlib import Path
r=Path('/workspace/thesis/Chapters/08_Control_Firmware')
changes={
'01_Control_Objectives.tex': [
('In PWR-1.9.20, the secondary-bulk voltage', 'In the baseline firmware, the secondary-bulk voltage'),
],
'02_Architecture_Timing.tex': [
('Control and timing paths in PWR-1.9.20.', 'Control and timing paths in the baseline firmware.'),
('Hardware resources in PWR-1.9.20.', 'Hardware resources used by the baseline firmware.'),
],
'07_V2_DMA.tex': [
(r'In PWR-1.7.0, continuous ADC1 acquisition through DMA was introduced. In PWR-1.9.20, the three-channel scan uses', r'Blocking reads were replaced with continuous ADC1 acquisition through DMA. In the baseline firmware, the three-channel scan uses'),
('They do not select an active PI output-power controller in PWR-1.9.20.', 'They do not select an active PI output-power controller in the baseline firmware.'),
],
'08_Control_Law.tex': [
('Functional summary of the active PWR-1.9.20 control path.', 'Functional summary of the baseline voltage-control path.'),
],
'11_State_Machine.tex': [
('Operating flow in PWR-1.9.20.', 'Operating flow in the baseline firmware.'),
],
'13_Timing_Resources.tex': [
(r'The source used for the measured baseline reports PWR-1.9.20. Older supporting text also carries PWR-1.9.13, so each test is identified by its source and runtime \texttt{VER}, together with its \texttt{EXPORT}.', r'Older supporting notes name a different revision from the archived baseline. Each test therefore needs its source and runtime \texttt{VER} response recorded together with its \texttt{EXPORT}.'),
],
'14_Version_Comparison.tex': [
(r'\Cref{tab:ctrl-version-identity} lists V0, V1, V2, and the final controller in that order. These labels mark development stages and explain the design choices.', r'\Cref{tab:ctrl-version-identity} follows the progression from open-loop commands through blocking and DMA-based feedback to the final baseline. The stages are named by their control behavior so they remain distinct from the V1, V2, and V3 hardware revisions.'),
('V0 & Open-loop carrier', 'Open loop & Open-loop carrier'),
('V1 & Voltage feedback', 'Blocking feedback & Voltage feedback'),
('V2 & Continuous ADC DMA', 'DMA feedback & Continuous ADC DMA'),
('PWR-1.9.20 & Burst-edge alignment', 'Final baseline & Burst-edge alignment'),
],
'15_PWR_2_Port.tex': [
(r'The port was implemented in PWR-2.0.0, and browser UART control was added in PWR-2.0.1. This V2 is the project prototype. The V2 label in Section~\ref{sec:ctrl-v2} refers to the earlier DMA-control stage used in its software development.', r'The hardware port was implemented first, followed by browser control and logging over the UART. These changes belong to the V2 hardware development; the earlier DMA-based feedback work is described in Section~\ref{sec:ctrl-v2}.'),
(r'The PWR-1.9.20 voltage-control structure was kept, with conditional definitions for board-dependent functions. The same PWR-2.0.1 sketch can target either MCU.', r'The baseline voltage-control structure was kept, with conditional definitions for board-dependent functions. The same archived V2 firmware can target either MCU.'),
(r'The complete PWR-1.9.20 and PWR-2.0.1 sources are included in Appendix~\ref{app:full-embedded-source}.', r'The complete baseline and V2 firmware sources are included in Appendix~\ref{app:full-embedded-source}; their software identifiers are given in \cref{sec:ctrl-firmware-identities}.'),
('Changes from the measured-baseline controller to the F410 target in PWR-2.0.1.', 'Changes from the measured-baseline controller to the V2 controller port.'),
(r'In PWR-2.0.1, an opt-in protocol was added over the existing', r'An opt-in browser protocol was added to the V2 firmware over the existing'),
],
}
for name,pairs in changes.items():
 p=r/name; b=p.read_bytes()
 for a,c in pairs:
  x=a.encode(); y=c.encode()
  if x not in b:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
  elif b'\n' not in x and b'\r\n' in b:y=y.replace(b'\n',b'\r\n')
  assert b.count(x)==1,(name,a,b.count(x))
  b=b.replace(x,y)
 p.write_bytes(b)
print('Edited',len(changes),'control chapter files')
