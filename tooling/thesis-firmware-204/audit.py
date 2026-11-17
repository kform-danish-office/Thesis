from pathlib import Path
import hashlib,json,zipfile,re
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-firmware-204'); sha=lambda b:hashlib.sha256(b).hexdigest()
old=Path('/workspace/tooling/thesis-channel-labels/Thesis_V1_V2_V3_Source.zip')
with zipfile.ZipFile(old) as z:
 assert z.testzip() is None
 previous={n:sha(z.read(n)) for n in z.namelist()}
current={p.relative_to(root).as_posix():sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
assert not set(previous)-set(current)
changed=sorted(n for n in previous if previous[n]!=current[n]);new=sorted(set(current)-set(previous))
allowed={p.relative_to(r/'before').as_posix() for p in (r/'before').rglob('*') if p.is_file()}
assert set(changed)<=allowed,sorted(set(changed)-allowed)
assert all(n.startswith('Code/PWR_2_0_4/') or n in {'Code/PWR_2_0_1/source_manifest.json','Code/PWR_2_0_1/software_verification.json'} for n in new),new
for n in previous:
 if n.startswith(('Data/','Pictures/')) or n.endswith('.ino') or n.startswith('Code/PWR_2_0_1/'):
  assert previous[n]==current[n],n
manifest=json.loads((root/'Code/source_manifest.json').read_text())
for row in manifest['files']:
 p=root/row['copy'];assert sha(p.read_bytes())==row['sha256']
 if row['copy'].startswith('Code/PWR_2_0_4/'):
  assert p.read_bytes()==(Path('/workspace/working-source')/row['source']).read_bytes()
assert (root/'Code/PWR_2_0_1/source_manifest.json').read_bytes()==(r/'before/Code/source_manifest.json').read_bytes()
assert (root/'Code/PWR_2_0_1/software_verification.json').read_bytes()==(r/'before/Code/software_verification.json').read_bytes()
for name in ['H_Full_Embedded_Source.tex','I_Full_Supporting_Source.tex']:
 text=(root/'Backmatter/Appendices'/name).read_text()
 for path in re.findall(r'\\lstinputlisting\[[^\]]*\]\{([^}]+)\}',text):assert (root/path).is_file(),path
 assert not re.search('firstline=|lastline=',text)
prose='\n'.join(p.read_text() for folder in ['Chapters','Frontmatter','Backmatter'] for p in (root/folder).rglob('*.tex'))
assert not re.search(r'240[^\n]{0,100}(?:goal|objective)|(?:goal|objective)[^\n]{0,100}240',prose)
assert prose.count('including \\SI{240}{\\watt}')==1
assert 'APEC digest raised the question' in prose
# Record this authorized revision without changing original import digests.
mp=Path('/workspace/tooling/thesis-change-manifest.json');entries=json.loads(mp.read_text());lookup={e['path']:e for e in entries}
for n in changed+new:
 if n in lookup:lookup[n]['sha256']=current[n]
 else:entries.append({'path':n,'sha256':current[n],'original_sha256':previous.get(n)})
mp.write_text(json.dumps(entries,indent=2)+'\n')
report={'source_files':len(current),'previous_source_files':len(previous),'changed':changed,'new':new,'unchanged':len(previous)-len(changed),'original_data_pictures_code_preserved':True,'current_snapshot_matches_working_source':True,'current_manifest_matches':True,'historical_manifests_preserved':True}
(r/'source-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS: {len(changed)} edited, {len(new)} added, {report["unchanged"]} prior files unchanged; {len(current)} total. All original data, pictures and historical code preserved; current snapshot matches working-source.')
