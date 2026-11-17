from pathlib import Path
import fitz,shutil,zipfile,json,hashlib
out=Path('/workspace/tooling/v2-cover'); r=Path('/workspace/thesis'); doc=fitz.open('/workspace/thesis-build/main.pdf')
cover=fitz.open(); cover.insert_pdf(doc,from_page=0,to_page=0); cover.save(out/'V2_Cover.pdf'); doc[0].get_pixmap(matrix=fitz.Matrix(1,1)).save(out/'cover-preview.png')
shutil.copy2('/workspace/thesis-build/main.pdf',out/'Thesis_V2_Cover.pdf')
with zipfile.ZipFile(out/'Thesis_V2_Cover_Source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(r.rglob('*')):
  if p.is_file(): z.write(p,p.relative_to(r))
with zipfile.ZipFile(out/'Thesis_V2_Cover_Source.zip') as z: assert z.testzip() is None
(out/'artifacts.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.suffix in ['.pdf','.zip']},indent=2)+'\n')
print('PDF pages:',len(doc))
