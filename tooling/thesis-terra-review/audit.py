from pathlib import Path
import collections, difflib, hashlib, json, re, zipfile

root = Path('/workspace/thesis')
review = Path('/workspace/tooling/thesis-terra-review')
baseline = Path('/workspace/tooling/thesis-direct-results/Thesis_V1_V2_V3_Source.zip')
judgements = json.loads((review/'judgements.json').read_text())
expected = collections.defaultdict(list)
for j in judgements:
    expected[j['path']].append(j)

files = {p.relative_to(root).as_posix(): p for p in root.rglob('*') if p.is_file()}
changed, diffs = [], []
with zipfile.ZipFile(baseline) as archive:
    assert set(archive.namelist()) == set(files)
    for name, path in files.items():
        before, after = archive.read(name), path.read_bytes()
        if before == after:
            continue
        assert name in expected, name
        changed.append(name)
        assert before == (review/'before'/name).read_bytes(), name
        original = before.decode()
        proposed = original
        for j in expected[name]:
            assert proposed.count(j['old']) == 1, j['id']
            proposed = proposed.replace(j['old'], j['final_new'])
        assert proposed.encode() == after, name
        # Repeated quantities may be deleted, but their values and units remain.
        for pattern in [r'\\SI\{[^}]+\}\{[^}]+\}', r'\\(?:label|cite|cref|ref|eqref)\{[^}]+\}']:
            assert set(re.findall(pattern, original)) == set(re.findall(pattern, proposed)), (name, pattern)
        for env in ['equation', 'align', 'gather']:
            pattern = rf'\\begin\{{{env}\*?\}}.*?\\end\{{{env}\*?\}}'
            assert re.findall(pattern, original, re.S) == re.findall(pattern, proposed, re.S), name
        diffs += difflib.unified_diff(original.splitlines(True), proposed.splitlines(True), fromfile='before/'+name, tofile='after/'+name)
assert set(changed) == set(expected)
assert not any(p.startswith(('Pictures/', 'Code/', 'Data/', 'Setup/')) for p in changed)

manifest_path = Path('/workspace/tooling/thesis-change-manifest.json')
manifest = json.loads(manifest_path.read_text())
by_path = {r['path']:r for r in manifest}
originals = {r['path']:r['sha256'] for r in json.loads(Path('/workspace/tooling/thesis-source-manifest.json').read_text())}
for name in changed:
    if name not in by_path:
        entry = {'path':name, 'original_sha256':originals[name]}
        manifest.append(entry)
        by_path[name] = entry
    by_path[name]['sha256'] = hashlib.sha256(files[name].read_bytes()).hexdigest()
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
(review/'changes.diff').write_text(''.join(diffs))
result = {
    'source_files':len(files), 'changed_files':sorted(changed),
    'unchanged_files':len(files)-len(changed), 'applied_proposals':len(judgements),
    'accepted':sum(j['decision']=='Accept' for j in judgements),
    'lead_rewritten':sum(j['decision']=='Revise' for j in judgements),
    'exact_approved_replacements_only':True,
    'unique_quantities_units_and_references_preserved':True,
    'display_equations_preserved':True,
    'code_data_images_and_layout_unchanged':True,
}
(review/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
