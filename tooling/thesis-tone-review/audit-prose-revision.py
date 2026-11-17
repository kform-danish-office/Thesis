"""Audit a prose-only revision against the untouched local baseline.

This checks protected content, not scientific meaning; changed prose still
requires editorial review. No LaTeX source is modified by this script.
"""
from pathlib import Path
import collections
import difflib
import hashlib
import json
import re

root = Path('/workspace/thesis')
review = Path('/workspace/tooling/thesis-tone-review')
before = review / 'original-source'
protected_envs = {
    'table', 'table*', 'figure', 'figure*', 'longtable', 'tabular', 'tabular*',
    'tabularx', 'array', 'equation', 'equation*', 'align', 'align*', 'aligned',
    'gather', 'gather*', 'multline', 'multline*', 'displaymath', 'math',
    'lstlisting', 'verbatim', 'Verbatim', 'tikzpicture', 'circuitikz',
    'algorithm', 'algorithmic',
}
command = re.compile(r'\\(?:[A-Za-z@]+\*?|[^A-Za-z\s])')
env_token = re.compile(r'\\(begin|end)\{([^}]+)\}')
numbers = re.compile(r'\d+(?:\.\d+)*')
math = re.compile(r'\\\(.*?\\\)|\\\[.*?\\\]|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$', re.S)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def environments(text):
    stack = []
    result = []
    for token in env_token.finditer(text):
        kind, name = token.groups()
        if kind == 'begin':
            stack.append((name, token.start()))
        else:
            assert stack and stack[-1][0] == name, ('mismatched environment', name)
            _, start = stack.pop()
            if name in protected_envs:
                result.append((start, text[start:token.end()]))
    assert not stack, ('unclosed environments', stack)
    return [value for _, value in sorted(result)]

def macros(text):
    """Capture each control sequence with adjacent balanced argument groups."""
    result = []
    for match in command.finditer(text):
        end = match.end()
        groups = []
        while True:
            start = end
            while start < len(text) and text[start].isspace():
                start += 1
            if start == len(text) or text[start] not in '{[':
                break
            opening = text[start]
            closing = '}' if opening == '{' else ']'
            depth = 1
            cursor = start + 1
            while cursor < len(text) and depth:
                if text[cursor] == '\\':
                    cursor += 2
                    continue
                if text[cursor] == opening:
                    depth += 1
                elif text[cursor] == closing:
                    depth -= 1
                cursor += 1
            if depth:
                break  # invalid source is also checked by the actual TeX build
            groups.append(text[start:cursor])
            end = cursor
        result.append((match.group(), groups))
    return result

def allowed(path):
    return (path.startswith('Chapters/') and path.endswith('.tex')) or path == 'Frontmatter/Abstract.tex' or (path.startswith('Backmatter/Appendices/') and path.endswith('.tex'))

rows = json.loads((review / 'baseline-manifest.json').read_text())
original_paths = {row['path'] for row in rows}
actual_paths = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
# Later user-authorized V2 additions are checked separately; this audit still
# compares every original source and all protected prose content to its baseline.
added_manifest = Path('/workspace/tooling/v2-results-assets-manifest.json')
added_rows = json.loads(added_manifest.read_text()) if added_manifest.exists() else []
added_paths = {row['path'] for row in added_rows}
assert not original_paths.intersection(added_paths), 'V2 additions must not replace original source'
assert actual_paths == original_paths | added_paths, {'added': sorted(actual_paths-original_paths-added_paths), 'removed': sorted(original_paths-actual_paths)}
for row in added_rows:
    assert sha(root / row['path']) == row['sha256'], ('V2 addition changed', row['path'])
changes = []
errors = []
diffs = []
for row in rows:
    relative = row['path']
    old_path, new_path = before / relative, root / relative
    assert sha(old_path) == row['sha256'], ('backup modified', relative)
    current = sha(new_path)
    if current == row['sha256']:
        continue
    if not allowed(relative):
        errors.append({'path': relative, 'check': 'outside authorized prose scope'})
        continue
    old_raw, new_raw = old_path.read_bytes(), new_path.read_bytes()
    old, new = old_raw.decode('utf-8'), new_raw.decode('utf-8')
    checks = {
        'numeric_sequence': numbers.findall(old) == numbers.findall(new),
        'math': math.findall(old) == math.findall(new),
        'protected_environments': environments(old) == environments(new),
        'latex_commands_and_arguments': macros(old) == macros(new),
        'newline_style': (b'\r\n' in old_raw) == (b'\r\n' in new_raw) and (old_raw.count(b'\n')-old_raw.count(b'\r\n') == 0) == (new_raw.count(b'\n')-new_raw.count(b'\r\n') == 0),
    }
    for check, passed in checks.items():
        if not passed:
            errors.append({'path': relative, 'check': check})
    change = {'path': relative, 'sha256': current, 'original_sha256': row['sha256'], 'bytes_before': len(old_raw), 'bytes_after': len(new_raw), 'checks': checks}
    changes.append(change)
    diffs.extend(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), fromfile='original/'+relative, tofile='current/'+relative))

result = {'baseline_files': len(rows), 'changed_files': len(changes), 'unchanged_files': len(rows)-len(changes), 'separately_verified_v2_additions': len(added_rows), 'errors': errors, 'changes': changes}
(review / 'prose-audit.json').write_text(json.dumps(result, indent=2)+'\n')
(review / 'prose.diff').write_text(''.join(diffs))
print(json.dumps({key: value for key, value in result.items() if key != 'changes'}, indent=2))
if errors:
    raise SystemExit(1)
print('PASS: numeric sequences, math, environments, LaTeX commands/arguments, newline style and all non-prose assets preserved')
