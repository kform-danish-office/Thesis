from pathlib import Path
import re,collections,json,difflib
base=Path('/workspace/tooling/apec-style-edit/before')
root=Path('/workspace/thesis')
ns={}
exec(Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0],ns)
changes=[];errors=[]
for d in ['02_Background','03_Requirements_Architecture','04_Topology_Analysis','05_Modeling_Simulation','06_Magnetics_Integration']:
 for new_path in sorted((root/'Chapters'/d).glob('*.tex')):
  rel=new_path.relative_to(root);old_path=base/rel
  oldraw,newraw=old_path.read_bytes(),new_path.read_bytes()
  if oldraw==newraw: continue
  old,new=oldraw.decode(),newraw.decode()
  oldmacro,newmacro=ns['macros'](old),ns['macros'](new)
  om,nm=collections.Counter((x,tuple(a)) for x,a in oldmacro),collections.Counter((x,tuple(a)) for x,a in newmacro)
  oldmath,newmath=collections.Counter(ns['math'].findall(old)),collections.Counter(ns['math'].findall(new))
  checks={
   'math':oldmath==newmath,
   'protected_environments':ns['environments'](old)==ns['environments'](new),
   'command_arguments':om==nm,
   'newline':(oldraw.count(b'\r\n'),oldraw.count(b'\n'))==(newraw.count(b'\r\n'),newraw.count(b'\n')),
  }
  row={'path':str(rel),'checks':checks,'before_words':len(old.split()),'after_words':len(new.split())}
  if not checks['math']:row['math_removed']=list((oldmath-newmath).elements());row['math_added']=list((newmath-oldmath).elements())
  if not checks['command_arguments']:row['commands_removed']=list((om-nm).elements());row['commands_added']=list((nm-om).elements())
  changes.append(row)
  if not all(checks.values()):errors.append(row)
result={'changed_files':len(changes),'before_words':sum(x['before_words'] for x in changes),'after_words':sum(x['after_words'] for x in changes),'errors':errors,'changes':changes}
Path('/workspace/tooling/apec-style-edit/early-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='changes'},indent=2))
