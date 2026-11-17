from pathlib import Path
from collections import Counter
import re,json,difflib
r=Path('/workspace/tooling/usb-pd-wording-review');root=Path('/workspace/thesis');base=r/'before'
rows=json.loads((r/'control-edits.json').read_text());names=sorted(set(x['path'] for x in rows));ns={}
exec(Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0],ns)
patterns={
 'SI expressions':r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+',
 'labels':r'\\label\{[^}]*\}',
 'citations':r'\\cite\w*\*?(?:\[[^\]]*\])?\{[^}]*\}',
 'refs and paths':r'\\(?:ref|cref|Cref|eqref|pageref|sourcefile|lstinputlisting|input|include|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}',
 'numeric tokens':r'\d+(?:\.\d+)*'
}
errors=[];checks=[];diff=[]
for rel in names:
 a=(base/rel).read_bytes();b=(root/rel).read_bytes();aa=a.decode();bb=b.decode();check={'path':rel}
 check['math']=Counter(ns['math'].findall(aa))==Counter(ns['math'].findall(bb))
 check['protected environments']=ns['environments'](aa)==ns['environments'](bb)
 for key,pat in patterns.items():check[key]=Counter(re.findall(pat,aa))==Counter(re.findall(pat,bb))
 check['line ending style']=(b'\r\n' in a,b'\n' in a.replace(b'\r\n',b''))==(b'\r\n' in b,b'\n' in b.replace(b'\r\n',b''))
 check['final newline']=a.endswith(b'\n')==b.endswith(b'\n')
 errors.extend((rel,key) for key,passed in check.items() if key!='path' and not passed);checks.append(check)
 diff.extend(difflib.unified_diff(aa.splitlines(True),bb.splitlines(True),fromfile='before/'+rel,tofile='corrected/'+rel))
(r/'control-validation.json').write_text(json.dumps({'files':len(names),'errors':errors,'checks':checks},indent=2)+'\n')
(r/'control-prose.diff').write_text(''.join(diff));print('Files:',len(names),'Errors:',errors);assert not errors
