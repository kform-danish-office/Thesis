from pathlib import Path
import csv,hashlib,json
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-pdf-prose')
baseline={x['path']:x['sha256'] for x in json.loads((r/'baseline-manifest.json').read_text())}
changed={name for name,h in baseline.items() if hashlib.sha256((root/name).read_bytes()).hexdigest()!=h}
p=root/'Data/measurements/processed_rewrite/generated_output_checksums.csv'
with p.open(newline='') as f:reader=csv.DictReader(f);columns=reader.fieldnames;rows=list(reader)
updates=[]
for row in rows:
 name=row['output'].replace(chr(92),'/')
 if name in changed:
  q=root/name;row['sha256']=hashlib.sha256(q.read_bytes()).hexdigest();row['size_bytes']=str(q.stat().st_size);updates.append(row['output'])
backup=r/'before'/p.relative_to(root);backup.parent.mkdir(parents=True,exist_ok=True)
if not backup.exists():backup.write_bytes(p.read_bytes())
with p.open('w',newline='') as f:writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader();writer.writerows(rows)
(r/'checksum-updates.json').write_text(json.dumps(updates,indent=2)+'\n')
ledger=Path('/workspace/tooling/thesis-change-manifest.json');records=json.loads(ledger.read_text());by={x['path']:x for x in records};orig={x['path']:x['sha256'] for x in json.loads(Path('/workspace/tooling/thesis-source-manifest.json').read_text())}
for name,h in baseline.items():
 new=hashlib.sha256((root/name).read_bytes()).hexdigest()
 if new!=h:
  if name not in by:by[name]={'path':name,'original_sha256':orig.get(name)};records.append(by[name])
  by[name]['sha256']=new
ledger.write_text(json.dumps(records,indent=2)+'\n')
p=r/'judgement.md';s=p.read_text().replace('across 60 files','across 59 files');p.write_text(s)
print('Updated',len(updates),'generated table checksums and current thesis change ledger.')
