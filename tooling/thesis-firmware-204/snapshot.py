from pathlib import Path
import shutil,json,hashlib,re
src=Path('/workspace/working-source');root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-firmware-204');dest=root/'Code/PWR_2_0_4'
# Freeze editable source, its build tools and browser runtime; omit generated outputs and deployment history.
files=[src/'thesi_power_control.ino',src/'README.md']
files += [p for p in (src/'docs').rglob('*') if p.is_file()]
files += [p for p in (src/'firmware').iterdir() if p.is_file()]
files += [p for p in (src/'firmware/releases').glob('*.md')]
for p in (src/'web').rglob('*'):
 rel=p.relative_to(src/'web')
 if p.is_file() and (len(rel.parts)==1 and (p.suffix in {'.html','.css','.js','.mjs'} or p.name in {'package.json','vercel.json','README.md'}) or rel.parts[0] in {'tests','fonts'}):files.append(p)
rows=[]
for p in sorted(set(files)):
 d=dest/p.relative_to(src);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
 rows.append({'source':p.relative_to(src).as_posix(),'copy':d.relative_to(root).as_posix(),'bytes':d.stat().st_size,'lines':len(d.read_bytes().splitlines()) if d.suffix not in {'.ttf','.png'} else None,'sha256':hashlib.sha256(d.read_bytes()).hexdigest(),'kind':'source' if d.suffix in {'.ino','.js','.mjs','.css','.html','.json','.py','.ps1','.ld'} else 'reference'})
old=root/'Code/source_manifest.json';backup=r/'before/Code/source_manifest.json';backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(old,backup)
shutil.copy2(old,root/'Code/PWR_2_0_1/source_manifest.json')
baseline=root/'Code/thesi_power_control_PWR_1_9_20.ino'
rows.append({'source':'baseline PWR-1.9.20','copy':baseline.relative_to(root).as_posix(),'bytes':baseline.stat().st_size,'lines':len(baseline.read_bytes().splitlines()),'sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),'kind':'source'})
old.write_text(json.dumps({'firmware':'PWR-2.0.4 (F410); PWR-2.0.3 (G071 target)','historical_manifest':'Code/PWR_2_0_1/source_manifest.json','files':rows},indent=2)+'\n')
shutil.copy2(root/'Code/software_verification.json',r/'before/Code/software_verification.json');shutil.copy2(root/'Code/software_verification.json',root/'Code/PWR_2_0_1/software_verification.json')
(r/'snapshot-files.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Frozen',len(rows)-1,'current files;',len((dest/'thesi_power_control.ino').read_bytes().splitlines()),'firmware lines')
