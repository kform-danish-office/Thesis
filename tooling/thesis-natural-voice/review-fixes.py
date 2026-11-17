from pathlib import Path
r=Path('/workspace/thesis')
changes={
'Frontmatter/Abstract.tex': [('A USB-C laboratory power supply was built and tested based on an earlier DTU charge-pump power-factor-correction (PFC) resonant converter, using the supplied planar magnetics.', 'A USB-C laboratory power supply based on an earlier DTU charge-pump power-factor-correction (PFC) resonant converter was built and tested using the supplied planar magnetics.')],
'Chapters/01_Introduction/03_Aim_Objectives.tex': [('The component and control requirements are established through analysis, followed by the hardware and firmware implementation.', 'The component and control requirements are established through analysis. The hardware and firmware implementation is then described.')],
'Chapters/08_Control_Firmware/15_PWR_2_Port.tex': [('Periodic samples are dropped when the queue is full', 'Periodic samples are dropped when the queue is congested')],
'Chapters/07_Hardware/13_Thermal.tex': [('The full test duration and ambient conditions were not recorded with the high-power captures.', 'Complete records of test duration and ambient conditions were not included with the high-power captures.')],
'Chapters/07_Hardware/16_V2_F410.tex': [('These details were not recorded together.', 'The supplied records do not include these details together.')],
'Chapters/12_Conclusion/02_Research_Questions.tex': [('points and were calculated from paired readings.', 'points and include calculations from paired readings.')],
}
for name,edits in changes.items():
 p=r/name; b=p.read_bytes()
 for a,c in edits:
  assert b.count(a.encode())==1,(name,a)
  b=b.replace(a.encode(),c.encode())
 p.write_bytes(b)
print('Applied independent review fixes')
