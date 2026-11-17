"""Validate and render the compiled V2 testing update without editing it."""
from pathlib import Path
import json
import re
import fitz

review = Path('/workspace/tooling/v2-testing-section-2026-10-27')
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
assert 'measurements were used to calculate output powers' in abstract_text
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
section = next(row for row in doc.get_toc() if 'V2 Testing and Resonant-Tank Changes' in row[1])
start_page = section[2]
end_page = next(row[2] for row in doc.get_toc() if row[0] < section[0] and row[2] > start_page)-1
assert start_page <= end_page
thermal_page = next(i+1 for i in range(start_page-1,end_page) if 'regional surface maximum' in re.sub(r'\s+', ' ', doc[i].get_text()) and doc[i].get_images())
section_text = ' '.join(doc[i].get_text() for i in range(start_page-1,end_page))
assert '60' in section_text and '1.66' in section_text and 'D10' in section_text
result = {
    'v2_section_pages': [start_page,end_page], 'v2_thermal_page': thermal_page,
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
selected.update({start_page:'v2-section-start',thermal_page:'v2-thermal-evidence',end_page:'v2-section-end'})
excerpt = fitz.open()
excerpt.insert_pdf(doc, from_page=start_page-1, to_page=end_page-1)
excerpt.save(review / 'V2_Testing_Section.pdf')
for number, label in selected.items():
    page = doc[number - 1]
    page.get_pixmap(matrix=fitz.Matrix(1200 / page.rect.width, 1200 / page.rect.width)).save(output / f'{number:03d}-{label}.png')
(review / 'rendered-pages.json').write_text(json.dumps(selected, indent=2) + '\n')
print(f'PASS: {len(doc)} pages, all 12 chapters, references and appendices A–J; new V2 section, original abstract and headings present; no missing characters/citations/references or physical-page text overflow')
print(f'Warnings: {result["underfull_boxes"]} underfull horizontal boxes; {result["overfull_boxes"]} overfull; math-font size substitutions={result["font_size_substitution_warning"]}')
