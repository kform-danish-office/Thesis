"""Check the explicitly scoped V2 content addition against its source backup."""
from pathlib import Path
import collections
import difflib
import hashlib
import json
import re

review = Path('/workspace/tooling/v2-testing-section-2026-10-27')
root = Path('/workspace/thesis')
before = review / 'before'
# Reuse the retained parser functions without running the historical audit.
parser = Path('/workspace/tooling/thesis-voice-polish/audit-prose-revision.py').read_text().split("rows = json.loads", 1)[0]
scope = {}
exec(parser, scope)
environments, macros, math = (scope[k] for k in ['environments', 'macros', 'math'])
numbers = scope['numbers']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def subsequence(old, new):
    iterator = iter(new)
    return all(any(item == candidate for candidate in iterator) for item in old)

edits = {
    'Frontmatter/Abstract.tex', 'Frontmatter/Approval.tex',
    'Chapters/07_Hardware/16_V2_F410.tex',
    'Chapters/10_Results/chapter.tex',
    'Chapters/10_Results/14_Revised_Plan_Status.tex',
    'Chapters/12_Conclusion/03_Contributions.tex', 'README.md',
}
additions = {
    'Chapters/10_Results/15_V2_Testing_Update.tex',
    'Data/project_records/V2_Testing_Update.txt',
    'Data/measurements/v2_results/evidence/v2_bridge_thermal_original.jpg',
    'Data/measurements/v2_results/evidence/v2_bridge_thermal_provenance.json',
}
baseline = json.loads((review / 'before-manifest.json').read_text())
original_paths = {r['path'] for r in baseline}
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual == original_paths | additions, {'added': actual-original_paths-additions, 'missing': original_paths-actual}
changed = []
diffs = []
for row in baseline:
    rel = row['path']
    oldp, newp = before / rel, root / rel
    assert sha(oldp) == row['sha256'], ('backup changed', rel)
    if sha(newp) == row['sha256']:
        continue
    assert rel in edits, ('unapproved change', rel)
    oldraw, newraw = oldp.read_bytes(), newp.read_bytes()
    old, new = oldraw.decode(), newraw.decode()
    assert bool(b'\r\n' in oldraw) == bool(b'\r\n' in newraw), ('newline type', rel)
    assert (oldraw.count(b'\n') == oldraw.count(b'\r\n')) == (newraw.count(b'\n') == newraw.count(b'\r\n')), ('bare LF introduced', rel)
    assert oldraw.endswith(b'\n') == newraw.endswith(b'\n'), ('EOF newline', rel)
    assert subsequence(numbers.findall(old), numbers.findall(new)), ('original numeric sequence', rel)
    assert math.findall(old) == math.findall(new), ('old math changed', rel)
    assert subsequence(macros(old), macros(new)), ('original commands/arguments', rel)
    normalized_old = old
    if rel.endswith('14_Revised_Plan_Status.tex'):
        # Only the three explicitly reviewed qualitative status rows may change.
        for identifier in ['AP-03', 'AP-05', 'AP-08']:
            a = next(line for line in old.splitlines() if line.startswith(identifier+' &'))
            b = next(line for line in new.splitlines() if line.startswith(identifier+' &'))
            normalized_old = normalized_old.replace(a, b)
        for identifier in ['AP-01', 'AP-02', 'AP-04', 'AP-06', 'AP-07']:
            a = next(line for line in old.splitlines() if line.startswith(identifier+' &'))
            b = next(line for line in new.splitlines() if line.startswith(identifier+' &'))
            assert a == b, ('quantitative plan row changed', identifier)
    assert environments(normalized_old) == environments(new), ('protected environment changed', rel)
    changed.append({'path': rel, 'baseline_sha256': row['sha256'], 'sha256': sha(newp)})
    diffs.extend(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile='before/'+rel, tofile='current/'+rel))
assert {r['path'] for r in changed} == edits

photo = root / 'Data/measurements/v2_results/evidence/v2_bridge_thermal_original.jpg'
assert photo.read_bytes() == Path('/workspace/tooling/v2-rectifier-review/1000048178-original.jpg').read_bytes()
meta = json.loads((photo.parent / 'v2_bridge_thermal_provenance.json').read_text())
assert sha(photo) == meta['original_photo']['sha256']
assert meta['user_report']['electrical_output_voltage_steady'] is True
section = (root/'Chapters/10_Results/15_V2_Testing_Update.tex').read_text()
assert '\\SI{60}{\\nano\\second}' in section
assert '\\SI{16}{\\nano\\second}' not in section
assert not re.search(r'\b(?:I|we|our|you|your)\b', section, re.I)
assert '\\label{sec:res-v2-testing}' in section
for rel in sorted(additions):
    newp = root / rel
    if newp.suffix in {'.tex', '.txt', '.json'}:
        diffs.extend(difflib.unified_diff([], newp.read_text().splitlines(True), fromfile='/dev/null', tofile='current/'+rel))
    changed.append({'path': rel, 'baseline_sha256': None, 'sha256': sha(newp)})
result = {'baseline_files': len(baseline), 'current_files': len(actual), 'edited_files': len(edits), 'added_files': len(additions), 'unchanged_files': len(baseline)-len(edits), 'authorized_status_row_updates': ['AP-03','AP-05','AP-08'], 'errors': [], 'changes': changed}
(review/'source-audit.json').write_text(json.dumps(result, indent=2)+'\n')
(review/'v2-testing.diff').write_text(''.join(diffs))
print('PASS:',len(edits),'existing files updated;',len(additions),'additions;',len(baseline)-len(edits),'existing files byte-identical')
print('Original numbers, equations, command arguments, technical environments (apart from three explicit status rows), source paths and thermal-photo pixels preserved')
