"""Audit the V2 schematic display change without modifying thesis source."""
from pathlib import Path
from collections import Counter
import difflib, hashlib, json, re
import fitz

root=Path('/workspace/thesis');review=Path('/workspace/tooling/v2-main-schematics');before=review/'before'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(before).as_posix():p for p in before.rglob('*') if p.is_file()}
new={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()}
assert old.keys()<=new.keys()
added=sorted(new.keys()-old.keys())
assert set(added)=={f'Pictures/Thesis/07_Hardware/Rebuilt/schematic_v2_{name}_excerpt.pdf' for name in ['power_stage','input','usb','controller']},added
ns={};exec(Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0],ns)
labels=json.loads((review/'label-migration.json').read_text())
patterns={
 'math':ns['math'],
 'quantities':re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+'),
 'citations':re.compile(r'\\cite\w*\*?(?:\[[^\]]*\])?\{[^}]*\}'),
 'labels':re.compile(r'\\label\{[^}]*\}'),
 'source_paths':re.compile(r'\\(?:sourcefile|lstinputlisting|input|include)(?:\[[^\]]*\])?\{[^}]*\}'),
}
changes=[];diff=[]
for rel,op in sorted(old.items()):
 np=new[rel]
 if sha(op)==sha(np):continue
 assert rel.endswith('.tex'),('Original nonprose asset changed',rel)
 a=op.read_text();b=np.read_text();normalized=a
 for left,right in labels.items():normalized=normalized.replace(left,right)
 for kind,pat in patterns.items():assert Counter(pat.findall(normalized))==Counter(pat.findall(b)),(rel,kind)
 for env in ['table','table*','equation','equation*','align','align*','lstlisting','verbatim','Verbatim','tikzpicture']:
  pat=re.compile(r'\\begin\{'+re.escape(env)+r'\}.*?\\end\{'+re.escape(env)+r'\}',re.S)
  normalized_table=normalized.replace('Corrected circuit reference and revision comparison','Bring-up correction record and revision comparison')
  assert pat.findall(normalized_table)==pat.findall(b),(rel,env)
 changes.append({'path':rel,'before_sha256':sha(op),'sha256':sha(np)})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+rel,tofile='v2-drawings/'+rel))
main='\n'.join(p.read_text() for p in (root/'Chapters').rglob('*.tex'))
assert 'schematic_v11_' not in main
for oldlabel in labels:assert oldlabel not in main
assert main.count('schematic_v2_')==6
for path in added:
 d=fitz.open(new[path]);expected=2 if '_input_' in path else 1;assert len(d)==expected
 for page in d:
  assert page.get_xobjects(),('Not an embedded vector page',path)
  assert not [img for img in page.get_image_info() if (fitz.Rect(img['bbox']) & page.rect).get_area()>0],('Visible raster image introduced',path)
  assert page.get_text().strip(),('Missing extractable circuit labels',path)
result={'baseline_files':len(old),'current_files':len(new),'changed_files':changes,'added_files':[{'path':p,'sha256':sha(new[p])} for p in added],'unchanged_files':len(old)-len(changes),'main_schematic_inclusions':6,'figure_label_migration':labels,'checks':'Existing nonprose assets, code, measurements, math, quantities, citations and source inclusions unchanged. Only V2 figure substitutions, captions and locally necessary context edited. Four vector-only crop files added; original full PDFs and appendices retained.'}
(review/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');(review/'schematic-display.diff').write_text(''.join(diff))
print('PASS:',len(changes),'TeX files edited;',len(added),'new vector PDFs;',len(old)-len(changes),'source files unchanged;',len(new),'total files')
