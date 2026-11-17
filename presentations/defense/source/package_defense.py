"""Package the editable defense, preview, notes and reproducible build source."""
from pathlib import Path
import hashlib,json,shutil,zipfile
R=Path(__file__).resolve().parent;NAME='Thesis_Defense_Supervisor_Flow';DOWNLOAD='Defense_Supervisor_Flow'
assert (R/'review/final-review.json').exists(), 'Complete the rendered-deck review first.'
review=json.loads((R/'review/final-review.json').read_text())
assert review['decision']=='Accept', 'Resolve the final review before packaging.'
for ext in ['pptx','pdf']:
 assert hashlib.sha256((R/(NAME+'.'+ext)).read_bytes()).hexdigest()==review['artifacts'][ext]['sha256'], 'Review the current '+ext+' before packaging.'
v=json.loads((R/'review/validation.json').read_text());assert v['slides']==20 and v['main_slides']==16
scripts=['build_defense.py','focused_layouts.py','deck_tools.py','equation_math.py','circuit_tools.py','chart_tools.py','master_circuit.py','prior_layouts.py','legacy_layouts.py','render_defense.py','validate_defense.py','package_defense.py']
files=[R/n for n in scripts+['README.md','requirements.txt','manifest.json','Speaker_Notes.md']]
assets=['original-digest-results.png','iec-harmonic-figure.json','adapter-scale.json','thermal_intermediate.jpg','v2_board.png','original-digest-power-stage.png','adapter_5w.jpg','adapter_20w.jpg','adapter_140w.jpg','v1_scope_5v_3a.png','v1_scope_20v_4p7a.png','v1_thermal_20v_4p7a.png','thermal_final.jpg','v2_complete_power_schematic.png','v2_complete_power_schematic.pdf','v2_schematic.pdf','v1_dc_operating_points.csv','v1_power_quality.csv','v1_efficiency.csv','v2_summary.csv']
files += [R/'assets'/n for n in assets]
files += [R/'review/iec-research/source-notes.md']
files += [R/'template'/n for n in ['DTU_Blue_base.pptx','DTU Template 16_9 - Blue EN.potx']]
files += sorted((R/'proposals').glob('*.json'))
files += [R/'review'/n for n in ['adapter-photo-downloads.json','text-judgments.json','final-review.json','final-review.md','validation.json','thesis-baseline.json']]
source=R/(NAME+'_Source.zip')
with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(set(files)):z.write(p,p.relative_to(R))
with zipfile.ZipFile(source) as z:assert z.testzip() is None
for ext in ['pptx','pdf']:shutil.copy2(R/(NAME+'.'+ext),Path('/workspace')/(DOWNLOAD+'.'+ext))
shutil.copy2(source,Path('/workspace')/(DOWNLOAD+'_Source.zip'))
with zipfile.ZipFile(Path('/workspace')/(DOWNLOAD+'.zip'),'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for ext in ['pptx','pdf']:z.write(Path('/workspace')/(DOWNLOAD+'.'+ext),DOWNLOAD+'.'+ext)
 z.write(R/'Speaker_Notes.md','Speaker_Notes.md');z.write(source,'Build_Source.zip')
 z.writestr('OPEN_THIS_FIRST.txt','Open '+DOWNLOAD+'.pptx for the editable slides and speaker notes.\n16 main slides are planned for approximately 25 minutes, followed by four result/reference backups.\nThe PDF is a preview. Build_Source.zip contains the scripts, data, images and original DTU template.\n')
with zipfile.ZipFile(Path('/workspace')/(DOWNLOAD+'.zip')) as z:assert z.testzip() is None
records=[]
for suffix in ['.pptx','.pdf','.zip','_Source.zip']:
 p=Path('/workspace')/(DOWNLOAD+suffix);p.chmod(0o644);records.append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(R/'review/downloads.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records,indent=2))
