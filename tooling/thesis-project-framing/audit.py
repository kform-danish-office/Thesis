from pathlib import Path
from collections import Counter
import hashlib,json,re,difflib

root=Path('/workspace/thesis');review=Path('/workspace/tooling/thesis-project-framing');base=review/'before'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(base).as_posix():p for p in base.rglob('*') if p.is_file()}
new={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()}
assert old.keys()==new.keys()
edits={x['path']:x for x in json.loads((review/'edits.json').read_text())}
patterns={
 'math':re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$',re.S),
 'quantities':re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+'),
 'labels_refs_citations_paths':re.compile(r'\\(?:label|ref|cref|Cref|cite\w*|sourcefile|input|include|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}')
}
changes=[];diff=[]
for rel,op in sorted(old.items()):
 np=new[rel]
 if sha(op)==sha(np):continue
 assert rel in edits,rel
 row=edits[rel];assert op.read_bytes().replace(row['before'].encode(),row['after'].encode())==np.read_bytes(),rel
 a=op.read_text();b=np.read_text()
 for name,pat in patterns.items():assert Counter(pat.findall(a))==Counter(pat.findall(b)),(rel,name)
 changes.append({'path':rel,'before_sha256':sha(op),'sha256':sha(np)})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+rel,tofile='correct-framing/'+rel))
assert len(changes)==9
for folder in ['Chapters','Frontmatter','Backmatter','Setup']:
 for path in (root/folder).rglob('*.tex'):
  assert not re.search(r'\b(?:laboratory|lab|bench)\s+(?:power\s+)?supply\b',path.read_text(),re.I),str(path)
assert 'The main change was the load:' in (root/'Chapters/01_Introduction/chapter.tex').read_text()
result={'source_files':len(new),'edited_files':len(changes),'unchanged_files':len(new)-len(changes),'changes':changes,'checks':'Exact nine wording replacements only; original load-focused opening restored in established impersonal voice. All numerical quantities, math, citations, labels, inclusions, assets, data and code unchanged. No lab-supply project framing remains in authored TeX.'}
(review/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');(review/'framing.diff').write_text(''.join(diff));print({k:v for k,v in result.items() if k!='changes'})
