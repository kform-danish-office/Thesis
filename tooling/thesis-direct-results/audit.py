from pathlib import Path
import zipfile,json,hashlib,re,difflib
r=Path('/workspace/tooling/thesis-direct-results');root=Path('/workspace/thesis');sha=lambda b:hashlib.sha256(b).hexdigest()
edits=sum((json.loads((r/n).read_text()) for n in ['v2-edits.json','late-edits.json','technical-edits.json']),[])
with zipfile.ZipFile('/workspace/tooling/thesis-natural-attribution/Thesis_V1_V2_V3_Source.zip') as z:
 assert z.testzip() is None
 previous={n:sha(z.read(n)) for n in z.namelist()}
current={p.relative_to(root).as_posix():sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
assert set(previous)==set(current)
changed=sorted(n for n in previous if previous[n]!=current[n]);assert set(changed)=={e['path'] for e in edits}
diff=[];removed_repeated_quantities=[]
for n in changed:
 before=(r/'before'/n).read_bytes();after=(root/n).read_bytes();assert sha(before)==previous[n],n
 old=before.decode();expected=old
 for e in edits:
  if e['path']==n:
   assert e['old'] in expected,(n,e['old'][:80]);expected=expected.replace(e['old'],e['new'])
 assert expected.encode()==after,n
 text=after.decode()
 for pattern in [r'\\label\{[^}]+\}',r'\\\([\s\S]*?\\\)',r'\$[^$]*\$',r'\\begin\{equation\}[\s\S]*?\\end\{equation\}']:
  assert re.findall(pattern,old)==re.findall(pattern,text),(n,pattern)
 qty=r'\\(?:SI|SIrange|num|numrange)\{[^}]*\}(?:\{[^}]*\})?'
 assert set(re.findall(qty,old))==set(re.findall(qty,text)),(n,'quantity changed')
 diff.extend(difflib.unified_diff(old.splitlines(True),text.splitlines(True),fromfile='before/'+n,tofile='after/'+n))
for n in previous:
 if n.startswith(('Data/','Pictures/','Code/')):assert previous[n]==current[n],n
prose='\n'.join(p.read_text() for folder in ['Chapters','Frontmatter','Backmatter'] for p in (root/folder).rglob('*.tex'))
assert not re.search(r'establish|does not demonstrate|do not demonstrate|does not verify|do not verify',prose,re.I)
p=Path('/workspace/tooling/thesis-change-manifest.json');m=json.loads(p.read_text());lookup={x['path']:x for x in m}
for n in changed:
 if n in lookup:lookup[n]['sha256']=current[n]
 else:m.append({'path':n,'sha256':current[n],'original_sha256':previous[n]})
p.write_text(json.dumps(m,indent=2)+'\n')
report={'source_files':len(current),'changed':changed,'unchanged':len(current)-len(changed),'exact_replacements':len(edits),'all_unique_SI_quantities_equations_labels_preserved':True,'data_pictures_all_code_byte_identical':True}
(r/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n');(r/'all-wording.diff').write_text(''.join(diff));print(f'PASS: {len(edits)} exact edits in {len(changed)} files; {report["unchanged"]} files byte-identical. Quantities, equations, labels and all data/images/code retained.')
