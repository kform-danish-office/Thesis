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
review = Path('/workspace/tooling/thesis-natural-voice')
before = review / 'before'
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
    return (path.startswith('Chapters/') and path.endswith('.tex')) or path in {'Frontmatter/Abstract.tex','Frontmatter/Approval.tex','Frontmatter/Acknowledgements.tex','README.md'} or (path.startswith('Backmatter/Appendices/') and path.endswith('.tex'))

def prose_pronouns(text):
    # Reporting aid: a remaining I can be an electrical symbol or a Roman numeral.
    text = math.sub('', text)
    for env in protected_envs:
        text = re.sub(r'\\begin\{' + re.escape(env) + r'\}.*?\\end\{' + re.escape(env) + r'\}', '', text, flags=re.S)
    text = re.sub(r'\\(?:texttt|sourcefile|url|path|lstinputlisting|input|includegraphics|cite\w*|ref|cref|Cref|label)\*?(?:\[[^]]*\])?(?:\{(?:[^{}]|\{[^{}]*\})*\})+', '', text)
    found=[]
    for line in text.splitlines():
        if re.search(r'\b(?:I|me|my|My|we|We|our|Our|you|You|your|Your)\b', line):
            found.append(line.strip())
    return found

rows = json.loads((review / 'before-manifest.json').read_text())
heading_edits = json.loads((review / 'heading-edits.json').read_text())
original_paths = {row['path'] for row in rows}
actual_paths = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual_paths == original_paths, {'added': sorted(actual_paths-original_paths), 'removed': sorted(original_paths-actual_paths)}
changes=[]
errors=[]
diffs=[]
pronouns={}
authorized_headings=[]
for row in rows:
    relative = row['path']
    old_path, new_path = before / relative, root / relative
    assert sha(old_path) == row['sha256'], ('backup modified',relative)
    current=sha(new_path)
    if new_path.suffix == '.tex' and (relative.startswith(('Chapters/','Backmatter/Appendices/')) or relative in {'Frontmatter/Abstract.tex','Frontmatter/Approval.tex','Frontmatter/Acknowledgements.tex'}):
        remaining=prose_pronouns(new_path.read_text())
        if remaining: pronouns[relative]=remaining
    if current == row['sha256']:
        continue
    if not allowed(relative):
        errors.append({'path':relative,'check':'outside authorized prose scope'})
        continue
    old_raw,new_raw=old_path.read_bytes(),new_path.read_bytes()
    old,new=old_raw.decode('utf-8'),new_raw.decode('utf-8')
    normalized_old=old
    for original,revised in heading_edits.get(relative,[]):
        if revised in new:
            assert normalized_old.count(original)==1,(relative,original)
            assert new.count(revised)==1,(relative,revised)
            normalized_old=normalized_old.replace(original,revised)
            authorized_headings.append({'path':relative,'before':original,'after':revised})
    checks={
        'numeric_sequence':numbers.findall(old)==numbers.findall(new),
        'math':math.findall(old)==math.findall(new),
        'protected_environments':environments(old)==environments(new),
        'latex_commands_and_arguments_except_authorized_headings':macros(normalized_old)==macros(new),
        'newline_style':(b'\r\n' in old_raw)==(b'\r\n' in new_raw) and (old_raw.count(b'\n')-old_raw.count(b'\r\n')==0)==(new_raw.count(b'\n')-new_raw.count(b'\r\n')==0),
        'final_newline':old_raw.endswith(b'\n')==new_raw.endswith(b'\n'),
    }
    for check,passed in checks.items():
        if not passed:errors.append({'path':relative,'check':check})
    changes.append({'path':relative,'sha256':current,'baseline_sha256':row['sha256'],'bytes_before':len(old_raw),'bytes_after':len(new_raw),'checks':checks})
    diffs.extend(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='before/'+relative,tofile='polished/'+relative))
result={'baseline_files':len(rows),'changed_files':len(changes),'unchanged_files':len(rows)-len(changes),'authorized_heading_changes':authorized_headings,'errors':errors,'remaining_pronoun_candidates':pronouns,'changes':changes}
(review/'prose-audit.json').write_text(json.dumps(result,indent=2)+'\n')
(review/'wording.diff').write_text(''.join(diffs))
print(json.dumps({k:v for k,v in result.items() if k not in {'changes','remaining_pronoun_candidates','authorized_heading_changes'}},indent=2))
print('Authorized heading/TOC edits:',len(authorized_headings),'files with pronoun candidates:',len(pronouns))
if errors:raise SystemExit(1)
print('PASS: numeric sequences, math, protected environments, LaTeX commands/arguments except explicit heading edits, newline styles and all non-prose files preserved')
