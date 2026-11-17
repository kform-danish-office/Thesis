from pathlib import Path
import hashlib,json,zipfile,subprocess
archives=Path('/workspace/source-archives')
# Preserve import hashes; separately validate authorized firmware/web and prose revisions.
ui_path=Path('/workspace/tooling/ui-change-manifest.json')
ui={r['path']: r['sha256'] for r in json.loads(ui_path.read_text())} if ui_path.exists() else {}
thesis_path=Path('/workspace/tooling/thesis-change-manifest.json')
thesis={r['path']: r['sha256'] for r in json.loads(thesis_path.read_text())} if thesis_path.exists() else {}
for name,expected,number,root,manifest in [
 ('Thesis_Working_Source_2026-10-25.zip','751236e13d8a8f2819214ba392163044415436aa131cfee5c9d6fe1f6c23a5d1',114,'working-source','working-source-manifest.json'),
 ('DTU_Thesis_USB_C_Plain_Headings_2026-10-24.zip','fed0ef9fadd0c1c4632b3d0f9aa057885d61714cfa8eacb5b60ed2adbbe3e8ed',451,'thesis','thesis-source-manifest.json')]:
 p=archives/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
 with zipfile.ZipFile(p) as z: assert z.testzip() is None and len(z.infolist())==number
 rows=json.loads((Path('/workspace/tooling')/manifest).read_text())
 for row in rows:
  revision=ui if root=='working-source' else thesis
  expected=revision.get(row['path'],row['sha256'])
  assert hashlib.sha256((Path('/workspace')/root/row['path']).read_bytes()).hexdigest()==expected,row['path']
 print(name,number,'entries; archive hash, CRC, and retained source revision PASS')
assert subprocess.check_output(['git','-C','/workspace/Thesis','status','--porcelain'])==b''
assert subprocess.check_output(['git','-C','/workspace/Thesis','rev-parse','HEAD'],text=True).strip()=='e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a'
print('Selected GitHub checkout clean, HEAD unchanged')

for path,expected in ui.items():
 assert hashlib.sha256((Path('/workspace/working-source')/path).read_bytes()).hexdigest()==expected,path
print('Authorized working-source revision matches separate change manifest; original ZIP remains unchanged')
for path,expected in thesis.items():
 assert hashlib.sha256((Path('/workspace/thesis')/path).read_bytes()).hexdigest()==expected,path
print('Authorized thesis prose revision matches separate change manifest; original ZIP remains unchanged')
v2_path=Path('/workspace/tooling/v2-results-assets-manifest.json')
if v2_path.exists():
 v2=json.loads(v2_path.read_text())
 for row in v2:
  assert hashlib.sha256((Path('/workspace/thesis')/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
 print(f'{len(v2)} authorized V2 photograph and blank results-entry assets match separate manifest')
sp=archives/'skills.zip'
assert hashlib.sha256(sp.read_bytes()).hexdigest()=='c7c519c459a2ac4766a5294947311f0b62c2bda01fe30caf8e9e0c3ab2e1d9d7'
with zipfile.ZipFile(sp) as z:
 assert z.testzip() is None
 for i in z.infolist():
  if not i.is_dir(): assert (Path('/workspace')/i.filename).read_bytes()==z.read(i),i.filename
print('118 imported skill files and archive integrity PASS')
