from pathlib import Path
import re,collections,json,difflib
base=Path('/workspace/tooling/apec-style-edit/before/Chapters')
root=Path('/workspace/thesis/Chapters')
files=[p for d in ('09_Experimental_Methods','10_Results') for p in sorted((root/d).glob('*.tex'))]
patterns={
 'SI quantities':r'\\SI(?:range)?\{[^}]*\}\{[^}]*\}(?:\{[^}]*\})?',
 'inline math':r'\\\(.*?\\\)',
 'display math':r'\\\[.*?\\\]',
 'equations':r'\\begin\{(?:equation|align)\*?\}.*?\\end\{(?:equation|align)\*?\}',
 'tables':r'\\begin\{table\}.*?\\end\{table\}',
 'figures':r'\\begin\{figure\}.*?\\end\{figure\}',
 'labels/citations/refs/paths':r'\\(?:label|cite|ref|cref|sourcefile|input|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}',
}
fail=[];stats=[]
for p in files:
 b=base/p.relative_to(root); before=b.read_text();after=p.read_text()
 if before==after:continue
 for title,pat in patterns.items():
  left=re.findall(pat,before,re.S);right=re.findall(pat,after,re.S)
  if collections.Counter(left)!=collections.Counter(right):fail.append((str(p.relative_to(root)),title,list((collections.Counter(left)-collections.Counter(right)).elements()),list((collections.Counter(right)-collections.Counter(left)).elements())))
 if (b'\r\n' in b.read_bytes())!=(b'\r\n' in p.read_bytes()):fail.append((str(p),'line endings'))
 word=lambda s:len(re.findall(r"\b[\w'-]+\b",s))
 stats.append((str(p.relative_to(root)),word(before),word(after)))
print(json.dumps({'changed_count':len(stats),'before_words':sum(t[1] for t in stats),'after_words':sum(t[2] for t in stats),'failures':fail,'files':stats},indent=2))
Path('/workspace/tooling/apec-style-edit/methods-results-validation.json').write_text(json.dumps({'changed_count':len(stats),'before_words':sum(t[1] for t in stats),'after_words':sum(t[2] for t in stats),'failures':fail,'files':stats},indent=2)+'\n')
