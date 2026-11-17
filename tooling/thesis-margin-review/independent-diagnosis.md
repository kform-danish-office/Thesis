# Independent margin diagnosis

Read-only inspection of the 424-page thesis PDF and current layout source. The complete prior artifact `/workspace/tooling/apec-style-edit/Thesis_V1_V2_V3.pdf` was used when the live build output began being replaced. No thesis files, builds, publication, or repository state were changed by this reviewer.

## Confirmed cause

The document uses `twoside` and previously set `inner=3.5cm,outer=2.5cm` after the cover. That creates mirrored binding margins. On single-page/continuous PDF viewing, the body visibly shifts horizontally by 10 mm at every page transition:

| Body page | Left/right text edges | Left/right margins |
| --- | --- | --- |
| 1 (physical 23) | 99.21–524.34 pt | 35 / 25 mm |
| 2 (physical 24) | 70.87–496.00 pt | 25 / 35 mm |
| 5 (physical 27) | 99.21–524.34 pt | 35 / 25 mm |
| 6 (physical 28) | 70.87–496.00 pt | 25 / 35 mm |

The sampled full-length prose lines repeatedly match these same edges; this is a layout setting, not random overflow. Long-line samples are saved in `before-margin-samples.json`; not every line is a margin probe because tables, lists, and code may be indented.

## Minimal correction

Replace only body `inner=3.5cm,outer=2.5cm` with `left=3cm,right=3cm`. This keeps the existing 150 mm text width, top/bottom geometry, text height, font, line wrapping and artwork scale while centering the body consistently. Retaining `twoside` preserves the intentional alternating footer arrangement. Expected post-change body edges are approximately 85.04–510.24 pt on both odd and even pages.

## Other layout observations

- All 424 physical MediaBoxes are A4. There are 371 portrait displayed pages and 53 intentionally rotated landscape pages. Landscape drawings/tables are not evidence of changing portrait margins.
- The only live document geometry transitions are the specially designed front cover, the body setting in `main.tex`, and the back cover. No chapter-specific `newgeometry`, manual `hoffset`/`voffset`, or side-margin changes were found. Two standalone project-record TeX files declare their own 2.5 cm geometry, but they are retained source records, not input into the main document.
- Regular continuation prose starts around y=82.15 pt. Chapter-title ink starts around y=105–106 pt, followed by the chapter introduction. The slight differences between title glyph bounds are normal font shapes; the additional opening space is consistently associated with chapter headings, not a changing geometry setting.
- `\raggedbottom` is intentionally active. Short pages and large figures therefore leave different amounts of bottom whitespace rather than stretching paragraph/list gaps. This is distinct from the horizontal 10 mm shift.
- Some figure-only pages use `[p]` and TeX's vertical float centering. Their captions may appear far down the page because artwork is above them. Comparing first extracted text coordinates on those pages would misdiagnose the top margin. No additional geometry correction is needed for them.
- Imported schematic/PCB PDFs have their own internal white space and are scaled into the same content frame. Do not crop technical artwork solely to make its ink bounds imitate prose margins.

After the correction, verify both odd/even prose and footer anchors, preserve 150 mm body width, render consecutive pages and retain all schematic/PCB pages and source content. No broader prose or float-placement edit is justified by this margin report.

## Independent post-change verification

The rebuilt current PDF was checked after changing body geometry to symmetric 30 mm margins. All 424 pages remain. On adjacent body pages 1 and 2 (physical 23/24), the full prose left edge is 85.039 pt = 29.9999 mm on both pages. Median full-line right ink edges are 510.167 pt, giving approximately 30.026 mm of right whitespace (the small difference reflects glyph ink rather than the text-box boundary). Prose width is approximately 149.976 mm on both. The rendered adjacent-page previews were inspected; body, table and footer anchors now align consistently. The chapter-opening spacing remains intentional and continuation text occupies the same top frame.

The 486-file source manifest independently confirms only `main.tex` changed. No source paths were added or removed, and the other 485 files match the before hashes. No further margin/geometry defect was identified. Numeric sample results are in `independent-postchange-verification.json`.
