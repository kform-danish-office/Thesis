"""Check the focused prose review against the frozen current thesis."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,difflib

root=Path('/workspace/thesis');review=Path('/workspace/tooling/usb-pd-wording-review');before=review/'before'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(before).as_posix():p for p in before.rglob('*') if p.is_file()}
new={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()}
assert old.keys()==new.keys(), 'Source paths changed'
ns={};exec(Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0],ns)
patterns={
 'math':ns['math'],
 'quantities':re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+'),
 'numeric_tokens':re.compile(r'\d+(?:\.\d+)*'),
 'labels':re.compile(r'\\label\{[^}]*\}'),
 'citations':re.compile(r'\\cite\w*\*?(?:\[[^\]]*\])?\{[^}]*\}'),
 'source_paths':re.compile(r'\\(?:sourcefile|lstinputlisting|input|include|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}'),
}
changes=[];errors=[];diff=[]
for rel,a in sorted(old.items()):
 b=new[rel]
 if sha(a)==sha(b):continue
 assert rel.endswith('.tex') and rel.startswith(('Chapters/','Frontmatter/','Backmatter/Appendices/')),('Outside prose scope',rel)
 left=a.read_text();right=b.read_text()
 checks={key:Counter(pat.findall(left))==Counter(pat.findall(right)) for key,pat in patterns.items()}
 checks['protected_environments']=ns['environments'](left)==ns['environments'](right)
 checks['commands_and_arguments']=Counter((x,tuple(y)) for x,y in ns['macros'](left))==Counter((x,tuple(y)) for x,y in ns['macros'](right))
 checks['newline_style']=(b'\r\n' in a.read_bytes())==(b'\r\n' in b.read_bytes())
 for key,value in checks.items():
  if not value:errors.append({'path':rel,'check':key})
 changes.append({'path':rel,'before_sha256':sha(a),'sha256':sha(b),'checks':checks})
 diff.extend(difflib.unified_diff(left.splitlines(True),right.splitlines(True),fromfile='before/'+rel,tofile='clear-prose/'+rel))
intro=(root/'Chapters/01_Introduction/10_Controller_Basics.tex').read_text()
assert 'connector VBUS independently' not in intro
assert 'These nodes are distinguished' not in intro
assert 'selected PD level' in intro and 'secondary bulk voltage' in intro
mot=(root/'Chapters/01_Introduction/01_Motivation.tex').read_text()
assert 'MHz switching' not in mot and 'MHz operation' not in mot
assert 'megahertz frequencies' in mot and r'\SI{1}{\mega\hertz}' in mot
result={'baseline_files':len(old),'current_files':len(new),'edited_files':len(changes),'unchanged_files':len(old)-len(changes),'changes':changes,'errors':errors,'checks':'All source paths, nonprose assets, raw data, code, tables/figures, mathematical content, numeric tokens and LaTeX arguments preserved. Stage-regulation roles and unit prose clarified.'}
(review/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');(review/'wording.diff').write_text(''.join(diff))
print(json.dumps({k:v for k,v in result.items() if k not in {'changes'}},indent=2))
assert not errors,errors
