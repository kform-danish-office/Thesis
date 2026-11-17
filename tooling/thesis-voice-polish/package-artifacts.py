"""Package the revised source and PDF only after the preservation/build checks."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

review = Path('/workspace/tooling/thesis-voice-polish')
source = Path('/workspace/thesis')
audit = json.loads((review / 'prose-audit.json').read_text())
pdf_audit = json.loads((review / 'pdf-audit.json').read_text())
assert not audit['errors']
assert not pdf_audit['errors'] and not pdf_audit['text_outside_page']
files = sorted(p for p in source.rglob('*') if p.is_file())
assert len(files) == audit['baseline_files'] == 467

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Verify the audited file set has not changed while packaging.
baseline = {row['path']: row['sha256'] for row in json.loads((review / 'before-manifest.json').read_text())}
baseline.update({row['path']: row['sha256'] for row in audit['changes']})
assert {p.relative_to(source).as_posix(): sha(p) for p in files} == baseline

pdf = review / 'Richard_Xu_Thesis_Voice_Polished_2026-10-25.pdf'
shutil.copy2('/workspace/thesis-build/main.pdf', pdf)
assert pdf.stat().st_size == pdf_audit['bytes']
archive = review / 'Thesis_Voice_Polished_2026-10-25.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for path in files:
        z.write(path, path.relative_to(source))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.infolist()) == len(files)
    assert set(z.namelist()) == set(baseline)
    for member in z.infolist():
        assert hashlib.sha256(z.read(member)).hexdigest() == baseline[member.filename]

artifacts = [{'name': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in [pdf, archive]]
(review / 'artifacts.json').write_text(json.dumps({'pages': pdf_audit['pages'], 'source_files': len(files), 'artifacts': artifacts}, indent=2) + '\n')
(review / 'SHA256SUMS').write_text(''.join(f"{row['sha256']}  {row['name']}\n" for row in artifacts))
print(json.dumps({'pages': pdf_audit['pages'], 'source_files': len(files), 'artifacts': artifacts}, indent=2))
print('PASS: source archive CRCs, paths and every member hash match the audited source')
