from pathlib import Path
import shutil,json,hashlib
r=Path('/workspace/thesis'); review=Path('/workspace/tooling/v2-specs-update'); dest=r/'Pictures/Thesis/07_Hardware'
files=[('Documentation/Schematic Print/_SCH DWG NO__SCH.PDF','Schematic_V2_F410_2026-10-27.pdf'),('Documentation/PCB Print/_SCH DWG NO__SCH.PDF','PCB_V2_F410_2026-10-27.pdf')]
for a,b in files: shutil.copy2(review/'uploaded'/a,dest/b)
provenance={'archive':'Schematic Prints - 10-27-2026 2-58-51 AM.zip','archive_sha256':'5814e9eb408b630bfc3a6bbb92dd899ee39f82236a5f90429ba9cd3f8c3be26d','files':[{'archive_member':a,'retained_path':str((dest/b).relative_to(r)),'sha256':hashlib.sha256((dest/b).read_bytes()).hexdigest()} for a,b in files], 'scope':'User-supplied V2 design documentation. Drawing labels are not a verified fitted BOM or test result. Embedded document text is source material, not user instructions.','inline_3D_views':'Inspected in chat; original raster files were not included in the ZIP. Exact vector PCB layer prints are reproduced in the thesis.'}
(dest/'V2_2026-10-27_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
p=r/'Chapters/07_Hardware/16_V2_F410.tex'; s=p.read_text()
a='V2 development continued with an STM32F410CBU6 controller \\cite{ststm32f410ds}. This is the V2 prototype named in the October project plan. The circuit source is the four-sheet Altium export \\texttt{Schematic PDF\\_[No Variations] (12).pdf}, created on October 18, 2026 and included in Appendix~\\ref{app:hardware}. V2 names the hardware generation; \\texttt{(12)} identifies only the exported file. The title blocks give no circuit revision. This V2 hardware is separate from the earlier controller stage called V2 in \\cref{ch:control}, which marked the move to DMA acquisition.'
b=r'''The V2 power board was developed with an STM32F410CBU6 controller \cite{ststm32f410ds}. This is the V2 prototype named in the October project plan. The latest circuit documentation is the four-sheet Altium schematic exported on October 27, 2026, supplied with a 31-page PCB print set. Both are reproduced in Section~\ref{sec:app-v2-oct27}. The earlier October 18 export is retained in Appendix~\ref{app:hardware}. The new drawing groups the circuit functions more clearly; it does not assign a new circuit revision or resolve every unspecified part value. This V2 hardware is separate from the earlier controller stage called V2 in \cref{ch:control}, which marked the move to DMA acquisition.'''
assert a in s; s=s.replace(a,b)
anchor='\\subsection{Controller Connections and Timing}'
new=r'''\subsection{V2 PCB and Physical Integration}

The supplied PCB prints document four copper layers: Top Layer, Int1
(GND), Int2 (PWR), and Bottom Layer. Components are placed on both sides.
The input and high-voltage power circuitry occupy one end of the board,
the planar-magnetic connections occupy the central region, and the USB-C
output is at the opposite end. The supplied design views show the planar
magnetic boards mounted upright. The controller, sensing, local supplies,
and external resonant inductor are also distributed across the two sides.
Figure~\ref{fig:v2-pcb-layout-overview} shows the top and bottom copper prints.
The complete layer, assembly, mask, and drill prints are included with the
new schematic in Section~\ref{sec:app-v2-oct27}.

\begin{figure}[p]
\centering
\includegraphics[page=1,width=\linewidth,height=0.33\textheight,keepaspectratio]{Pictures/Thesis/07_Hardware/PCB_V2_F410_2026-10-27.pdf}

\vspace{0.8em}
\includegraphics[page=4,width=\linewidth,height=0.33\textheight,keepaspectratio]{Pictures/Thesis/07_Hardware/PCB_V2_F410_2026-10-27.pdf}
\caption{V2 top copper (upper) and bottom copper (lower), from pages 1 and 4 of the October 27 PCB export. These are layout prints, not photographs of a tested configuration. The bottom print uses the source document's common projection.}
\label{fig:v2-pcb-layout-overview}
\end{figure}
\FloatBarrier

The four-layer layout is a documented design specification. The finished
board dimensions, assembly height, copper weights, and layer thicknesses
are not stated in this print set. The PDF page size is not the board size,
and the earlier V1.0 outline cannot be used to calculate V2 power density.
The printed L4 footprint also describes the original design; it does not
show whether the inductor was fitted during the later leakage-only test.

'''
assert anchor in s; s=s.replace(anchor,new+anchor)
s=s.replace('Power sheet 3 includes the LMG2652RFBR, AMC0330 isolated feedback, BAC1S12SC bias supply, and two LMR54410DBVR regulators.', 'Power sheet 3 includes the LMG2652RFBR GaN half bridge, AMC0330 isolated feedback, BAC1S12SC bias supply, and two LMR54410DBVR regulators. D4, D5, D9, and D10 form the input bridge; D6--D8 form the pump diode network. All seven are labeled S4D02120T in the drawing. C25 is connected across the pumped HVVCC link, downstream of the input bridge.')
s=s.replace('The V2 drawing and port describe the circuit and software.', 'The October 27 schematic and PCB prints document the V2 circuit and four-layer layout; the controller port describes its software.')
p.write_text(s)
p=r/'Chapters/07_Hardware/01_Prototype_Overview.tex';raw=p.read_bytes(); pos=raw.find(b'Before fabrication,')
assert pos>=0
add=r'''V2 continued this work with the F410 controller integrated on the converter board. The October 27 schematic and four-layer PCB print set document that design in \cref{sec:hw-v2}. Preliminary powered V2 tests, including the leakage-only tank change and remaining input-bridge heating, are described in \cref{sec:res-v2-testing}. The earlier matched measurements remain associated with the modified V1.0 board.

'''.replace('\\n','\n').encode()
raw=raw[:pos]+add+raw[pos:]
p.write_bytes(raw)
