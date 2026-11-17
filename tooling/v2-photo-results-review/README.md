# V2 photograph and blank results-entry pack — 2026-10-25

The user supplied `1000048075.jpg`, identified the board as V2, and requested a
crop/cleanup and preparation for entering its results. No measurement values
were supplied. The work adds sixteen files below `/workspace/thesis`; existing
thesis text, figures, data, frozen code and the compiled 384-page PDF are intact.

## Photo deliverables

Persistent photo directory:
`/workspace/thesis/Pictures/Thesis/07_Hardware/V2_2026-10-25`.

- `v2_board_original.jpg`: unchanged upload, 591 × 1280 pixels; SHA-256
  `0ca0e42a90be805e7854421ac385da3fdaaa08c4c43c68c9dd58b9afb005d4aa`.
- `v2_board_documentary_crop.pdf`: thesis-ready landscape framing, 495 × 322 bp,
  from x=15..510/y=333..655 in source pixels. Keeps the full visible board and
  attached connections. The embedded JPEG decodes to exactly the original RGB
  pixels; no retouching, resampling or component reconstruction. JPEG container
  metadata differs from the original, whose bytes are retained separately.
- `v2_board_cleaned_illustration.png`: the built-in imagegen cleanup, 1536 × 1024.
  It redraws small PCB details despite preservation constraints. It is labeled
  as an illustration and is not used as the thesis's documentary source.
- `figure_v2_board.tex`: ready-to-include figure that references the faithful PDF.
  It has not been inserted into the main thesis.
- `provenance.json`, `image-edit-prompt.txt` and `README.md`: identity, hashes,
  methods, the full built-in prompt and usage instructions.

The workspace imagegen skill was read and applied in built-in mode; no CLI/API
key was used. The original and generated output were inspected. The crop was
visually checked for the complete visible board perimeter. No MCU, exact board
revision, firmware, energization, electrical result or capture date was inferred.

## Entry workbook and CSVs

`/workspace/thesis/Data/measurements/v2_results/V2_Results_Entry.xlsx` contains
Instructions, Dictionary and six entry sheets: Test setup, Instruments, Steady
state, Events, Thermal and Evidence. The six matching UTF-8 CSVs are header-only.
The workbook freezes headers and the first three identifier columns, has
quantity/status dropdowns and quantity/unit checks, and contains no calculated
measurement formulas or example measurement rows. Numeric measurement cells are
blank. IDs link readings to their setup, actual time windows and retained files.

The dictionary covers actual assembly/firmware, rework and sensing calibration,
instrument settings/uncertainty, physical load, PDO/APDO negotiation, power and
auxiliary boundaries, shared measurement windows, transient timing and sustained
thermal history. It keeps MCU telemetry separate from connector measurements,
logged and recomputed PF/THD separate, instantaneous ripple separate from spread
of average readings, and surface readings separate from junction estimates.
Criteria and planned tests remain declarations, not measured outcomes. Existing
V1.0 results and the plan's reported V2 point were not copied into the templates.

## Validation and packaging

- Both crop and ready figure compiled successfully using XeLaTeX. Sources/logs:
  `documentary-crop.tex`, `crop-build.log`, `figure-check.tex`, `figure-check.log.txt`.
- Crop PDF has one page with the declared bounds. Decoded embedded pixels were
  compared byte-for-byte with the decoded original; the comparison passed.
- Workbook reload, internal ZIP CRC, six unique CSV header sets, exact sheet/CSV
  schema agreement, zero measurement rows and zero formula cells passed. A
  separate read-only review found no scientific/data-entry issues. No Excel GUI
  or real measurement-entry session was exercised.
- `python3 /workspace/tooling/v2-photo-results-review/package-assets.py` checks
  schemas and creates the starter bundle. It checks all bundle CRCs and hashes.
- `python3 /workspace/tooling/verify-sources.py` passed original archives,
  current firmware/web/prose hashes, all sixteen new assets, skills and clean
  unchanged GitHub checkout.
- `python3 /workspace/tooling/thesis-tone-review/audit-prose-revision.py` passed
  all 451 original files and separately verified the sixteen additions. Its
  protected-content assertions remain active; new assets have a separate manifest.

Bundle: `V2_Photo_Results_Starter_2026-10-25.zip` (2,837,185 bytes), SHA-256
`59e3f1399ac1e13bdde660d7704b1c4dee5974c4ce95a73fb9554c20cc0155ea`.
It contains the sixteen new files under their original `Pictures/` and `Data/`
paths, plus a README and file-hash manifest. It adds to an existing thesis source
tree; it is not a full thesis archive. `artifacts.json` records artifact hashes.

Persistent source now has 467 files: 451 retained source files and sixteen V2
additions. Their current hashes are recorded in
`/workspace/tooling/v2-results-assets-manifest.json`. Original approved archives,
import hashes and the previous 451-file prose-revision ZIP remain unchanged;
the older ZIP does not contain this new pack. When entering real data, retain
raw evidence and record the authorized new hashes without overwriting user work
to satisfy an old manifest.

No hardware was used or configured. No existing thesis source, firmware/web,
GitHub reference, sharing settings, deployment or environment publication changed.
Updated paths/limits are saved in the startup draft. The user reviews/saves and
publishes with Only me to snapshot the new files; draft saving is not publication
or proof of restoration in a fresh task.
