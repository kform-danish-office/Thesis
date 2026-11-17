from pathlib import Path
from collections import Counter
import re,json,hashlib,difflib

root=Path('/workspace/thesis')
review=Path('/workspace/tooling/thesis-direct-language')
base=review/'before'
edits=json.loads((review/'early-edits.json').read_text())
patterns={
 'SI quantities':re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+'),
 'math':re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$',re.S),
 'numeric tokens':re.compile(r'\d+(?:\.\d+)*'),
 'labels':re.compile(r'\\label\{[^}]*\}'),
 'references/citations/paths':re.compile(r'\\(?:cite\w*|ref|cref|Cref|eqref|pageref|sourcefile|input|include|includegraphics|lstinputlisting)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+'),
}
envs=['equation','equation*','align','align*','gather','gather*','lstlisting','verbatim','Verbatim','tikzpicture','circuitikz']
rows=[];errors=[];diff=[]
for item in edits:
 rel=item['path'];p=root/rel;q=base/rel;a=q.read_text();b=p.read_text()
 checks={name:Counter(pat.findall(a))==Counter(pat.findall(b)) for name,pat in patterns.items()}
 for env in envs:
  pat=re.compile(r'\\begin\{'+re.escape(env)+r'\}.*?\\end\{'+re.escape(env)+r'\}',re.S)
  checks[env]=pat.findall(a)==pat.findall(b)
 checks['newline_style']=(b'\r\n' in p.read_bytes())==(b'\r\n' in q.read_bytes())
 checks['final_newline']=p.read_bytes().endswith(b'\n')==q.read_bytes().endswith(b'\n')
 checks['table_columns']=a.count('&')==b.count('&')
 for key,value in checks.items():
  if not value:errors.append({'path':rel,'check':key})
 rows.append({'path':rel,'checks':checks,'before_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+rel,tofile='direct/'+rel))
out={'changed_files':len(rows),'replacements':sum(sum(x['occurrences'] for x in r['replacements']) for r in edits),'errors':errors,'files':rows}
(review/'early-validation.json').write_text(json.dumps(out,indent=2)+'\n');(review/'early-prose.diff').write_text(''.join(diff))
print(json.dumps({k:v for k,v in out.items() if k!='files'},indent=2))
assert not errors,errors
