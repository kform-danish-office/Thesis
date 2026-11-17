from pathlib import Path
import shutil,json
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-firmware-204');changes=[]
def change(n,old,new):
 p=root/n;s=p.read_bytes().decode();assert old in s,n
 b=r/'before'/n;b.parent.mkdir(parents=True,exist_ok=True)
 if not b.exists():shutil.copy2(p,b)
 p.write_bytes(s.replace(old,new).encode());changes.append(n)
change('Chapters/01_Introduction/10_Controller_Basics.tex','burst modulation of the fixed-frequency half bridge.','burst modulation of the half bridge.')
change('Chapters/08_Control_Firmware/14_Version_Comparison.tex','Final baseline & Burst-edge alignment attempts, startup precharge, no-load guard, and loaded duty trim & Limit commanded energy at startup and no load, reduce continued charging after load removal, and adjust transfer as load changes\\\\','Final baseline & Burst-edge alignment attempts, startup precharge, no-load guard, and loaded duty trim & Limit commanded energy at startup and no load, reduce continued charging after load removal, and adjust transfer as load changes\\\\\nV2 calibration and setup & Browser calibration, reference-load settings, and output-OFF carrier timing & Repeat duty searches for known loads and vary switching frequency and dead time without rebuilding the firmware\\\\')
change('Chapters/12_Conclusion/03_Contributions.tex','were adapted, and a flash settings journal, browser commands, and logging\r\nwere implemented.','were adapted, and a flash settings journal, browser commands, and logging\r\nwere implemented. Browser calibration and editable reference-load settings\r\nwere then added to repeat the duty search for connected test loads. Carrier\r\nfrequency and dead time can be set together with output disabled, allowing\r\nswitching conditions to be varied without rebuilding the firmware.')
change('Chapters/12_Conclusion/03_Contributions.tex','the firmware version used on the bench was not recorded, and comparable\r\npower and thermal-endurance tests are still needed.','powered tests of the later adjustable firmware and comparable power and\r\nthermal-endurance measurements are still needed.')
(r/'context-edited-files.json').write_text(json.dumps(changes,indent=2)+'\n')
