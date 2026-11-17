from pathlib import Path
import ast,csv,json,re,tempfile,difflib
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-pdf-prose');data=root/'Data/measurements/processed_rewrite'
source=(root/'Data/analysis/rebuild_results.py').read_text();tree=ast.parse(source)
output=Path(tempfile.mkdtemp(prefix='thesis-table-check-',dir='/tmp'))
def load(name):
 with (data/name).open(newline='') as f:rows=list(csv.DictReader(f))
 for row in rows:
  for k,v in row.items():
   if k in {'record_id','test_id','firmware','notes','image_id'}:continue
   if v=='':row[k]=None
   elif v in {'True','False'}:row[k]=v=='True'
   elif re.fullmatch(r'[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?',v):row[k]=int(v) if k in {'sample_count','source_row'} else float(v)
 return rows
ctx={'Path':Path,'OUT':output,'dc':load('dc_operating_points.csv'),'ac':load('ac_detail_statistics.csv'),'eff':load('efficiency_screening.csv'),'pq':load('power_quality_logged.csv'),'thermal':load('thermal_camera_readings.csv'),'raw_index':load('raw_waveform_index.csv'),'trans':load('transient_recorded_fields.csv')}
ctx['complete']=[x for x in load('all_workbook_rows.csv') if x['status']!='Planned']
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'f','idtex','tex_plain','table'}]
exec(compile(ast.Module(body=funcs,type_ignores=[]),'<presentation-functions>','exec'),ctx)
selected=json.loads((r/'generator-presentation-audit.json').read_text())['modified_table_calls']
for n in tree.body:
 if not (isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='table'):continue
 if ast.literal_eval(n.value.args[0]) in selected:exec(compile(ast.Module(body=[n],type_ignores=[]),'<presentation-call>','exec'),ctx)
fail=[]
for name in selected:
 actual=(output/name).read_text();wanted=(data/name).read_text()
 if actual!=wanted:
  fail.append(name);(r/(name+'.renderer.diff')).write_text(''.join(difflib.unified_diff(wanted.splitlines(True),actual.splitlines(True),fromfile='accepted-table',tofile='renderer')))
report={'tables':selected,'mismatches':fail,'temporary_output':str(output),'numerical_inputs':'unchanged existing CSVs; no recomputation or current-tree regeneration'}
(r/'table-renderer-audit.json').write_text(json.dumps(report,indent=2)+'\n')
assert not fail,fail
print('PASS:',len(selected),'accepted tables reproduced exactly from unchanged CSVs by updated presentation code.')
