from pathlib import Path
from collections import Counter
import json,re,hashlib,difflib

root=Path('/workspace/thesis')
review=Path('/workspace/tooling/thesis-direct-language')
base=review/'before'
rows=json.loads((review/'control-edits.json').read_text())
paths=sorted({r['path'] for r in rows})
patterns={
 'quantities':r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+',
 'math':r'\\\(.*?\\\)|\\\[.*?\\\]|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$',
 'numeric_tokens':r'\d+(?:\.\d+)*',
 'MCU_pins':r'\bP[A-H]\d+\b',
 'labels':r'\\label\{[^}]*\}',
 'citations':r'\\cite\w*\*?(?:\[[^\]]*\])?\{[^}]*\}',
 'source_paths':r'\\(?:sourcefile|lstinputlisting|input|include|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}',
 'references':r'\\(?:ref|cref|Cref|eqref|pageref)\{[^}]*\}',
}
results=[];errors=[];diff=[]
for name in paths:
 a=(base/name).read_text();b=(root/name).read_text()
 checks={key:Counter(re.findall(pattern,a,re.S))==Counter(re.findall(pattern,b,re.S)) for key,pattern in patterns.items()}
 if name=='Chapters/08_Control_Firmware/14_Version_Comparison.tex':
  assert a.count('V1, V2, and V3')==1 and 'V1, V2, and V3' not in b
  # Remove only the redundant board-version reminder, not numerical data.
  checks['numeric_tokens']=Counter(re.findall(patterns['numeric_tokens'],a.replace('V1, V2, and V3','')))==Counter(re.findall(patterns['numeric_tokens'],b))
 for env in ['equation','equation*','align','align*','tikzpicture','verbatim','Verbatim']:
  p=re.compile(r'\\begin\{'+re.escape(env)+r'\}.*?\\end\{'+re.escape(env)+r'\}',re.S)
  checks[env]=p.findall(a)==p.findall(b)
 p=re.compile(r'\\begin\{lstlisting\}(?:\[[\s\S]*?\])?([\s\S]*?)\\end\{lstlisting\}')
 checks['listing_code']=p.findall(a)==p.findall(b)
 aa=(base/name).read_bytes();bb=(root/name).read_bytes()
 checks['newline_style']=(aa.count(b'\n')-aa.count(b'\r\n')==0)==(bb.count(b'\n')-bb.count(b'\r\n')==0) and (b'\r\n' in aa)==(b'\r\n' in bb)
 checks['final_newline']=aa.endswith(b'\n')==bb.endswith(b'\n')
 row={'path':name,'checks':checks,'before_sha256':hashlib.sha256(aa).hexdigest(),'sha256':hashlib.sha256(bb).hexdigest()}
 results.append(row)
 for check,passed in checks.items():
  if not passed:errors.append({'path':name,'check':check})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+name,tofile='direct/'+name))
out={'edited_files':len(results),'replacements':len(rows),'documented_exceptions':{'Chapters/08_Control_Firmware/14_Version_Comparison.tex':'The redundant V1/V2/V3 hardware-version reminder was removed; those labels are already introduced in Section8.1. All numerical values, software IDs and MCU pins remain unchanged.'},'errors':errors,'files':results}
(review/'control-validation.json').write_text(json.dumps(out,indent=2)+'\n')
(review/'control-prose.diff').write_text(''.join(diff))
print(json.dumps({k:v for k,v in out.items() if k!='files'},indent=2))
assert not errors,errors
