from pathlib import Path
import json,hashlib,shutil,zipfile,fitz
out=Path('/workspace/tooling/thesis-author-narrative');root=Path('/workspace/thesis')
checks=json.loads((out/'pdf-audit.json').read_text());assert not checks['errors'] and not checks['text_outside_page'] and checks['overfull_boxes']==0
assert len(json.loads((out/'embedded-document-pages.json').read_text()))==35
pdf=out/'Thesis_Corrected_Narrative.pdf';shutil.copy2('/workspace/thesis-build/main.pdf',pdf)
d=fitz.open(pdf); toc=d.get_toc(); first=next(x[2]-1 for x in toc if x[0]==1 and x[1].startswith('1 '));end=next(x[2]-2 for x in toc if x[0]==1 and x[1].startswith('2 ')); intro=fitz.open();intro.insert_pdf(d,from_page=first,to_page=end);intro.save(out/'Introduction_Preview.pdf')
sources=sorted(p for p in root.rglob('*') if p.is_file()); zpath=out/'Thesis_Corrected_Source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sources:z.write(p,p.relative_to(root))
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 assert set(z.namelist())=={p.relative_to(root).as_posix() for p in sources}
 for p in sources:assert hashlib.sha256(z.read(p.relative_to(root).as_posix())).digest()==hashlib.sha256(p.read_bytes()).digest()
a={'pages':len(d),'source_files':len(sources),'intro_pages':len(intro),'artifacts':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [pdf,zpath,out/'Introduction_Preview.pdf']}}
(out/'artifacts.json').write_text(json.dumps(a,indent=2)+'\n');(out/'SHA256SUMS').write_text(''.join(f"{v['sha256']}  {k}\n" for k,v in a['artifacts'].items()))
print(f"PASS: {len(d)}-page thesis, {len(intro)}-page intro and {len(sources)}-file source ZIP; all ZIP members verified")
