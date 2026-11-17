from pathlib import Path
import hashlib,json,re,difflib
root=Path('/workspace/thesis');review=Path('/workspace/tooling/v3-story-update');before=review/'before'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(before).as_posix():p for p in before.rglob('*') if p.is_file()};new={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()}
added=sorted(set(new)-set(old));assert not (set(old)-set(new))
assert added==['Chapters/01_Introduction/09_V3_Development.tex','Chapters/10_Results/16_V3_Design_Outcome.tex'],added
helpers=Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0];ns={};exec(helpers,ns)
protected_env=ns['environments'];math=ns['math'];labels=re.compile(r'\\label\{[^}]*\}');graphics=re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}')
allowed_table_names={'Chapters/10_Results/14_Revised_Plan_Status.tex':('tab:revised-plan-results-status','AP-06 &'), 'Backmatter/Appendices/J_Revised_Plan_Integration.tex':('tab:plan-thesis-map',)}
changes=[];diff=[]
for name,p in old.items():
 q=new[name]
 if sha(p)==sha(q):continue
 assert q.suffix=='.tex' or name=='README.md',('nonprose changed',name)
 a=p.read_text();b=q.read_text()
 assert math.findall(a)==math.findall(b),('math',name)
 assert labels.findall(a)==labels.findall(b),('labels',name)
 assert graphics.findall(a)==graphics.findall(b),('graphics',name)
 for env in protected_env(a):
  if any(key in env for key in allowed_table_names.get(name,())):continue
  assert env in b,('existing equation/table/figure changed',name,env[:100])
 changes.append({'path':name,'before_sha256':sha(p),'sha256':sha(q)})
 diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+name,tofile='revised/'+name))
# Preserve the numerical baseline and criterion rows not affected by the new account.
name='Chapters/10_Results/14_Revised_Plan_Status.tex';a=old[name].read_text();b=new[name].read_text()
for ap in ['AP-01','AP-02','AP-04','AP-05']:
 row=next(line for line in a.splitlines() if line.startswith(ap+' &'));assert row in b,ap
# The entire measured-performance answer is retained verbatim.
name='Chapters/12_Conclusion/02_Research_Questions.tex';a=old[name].read_text();b=new[name].read_text();start=a.index('\\paragraph{RQ3:');end=a.index('\\paragraph{RQ4:');assert a[start:end] in b
for name in added:
 assert not re.search(r'uploaded|supplied on|in the chat',new[name].read_text(),re.I)
report={'baseline_files':len(old),'current_files':len(new),'edited_files':len(changes),'unchanged_files':len(old)-len(changes),'added_files':added,'changes':changes,'checks':'All original non-prose assets, measurements, code, figures, labels, math and baseline performance answer preserved. Only two status/integration tables deliberately updated; all other original table and figure blocks unchanged.'}
(review/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n');(review/'story.diff').write_text(''.join(diff))
print({k:v for k,v in report.items() if k!='changes'})
