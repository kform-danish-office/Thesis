from pathlib import Path
import json,hashlib,re,difflib
root=Path('/workspace/thesis');rev=Path('/workspace/tooling/mcu-reader-introduction');before=rev/'before';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(before).as_posix():p for p in before.rglob('*') if p.is_file()};new={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()};assert set(old)<=set(new)
assert sorted(set(new)-set(old))==['Chapters/01_Introduction/10_Controller_Basics.tex']
helpers=Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0];ns={};exec(helpers,ns)
math=ns['math'];envs=ns['environments'];quantities=re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+');labels=re.compile(r'\\label\{[^}]*\}');graphics=re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}')
changes=[];diff=[]
for name,p in old.items():
 q=new[name]
 if sha(p)==sha(q):continue
 assert name.endswith('.tex'),('nonprose changed',name)
 a=p.read_text();b=q.read_text()
 for kind,pattern in [('math',math),('numerical quantities',quantities),('labels',labels),('graphics',graphics)]:assert pattern.findall(a)==pattern.findall(b),(name,kind)
 for env in envs(a):
  # Only glossary descriptions and one intro feedback-description row are edited.
  if name=='Frontmatter/Nomenclature.tex':continue
  if name=='Chapters/01_Introduction/08_V2_Prototype.tex' and ('tab:intro-v2-specs' in env or 'Feedback &' in env):continue
  if name=='Chapters/08_Control_Firmware/02_Architecture_Timing.tex' and 'fig:ctrl-software-architecture' in env:continue
  assert env in b,('protected block changed',name,env[:70])
 changes.append({'path':name,'before_sha256':sha(p),'sha256':sha(q)})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+name,tofile='reader-revision/'+name))
primer=(root/'Chapters/01_Introduction/10_Controller_Basics.tex').read_text();main=(root/'Chapters/01_Introduction/chapter.tex').read_text()
assert main.index('10_Controller_Basics')<main.index('08_V2_Prototype')
assert primer.index('What the Microcontroller and Its Pins Do')<primer.index('PA1 means')<primer.index('\\begin{table}')
for word in ['analog-to-digital converter','Direct memory access','universal asynchronous receiver-transmitter','physical package-terminal numbers','supply and ground pins']:assert word in primer,word
assert 'PA1 feedback variable' not in (root/'Frontmatter/Nomenclature.tex').read_text()
result={'baseline_files':len(old),'current_files':len(new),'edited_files':len(changes),'unchanged_files':len(old)-len(changes),'added_files':sorted(set(new)-set(old)),'changes':changes,'checks':'Math, numerical quantities, existing labels, source graphics, raw data, code and earlier figure/table blocks preserved except named explanatory glossary/table/caption edits. Primer precedes first main-text pin table.'}
(rev/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');(rev/'reader-revision.diff').write_text(''.join(diff));print({k:v for k,v in result.items() if k!='changes'})
