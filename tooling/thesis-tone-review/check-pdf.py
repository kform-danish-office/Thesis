"""Check the compiled thesis artifact and render representative pages."""
from pathlib import Path
import json
import re
import fitz

review = Path('/workspace/tooling/thesis-tone-review')
pdf = Path('/workspace/thesis-build/main.pdf')
doc = fitz.open(pdf)
top_level = [row for row in doc.get_toc() if row[0] == 1]
chapters = [row for row in top_level if re.match(r'^\d+ ', row[1])]
appendices = [row for row in top_level if re.match(r'^[A-J] ', row[1])]
assert len(chapters) == 12, chapters
assert len(appendices) == 10, appendices
assert any(row[1] == 'References' for row in top_level)
assert all(1 <= row[2] <= len(doc) for row in top_level)
assert 'It also calls for a common method for comparing' in doc[3].get_text()

issues = []
for index, page in enumerate(doc):
    for word in page.get_text('words'):
        if not word[4].strip():
            continue
        # MuPDF word boxes are unrotated; landscape pages have a /Rotate entry.
        bounds = fitz.Rect(word[:4]) * page.rotation_matrix
        if (bounds.x0 < -1 or bounds.y0 < -1 or bounds.x1 > page.rect.width + 1 or bounds.y1 > page.rect.height + 1):
            issues.append({'page': index + 1, 'word': word[4], 'bounds': list(bounds), 'page_bounds': list(page.rect)})

log = Path('/workspace/thesis-build/main.log').read_text(errors='replace')
bad_log = [line for line in log.splitlines() if re.search(r'Missing character|undefined references|undefined citations|Citation.*undefined|Reference.*undefined|multiply defined|^! ', line)]
assert not bad_log, bad_log
result = {
    'pages': len(doc), 'bytes': pdf.stat().st_size,
    'extracted_text_characters': len(Path('/workspace/thesis-build/main.txt').read_text()),
    'chapter_count': len(chapters), 'appendix_count': len(appendices),
    'top_level_bookmarks': top_level, 'text_outside_page': issues,
    'missing_character_reference_or_citation_errors': bad_log,
    'underfull_boxes': len(re.findall(r'Underfull \\hbox', log)),
    'overfull_boxes': len(re.findall(r'Overfull \\hbox', log)),
    'font_size_substitution_warning': 'Size substitutions with differences' in log,
}
(review / 'pdf-layout-audit.json').write_text(json.dumps(result, indent=2) + '\n')
assert not issues, issues[:5]

out = review / 'page-previews'
out.mkdir(exist_ok=True)
selected = {1: 'cover', 4: 'abstract', 23: 'introduction', 100: 'results', 119: 'discussion', 126: 'conclusion', 161: 'data-appendix', 176: 'code-appendix', 381: 'plan-appendix', 384: 'backpage'}
for number, label in selected.items():
    page = doc[number - 1]
    scale = 1200 / page.rect.width
    page.get_pixmap(matrix=fitz.Matrix(scale, scale)).save(out / f'{number:03d}-{label}.png')
print(f'PASS: {len(doc)} pages; all 12 chapters, references and appendices A–J present; no missing characters/citations/references or page-bound text overflow')
print(f'Nonfatal warnings: {result["underfull_boxes"]} underfull boxes; {result["overfull_boxes"]} overfull boxes; font size substitutions={result["font_size_substitution_warning"]}')
