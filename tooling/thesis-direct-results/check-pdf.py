"""Validate and render the compiled voice-polished thesis without editing it."""
from pathlib import Path
import json
import re
import fitz

review = Path('/workspace/tooling/thesis-direct-results')
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
assert any(row[1] == 'F Project Contributions and Earlier DTU Designs' for row in top)
abstract = next(index + 1 for index, page in enumerate(doc) if index < 16 and re.search(r'^\s*Abstract\s*$', page.get_text(), re.M))
abstract_text = re.sub(r'\s+', ' ', doc[abstract - 1].get_text().replace('-\n',''))
assert 'was implemented' in abstract_text
assert 'yielded' in abstract_text and 'preliminary efficiency estimates' in abstract_text
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

for title in ['From the V2 Findings to V3','V3 Edge-Card Design','V3 Design Outcome and Revision Comparison']:
    assert any(title in row[1] for row in doc.get_toc()),title
v3_page=next(row[2]-1 for row in doc.get_toc() if 'V3 Design Outcome and Revision Comparison' in row[1])
v3_text=' '.join(texts[v3_page:v3_page+2])
assert re.search(r'8\s*%',v3_text)
assert 'estimate' in v3_text and 'USB-PD' in v3_text
print('PASS: V1/V2/V3 development sections and qualified design-volume outcome present')

signal_page=next(row[2] for row in doc.get_toc() if 'Control Architecture and MCU Pins' in row[1])
v2_page=next(row[2] for row in doc.get_toc() if 'Development of the V2 Prototype' in row[1])
assert signal_page<v2_page
signal_text=' '.join(texts[signal_page-1:v2_page])
assert 'primary' in signal_text and 'PA0' in signal_text
assert 'PA1' in signal_text and 'PA2' in signal_text
assert 'PC4' in signal_text and 'PB13' in signal_text
assert 'MCU pin' in signal_text and 'pin assignments' in signal_text
assert 'small programmable computer' not in signal_text
assert not any('Circuit and Controller Basics' in row[1] for row in doc.get_toc())
print('PASS: compact control-architecture section and board-specific signal table precede V2 pin references')

all_text=' '.join(texts)
for removed in ['Development capture with irregular partial switching','Clean carrier burst after no-load tuning','Qualitative record of no-load switching development','No-load development photographs']:
    assert removed not in all_text,removed
results_start=chapters[10]-1
raw=[i for i in range(results_start,len(doc)) if 'Raw C2 waveforms' in texts[i]]
assert raw and doc[raw[0]].get_xobjects()
print('PASS: selected photo figure/caption removed; raw C2 waveform figure retained')

identity_page=next(row[2]-1 for row in doc.get_toc() if 'Firmware Development and Versions' in row[1])
identity_text=' '.join(texts[identity_page:identity_page+2])
assert 'PWR-1.9.20' in identity_text and 'PWR-2.0.4' in identity_text
assert 'firmware' in identity_text.lower() and 'PWR' in identity_text
# Before the control chapter, revision numbers are not used as narrative labels.
main_early=' '.join(texts[chapters[1]-1:chapters[8]-1])
assert not re.search(r'PWR-[0-9]',main_early)
print('PASS: software identities introduced in context; early prose uses descriptive stages')
