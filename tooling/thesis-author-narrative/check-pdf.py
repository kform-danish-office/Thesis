"""Validate and render the compiled voice-polished thesis without editing it."""
from pathlib import Path
import json
import re
import fitz

review = Path('/workspace/tooling/thesis-author-narrative')
pdf = Path('/workspace/thesis-build/main.pdf')
doc = fitz.open(pdf)
top = [row for row in doc.get_toc() if row[0] == 1]
chapters = {int(match.group(1)): row[2] for row in top if (match := re.match(r'^(\d+) ', row[1]))}
appendices = {match.group(1): row[2] for row in top if (match := re.match(r'^([A-J]) ', row[1]))}
assert set(chapters) == set(range(1, 13)), chapters
assert set(appendices) == set('ABCDEFGHIJ'), appendices
assert any(row[1] == 'References' for row in top)
assert all(1 <= row[2] <= len(doc) for row in top)
assert any(row[1] == 'Preface and Project Contribution' for row in top)
assert any(row[1] == 'F Project Contributions and Inherited Designs' for row in top)
abstract = next(index + 1 for index, page in enumerate(doc) if index < 16 and re.search(r'^\s*Abstract\s*$', page.get_text(), re.M))
abstract_text = re.sub(r'\s+', ' ', doc[abstract - 1].get_text())
assert 'was built and tested' in abstract_text
assert 'gave output powers' in abstract_text
assert not re.search(r'\b(?:I|my|we|our)\b', abstract_text)

outside = []
for index, page in enumerate(doc):
    for word in page.get_text('words'):
        if not word[4].strip():
            continue
        bounds = fitz.Rect(word[:4]) * page.rotation_matrix
        if bounds.x0 < -1 or bounds.y0 < -1 or bounds.x1 > page.rect.width + 1 or bounds.y1 > page.rect.height + 1:
            outside.append({'page': index + 1, 'word': word[4], 'bounds': list(bounds), 'page_bounds': list(page.rect)})

log = Path('/workspace/thesis-build/main.log').read_text(errors='replace')
errors = [line for line in log.splitlines() if re.search(r'Missing character|undefined references|undefined citations|Citation.*undefined|Reference.*undefined|multiply defined|^! ', line)]
assert not errors, errors
result = {
    'pages': len(doc), 'bytes': pdf.stat().st_size,
    'extracted_text_characters': len(Path('/workspace/thesis-build/main.txt').read_text()),
    'chapters': chapters, 'appendices': appendices, 'abstract_page': abstract,
    'top_level_bookmarks': top, 'text_outside_page': outside, 'errors': errors,
    'underfull_boxes': len(re.findall(r'Underfull \\hbox', log)),
    'overfull_boxes': len(re.findall(r'Overfull \\hbox', log)),
    'font_size_substitution_warning': 'Size substitutions with differences' in log,
}
(review / 'pdf-audit.json').write_text(json.dumps(result, indent=2) + '\n')
assert not outside, outside[:5]

output = review / 'page-previews'
output.mkdir(exist_ok=True)
selected = {1: 'cover', 3: 'preface', abstract: 'abstract', abstract + 1: 'acknowledgments', chapters[1]: 'introduction', chapters[7]: 'hardware', chapters[10]: 'results', chapters[12]: 'conclusion', appendices['E']: 'measurement-appendix', appendices['H']: 'code-appendix', appendices['J']: 'plan-appendix', len(doc): 'backpage'}
for number, label in selected.items():
    page = doc[number - 1]
    page.get_pixmap(matrix=fitz.Matrix(1200 / page.rect.width, 1200 / page.rect.width)).save(output / f'{number:03d}-{label}.png')
(review / 'rendered-pages.json').write_text(json.dumps(selected, indent=2) + '\n')
print(f'PASS: {len(doc)} pages, all 12 chapters, references and appendices A–J; abstract/passive headings correct; no missing characters/citations/references or physical-page text overflow')
print(f'Warnings: {result["underfull_boxes"]} underfull horizontal boxes; {result["overfull_boxes"]} overfull; math-font size substitutions={result["font_size_substitution_warning"]}')

# The source PDFs are embedded as static vector pages; verify every caption
# occurs on its own page in the new Appendix B section, after the LoF.
start = next(row[2]-1 for row in doc.get_toc() if 'V2 Schematic and PCB Design' in row[1])
texts = [re.sub(r'\s+', ' ', p.get_text()) for p in doc]
embedded = {}
for kind, count in [('schematic, sheet',4),('PCB print',31)]:
    for n in range(1,count+1):
        prefix=f'V2 {kind} {n}:'
        found=[i for i in range(start,len(doc)) if prefix in texts[i]]
        assert len(found)==1,(prefix,found)
        assert doc[found[0]].get_xobjects(),('missing vector page',prefix)
        embedded[prefix]=found[0]+1
assert len(set(embedded.values()))==35
(review/'embedded-document-pages.json').write_text(json.dumps(embedded,indent=2)+'\n')
print('PASS: all 4 new schematic and 31 PCB pages present in compiled thesis')

# Authorial prose should contain neither the handoff date nor chat history.
intro_start=chapters[1]-1
intro_end=chapters[2]-1
intro_text=' '.join(texts[intro_start:intro_end])
assert 'documentation supplied on' not in intro_text
assert 'October 27' not in intro_text
assert 'supplied in the chat' not in ' '.join(texts)
assert not any('October 27' in row[1] or 'October 18' in row[1] for row in doc.get_toc())
print('PASS: introduction and PDF headings contain no file-handoff dates; chat reference removed')
