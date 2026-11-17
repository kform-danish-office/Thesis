from pathlib import Path
import fitz,shutil,json,hashlib,zipfile
out=Path('/workspace/tooling/v2-photos-95w'); source=Path('/workspace/thesis'); pdf=Path('/workspace/thesis-build/main.pdf')
doc=fitz.open(pdf)
start=next(i for i,p in enumerate(doc) if 'V2 Testing and Resononant' in p.get_text()) if False else next(i for i,p in enumerate(doc) if 'The V2 prototype was first tested' in p.get_text())
end=next(i for i,p in enumerate(doc) if i >= start and 'V2 assembly overview (upper left)' in p.get_text())
text='\n'.join(doc[i].get_text() for i in range(start,end+1))
assert '95 W' in text
assert len(doc[end].get_images())>=3
excerpt=fitz.open(); excerpt.insert_pdf(doc,from_page=start,to_page=end); excerpt.save(out/'V2_Testing_Photos_95W.pdf')
shutil.copy2(pdf,out/'Thesis_V2_Photos_95W.pdf')
doc[end].get_pixmap(matrix=fitz.Matrix(1,1)).save(out/'photo-page.png')
with zipfile.ZipFile(out/'Thesis_V2_Photos_95W_Source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(source.rglob('*')):
  if p.is_file(): z.write(p,p.relative_to(source))
with zipfile.ZipFile(out/'Thesis_V2_Photos_95W_Source.zip') as z: assert z.testzip() is None
artifacts={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in out.iterdir() if p.suffix in ('.pdf','.zip')}
(out/'artifacts.json').write_text(json.dumps({'thesis_pages':len(doc),'excerpt_physical_pages':[start+1,end+1],'artifacts':artifacts},indent=2)+'\n')
print(len(doc),'pages; excerpt',start+1,end+1)
