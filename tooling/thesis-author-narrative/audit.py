from pathlib import Path
import hashlib,json,re,difflib
root=Path('/workspace/thesis');review=Path('/workspace/tooling/thesis-author-narrative');before=review/'before'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(before).as_posix():p for p in before.rglob('*') if p.is_file()};new={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()};assert old.keys()==new.keys()
allowed={'Chapters/01_Introduction/08_V2_Prototype.tex','Chapters/07_Hardware/01_Prototype_Overview.tex','Chapters/07_Hardware/16_V2_F410.tex','Chapters/10_Results/15_V2_Testing_Update.tex','Chapters/12_Conclusion/04_Future_Work.tex','Backmatter/Appendices/B_Hardware_Documentation.tex'}
math=re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$',re.S)
# Every numerical quantity and source graphic stays identical; only authorial prose changes.
quantities=re.compile(r'\\(?:SI|SIrange|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+')
figures=re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}')
labels=re.compile(r'\\label\{[^}]*\}')
cites=re.compile(r'\\cite\w*\*?(?:\[[^\]]*\])?(?:\{[^}]*\})')
changes=[];diff=[]
for name,p in old.items():
 q=new[name]
 if sha(p)==sha(q):continue
 assert name in allowed,name
 a=p.read_text();b=q.read_text()
 for kind,pattern in [('math',math),('quantities',quantities),('source figures',figures),('labels',labels),('citations',cites)]:
  assert pattern.findall(a)==pattern.findall(b),(name,kind)
 assert 'supplied on October' not in b and 'supplied in the chat' not in b,name
 changes.append({'path':name,'before_sha256':sha(p),'sha256':sha(q)})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+name,tofile='author-narrative/'+name))
assert set(x['path'] for x in changes)==allowed
body=(root/'Chapters/01_Introduction/08_V2_Prototype.tex').read_text()+(root/'Chapters/07_Hardware/16_V2_F410.tex').read_text()+(root/'Backmatter/Appendices/B_Hardware_Documentation.tex').read_text()
for phrase in ['October 27','October 18','supplied on','supplied in the chat','Schematic Prints - 10-27-2026']:
 assert phrase not in body,phrase
report={'baseline_files':len(old),'current_files':len(new),'edited_files':len(changes),'unchanged_files':len(new)-len(changes),'changes':changes,'checks':'All original assets and evidence unchanged; mathematical expressions, numerical quantities, source graphics, labels and citations identical. File-handoff narrative removed from V2 introduction, hardware and appendix.'}
(review/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n');(review/'wording.diff').write_text(''.join(diff))
print({k:v for k,v in report.items() if k!='changes'})
