from pathlib import Path
from collections import Counter
import re,json,ast,hashlib,difflib
root=Path('/workspace/thesis');rev=Path('/workspace/tooling/thesis-direct-language');base=rev/'before'
assigned=['Backmatter/Appendices/'+x for x in ['A_Analytical_Equations.tex','C_Firmware_Documentation.tex','D_Modeling_Files.tex','E_Experimental_Data.tex','F_Contribution_Provenance.tex','G_Software_Tools.tex','H_Full_Embedded_Source.tex','I_Full_Supporting_Source.tex','J_Revised_Plan_Integration.tex']]
ns={};exec(Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0],ns)
patterns={'math':ns['math'],'SI quantities':re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+'),'numeric tokens':re.compile(r'\d+(?:\.\d+)*'),'labels/refs/cites/paths':re.compile(r'\\(?:label|ref|cref|Cref|cite\w*|sourcefile|input|include|includegraphics|path)(?:\[[^\]]*\])?\{[^}]*\}')}
errors=[];changes=[];diff=[]
for rel in assigned:
 a=(base/rel).read_bytes();b=(root/rel).read_bytes()
 if a==b:continue
 left=a.decode();right=b.decode()
 checks={k:Counter(pat.findall(left))==Counter(pat.findall(right)) for k,pat in patterns.items()}
 for env in ['equation','equation*','align','align*','tikzpicture','verbatim','Verbatim']:
  p=re.compile(r'\\begin\{'+re.escape(env)+r'\}.*?\\end\{'+re.escape(env)+r'\}',re.S);checks[env]=p.findall(left)==p.findall(right)
 def listing_body(s):return re.findall(r'\\begin\{lstlisting\}(?:\[[\s\S]*?\])?([\s\S]*?)\\end\{lstlisting\}',s)
 checks['listing bodies']=listing_body(left)==listing_body(right)
 # Caption wording may change, but the listed file, code style and label may not.
 def source_listings(s):
  found=[]
  for match in re.finditer(r'\\lstinputlisting\[([^\n]*)\]\{([^}]*)\}',s):
   options=re.sub(r'caption=\{[^}]*\}',r'caption={TEXT}',match.group(1));found.append((options,match.group(2)))
  return found
 checks['listed sources and noncaption options']=source_listings(left)==source_listings(right)
 checks['newline style']=(b'\r\n' in a)==(b'\r\n' in b)
 for k,v in checks.items():
  if not v:errors.append({'path':rel,'check':k,'removed':list((Counter(patterns[k].findall(left))-Counter(patterns[k].findall(right))).elements()) if k in patterns else [],'added':list((Counter(patterns[k].findall(right))-Counter(patterns[k].findall(left))).elements()) if k in patterns else []})
 changes.append({'path':rel,'before_sha256':hashlib.sha256(a).hexdigest(),'sha256':hashlib.sha256(b).hexdigest(),'checks':checks});diff.extend(difflib.unified_diff(left.splitlines(True),right.splitlines(True),fromfile='before/'+rel,tofile='direct/'+rel))
mapdata=json.loads((rev/'generated-caption-edits.json').read_text());by={}
for row in mapdata['table_edits']:by.setdefault(row['path'],[]).append(row)
for rel,rows in by.items():
 a=(base/rel).read_bytes();b=(root/rel).read_bytes();restored=b
 for row in rows:restored=restored.replace(row['after'].encode(),row['before'].encode())
 assert restored==a,('Nonpresentation table change',rel)
 changes.append({'path':rel,'before_sha256':hashlib.sha256(a).hexdigest(),'sha256':hashlib.sha256(b).hexdigest(),'checks':{'only_caption_and_approved_header_strings_changed':True,'all_data_rows_byte_identical':True}})
 diff.extend(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='before/'+rel,tofile='direct/'+rel))
rel=mapdata['generator_path'];a=(base/rel).read_bytes();b=(root/rel).read_bytes();reverse={row['after']:row['before'] for row in mapdata['generator_string_replacements']}
class Restore(ast.NodeTransformer):
 def visit_Constant(self,node):
  if isinstance(node.value,str) and node.value in reverse:node.value=reverse[node.value]
  return node
oldtree=ast.parse(a.decode());newtree=Restore().visit(ast.parse(b.decode()));assert ast.dump(oldtree,include_attributes=False)==ast.dump(newtree,include_attributes=False),'Generator behavior changed'
assert len(a.splitlines())==len(b.splitlines()),'Generator line count changed'
changes.append({'path':rel,'before_sha256':hashlib.sha256(a).hexdigest(),'sha256':hashlib.sha256(b).hexdigest(),'checks':{'AST_identical_outside_approved_presentation_strings':True,'line_count_unchanged':True}})
diff.extend(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='before/'+rel,tofile='direct/'+rel))
result={'changed_files':len(changes),'appendix_files_changed':len(changes)-len(by)-1,'generated_table_files_changed':len(by),'generator_files_changed':1,'errors':errors,'changes':changes}
(rev/'appendices-validation.json').write_text(json.dumps(result,indent=2)+'\n');(rev/'appendices-prose.diff').write_text(''.join(diff));print(json.dumps({k:v for k,v in result.items() if k!='changes'},indent=2));assert not errors,errors
