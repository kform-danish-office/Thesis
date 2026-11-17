from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, hashlib, json, datetime

root = Path('/workspace/working-source/web/dist')
paths = sorted(p for p in root.rglob('*') if p.is_file())
assert len(paths) == 15
base = 'https://thesis-power-lab.vercel.app'

def verify(path):
    relative = path.relative_to(root).as_posix()
    url = base + '/' + ('' if relative == 'index.html' else relative)
    body = subprocess.check_output(['curl', '--fail', '--silent', '--show-error', '--retry', '2', url])
    assert body == path.read_bytes(), relative + ' differs from dist'
    return {'path': relative, 'url': url, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'matches_dist': True}

with ThreadPoolExecutor(max_workers=5) as pool:
    rows = list(pool.map(verify, paths))
result = {
    'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'READY',
    'deployment_id': 'dpl_zw1813ksvrYLVwtvwzYCNXDWBGZw',
    'production_url': base,
    'deployment_url': 'https://thesis-power-595hapk7q-danishoffice.vercel.app',
    'files': rows,
}
Path('/workspace/tooling/carrier-timing-review/deployment-verification.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: all 15 live app/font/license assets exactly match the final local build; TLS verified')
