from pathlib import Path
import hashlib,json,difflib,re,zipfile,fitz
r=Path('/workspace/thesis'); review=Path('/workspace/tooling/v2-specs-update'); before=review/'before'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(before).as_posix():p for p in before.rglob('*') if p.is_file()}; new={p.relative_to(r).as_posix():p for p in r.rglob('*') if p.is_file()}
assert set(old)<=set(new)
changes=[];diff=[]
helpers=Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0]
ns={};exec(helpers,ns)
allowed_table_label='tab:app-revision-register'
for name,oldp in old.items():
 p=new[name]
 if sha(oldp)==sha(p):continue
 assert p.suffix=='.tex',('non-TeX changed',name)
 assert name.startswith(('Frontmatter/','Chapters/01_Introduction/','Chapters/07_Hardware/','Chapters/11_Discussion/','Chapters/12_Conclusion/','Backmatter/Appendices/'))
 a=oldp.read_text();b=p.read_text()
 assert ns['math'].findall(a)==ns['math'].findall(b),('math altered',name)
 assert set(re.findall(r'\\label\{([^}]+)\}',a))<=set(re.findall(r'\\label\{([^}]+)\}',b)),('label removed',name)
 for e in ns['environments'](a):
  if name == 'Backmatter/Appendices/B_Hardware_Documentation.tex' and (allowed_table_label in e or 'V2 F410 schematic & Four-sheet export' in e): continue
  assert e in b,('existing figure/table/equation changed',name,e[:90])
 changes.append({'path':name,'before_sha256':sha(oldp),'sha256':sha(p)})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+name,tofile='current/'+name))
added=sorted(set(new)-set(old))
assert added==sorted(['Chapters/01_Introduction/08_V2_Prototype.tex','Pictures/Thesis/07_Hardware/Schematic_V2_F410_2026-10-27.pdf','Pictures/Thesis/07_Hardware/PCB_V2_F410_2026-10-27.pdf','Pictures/Thesis/07_Hardware/V2_2026-10-27_provenance.json']),added
append=(r/'Backmatter/Appendices/B_Hardware_Documentation.tex').read_text()
for base,count in [('Schematic',4),('PCB',31)]:
 name=f'{base}_V2_F410_2026-10-27.pdf'
 included=[int(x) for x in re.findall(r'\\includegraphics\[page=(\d+),[^\]]+\]\{Pictures/Thesis/07_Hardware/'+re.escape(name)+r'\}',append)]
 assert included==list(range(1,count+1)),(base,included)
 assert len(fitz.open(r/'Pictures/Thesis/07_Hardware'/name))==count
provenance=json.loads((r/'Pictures/Thesis/07_Hardware/V2_2026-10-27_provenance.json').read_text())
with zipfile.ZipFile('/workspace/source-archives/'+provenance['archive']) as z:
 assert z.testzip() is None
 for row in provenance['files']:
  assert hashlib.sha256(z.read(row['archive_member'])).hexdigest()==sha(r/row['retained_path'])==row['sha256']
report={'baseline_files':len(old),'current_files':len(new),'edited_files':len(changes),'added_files':added,'unchanged_files':len(old)-len(changes),'changes':changes,'preserved':'All earlier non-TeX assets, equations, labels, tables/figures except the documented AppendixB revision register; all35 new source document pages included exactly once in AppendixB.'}
(review/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n');(review/'v2-specs.diff').write_text(''.join(diff))
print({k:v for k,v in report.items() if k!='changes'})
