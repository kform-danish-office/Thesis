from pathlib import Path
r=Path('/workspace/thesis');changes=[]
def edit(name,pairs):
 p=r/name;b=p.read_bytes();n=0
 for a,c in pairs:
  x=a.encode();y=c.encode()
  if x not in b:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
  elif b'\n' not in x and b'\r\n' in b:y=y.replace(b'\n',b'\r\n')
  assert b.count(x)==1,(name,a,b.count(x));b=b.replace(x,y);n+=1
 p.write_bytes(b);changes.append((name,n))
edit('Chapters/01_Introduction/chapter.tex',[
 ('on the STM32G071 microcontroller, a programmable chip','on the microcontroller (MCU), a programmable chip'),
 ('the F410-based V2 board','the V2 board')])
edit('Chapters/01_Introduction/01_Motivation.tex',[
 ('an STM32G071 controller','an MCU')])
edit('Chapters/01_Introduction/02_Problem_Statement.tex',[
 ('regulated by the STM32.','regulated by the MCU.')])
edit('Chapters/01_Introduction/05_Contributions_Attribution.tex',[
 ('The STM32G071 firmware was developed','The MCU firmware was developed'),
 ('The controller was then ported to the STM32F410CBU6 on V2.','The firmware was then adapted for the MCU on V2.')])
edit('Chapters/01_Introduction/06_Scope_Limitations.tex',[
 ('The F410-based V2 design','The V2 design'),
 ('The revised plan identifies the F410 controller and PWR-2 firmware as the V2 development described here.','The revised plan identifies the integrated controller and PWR-2 firmware as the V2 development described here.')])
edit('Chapters/01_Introduction/07_Thesis_Structure.tex',[
 ('follows the G071 controller development, the F410 port,','follows the MCU firmware development, its adaptation for V2,')])
edit('Chapters/01_Introduction/08_V2_Prototype.tex',[
 ('V2 was then designed with the STM32F410CBU6 controller on the\nconverter board in place of the separate G071 platform.','V2 was then designed with the MCU on the converter board in place of\nthe separate controller platform.'),
 ('The controller connections were changed for the F410.','The MCU connections were changed for V2.')])
edit('Chapters/02_Background/07_USBC_Context.tex',[
 ('on the STM32 microcontroller','on the MCU')])
edit('Chapters/03_Requirements_Architecture/02_Electrical_Specifications.tex',[
 ('the baseline G071 timing and feedback parameters','the original prototype\'s MCU timing and feedback parameters'),
 ('describe the V2 F410 port,','describe the V2 MCU implementation,')])
edit('Chapters/03_Requirements_Architecture/03_Functional_Requirements.tex',[
 ('In the G071 implementation below,','In the original prototype below,')])
edit('Chapters/03_Requirements_Architecture/04_USBC_Interface.tex',[
 ('The STM32 controls the upstream converter','The MCU controls the upstream converter'),
 ("the STM32's secondary-voltage sensing input", "the MCU's secondary-voltage sensing input")])
edit('Chapters/03_Requirements_Architecture/06_System_Architecture.tex',[
 ('to the primary-referenced STM32','to the primary-referenced MCU'),
 ('The STM32G071 produces the complementary switching commands','The MCU on the original prototype produces the complementary switching commands')])
edit('Chapters/03_Requirements_Architecture/07_Operating_Modes.tex',[
 ('In the G071 implementation,','On the original prototype,')])
edit('Chapters/03_Requirements_Architecture/09_Revised_Plan_Criteria.tex',[
 ('The F410/PWR-2 circuit and firmware are part of this V2 development.','The integrated MCU and PWR-2 firmware are part of this V2 development.')])
edit('Chapters/04_Topology_Analysis/01_Topology_Overview.tex',[
 ('PA10 on the G071.','PA10 on the original prototype.')])
edit('Chapters/04_Topology_Analysis/09_Device_Stress.tex',[
 ('the G071 burst-enable output PA10','the MCU burst-enable output PA10 on the original prototype')])
edit('Chapters/04_Topology_Analysis/10_USBC_Adaptation.tex',[
 ('The STM32 therefore responds','The MCU therefore responds')])
edit('Chapters/05_Modeling_Simulation/02_Uploaded_LTspice_Files.tex',[
 ('the STM32 burst controller','the MCU burst controller')])
edit('Chapters/05_Modeling_Simulation/07_Startup_NoLoad.tex',[
 ('the G071 burst-enable output PA10','the MCU burst-enable output PA10 on the original prototype')])
edit('Chapters/07_Hardware/chapter.tex',[
 ('On the G071, PA8 and PA9 provide','On the original prototype, PA8 and PA9 provide'),
 ('Their F410 counterparts are described','The corresponding V2 connections are described')])
edit('Chapters/07_Hardware/01_Prototype_Overview.tex',[
 ('with the F410 controller integrated','with the MCU integrated')])
edit('Chapters/07_Hardware/05_Gate_Drive.tex',[
 ('sent from the STM32 controller','sent from the MCU'),
 ('On the G071 test platform,','On the original prototype,')])
edit('Chapters/07_Hardware/08_Sensing.tex',[
 ('to the primary-side STM32.','to the primary-side MCU.')])
edit('Chapters/07_Hardware/09_Protection.tex',[
 ('on the G071 output PA10','on the original prototype\'s MCU output PA10')])
edit('Chapters/07_Hardware/12_EMI.tex',[
 ('the G071 enable output PA10','the MCU enable output PA10 on the original prototype')])
edit('Chapters/07_Hardware/16_V2_F410.tex',[
 ('\\section{V2 Hardware and the F410 Controller}','\\section{V2 Hardware and MCU Integration}'),
 ('The V2 power board was developed with an STM32F410CBU6 controller','The V2 power board was developed with the MCU on the converter PCB'),
 ("The F410 port uses the G071's fixed", "The V2 MCU retains the original prototype's fixed"),
 ('the F410 code configures center-aligned TIM1','the MCU code configures center-aligned TIM1'),
 ('using the timer functions in the F410 reference manual','using the timer functions in the MCU reference manual'),
 ('On the F410, DMA2 Stream0 Channel0 identifies','On V2, DMA2 Stream0 Channel0 identifies'),
 ('from the F410 design','from the V2 design')])
edit('Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex',[
 ('The F410 assignments do not by themselves define','The existing MCU assignments do not by themselves define')])
edit('Chapters/08_Control_Firmware/chapter.tex',[
 ('On the G071, PA8 and PA9 carry','On the original prototype, PA8 and PA9 carry')])
edit('Chapters/08_Control_Firmware/01_Control_Objectives.tex',[
 ('the G071 burst-enable output PA10','the MCU burst-enable output PA10 on the original prototype')])
edit('Chapters/08_Control_Firmware/02_Architecture_Timing.tex',[
 ('direct configuration of the STM32G071 peripherals','direct configuration of the MCU peripherals')])
edit('Chapters/08_Control_Firmware/09_Limits_Antiwindup.tex',[
 ('The G071 burst-enable output PA10','The MCU burst-enable output PA10 on the original prototype')])
edit('Chapters/08_Control_Firmware/12_Fault_Handling.tex',[
 ('the G071 burst-enable output PA10','the MCU burst-enable output PA10 on the original prototype')])
edit('Chapters/08_Control_Firmware/15_PWR_2_Port.tex',[
 ('For the F410, the complementary carrier,','For V2, the complementary carrier,'),
 ('On the F410, TIM1 provides programmed dead time','On V2, TIM1 provides programmed dead time'),
 ('follow the F410 device and timer documentation','follow the MCU device and timer documentation'),
 ('The F410 analog-to-digital converter','The MCU analog-to-digital converter'),
 ('\\subsection{Saving Settings on the F410}','\\subsection{Saving MCU Settings}'),
 ('The F410 has no dedicated EEPROM.','The V2 MCU has no dedicated EEPROM.')])
edit('Chapters/09_Experimental_Methods/05_Probing.tex',[
 ('The G071 burst-enable output PA10','The MCU burst-enable output PA10 on the original prototype')])
report=Path('/workspace/tooling/thesis-figure-mcu-edit/naming-main-notes.md')
report.write_text('# MCU naming in Chapters 1–9\n\nChanged routine prose to refer to the MCU, with original-prototype or V2 context where a pin role depends on the board. Kept model names in the educational pin comparison, actual component-identification entries, explicit port/assignment comparisons, and the genuine STM32 software framework name. No source paths, code, numerical quantities, mathematical expressions, labels or citations changed.\n\n'+ '\n'.join(f'- {p} ({n} replacements)' for p,n in changes)+'\n')
print(len(changes),'files edited;',sum(n for _,n in changes),'targeted replacements')
