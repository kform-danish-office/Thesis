from pathlib import Path
import json,hashlib,zipfile,re,collections
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-pdf-prose')
baseline=Path('/workspace/tooling/thesis-v2-load-thermal/Thesis_V1_V2_V3_Source.zip')
with zipfile.ZipFile(baseline) as z:old={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
new={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
assert old.keys()==new.keys()
changed=[p for p in old if old[p]!=new[p]]
props=json.loads((r/'astra-approved.json').read_text());approved={p['path'] for p in props}
extra={'Data/analysis/rebuild_results.py','Data/measurements/processed_rewrite/generated_output_checksums.csv'}
assert set(changed)==approved|extra,(set(changed)-(approved|extra),(approved|extra)-set(changed))
protected=[p for p in old if p not in changed];assert all(old[p]==new[p] for p in protected)
assert all(old[p]==new[p] for p in old if p.startswith(('Code/','Pictures/','Firmware/','Setup/','Data/project_records/','Data/measurements/v2_load_thermal/')) or p=='main.tex')
def rows(text):
 body=text.replace('\r\n','\n').split('\\endhead\n',1)[1].split('\\bottomrule',1)[0]
 return [line.removesuffix('\\\\').split(' & ') for line in body.splitlines() if line.endswith('\\\\')]
checks=[]
for p in changed:
 if not p.startswith('Data/measurements/processed_rewrite/') or not p.endswith('.tex') or p.endswith('measurement_appendix.tex'):continue
 a=rows(old[p].decode());b=rows(new[p].decode());assert len(a)==len(b),p
 for x,y in zip(a,b):
  x[0]=re.sub(r' / \d+$','',x[0])
  if p.endswith('raw_waveform_source_table.tex'):x.pop(1)
  elif p.endswith('thermal_complete_table.tex'):x.pop()
  if p.endswith('record_metadata_table.tex'):assert x[:3]==y[:3],(p,x,y)
  else:assert x==y,(p,x,y)
 checks.append({'table':p,'rows':len(a),'measurement_cells_unchanged':True})
unit_re=re.compile(r'\\SI(?:range)?(?:\[[^\]]*\])?\{[^{}]*\}(?:\{[^{}]*\}){1,2}')
qtyold=collections.Counter();qtynew=collections.Counter()
for p in changed:
 if p.endswith('.tex') and p.startswith(('Chapters/','Frontmatter/','Backmatter/')):
  qtyold.update(unit_re.findall(old[p].decode()));qtynew.update(unit_re.findall(new[p].decode()))
assert not (set(qtynew)-set(qtyold))
assert not (set(qtyold)-set(qtynew)),set(qtyold)-set(qtynew)
report={'baseline':str(baseline),'total_files':len(old),'changed_files':len(changed),'unchanged_files':len(protected),'added_files':[],'deleted_files':[],'changed_paths':changed,'unchanged_sha256':{p:hashlib.sha256(old[p]).hexdigest() for p in protected},'table_checks':checks,'quantity_form_set_preserved':True,'removed_repeated_quantity_mentions':dict(qtyold-qtynew),'data_figures_firmware_and_layout_preserved':True,'presentation_code_computational_ast_unchanged':json.loads((r/'generator-presentation-audit.json').read_text())['computational_ast_unchanged']}
(r/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS: {len(changed)} intended changes; {len(protected)} files byte-identical; no additions/deletions. All original data/images/firmware/layout and measured table cells preserved.')
