from pathlib import Path
import json,hashlib,shutil,zipfile
out=Path('/workspace/tooling/thesis-natural-voice'); root=Path('/workspace/thesis')
assert not json.loads((out/'prose-audit.json').read_text())['errors']
checks=json.loads((out/'pdf-audit.json').read_text()); assert not checks['errors'] and not checks['text_outside_page'] and not checks['overfull_boxes']
pdf=out/'Thesis_Natural_Voice.pdf'; shutil.copy2('/workspace/thesis-build/main.pdf',pdf)
sources=sorted(p for p in root.rglob('*') if p.is_file()); source_zip=out/'Thesis_Natural_Voice_Source.zip'
with zipfile.ZipFile(source_zip,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sources: z.write(p,p.relative_to(root))
with zipfile.ZipFile(source_zip) as z:
 assert z.testzip() is None
 assert set(z.namelist())=={p.relative_to(root).as_posix() for p in sources}
 for p in sources:
  assert hashlib.sha256(z.read(p.relative_to(root).as_posix())).digest()==hashlib.sha256(p.read_bytes()).digest()
a={'pages':checks['pages'],'source_files':len(sources),'artifacts':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [pdf,source_zip]}}
(out/'artifacts.json').write_text(json.dumps(a,indent=2)+'\n')
(out/'SHA256SUMS').write_text(''.join(f"{v['sha256']}  {k}\n" for k,v in a['artifacts'].items()))
print(f"Packaged {checks['pages']} pages and {len(sources)} source files; archive CRC and all member hashes verified")
