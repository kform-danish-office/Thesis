from pathlib import Path
import shutil,json
root=Path('/workspace/thesis');review=Path('/workspace/tooling/thesis-firmware-204');edits=[]
def replace(name,old,new):
 p=root/name;raw=p.read_bytes();s=raw.decode();assert old in s,(name,old)
 backup=review/'before'/name;backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():backup.write_bytes(raw)
 p.write_bytes(s.replace(old,new).encode());edits.append({'path':name,'old':old,'new':new})
replace('Frontmatter/Abstract.tex',' Operation toward \\SI{240}{\\watt} USB-PD Extended Power Range (EPR) is a longer-term development objective.','')
replace('Chapters/01_Introduction/09_V3_Development.tex','The immediate objective remains \\SI{100}{\\watt}; operation toward\n\\SI{240}{\\watt} USB-PD EPR is a longer-term goal. The design changes and\nremaining checks are described in \\cref{sec:hw-v3-plan}.','The objective remains \\SI{100}{\\watt}. The design changes and remaining\nchecks are described in \\cref{sec:hw-v3-plan}.')
replace('Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex','The immediate objective remains \\SI{100}{\\watt}. Operation toward the\n\\SI{240}{\\watt} USB-PD Extended Power Range (EPR) level is a longer-term\ndevelopment goal. That increase would require the complete power path,\ncontrol, thermal design, and external USB-PD output stage to be checked.\nIt is not a capability demonstrated by the reduced V3 layout.','The objective remains \\SI{100}{\\watt}. Transformer optimization and\nmatched power and thermal tests are needed to assess whether the revised\nconverter can reach this output continuously.')
replace('Chapters/11_Discussion/05_Magnetics_Integration.tex','support the \\SI{100}{\\watt} objective. The longer-term\r\n\\SI{240}{\\watt} EPR goal additionally requires review of the pump,\r\nswitches, tank, rectifiers, control, cooling, and USB-PD output stage.','support the \\SI{100}{\\watt} objective.\r\n\r\nFeedback on the APEC digest raised the question of whether the converter\r\ncould support higher loads, including \\SI{240}{\\watt} USB-PD Extended\r\nPower Range (EPR). Assessing higher-power operation first requires the\r\nsecondary-winding heating and limited power increase in the tested\r\nhigh-load range to be resolved.')
replace('Chapters/12_Conclusion/02_Research_Questions.tex','remain unfinished. The immediate objective is \\SI{100}{\\watt};\r\n\\SI{240}{\\watt} EPR remains a longer-term goal.','remain unfinished. The objective is \\SI{100}{\\watt}.')
replace('Chapters/12_Conclusion/04_Future_Work.tex','\r\nThe longer-term \\SI{240}{\\watt} USB-PD EPR goal requires adequate pump\r\ncharge transfer, switch and capacitor stress margins, rectification,\r\nmagnetic current capability, control range, isolation, cooling, and output\r\nhardware. EPR delivery has not been demonstrated.\r\n','')
replace('README.md','The 100 W target and longer-term 240 W EPR goal are not continuous ratings.','The project target remains 100 W. The question of higher-load operation, including 240 W USB-PD EPR, arose from feedback on the APEC digest.')
(review/'epr-scope-edits.json').write_text(json.dumps(edits,indent=2)+'\n')
print('Corrected EPR scope in',len(edits),'files')
