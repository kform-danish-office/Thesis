from pathlib import Path
r=Path('/workspace/thesis')

def edit(name, pairs):
    p=r/name; raw=p.read_bytes()
    for old,new in pairs:
        a=old.encode(); c=new.encode()
        if a not in raw:
            a=a.replace(b'\n',b'\r\n');c=c.replace(b'\n',b'\r\n')
        elif b'\n' not in a and b'\r\n' in raw:
            c=c.replace(b'\n',b'\r\n')
        assert raw.count(a)==1,(name,old[:100],raw.count(a))
        raw=raw.replace(a,c)
    p.write_bytes(raw)

edit('Chapters/01_Introduction/08_V2_Prototype.tex',[
('The V2 documentation supplied on October 27, 2026 describes this\nintegrated design. The main specifications are summarized in',
 'The main V2 design specifications are summarized in'),
('V2 design summary from the schematic, PCB prints, and archived controller source. These are design specifications, rather than verified continuous-performance ratings.',
 'V2 prototype design specifications. Timing values refer to the archived controller source; continuous performance is assessed separately.'),
('PCB & Four copper layers; assembly dimensions, thickness, and copper weight are not specified in the supplied print set',
 'PCB & Four copper layers, including internal GND and PWR layers'),
])

edit('Chapters/07_Hardware/01_Prototype_Overview.tex',[
('The October 27 schematic and four-layer PCB print set document that design',
 'The schematic and four-layer PCB layout are described'),
])

p=r/'Chapters/07_Hardware/16_V2_F410.tex';s=p.read_text();paragraph=s.split('\n\n')[1]
edit('Chapters/07_Hardware/16_V2_F410.tex',[
(paragraph,
 r'''The V2 power board was developed with an STM32F410CBU6 controller \cite{ststm32f410ds}. The power stage, sensing, local supplies, and USB-C output were integrated on a four-layer PCB. The circuit and PCB design are documented in Section~\ref{sec:app-v2-oct27}. This V2 hardware is separate from the earlier controller stage called V2 in \cref{ch:control}, which marked the move to DMA acquisition.'''),
('The supplied PCB prints document four copper layers: Top Layer, Int1',
 'The V2 PCB was designed with four copper layers: Top Layer, Int1'),
('output is at the opposite end. The supplied design views show the planar\nmagnetic boards mounted upright.',
 'output is at the opposite end. The planar-magnetic boards are mounted\nupright in the mechanical design.'),
('new schematic in Section~', 'schematic in Section~'),
('V2 top copper (upper) and bottom copper (lower), from pages 1 and 4 of the October 27 PCB export. These are layout prints, not photographs of a tested configuration. The bottom print uses the source document\'s common projection.',
 'V2 top copper (upper) and bottom copper (lower). Both layers are shown in the same projection. These layout views describe the board design; fitted changes made during testing are described separately.'),
('The four-layer layout is a documented design specification. The finished\nboard dimensions, assembly height, copper weights, and layer thicknesses\nare not stated in this print set. The PDF page size is not the board size,\nand the earlier V1.0 outline cannot be used to calculate V2 power density.\nThe printed L4 footprint also describes the original design; it does not\nshow whether the inductor was fitted during the later leakage-only test.',
 'The finished board dimensions, assembly height, copper weights, and layer\nthicknesses are not specified in the PCB drawings. V2 power density\ntherefore requires separate assembly measurements. The L4 footprint belongs\nto the original resonant branch. The external inductor was removed during\nthe later leakage-only test described in \\cref{sec:res-v2-testing}.'),
(r'The source and PDF are under \sourcefile{Data/project_records}. ', ''),
('The supplied records do not include these details together.',
 'A complete test record linking these conditions is not available.'),
('The October 27 schematic and PCB prints document the V2 circuit and four-layer layout; the controller port describes its software.',
 'The V2 circuit and four-layer PCB layout describe the hardware design; the controller port describes its software.'),
])

edit('Backmatter/Appendices/B_Hardware_Documentation.tex',[
('Earlier V2 F410 schematic & Four-sheet export created October 18, 2026; retained as an earlier circuit reference',
 'Earlier V2 F410 schematic & Initial circuit reference for the F410 design'),
('Current V2 documentation & October 27 four-sheet schematic and 31-page PCB print set; reproduced in Section~',
 'V2 schematic and PCB & Four-sheet schematic and 31-page PCB print set; reproduced in Section~'),
(r'The three earlier four-sheet schematic sets below cover V1.0, V1.1, and the October 18 V2 F410 drawing. The latest V2 schematic and complete PCB print set follow in Section~\ref{sec:app-v2-oct27} and support the design description in \cref{sec:hw-v2}. The vector pages keep component labels readable when enlarged. V1.0 was used for the manufactured test board; V1.1 contains the later changes listed above. The V2 export was originally named \sourcefile{Schematic PDF_[No Variations] (12).pdf}. The number belongs to the export; the title blocks have no assigned drawing revision. Each set contains the project hierarchy, USB-C output, power and sensing circuits, and STM32 controller.',
 r'The schematic sets below cover V1.0, V1.1, and an earlier V2 F410 circuit drawing. The complete V2 schematic and PCB design follow in Section~\ref{sec:app-v2-oct27} and support the hardware description in \cref{sec:hw-v2}. The vector pages keep component labels readable when enlarged. V1.0 was used for the manufactured test board; V1.1 contains the later corrections listed above. Each set contains the project hierarchy, USB-C output, power and sensing circuits, and STM32 controller.'),
('V2 F410 schematic, sheet 1: Project hierarchy. Export created October 18, 2026.',
 'Earlier V2 F410 schematic, sheet 1: Project hierarchy.'),
('V2 F410 schematic, sheet 2: USB-C output stage. Values are those in the drawing.',
 'Earlier V2 F410 schematic, sheet 2: USB-C output stage. Values are those in the drawing.'),
(r'V2 F410 schematic, sheet 3: Power stage, local supplies, and sensing. Unspecified resonant parts and divider labels require confirmation as explained in \cref{sec:hw-v2}.',
 r'Earlier V2 F410 schematic, sheet 3: Power stage, local supplies, and sensing. Unspecified resonant parts and divider labels require confirmation as explained in \cref{sec:hw-v2}.'),
('V2 F410 schematic, sheet 4: STM32F410CBU6 and direct PA0--PA2 feedback connections.',
 'Earlier V2 F410 schematic, sheet 4: STM32F410CBU6 and direct PA0--PA2 feedback connections.'),
('V2 Schematic and PCB Documentation: October 27 Export',
 'V2 Schematic and PCB Design'),
(r'''The new V2 documentation comprises a four-sheet schematic and the complete
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
retained above so the earlier circuit reference remains available.''',
 r'''The V2 circuit was organized around the MCU, the charge-pump/resonant
converter, and the USB-C output stage. The four-sheet schematic and
complete 31-page PCB print set are reproduced below. The component values
and feedback scaling that still need confirmation are discussed in
\cref{sec:hw-v2}.

The PCB drawings cover the top and bottom copper, two internal copper
layers, silkscreen, mask, assembly, mechanical, and drill information.
Layers named ``3D Body'' show the projected component outlines.
The drawings describe the original board design. The tank changes made
during powered testing are described in \cref{sec:res-v2-testing}.'''),
])
p=r/'Backmatter/Appendices/B_Hardware_Documentation.tex';b=p.read_bytes();assert b.count(b'V2 October 27 schematic')==4;assert b.count(b'V2 October 27 PCB print')==31;b=b.replace(b'V2 October 27 schematic',b'V2 schematic').replace(b'V2 October 27 PCB print',b'V2 PCB print');p.write_bytes(b)

edit('Chapters/10_Results/15_V2_Testing_Update.tex',[
(r'''The bench observations and their later timing correction are retained in
\sourcefile{Data/project_records/V2_Testing_Update.txt}; the original
thermal image and its source information are retained with the V2 evidence files.
''', ''),
(r'''Figure~\ref{fig:v2-board-test-photos}. The original photographs have been
retained. The board configuration used for each photograph and its
relationship to the \SI{95}{\watt}
thermal run have not been recorded.''',
 r'''Figure~\ref{fig:v2-board-test-photos}. These views show the board and bench
arrangement, but do not establish the exact fitted configuration during the
\SI{95}{\watt} thermal run.'''),
('The photographs document the supplied hardware and setup;',
 'The photographs show the V2 hardware and test setup;'),
])
edit('Chapters/12_Conclusion/04_Future_Work.tex',[
('the new drawings.', 'the V2 circuit design.'),
])
print('Removed file-handoff framing from V2 prose, captions and appendix')
