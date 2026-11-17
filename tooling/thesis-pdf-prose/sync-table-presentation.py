from pathlib import Path
import ast,json,re,hashlib
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-pdf-prose');f=root/'Data/analysis/rebuild_results.py'
original=f.read_bytes();s=original.decode();norm=s.replace('\r\n','\n');tree=ast.parse(norm);lines=norm.splitlines(keepends=True);starts=[0]
for line in lines:starts.append(starts[-1]+len(line))
def span(n):return (starts[n.lineno-1]+len(lines[n.lineno-1].encode()[:n.col_offset].decode()),starts[n.end_lineno-1]+len(lines[n.end_lineno-1].encode()[:n.end_col_offset].decode()))
def text(n):a,b=span(n);return norm[a:b]
patches=[];changed=[]
for stmt in tree.body:
 if not (isinstance(stmt,ast.Expr) and isinstance(stmt.value,ast.Call) and isinstance(stmt.value.func,ast.Name) and stmt.value.func.id=='table'):continue
 call=stmt.value;name=ast.literal_eval(call.args[0]);p=root/'Data/measurements/processed_rewrite'/name
 if not (r/'before'/p.relative_to(root)).exists():continue
 t=p.read_bytes().decode();caption=re.search(r'\\caption\{(.*)\}\\label',t).group(1)
 headers=t.split('\\toprule',1)[1].split('\\midrule',1)[0].strip().removesuffix('\\\\').split(' & ')
 widths=[float(x) for x in re.search(r'\\begin\{longtable\}\{(.+)\}',t).group(1).split('L{')[1:] for x in [x.split('\\linewidth')[0]]]
 rows=text(call.args[4]).replace("+' / '+str(r['source_row'])",'')
 if name=='thermal_complete_table.tex':rows=rows.replace(",idtex(Path(r['source_image']).name)",'')
 if name=='raw_waveform_source_table.tex':rows=rows.replace("idtex(Path(r['archived_path']).name),",'')
 if name=='record_metadata_table.tex':
  rows=rows.replace("'Included in row-level screening; instrument boundary unresolved'", "'Power comparison'")
  rows=rows.replace("else r['exclusion']", "else ('No nonzero DC input/output power pair' if r['exclusion']=='no nonzero measured DC output/input power' else r['exclusion'])")
 for n,new in [(call.args[1],repr(caption)),(call.args[3],repr(headers)),(call.args[4],rows)]:patches.append((*span(n),new))
 if name in {'thermal_complete_table.tex','raw_waveform_source_table.tex'}:
  patches.append((*span(call.args[5]),repr(widths)))
  # Match the table helper's four-decimal width normalization exactly.
  oldspec=re.search(r'\\begin\{longtable\}\{(.+)\}',t).group(1)
  newspec='@{}'+' '.join('L{'+f'{w*.88/sum(widths):.4f}'+'\\linewidth}' for w in widths)+'@{}'
  t=t.replace(oldspec,newspec);p.write_bytes(t.encode())
  if name=='thermal_complete_table.tex':
   dup=p.with_name('appendix_thermal_complete_table.tex');dup.write_bytes(t.replace('tab:thermal-results','tab:thermal-results-complete').encode())
 changed.append(name)
# Keep the unused all-measurements entry point consistent with the same presentation.
oldintro='''The workbook source is \\sourcefile{Data/measurements/Thesis_USB_PDO_3A_Limited_Test_Plan.xlsx},
sheet \\texttt{Load Data}; each electrical record carries its original row number.
Planned rows are retained in \\sourcefile{Data/measurements/processed_rewrite/all_workbook_rows.csv}
and are not treated as measurements. A blank field is unavailable, not zero.
The source waveforms are retained in \\sourcefile{Data/measurements/processed_rewrite/raw_waveforms}.
'''
for a,b,new in sorted(patches,reverse=True):norm=norm[:a]+new+norm[b:]
assert norm.count(oldintro)==1;norm=norm.replace(oldintro,'A blank field indicates an unavailable measurement.\n')
# The only changed top-level nodes are table presentation calls and the unused
# measurement-appendix introduction. All data selection/calculation/plot nodes match.
def computation(t):
 out=[]
 for n in t.body:
  if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call):
   c=n.value
   if isinstance(c.func,ast.Name) and c.func.id=='table':continue
   if isinstance(c.func,ast.Attribute) and c.func.attr=='write_text' and 'measurement_appendix.tex' in ast.dump(c.func.value):continue
  out.append(ast.dump(n,include_attributes=False))
 return out
assert computation(tree)==computation(ast.parse(norm))
b=r/'before/Data/analysis/rebuild_results.py';b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(original)
f.write_bytes(norm.replace('\n','\r\n').encode())
(r/'generator-presentation-audit.json').write_text(json.dumps({'modified_table_calls':changed,'computational_ast_unchanged':True,'width_normalization':['raw_waveform_source_table.tex','thermal_complete_table.tex','appendix_thermal_complete_table.tex']},indent=2)+'\n')
print('Synchronized',len(changed),'table calls; computational AST unchanged.')
