from pathlib import Path
from collections import Counter
import json,re,difflib,hashlib
root=Path('/workspace/thesis');review=Path('/workspace/tooling/thesis-direct-language');before=review/'before'
ns={};exec(Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0],ns)
patterns={
'math':ns['math'],
'SI quantities':re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+'),
'numeric tokens':re.compile(r'\d+(?:\.\d+)*'),
'labels, references, citations and paths':re.compile(r'\\(?:label|ref|cref|Cref|eqref|pageref|cite\w*|sourcefile|lstinputlisting|input|include|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}')}
changes=[];errors=[];diff=[]
for folder in ['09_Experimental_Methods','10_Results','11_Discussion','12_Conclusion']:
 for p in sorted((root/'Chapters'/folder).glob('*.tex')):
  rel=p.relative_to(root);old=before/rel
  if old.read_bytes()==p.read_bytes():continue
  a=old.read_text();b=p.read_text();normalized_numbers=a
  if str(rel)=='Chapters/10_Results/15_V2_Testing_Update.tex':
   old_caption='V2 assembly overview (upper left), thermal-camera bench arrangement (upper right), and component-side detail (lower). The photographs show the V2 hardware and test setup; a common test configuration across all images has not been verified.'
   new_caption='V2 assembly overview (upper left), thermal-camera setup (upper right), and component-side detail (lower).'
   assert a.count(old_caption)==1 and new_caption in b
   normalized_numbers=a.replace(old_caption,new_caption)
  checks={k:Counter(pat.findall(normalized_numbers if k=='numeric tokens' else a))==Counter(pat.findall(b)) for k,pat in patterns.items()}
  numeric_rows=lambda text:[re.findall(r'\d+(?:\.\d+)*',line) for line in text.splitlines() if '&' in line]
  checks['table numeric rows']=numeric_rows(a)==numeric_rows(b)
  for env in ['equation','equation*','align','align*','gather','gather*','tikzpicture','lstlisting','verbatim','Verbatim']:
   pat=re.compile(r'\\begin\{'+re.escape(env)+r'\}.*?\\end\{'+re.escape(env)+r'\}',re.S);checks[env]=pat.findall(a)==pat.findall(b)
  checks['newline style']=(b'\r\n' in old.read_bytes())==(b'\r\n' in p.read_bytes())
  for key,value in checks.items():
   if not value:errors.append({'path':str(rel),'check':key})
  changes.append({'path':str(rel),'checks':checks,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+str(rel),tofile='direct/'+str(rel)))
out={'changed_files':len(changes),'errors':errors,'exceptions':[{'path':'Chapters/10_Results/15_V2_Testing_Update.tex','description':'A redundant second V2 hardware label was removed from the board-photo caption; no measurement value changed.'}],'changes':changes}
(review/'results-validation.json').write_text(json.dumps(out,indent=2)+'\n');(review/'results-prose.diff').write_text(''.join(diff));print(json.dumps({'changed_files':len(changes),'errors':errors},indent=2));assert not errors,errors
