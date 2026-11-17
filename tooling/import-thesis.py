from pathlib import Path
import zipfile,hashlib,json
base=Path('/workspace/source-archives'); slices=base/'thesis-transfer';slices.mkdir(exist_ok=True)
containers=sorted(Path('/workspace/attachments').glob('*/Thesis_Transfer_Part_*.zip'))
assert len(containers)==3
manifest=None
for p in containers:
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  raw=z.read('TRANSFER_MANIFEST.json')
  if manifest is None: manifest=raw
  assert raw==manifest
  m=json.loads(raw);part=next(i for i in m['parts'] if i['container']==p.name)
  assert set(z.namelist())=={'TRANSFER_MANIFEST.json',part['payload_file']}
  b=z.read(part['payload_file']);assert len(b)==part['byte_size'];assert hashlib.sha256(b).hexdigest()==part['sha256']
  (slices/part['payload_file']).write_bytes(b)
  print(p.name,'CRC and payload SHA-256 PASS')
(slices/'TRANSFER_MANIFEST.json').write_bytes(manifest)
m=json.loads(manifest)
assert m['original_filename']=='DTU_Thesis_USB_C_Plain_Headings_2026-10-24.zip'
p=base/m['original_filename']
with p.open('wb') as out:
 for i in sorted(m['parts'],key=lambda i:i['order']):
  assert out.tell()==i['byte_offset'];out.write((slices/i['payload_file']).read_bytes())
assert p.stat().st_size==77661674
assert hashlib.sha256(p.read_bytes()).hexdigest()=='fed0ef9fadd0c1c4632b3d0f9aa057885d61714cfa8eacb5b60ed2adbbe3e8ed'
d=Path('/workspace/thesis');assert not list(d.iterdir())
with zipfile.ZipFile(p) as z:
 assert len(z.infolist())==451
 assert z.testzip() is None
 rows=[]
 for i in z.infolist():
  assert (d/i.filename).resolve().is_relative_to(d)
  assert (i.external_attr>>16)&0o170000 != 0o120000
  if not i.is_dir():rows.append({'path':i.filename,'sha256':hashlib.sha256(z.read(i)).hexdigest()})
 z.extractall(d)
 print('Original size/hash/451 entries/ZIP CRC PASS;',len(rows),'files extracted')
Path('/workspace/tooling/thesis-source-manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
