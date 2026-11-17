from pathlib import Path
import fitz
r=Path('/workspace/thesis'); p=r/'Backmatter/Appendices/B_Hardware_Documentation.tex'; raw=p.read_bytes(); s=raw.decode().replace('\r\n','\n')
s=s.replace('V2 F410 schematic & Four-sheet export created October 18, 2026; project V2 name, without an assigned drawing revision in its title blocks', 'Earlier V2 F410 schematic & Four-sheet export created October 18, 2026; retained as an earlier circuit reference')
line='Final resonant inductors &'
pos=s.index(line)
s=s[:pos]+r'''Current V2 documentation & October 27 four-sheet schematic and 31-page PCB print set; reproduced in Section~\ref{sec:app-v2-oct27}\\
'''+s[pos:]
a='The three four-sheet schematic sets cover V1.0, V1.1, and the V2 F410 implementation in \\cref{sec:hw-v2}.'
b='The three earlier four-sheet schematic sets below cover V1.0, V1.1, and the October 18 V2 F410 drawing. The latest V2 schematic and complete PCB print set follow in Section~\\ref{sec:app-v2-oct27} and support the design description in \\cref{sec:hw-v2}.'
assert a in s;s=s.replace(a,b)
s+=r'''

\clearpage
\section{V2 Schematic and PCB Documentation: October 27 Export}
\label{sec:app-v2-oct27}

The new V2 documentation comprises a four-sheet schematic and the complete
31-page PCB print set supplied in
\sourcefile{Schematic Prints - 10-27-2026 2-58-51 AM.zip}.
The schematic groups the system into the MCU, charge-pump/resonant converter,
and USB-C output stage. Its core part labels and controller connections
agree with the earlier V2 export. The unspecified tank values and divider
labels discussed in \cref{sec:hw-v2} remain unresolved.

All pages of both new documents are reproduced below. The PCB set contains
top and bottom copper, two internal copper layers, silkscreen, mask,
assembly, mechanical, and drill prints. The original layer names are used
in the captions. Layers named ``3D Body'' are printed footprint projections,
not the separate perspective renderings supplied in the chat. The prints
document the design; they do not identify every fitted part or the
configuration used in the later leakage-only bench test.

The original vector PDFs and a file-hash record are retained under
\sourcefile{Pictures/Thesis/07_Hardware}. The October 18 schematic is
retained above so the earlier circuit reference remains available.
'''
for n,name in enumerate(['System overview','USB-C output stage','Power stage, sensing, and local supplies','STM32F410 controller and service connections'],1):
 s+='\n'+r'\clearpage\begin{landscape}'+'\n'+r'\begin{figure}[H]\centering'+'\n'+fr'\includegraphics[page={n},width=\linewidth,height=0.86\textheight,keepaspectratio]{{Pictures/Thesis/07_Hardware/Schematic_V2_F410_2026-10-27.pdf}}'+'\n'+fr'\caption{{V2 October 27 schematic, sheet {n}: {name}.}}\label{{fig:app-v2-oct27-schematic-{n}}}'+'\n'+r'\end{figure}\end{landscape}'+'\n'
doc=fitz.open(r/'Pictures/Thesis/07_Hardware/PCB_V2_F410_2026-10-27.pdf'); toc=doc.get_toc()
labels={row[2]:row[1] for row in toc if row[0]==3}
print('PCB bookmarks:',len(labels))
for n in range(1,32):
 name=labels.get(n,f'Print {n}')
 # Bookmark names are literal layer descriptions, not LaTeX instructions.
 for old,new in [('&',r'\&'),('_',r'\_'),('%',r'\%'),('#',r'\#')]: name=name.replace(old,new)
 s+='\n'+r'\clearpage\begin{landscape}'+'\n'+r'\begin{figure}[H]\centering'+'\n'+fr'\includegraphics[page={n},width=\linewidth,height=0.86\textheight,keepaspectratio]{{Pictures/Thesis/07_Hardware/PCB_V2_F410_2026-10-27.pdf}}'+'\n'+fr'\caption{{V2 October 27 PCB print {n}: {name}.}}\label{{fig:app-v2-oct27-pcb-{n}}}'+'\n'+r'\end{figure}\end{landscape}'+'\n'
p.write_bytes(s.replace('\n','\r\n').encode())
