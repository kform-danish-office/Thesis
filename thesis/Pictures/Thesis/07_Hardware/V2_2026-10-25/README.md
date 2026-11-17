# V2 board photograph

The user supplied `1000048075.jpg` and identified the board as **V2** on
2026-10-25. That identifies the hardware generation; the exact assembly ID,
fitted MCU, running firmware, photo capture date and test conditions have not
been entered. The photograph is not a measurement result.

- `v2_board_original.jpg`: unchanged uploaded JPEG, 591 × 1280 pixels.
- `v2_board_documentary_crop.pdf`: tight landscape crop for the thesis. It keeps
  the full visible PCB perimeter and attached connections and crops away most
  of the room and lower bench. LaTeX trim/clip changes the framing only. The
  embedded JPEG's decoded RGB pixels match the original exactly; its JPEG
  container metadata can differ. No retouching, resampling or invented detail.
- `v2_board_cleaned_illustration.png`: built-in imagegen crop/lighting cleanup,
  1536 × 1024 pixels. It redraws fine PCB details. Use as an edited illustration,
  not to identify components, connections, fitted values or measurements.
- `figure_v2_board.tex`: ready-to-include figure using the documentary PDF.
- `provenance.json`: source hash, crop coordinates, user identification and
  separate provenance for both versions.
- `image-edit-prompt.txt`: full prompt used for the illustration.

To include the source-faithful figure in the V2 hardware section:

```tex
\input{Pictures/Thesis/07_Hardware/V2_2026-10-25/figure_v2_board.tex}
```

It is prepared but not inserted into the current thesis. Existing V1.0
photographs and results retain their original identity. Blank V2 measurement
templates and the entry workbook are in `Data/measurements/v2_results`.

The documentary crop is reproducible from
`/workspace/tooling/v2-photo-results-review/documentary-crop.tex` with XeLaTeX.
Its source-coordinate rectangle is x=15..510, y=333..655 (top-left origin).
The original photograph is the reference if the cleaned illustration differs.
