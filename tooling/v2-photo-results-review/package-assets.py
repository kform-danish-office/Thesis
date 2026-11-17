from pathlib import Path
import csv
import hashlib
import json
import zipfile
from openpyxl import load_workbook

root = Path('/workspace/thesis')
review = Path('/workspace/tooling/v2-photo-results-review')
data = root / 'Data/measurements/v2_results'
photos = root / 'Pictures/Thesis/07_Hardware/V2_2026-10-25'
book = data / 'V2_Results_Entry.xlsx'
wb = load_workbook(book, data_only=False)
sheets = {'test_setup.csv': 'Test setup', 'instruments.csv': 'Instruments', 'steady_state.csv': 'Steady state', 'events.csv': 'Events', 'thermal.csv': 'Thermal', 'evidence.csv': 'Evidence'}
for filename, sheet in sheets.items():
    with (data / filename).open(newline='', encoding='utf-8') as handle:
        rows = list(csv.reader(handle))
    assert len(rows) == 1 and len(rows[0]) == len(set(rows[0])), filename
    ws = wb[sheet]
    assert ws.max_row == 1, sheet
    assert [cell.value for cell in ws[1]] == rows[0], sheet
    assert ws.freeze_panes == 'D2', sheet  # first row and first three ID columns
assert all(cell.data_type != 'f' for ws in wb for row in ws for cell in row)
with zipfile.ZipFile(book) as archive:
    assert archive.testzip() is None
print('PASS: workbook and six CSV schemas agree; no measurement rows or formula cells; frozen headers and ZIP CRC valid')

files = sorted(path for directory in [data, photos] for path in directory.rglob('*') if path.is_file())
assert len(files) == 16, len(files)
manifest = [{'path': path.relative_to(root).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size} for path in files]
Path('/workspace/tooling/v2-results-assets-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
readme = '''# V2 photo and results-entry starter

This package adds files to an existing thesis source tree, preserving their Pictures/ and Data/ paths. It is not a complete thesis source archive.

Start with Data/measurements/v2_results/V2_Results_Entry.xlsx. All six entry sheets are blank; use the Instructions and Dictionary sheets. UTF-8 CSV alternatives and the full dictionary are beside the workbook. No measurements, board settings or results have been inferred.

For the thesis use Pictures/Thesis/07_Hardware/V2_2026-10-25/v2_board_documentary_crop.pdf: the source photograph's pixels are unchanged. The original JPG is retained. v2_board_cleaned_illustration.png is an AI-edited illustration with redrawn fine details and is not technical measurement evidence.

figure_v2_board.tex is ready to include in the V2 hardware section. It has not been inserted into the existing thesis. The user identified this photograph as V2; exact assembly ID, MCU, firmware and capture date remain to be entered.

V2_FILE_HASHES.json records all sixteen additions. No existing thesis source, data, bibliography, figures, firmware, hardware setting or Git checkout was changed.
'''
(review / 'README_V2_PHOTO_RESULTS.md').write_text(readme)
archive_path = review / 'V2_Photo_Results_Starter_2026-10-25.zip'
with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, path.relative_to(root).as_posix())
    archive.writestr('V2_FILE_HASHES.json', json.dumps(manifest, indent=2) + '\n')
    archive.writestr('README_V2_PHOTO_RESULTS.md', readme)
with zipfile.ZipFile(archive_path) as archive:
    assert archive.testzip() is None and len(archive.infolist()) == 18
    for row in manifest:
        assert hashlib.sha256(archive.read(row['path'])).hexdigest() == row['sha256']
artifacts = [book, photos / 'v2_board_documentary_crop.pdf', photos / 'v2_board_cleaned_illustration.png', archive_path]
result = {'source_root': str(root), 'added_source_files': 16, 'existing_source_files_modified': 0, 'measurement_rows': 0, 'workbook_sheets': wb.sheetnames, 'artifacts': [{'path': str(path), 'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in artifacts]}
(review / 'artifacts.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
