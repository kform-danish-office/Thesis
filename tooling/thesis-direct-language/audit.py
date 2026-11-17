"""Audit prose, caption and colour-PDF changes against the frozen source."""
from pathlib import Path
from collections import Counter,defaultdict
import ast,csv,difflib,hashlib,io,json,re
import fitz

root=Path('/workspace/thesis');review=Path('/workspace/tooling/thesis-direct-language');base=review/'before'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old={p.relative_to(base).as_posix():p for p in base.rglob('*') if p.is_file()}
new={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()}
assert old.keys()<=new.keys()
colour='Pictures/Thesis/07_Hardware/Schematic_V2_Colour.pdf'
assert new.keys()-old.keys()=={colour}
assert sha(new[colour])=='7af67969cea32d270498dacdd244b937c2496f113b85038893dbc88260f8d031'
assert new[colour].read_bytes()==Path('/workspace/source-archives/_SCH DWG NO__SCH.PDF').read_bytes()
rows=[]
for name in ['early-edits.json','control-edits.json','results-edits.json','appendices-edits.json','root-edits.json']:
 for item in json.loads((review/name).read_text()):
  if 'replacements' in item:
   rows.extend(dict(x,path=item['path']) for x in item['replacements'])
  else:rows.append(item)
presentation=json.loads((review/'generated-caption-edits.json').read_text());rows+=presentation['table_edits']
by=defaultdict(list)
for row in rows:by[row['path']].append(row)
ns={};exec(Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0],ns)
patterns={
 'math':ns['math'],
 'quantities':re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+'),
 'labels':re.compile(r'\\label\{[^}]*\}'),
 'citations':re.compile(r'\\cite\w*\*?(?:\[[^\]]*\])?\{[^}]*\}'),
 'source_paths':re.compile(r'\\(?:sourcefile|lstinputlisting|input|include|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}'),
}
assets={x['path']:x for x in json.loads((review/'colour-crop-manifest.json').read_text())['outputs']}
changes=[];errors=[];diff=[];mapping_notes=[]
for rel,op in sorted(old.items()):
 np=new[rel]
 if sha(op)==sha(np):continue
 checks={}
 if rel in by:
  a=op.read_text();b=np.read_text();expected=a
  for row in by[rel]:
   before=row['before'].replace('\r\n','\n');after=row['after'].replace('\r\n','\n')
   if before in expected:expected=expected.replace(before,after)
   elif after not in expected:mapping_notes.append({'path':rel,'before':before,'reason':'intermediate replacement not present'})
  tidy=lambda text:re.sub(r'[ \t]+\n','\n',text.replace('. }','.}'))
  checks['only_recorded_wording_changes_plus_whitespace_cleanup']=tidy(expected)==tidy(b)
  normalized=a.replace('Schematic_V2_F410_2026-10-27.pdf','Schematic_V2_Colour.pdf') if rel.endswith('B_Hardware_Documentation.tex') else a
  for key,pat in patterns.items():
   if key!='source_paths':checks[key]=Counter(pat.findall(normalized))==Counter(pat.findall(b))
  commands={r'\sourcefile',r'\lstinputlisting',r'\input',r'\include',r'\includegraphics'}
  paths=lambda text:Counter((cmd,args[-1]) for cmd,args in ns['macros'](text) if cmd in commands and args)
  checks['source_paths']=paths(normalized)==paths(b)
  for env in ['equation','equation*','align','align*','tikzpicture','circuitikz','verbatim','Verbatim']:
   pat=re.compile(r'\\begin\{'+re.escape(env)+r'\}.*?\\end\{'+re.escape(env)+r'\}',re.S);checks[env]=pat.findall(a)==pat.findall(b)
  pat=re.compile(r'\\begin\{lstlisting\}(?:\[[\s\S]*?\])?([\s\S]*?)\\end\{lstlisting\}');checks['code_listing_bodies']=pat.findall(a)==pat.findall(b)
  checks['newline_style']=(b'\r\n' in op.read_bytes())==(b'\r\n' in np.read_bytes())
  diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='before/'+rel,tofile='direct/'+rel))
 elif rel in assets:
  record=assets[rel];checks['approved_colour_crop_hash']=sha(np)==record['sha256'];a=fitz.open(op);b=fitz.open(np);checks['same_crop_geometry_and_labels']=len(a)==len(b) and all(x.rect==y.rect and Counter(w[4] for w in x.get_text('words'))==Counter(w[4] for w in y.get_text('words')) for x,y in zip(a,b));checks['all_pages_have_colour']=all(x['coloured_pixels_at_144dpi']>0 for x in record['pages'])
 elif rel==presentation['generator_path']:
  reverse={x['after']:x['before'] for x in presentation['generator_string_replacements']}
  class Restore(ast.NodeTransformer):
   def visit_Constant(self,node):
    if isinstance(node.value,str) and node.value in reverse:node.value=reverse[node.value]
    return node
  checks['generator_AST_same_outside_presentation_strings']=ast.dump(ast.parse(op.read_text()),include_attributes=False)==ast.dump(Restore().visit(ast.parse(np.read_text())),include_attributes=False)
 elif rel=='Data/measurements/processed_rewrite/generated_output_checksums.csv':
  a=list(csv.DictReader(io.StringIO(op.read_text())));b=list(csv.DictReader(io.StringIO(np.read_text())));updates={x['path'] for x in json.loads((review/'checksum-ledger-updates.json').read_text())};checks['same_checksum_ledger_entries']=len(a)==len(b);changed=0
  for x,y in zip(a,b):
   assert x['output']==y['output'];path=x['output'].replace('\\','/')
   if path in updates:assert y['sha256']==sha(root/path) and int(y['size_bytes'])==(root/path).stat().st_size;changed+=1
   else:assert x==y
  checks['only_12_approved_metadata_rows_refreshed']=changed==12
 else:raise AssertionError(('Unexpected file changed',rel))
 for check,value in checks.items():
  if not value:errors.append({'path':rel,'check':check})
 changes.append({'path':rel,'before_sha256':sha(op),'sha256':sha(np),'checks':checks})

# Pin names in the seven assignment rows are electrical data, not caption prose.
pinfile='Chapters/01_Introduction/10_Controller_Basics.tex'
def pin_cells(text):
 return [tuple(cell.strip() for cell in line.split('&')[1:]) for line in text.splitlines() if '&' in line and re.search(r'\bP[ABC]\d+',line)]
assert pin_cells(old[pinfile].read_text())==pin_cells(new[pinfile].read_text())
assert 'MCU pin assignments for the original controller and V2.' in new[pinfile].read_text()
assert "MCU's perspective" not in new[pinfile].read_text()
assert 'The software request is aligned with a carrier boundary' not in (root/'Backmatter/Appendices/C_Firmware_Documentation.tex').read_text()
result={'baseline_files':len(old),'current_files':len(new),'edited_files':len(changes),'unchanged_files':len(old)-len(changes),'added_files':[{'path':colour,'sha256':sha(new[colour])}],'changes':changes,'mapping_notes':mapping_notes,'errors':errors,'checks':'Caption/heading/table prose edits are explicitly mapped; SI quantities, mathematical content, pin data, raw data and code retained. Only generator presentation strings and generated-output checksum metadata changed outside TeX; four diagrams replaced by matching colour vector crops.'}
(review/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n');(review/'all-wording.diff').write_text(''.join(diff))
print(json.dumps({k:v for k,v in result.items() if k not in {'changes','mapping_notes'}},indent=2));print('Mapping notes:',len(mapping_notes));assert not errors,errors
