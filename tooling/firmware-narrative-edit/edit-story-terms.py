from pathlib import Path
import re,json,hashlib
root=Path('/workspace/thesis');rev=Path('/workspace/tooling/firmware-narrative-edit')
changes={
'Frontmatter/Abstract.tex':[("the final PWR-1.9.20 controller","the voltage-control firmware")],
'Chapters/01_Introduction/05_Contributions_Attribution.tex':[("the DMA-based PWR-1.9.20 controller","the DMA-based voltage controller")],
'Chapters/01_Introduction/06_Scope_Limitations.tex':[("the integrated controller and PWR-2 firmware","the integrated controller and its ported firmware")],
'Chapters/01_Introduction/08_V2_Prototype.tex':[("programmed dead time in PWR-2.0.1","programmed dead time in the archived V2 controller code")],
'Chapters/02_Background/08_Research_Gap.tex':[("the PWR-1.9.20 controller","the developed voltage-control firmware")],
'Chapters/03_Requirements_Architecture/07_Operating_Modes.tex':[("States and options in firmware PWR-1.9.20.","States and options in the baseline firmware.")],
'Chapters/03_Requirements_Architecture/09_Revised_Plan_Criteria.tex':[("The integrated MCU and PWR-2 firmware","The integrated MCU and its ported firmware")],
'Chapters/05_Modeling_Simulation/01_Objectives.tex':[("the final USB-C circuit and PWR-1.9.20 controller","the final USB-C circuit and voltage-control firmware")],
'Chapters/07_Hardware/01_Prototype_Overview.tex':[("The final controller was PWR-1.9.20.",r"The voltage-control firmware used for the identified final tests is described in Chapter~\ref{ch:control}.")],
'Chapters/07_Hardware/08_Sensing.tex':[("Use in PWR-1.9.20","Use in the baseline firmware")],
'Chapters/07_Hardware/16_V2_F410.tex':[("In PWR-2.0.0, the peripherals were changed to match the MCU and drawing. In PWR-2.0.1, browser telemetry and commands were added.","The firmware peripherals were adapted to the MCU and circuit connections. Browser telemetry and commands were then added to the ported controller."),("the archived PWR-2.0.1 source","the archived V2 controller source")],
'Chapters/09_Experimental_Methods/01_Objectives.tex':[("schematic reference, and PWR-1.9.20 was the final controller.",r"schematic reference. The baseline firmware used for the identified final runs is described in Section~\ref{sec:ctrl-firmware-identities}.")],
'Chapters/09_Experimental_Methods/07_Control_Tests.tex':[("For the final PWR-1.9.20 tests,","During the final baseline-control tests,")],
}
report=[]
for name,pairs in changes.items():
 p=root/name;old=p.read_bytes();b=old
 for a,c in pairs:
  x=a.encode();y=c.encode();assert b.count(x)==1,(name,a,b.count(x));b=b.replace(x,y)
 p.write_bytes(b);report.append(name)
# Preserve physical quantities, equations, labels, citations and source paths.
patterns={
 'quantities':r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+',
 'labels':r'\\label\{[^}]*\}',
 'citations':r'\\cite\w*\*?(?:\[[^\]]*\])?\{[^}]*\}',
 'sourcepaths':r'\\(?:sourcefile|includegraphics|input|lstinputlisting)(?:\[[^\]]*\])?\{[^}]*\}',
 'math':r'\\\(.*?\\\)|\\\[.*?\\\]|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$',
}
for name in report:
 a=(rev/'before'/name).read_text();b=(root/name).read_text()
 for key,pattern in patterns.items():assert re.findall(pattern,a,re.S)==re.findall(pattern,b,re.S),(name,key)
print('Edited',len(report),'files; preservation checks passed')
(rev/'story-terms-edited.json').write_text(json.dumps(report,indent=2)+'\n')
