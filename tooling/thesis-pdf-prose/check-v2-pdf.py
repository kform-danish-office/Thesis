from pathlib import Path
import fitz,json,re,hashlib
r=Path('/workspace/tooling/thesis-pdf-prose');d=fitz.open('/workspace/thesis-build/main.pdf')
chapter_start=next(x[2]-1 for x in d.get_toc() if x[1].startswith('10 '))
start=next(i for i in range(chapter_start,len(d)) if 'Secondary-Output Load and Thermal Tests' in d[i].get_text())
end=next(i for i in range(start,len(d)) if 'Next Layout Changes' in d[i].get_text())
print('New V2 section PDF pages',start+1,'through',end)
results=[];out=r/'v2-page-previews';out.mkdir(exist_ok=True)
for i in range(start,end):
 p=d[i];p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(out/f'{i+1:03}.png');imgs=[]
 for item in p.get_images():
  raw=d.extract_image(item[0]);imgs.append({'xref':item[0],'width':raw['width'],'height':raw['height'],'sha256':hashlib.sha256(raw['image']).hexdigest()})
 results.append({'page':i+1,'text':p.get_text(),'images':imgs})
manifest=json.loads((Path('/workspace/tooling/thesis-v2-load-thermal/thermal-import-manifest.json')).read_text());wanted={x['sha256']:x['member'] for x in manifest['members']}
found={}
for row in results:
 for img in row['images']:
  if img['sha256'] in wanted:found.setdefault(img['sha256'],[]).append(row['page'])
assert set(found)==set(wanted),{'missing':set(wanted)-set(found)}
assert all(len(p)==1 for p in found.values()),found
text=' '.join(x['text'] for x in results)
for c in ['015','017','018','019','020','021','022']:
 assert text.count('Capture '+c+':')==1,c
for phrase in ['None of the load points reached thermal equilibrium','voltage droop','83.9','98.3','137.08']:
 assert phrase in text,phrase
log=Path('/workspace/thesis-build/main.log').read_text(errors='replace');over=re.findall(r'Overfull \\[hv]box[^\n]*',log);assert not over,over
report={'pages':results,'original_thermal_images':[{ 'file':wanted[h],'page':pages[0],'sha256':h} for h,pages in found.items()],'overfull_hbox_vbox':over}
(r/'v2-pdf-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: all seven original JPEGs embedded unchanged exactly once; no overfull horizontal or vertical boxes.')
print('Rendered:',*[str(out/f'{i+1:03}.png') for i in range(start,end)])
