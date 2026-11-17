from pathlib import Path
import json,hashlib,re,difflib
root=Path('/workspace/thesis');rev=Path('/workspace/tooling/thesis-figure-mcu-edit');before=rev/'before';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(before).as_posix():p for p in before.rglob('*') if p.is_file()};new={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()};assert old.keys()==new.keys()
helpers=Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0];ns={};exec(helpers,ns)
math=ns['math'];quant=re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+');labels=re.compile(r'\\label\{([^}]*)\}');graphics=re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}');cites=re.compile(r'\\cite\w*\*?(?:\[[^\]]*\])?\{[^}]*\}')
changes=[];diff=[];removed_label='fig:no-load-switching-quality-photos';figure_file='Chapters/10_Results/05_Open_Circuit.tex';figure=(rev/'removed-figure.tex').read_text()
for name,p in old.items():
 q=new[name]
 if sha(p)==sha(q):continue
 assert name.endswith('.tex'),('non-prose changed',name)
 a=p.read_text();b=q.read_text();a_check=a.replace(figure,'') if name==figure_file else a
 for kind,pattern in [('math',math),('quantities',quant),('labels',labels),('graphics',graphics),('citations',cites)]:assert pattern.findall(a_check)==pattern.findall(b),(name,kind)
 for env in ['verbatim','Verbatim','tikzpicture','equation','equation*','align','align*']:
  pat=re.compile(r'\\begin\{'+re.escape(env)+r'\}.*?\\end\{'+re.escape(env)+r'\}',re.S);assert pat.findall(a_check)==pat.findall(b),(name,env)
 code_pattern=re.compile(r'\\begin\{lstlisting\}(?:\[[\s\S]*?\])?([\s\S]*?)\\end\{lstlisting\}')
 assert code_pattern.findall(a_check)==code_pattern.findall(b),(name,'listing content')
 changes.append({'path':name,'before_sha256':sha(p),'sha256':sha(q)})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+name,tofile='revised/'+name))
body='\n'.join(p.read_text() for p in root.rglob('*.tex') if 'Code' not in p.relative_to(root).parts)
for token in [removed_label,'partial_switching_removed_scope_crop.png','no_load_clean_switching_scope_crop.png']:
 assert token not in body,token
a=(before/'Chapters/10_Results/06_ZVS.tex').read_text();b=(root/'Chapters/10_Results/06_ZVS.tex').read_text();row=next(line for line in a.splitlines(True) if line.startswith('No-load development photographs &'));assert row not in b
for env in ns['environments'](a):
 if 'Replotted raw C2 exports' in env:assert env in b,'Raw C2 figure changed'
result={'baseline_files':len(old),'current_files':len(new),'edited_files':len(changes),'unchanged_files':len(new)-len(changes),'changes':changes,'checks':'Only requested figure block and its label/graphics removed. No dangling source reference. Raw C2 waveform figure, all original evidence/assets/code, mathematical expressions, numerical quantities, remaining labels/graphics and citations preserved.'}
(rev/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');(rev/'wording.diff').write_text(''.join(diff));print({k:v for k,v in result.items() if k!='changes'})
