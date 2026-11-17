"""Check prose revision against frozen source; does not assess scientific meaning."""
from pathlib import Path
from collections import Counter
import hashlib, json, re, difflib

root = Path('/workspace/thesis')
review = Path('/workspace/tooling/apec-style-edit')
before = review/'before'
ns = {}
exec(Path('/workspace/tooling/thesis-natural-voice/audit.py').read_text().split('rows = json.loads')[0], ns)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
old = {p.relative_to(before).as_posix():p for p in before.rglob('*') if p.is_file()}
new = {p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()}
assert old.keys() == new.keys(), 'Source paths changed'
patterns = {
    'math': ns['math'],
    'quantities': re.compile(r'\\(?:SI|SIrange|SIlist|num|numrange|ang)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+'),
    'labels': re.compile(r'\\label\{[^}]*\}'),
    'citations': re.compile(r'\\cite\w*\*?(?:\[[^\]]*\])?\{[^}]*\}'),
    'paths': re.compile(r'\\(?:sourcefile|lstinputlisting|input|include|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}'),
    'references': re.compile(r'\\(?:ref|cref|Cref|eqref|pageref)\{[^}]*\}')
}
exceptions = {
    'Chapters/01_Introduction/08_V2_Prototype.tex': {
        'references': 'Removed repeated reference to the superseded beginner primer; compact signal section remains in the introduction.'
    },
    'Chapters/07_Hardware/chapter.tex': {
        'references': 'Removed repeated reference to the superseded beginner primer; compact signal section remains in the introduction.'
    },
    'Chapters/08_Control_Firmware/chapter.tex': {
        'references': 'Removed repeated reference to the superseded beginner primer; compact signal section remains in the introduction.'
    },
    'Chapters/01_Introduction/10_Controller_Basics.tex': {
        'references': 'Removed repeated prose reference to unchanged signal table; first reference retained.'
    },
    'Chapters/10_Results/12_Compliance_Table.tex': {
        'protected_environments': 'FR-04 evidence wording corrected: removed development photographs are no longer cited; no-load voltage records and implemented burst control remain partly assessed.'
    }
}
changes=[]; errors=[]; diff=[]
for name, a in sorted(old.items()):
    b=new[name]
    if sha(a)==sha(b): continue
    assert name.endswith('.tex'), ('Non-prose asset changed',name)
    left=a.read_text();right=b.read_text()
    checks={key:Counter(pat.findall(left))==Counter(pat.findall(right)) for key,pat in patterns.items()}
    normalized=left
    if name=='Chapters/10_Results/12_Compliance_Table.tex':
        normalized=left.replace('No-load means and development burst photographs','No-load voltage records; burst control implemented in firmware')
    checks['protected_environments']=ns['environments'](normalized)==ns['environments'](right)
    for key, passed in checks.items():
        if not passed and key not in exceptions.get(name,{}): errors.append({'path':name,'check':key})
    row={'path':name,'before_sha256':sha(a),'sha256':sha(b),'before_words':len(left.split()),'after_words':len(right.split()),'checks':checks}
    changes.append(row)
    diff.extend(difflib.unified_diff(left.splitlines(True),right.splitlines(True),fromfile='before/'+name,tofile='technical/'+name))
assert not re.search(r'PWR-\d',' '.join(p.read_text() for p in root.glob('Chapters/0[1-7]*/*.tex')))
primer=(root/'Chapters/01_Introduction/10_Controller_Basics.tex').read_text()
assert 'Control Architecture and Signal Definitions' in primer
assert 'small programmable computer' not in primer
assert 'tab:intro-controller-signals' in primer
assert 'development burst photographs' not in (root/'Chapters/10_Results/12_Compliance_Table.tex').read_text()
result={'baseline_files':len(old),'current_files':len(new),'edited_files':len(changes),'unchanged_files':len(new)-len(changes),'before_words_edited_files':sum(r['before_words'] for r in changes),'after_words_edited_files':sum(r['after_words'] for r in changes),'exceptions':exceptions,'errors':errors,'changes':changes}
(review/'source-audit.json').write_text(json.dumps(result,indent=2)+'\n')
(review/'technical-prose.diff').write_text(''.join(diff))
print(json.dumps({k:v for k,v in result.items() if k not in {'changes','exceptions'}},indent=2))
assert not errors, errors
