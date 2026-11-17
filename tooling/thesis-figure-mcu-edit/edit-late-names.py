from pathlib import Path
r=Path('/workspace/thesis')
changes={
'Chapters/10_Results/06_ZVS.tex': [
('the G071 burst-enable signal at PA10','the MCU burst-enable signal at PA10')],
'Chapters/10_Results/14_Revised_Plan_Status.tex': [
('on the V1.0/G071 assembly','on the V1.0 assembly'),
('or the later F410/PWR-2.0.1 implementation','or the later integrated V2 implementation with PWR-2.0.1')],
'Chapters/11_Discussion/10_Plan_Gap_Diagnosis.tex': [('An F410 port,','An MCU port,')],
'Chapters/12_Conclusion/chapter.tex': [
('from G071 control and V1 testing to the integrated F410 V2 board','from MCU control and V1 testing to the integrated V2 board')],
'Chapters/12_Conclusion/01_Project_Summary.tex': [
('and STM32 controller were','and MCU were'),
('For the measured G071 prototype,','For the measured V1.0 prototype,'),
('V2 moved the STM32F410 controller onto a four-layer PCB with the','In V2, the MCU was integrated onto a four-layer PCB with the'),
('not the matched G071\nmeasurements above.','not the matched V1.0\nmeasurements above.')],
'Chapters/12_Conclusion/02_Research_Questions.tex': [
('The later V2 design integrates the F410 controller,','The later V2 design integrates the MCU,'),
('captured on the G071\nassembly. The control law was retained in the F410 port,','captured on the V1.0\nassembly. The control law was retained in the V2 MCU port,'),
('For the V1.0/G071 prototype,','For the V1.0 prototype,')],
'Chapters/12_Conclusion/03_Contributions.tex': [
('For V2, the F410 controller was integrated into the converter-board','For V2, the MCU was integrated into the converter-board')],
'Backmatter/Appendices/A_Analytical_Equations.tex': [
('For the measured G071 controller,','For the MCU on the measured V1.0 prototype,')],
'Backmatter/Appendices/B_Hardware_Documentation.tex': [
('Earlier V2 F410 schematic & Initial circuit reference for the F410 design','Earlier V2 schematic & Initial circuit reference for the V2 design'),
('an earlier V2 F410 circuit drawing','an earlier V2 circuit drawing'),
('and STM32 controller.','and MCU.'),
('sheet 4: STM32 controller.','sheet 4: MCU.'),
('Earlier V2 F410 schematic,','Earlier V2 schematic,'),
('sheet 4: STM32F410CBU6 and direct PA0--PA2 feedback connections.','sheet 4: MCU and direct PA0--PA2 feedback connections.'),
('sheet 4: STM32F410 controller and service connections.','sheet 4: MCU and service connections.')],
'Backmatter/Appendices/C_Firmware_Documentation.tex': [
('Port to the V2 F410 controller:','Port to the V2 MCU:'),
("The plan's V2 prototype and the F410/PWR-2 implementation are part of the same development.","The plan's V2 prototype and the PWR-2 MCU implementation are part of the same development."),
('The MCU and firmware names distinguish these stages here.','The board and firmware identities distinguish these stages here.'),
('The F410 assignments and peripheral choices follow the device documentation','The V2 MCU assignments and peripheral choices follow the device documentation'),
('the F410 values are ARR','the V2 settings are ARR'),
('On the F410, linker symbols and image extent','On V2, linker symbols and image extent'),
('Saved Settings and the F410 Flash Journal','Saved Settings and the MCU Flash Journal'),
('The default F410 linker layout is different.','The default MCU linker layout is different.'),
('and valid F410 storage layout.','and valid V2 storage layout.'),
('F410 also requires the included','The V2 build also requires the included')],
'Backmatter/Appendices/F_Contribution_Provenance.tex': [
('and the STM32 controller','and the MCU'),
('STM32 firmware &','MCU firmware &'),
('V2 F410 hardware and PWR-2.0.1 software &','V2 MCU hardware and PWR-2.0.1 software &')],
'Backmatter/Appendices/G_Software_Tools.tex': [
('support the F410 and browser connection;','support the V2 MCU and browser connection;'),
('For F410, \\sourcefile{firmware/stm32f410.ld}','For V2, \\sourcefile{firmware/stm32f410.ld}'),
('required for the F410 build;','required for the V2 build;'),
('Build and F410 image-check commands','Build and MCU image-check commands')],
'Backmatter/Appendices/H_Full_Embedded_Source.tex': [
('archived G071 version used to explain the measurements.','archived version used to explain the V1.0 measurements.')],
'Backmatter/Appendices/I_Full_Supporting_Source.tex': [
('F410 linker layout','MCU linker layout'),
('F410 HEX verifier','MCU HEX verifier')],
'Backmatter/Appendices/J_Revised_Plan_Integration.tex': [
('V2 includes the STM32F410/PWR-2 development;','V2 includes the MCU/PWR-2 development;'),
('document the F410 hardware and controller.','document the V2 circuit and MCU firmware.')],
}
counts={}
for name,pairs in changes.items():
 p=r/name;b=p.read_bytes();count=0
 for a,c in pairs:
  x=a.encode();y=c.encode()
  if x not in b:x=x.replace(b'\n',b'\r\n');y=y.replace(b'\n',b'\r\n')
  n=b.count(x)
  assert n>=1,(name,a)
  b=b.replace(x,y);count+=n
 p.write_bytes(b);counts[name]=count
print(counts)
