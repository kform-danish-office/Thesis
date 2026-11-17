from pathlib import Path
r=Path('/workspace/thesis')
def replace(name,a,b):
 p=r/name;raw=p.read_bytes();x=a.encode();y=b.encode()
 if x not in raw:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
 elif b'\n' not in x and b'\r\n' in raw:y=y.replace(b'\n',b'\r\n')
 assert raw.count(x)==1,(name,a[:110],raw.count(x));p.write_bytes(raw.replace(x,y))
name='Chapters/08_Control_Firmware/chapter.tex'
replace(name,r'''This chapter covers the PWR-1.9.20 controller used for the final measurements, followed by the PWR-2.0.1 port for V2 hardware and browser logging. Both complete sources are included in Appendix~\ref{app:full-embedded-source}.''',r'''This chapter follows the controller from initial switching tests to continuous measurement, voltage regulation, and the later V2 hardware port. Browser commands and logging were then added. Both complete controller sources are included in Appendix~\ref{app:full-embedded-source}.''')
replace(name,r'\input{Chapters/08_Control_Firmware/01_Control_Objectives}',r'''\section{Development Stages and Software Identification}
\label{sec:ctrl-firmware-identities}

The first control programs were used to bring up the converter with
manually selected switching commands. Voltage feedback was then added.
The measurement process was moved to DMA so that it could run while the
MCU handled control decisions. The resulting voltage-control firmware
became the baseline for the final identified tests. Its control structure
was retained when the program was adapted to the integrated V2 board.

The project software was assigned revision identifiers beginning with
\texttt{PWR}, followed by version numbers. These identify saved programs;
they are separate from the V1, V2, and V3 hardware names. The two archived
controller files are identified in Table~\ref{tab:ctrl-software-identities}.
Earlier test records can refer to earlier software revisions, so a
recorded identifier remains relevant when reproducing a particular test.

\begin{table}[htbp]
\centering
\small
\caption{Names used for the two archived controller programs.}
\label{tab:ctrl-software-identities}
\begin{tabularx}{\textwidth}{@{}L{0.22\textwidth}L{0.19\textwidth}Y@{}}
\toprule
Development stage & Software identifier & Role in this thesis\\
\midrule
Baseline voltage-control firmware & PWR-1.9.20 & Controller associated with the identified final V1.0 test records\\
Archived V2 firmware & PWR-2.0.1 & Hardware port with browser commands and logging; not an identification of the later bench-run firmware\\
\bottomrule
\end{tabularx}
\end{table}
\FloatBarrier

The control behavior is described below using these development stages.
The full software history and source-file details are given in
Appendix~\ref{app:firmware}.

\input{Chapters/08_Control_Firmware/01_Control_Objectives}''')
name='Backmatter/Appendices/C_Firmware_Documentation.tex'
replace(name,'Two firmware versions are included. PWR-1.9.20 is the controller baseline for the measured assembly. PWR-2.0.1 is the V2 STM32F410CBU6 port of that voltage controller and can also be built for the STM32G071. Reproducing a test requires the board, calibration, and settings as well as the firmware version.',r'The two archived controller programs are identified in \cref{sec:ctrl-firmware-identities}. Their PWR identifiers refer to software revisions, not hardware generations or power ratings. PWR-1.9.20 is the baseline voltage-control firmware associated with the identified final measurements. PWR-2.0.1 is its V2 hardware port with browser communication and can target either MCU. Reproducing a test also requires the board, calibration, and saved settings.')
replace(name,'The line ranges below refer to the frozen PWR-2.0.1 sketch, including comments and blank lines.','The line ranges below refer to the archived V2 sketch, including comments and blank lines.')
replace(name,'the earlier V2 control-development stage','the DMA-based control-development stage')
replace(name,"The plan's V2 prototype and the PWR-2 MCU implementation are part of the same development.","The plan's V2 prototype and the later MCU firmware port are part of the same development.")
replace(name,'Earlier in the controller history, the name V2 was also used for the move to DMA acquisition. The board and firmware identities distinguish these stages here.','The hardware generation and software revision must be identified separately; moving acquisition to DMA was a software-development step, not a new board.')
replace(name,'Decision order shared by the baseline and PWR-2.0.1 voltage-control path.','Decision order shared by the baseline and V2 voltage-control paths.')
replace(name,'Terminal command families in PWR-2.0.1.','Terminal command families in the archived V2 firmware.')
replace(name,'and PWR-2.0.1 defaults.','and archived V2 defaults.')
replace(name,'Function navigation for the frozen PWR-2.0.1 sketch.','Function navigation for the archived V2 sketch.')
replace(name,'Both PWR-2.0.1 targets were rebuilt','Both archived V2 firmware targets were rebuilt')
replace(name,'Checks run on the included PWR-2.0.1 snapshot.','Checks run on the archived V2 firmware.')
name='Backmatter/Appendices/G_Software_Tools.tex'
replace(name,'The PWR-2.0.1 tools','The archived V2 tools')
name='Backmatter/Appendices/H_Full_Embedded_Source.tex'
replace(name,'Both complete controller files are included here.',r'Both complete controller files are included here. Their software identifiers and development roles are introduced in \cref{sec:ctrl-firmware-identities}.')
print('Software identities contextualized; appendix routine IDs simplified')
