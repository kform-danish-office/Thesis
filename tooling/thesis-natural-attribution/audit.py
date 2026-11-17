from pathlib import Path
import json,hashlib,re,zipfile,difflib
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-natural-attribution');edits=json.loads((r/'edits.json').read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile('/workspace/tooling/thesis-firmware-204/Thesis_V1_V2_V3_Source.zip') as z:
 assert z.testzip() is None
 previous={n:sha(z.read(n)) for n in z.namelist()}
current={p.relative_to(root).as_posix():sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
assert set(previous)==set(current)
changed=sorted(n for n in previous if current[n]!=previous[n]);assert set(changed)=={e['path'] for e in edits}
diff=[]
for name in changed:
 before=(r/'before'/name).read_bytes();after=(root/name).read_bytes();assert sha(before)==previous[name]
 expected=before.decode()
 for e in edits:
  if e['path']==name:assert e['old'] in expected;expected=expected.replace(e['old'],e['new'])
 assert expected.encode()==after,name
 for pattern in [r'\\(?:SI|SIrange|num|numrange)\{[^}]*\}(?:\{[^}]*\})?',r'\\(?:label|ref|cref|Cref|cite|eqref|sourcefile|input|include)\{[^}]*\}',r'\$[^$]*\$',r'\\\([\s\S]*?\\\)',r'\\begin\{equation\}[\s\S]*?\\end\{equation\}']:
  assert re.findall(pattern,before.decode())==re.findall(pattern,after.decode()),(name,pattern)
 diff.extend(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile='before/'+name,tofile='after/'+name))
# All word occurrences left in authored TeX are internal labels or file paths.
remaining=[]
for folder in ['Chapters','Frontmatter','Backmatter']:
 for p in (root/folder).rglob('*.tex'):
  s=re.sub(r'\\(?:label|ref|cref|Cref|input|include)\{[^}]+\}','',p.read_text())
  assert not re.search(r'\binherited\b',s,re.I),p
# Preserve current import digests and record current hashes.
p=Path('/workspace/tooling/thesis-change-manifest.json');m=json.loads(p.read_text());lookup={x['path']:x for x in m}
for n in changed:
 if n in lookup:lookup[n]['sha256']=current[n]
 else:m.append({'path':n,'sha256':current[n],'original_sha256':previous[n]})
p.write_text(json.dumps(m,indent=2)+'\n')
report={'source_files':len(current),'changed':changed,'unchanged':len(current)-len(changed),'exact_contextual_replacements':len(edits),'technical_quantities_equations_references_preserved':True,'remaining_inherited_only_internal_identifiers':True}
(r/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n');(r/'wording.diff').write_text(''.join(diff))
print(f'PASS: {len(edits)} exact wording changes in {len(changed)} files; {report["unchanged"]} files byte-identical; quantities, equations, labels and citations unchanged.')
