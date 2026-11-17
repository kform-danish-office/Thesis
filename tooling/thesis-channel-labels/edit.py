from pathlib import Path
import json,hashlib
root=Path('/workspace/thesis');out=Path('/workspace/tooling/thesis-channel-labels'); edits=[]
def change(name,old,new):
 p=root/name;b=p.read_bytes();s=b.decode();assert old in s,name
 backup=out/'before'/name;backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():backup.write_bytes(b)
 p.write_bytes(s.replace(old,new).encode());edits.append({'path':name,'old':old,'new':new})
change('Chapters/08_Control_Firmware/chapter.tex','MCU port with browser commands and logging. The later bench-run version was not recorded.','MCU port with browser commands and logging.')
for name,old,new in [
('01_Introduction/07_Thesis_Structure.tex','what changes with a USB-C load','the requirements of powering a USB-C device'),
('02_Background/08_Research_Gap.tex','a supply with a detachable USB-C load','a power supply for USB-C devices that can be connected and disconnected during operation'),
('02_Background/07_USBC_Context.tex','Changes in USB-C load','Changes in current drawn from the USB-C output'),
('02_Background/06_Reference_2021.tex','A detachable USB-C load requires','Powering a USB-C device requires'),
('03_Requirements_Architecture/chapter.tex','The USB-C load requires','Supplying a USB-C device requires')]:change('Chapters/'+name,old,new)
legend='Yellow: half-bridge switch-node voltage. Green: secondary output voltage. Blue: USB-C VBUS output voltage.'
change('Chapters/10_Results/03_Steady_State.tex','The source notes identify yellow as the switch node, green as the secondary bulk voltage, and blue as USB-C VBUS. The complete capture groups are included with the test data.',legend)
change('Chapters/10_Results/03_Steady_State.tex','AC-coupled output-detail captures. CH1 is DC-coupled; CH2 and CH3 do not show absolute secondary-bus or VBUS voltage.','Output ripple captures. '+legend+' The yellow trace is DC-coupled; the green and blue traces are AC-coupled and show voltage ripple.')
change('Chapters/10_Results/04_Load_Transients.tex','Voltage response during load removal. Load current and firmware state were not recorded simultaneously with these traces.','Voltage response during load removal. '+legend)
(out/'edits.json').write_text(json.dumps(edits,indent=2)+'\n')
p=Path('/workspace/tooling/thesis-change-manifest.json');m=json.loads(p.read_text())
for e in m:
 if e['path'] in {x['path'] for x in edits}:e['sha256']=hashlib.sha256((root/e['path']).read_bytes()).hexdigest()
p.write_text(json.dumps(m,indent=2)+'\n')
