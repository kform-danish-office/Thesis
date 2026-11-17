from pathlib import Path
r=Path('/workspace/thesis')
def replace(name,a,b):
 p=r/name;raw=p.read_bytes();x=a.encode();y=b.encode()
 if x not in raw:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
 elif b'\n' not in x and b'\r\n' in raw:y=y.replace(b'\n',b'\r\n')
 assert raw.count(x)==1,(name,a[:100],raw.count(x));p.write_bytes(raw.replace(x,y))
p=r/'Chapters/10_Results/05_Open_Circuit.tex';b=p.read_bytes();a=b.index(b'\\begin{figure}');z=b.index(b'\\end{figure}',a)+len(b'\\end{figure}');removed=b[a:z];assert b'fig:no-load-switching-quality-photos' in removed
Path('/workspace/tooling/thesis-figure-mcu-edit/removed-figure.tex').write_bytes(removed);p.write_bytes(b[:a]+b[z:])
replace('Chapters/10_Results/05_Open_Circuit.tex',r'''The development photographs show cleaner pulses after minimum-cycle handling
and no-load duty control were revised in this work. The means above and the
load-removal captures in Section~\ref{sec:res-transient} show unloaded
operation at the tested points.''',r'''The no-load voltage measurements above and the load-removal captures in
Section~\ref{sec:res-transient} show unloaded operation at the tested points.''')
replace('Chapters/10_Results/10_Firmware_Comparison.tex',r'''Figure~\ref{fig:no-load-switching-quality-photos} shows cleaner no-load pulses
after tuning, and the loaded and load-removal tests show the combined
controller operating.''',r'''The loaded and load-removal tests show the combined controller operating.''')
replace('Frontmatter/Abstract.tex','with the STM32G071 microcontroller.','with the microcontroller (MCU).')
replace('Frontmatter/Abstract.tex','Development continued with an F410-based V2 board','Development continued with a V2 board')
replace('Frontmatter/Approval.tex','the STM32 firmware was developed.','the MCU firmware was developed.')
replace('Frontmatter/Approval.tex','the integrated V2 F410 board.','the integrated V2 board.')
replace('Frontmatter/Approval.tex','The F410 control connections,','The MCU control connections,')
replace('Frontmatter/Approval.tex','from converter bring-up and G071 control to the integrated F410 V2 board','from converter bring-up and initial MCU control to the integrated V2 board')
replace('Frontmatter/Nomenclature.tex','STM32 port A / B / C signal names','MCU port A / B / C signal names')
replace('Frontmatter/Nomenclature.tex','STM32 timer hardware block','MCU timer hardware block')
print('Crossed-out figure and its references removed; front matter model repetition reduced')
