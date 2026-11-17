from pathlib import Path
import json,hashlib,shutil,zipfile,fitz
r=Path('/workspace/tooling/thesis-figure-mcu-edit');root=Path('/workspace/thesis');check=json.loads((r/'pdf-audit.json').read_text());assert not check['errors'] and not check['text_outside_page'] and check['overfull_boxes']==0
assert len(json.loads((r/'embedded-document-pages.json').read_text()))==35
pdf=r/'Thesis_V1_V2_V3.pdf';shutil.copy2('/workspace/thesis-build/main.pdf',pdf)
files=sorted(p for p in root.rglob('*') if p.is_file());zpath=r/'Thesis_V1_V2_V3_Source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.relative_to(root))
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 assert set(z.namelist())=={p.relative_to(root).as_posix() for p in files}
 for p in files:assert hashlib.sha256(z.read(p.relative_to(root).as_posix())).digest()==hashlib.sha256(p.read_bytes()).digest()
a={'pages':check['pages'],'source_files':len(files),'artifacts':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [pdf,zpath]}}
(r/'artifacts.json').write_text(json.dumps(a,indent=2)+'\n');(r/'SHA256SUMS.txt').write_text(''.join(f"{v['sha256']}  {k}\n" for k,v in a['artifacts'].items()))
print(f'PASS: {check["pages"]} pages and {len(files)} source files; archive CRC/member hashes verified')
