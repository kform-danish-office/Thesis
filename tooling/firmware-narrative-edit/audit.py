from pathlib import Path
import hashlib,json,re,difflib
r=Path('/workspace/thesis');rev=Path('/workspace/tooling/firmware-narrative-edit');before=rev/'before';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(before).as_posix():p for p in before.rglob('*') if p.is_file()};new={p.relative_to(r).as_posix():p for p in r.rglob('*') if p.is_file()};assert old.keys()==new.keys()
helpers=Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0];ns={};exec(helpers,ns)
math=ns['math'];quant=re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+');labels=re.compile(r'\\label\{([^}]*)\}');graphics=re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}');paths=re.compile(r'\\(?:sourcefile|lstinputlisting|input|include)(?:\[[^\]]*\])?\{[^}]*\}');cites=re.compile(r'\\cite\w*\*?(?:\[[^\]]*\])?\{[^}]*\}')
changes=[];diff=[]
for name,p in old.items():
 q=new[name]
 if sha(p)==sha(q):continue
 assert name.endswith('.tex'),('nonprose changed',name)
 a=p.read_text();b=q.read_text()
 for kind,pat in [('math',math),('quantities',quant),('graphics',graphics),('source paths',paths),('citations',cites)]:assert pat.findall(a)==pat.findall(b),(name,kind)
 assert set(labels.findall(a))<=set(labels.findall(b)),('label removed',name)
 for env in ['verbatim','Verbatim','tikzpicture','equation','equation*','align','align*']:
  pat=re.compile(r'\\begin\{'+re.escape(env)+r'\}.*?\\end\{'+re.escape(env)+r'\}',re.S);assert pat.findall(a)==pat.findall(b),(name,env)
 pat=re.compile(r'\\begin\{lstlisting\}(?:\[[\s\S]*?\])?([\s\S]*?)\\end\{lstlisting\}');assert pat.findall(a)==pat.findall(b),(name,'listed code')
 changes.append({'path':name,'before_sha256':sha(p),'sha256':sha(q)})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+name,tofile='descriptive/'+name))
# Real record identifiers remain in one clearly introduced test-identity table.
name='Chapters/10_Results/01_Prototype_Verification.tex';a=old[name].read_text();b=new[name].read_text();key=next(line for line in a.splitlines() if line.startswith('Firmware &'));assert key in b
# Before the firmware chapter, visible PWR revision labels have been removed.
for folder in ['Frontmatter','Chapters/01_Introduction','Chapters/02_Background','Chapters/03_Requirements_Architecture','Chapters/04_Topology_Analysis','Chapters/05_Modeling_Simulation','Chapters/06_Magnetics_Integration','Chapters/07_Hardware']:
 for p in (r/folder).glob('*.tex'):assert not re.search(r'PWR-\d',p.read_text()),str(p)
intro=(r/'Chapters/08_Control_Firmware/chapter.tex').read_text();assert intro.index('The project software was assigned revision identifiers')<intro.index('PWR-1.9.20')
assert 'sec:ctrl-firmware-identities' in intro
result={'baseline_files':len(old),'current_files':len(new),'edited_files':len(changes),'unchanged_files':len(new)-len(changes),'changes':changes,'checks':'All evidence assets, raw measurements, code, mathematical expressions, numerical quantities, source paths, graphics and original labels retained. No early unexplained PWR revisions; exact measured-record firmware identities preserved.'}
(rev/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');(rev/'firmware-terms.diff').write_text(''.join(diff));print({k:v for k,v in result.items() if k!='changes'})
