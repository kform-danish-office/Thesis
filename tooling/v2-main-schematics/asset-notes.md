# V2 schematic display crops

Prepared four new derived PDFs (five pages) from the latest approved V2 schematic. Originals and all previous V1.1 crops are unchanged. No .tex/build/manifest/GitHub edits were performed by the asset task.

The generation script uses PyMuPDF `show_pdf_page` at unit scale with rectangular clips. All circuit symbols, wires, labels and values remain original vector content. Functional box boundaries are retained; unrelated sheet borders/title blocks are outside the clips. The source Altium logo image resource survives inside the original page form but is outside every displayed crop; no visible circuit content is rasterized.

## Outputs

- `Pictures/Thesis/07_Hardware/Rebuilt/schematic_v2_power_stage_excerpt.pdf`: 1 page(s).
  Source sheet 3, rectangle [22, 261, 1662, 629] points: Complete resonant/transformer, GaN half-bridge, and secondary rectifier/output boxes, including the charge-pump branch.
- `Pictures/Thesis/07_Hardware/Rebuilt/schematic_v2_input_excerpt.pdf`: 2 page(s).
  Source sheet 3, rectangle [22, 49, 748, 247] points: Complete AC input / EMI filter box.
  Source sheet 3, rectangle [762, 31, 957, 247] points: Complete mains rectifier box.
- `Pictures/Thesis/07_Hardware/Rebuilt/schematic_v2_usb_excerpt.pdf`: 1 page(s).
  Source sheet 2, rectangle [87, 65, 1200, 655] points: All functional USB-PD sheet regions, including bulk/output filtering, status, I2C service, controller/power stage/USB-C, and ground filter.
- `Pictures/Thesis/07_Hardware/Rebuilt/schematic_v2_controller_excerpt.pdf`: 1 page(s).
  Source sheet 4, rectangle [381, 89, 1230, 657] points: Complete MCU/power and control/sense-interface boxes; STLINK and status-LED boxes outside this crop remain on the full appendix sheet.

## Review and preservation

All five preview pages were visually inspected. The circuit regions are complete and reference labels remain within their functional boxes. Input filtering and mains rectification use separate PDF pages compatible with the existing two-subfigure schema. Power uses the complete charge-pump/resonant, GaN half-bridge and secondary-rectifier row, preserving shared signal names; auxiliary and sensing boxes are intentionally not part of that excerpt. The full source sheet remains in Appendix B. USB includes all functional boxes. MCU includes MCU/power plus control/sense-interface boxes.

Crops rendered at 144 dpi were compared against the corresponding original source regions. Three are pixel-identical; power and USB differ only in sub-pixel antialias samples from PDF form matrix serialization (mean channel error less than 0.001 on a 0–255 scale). Detailed metrics, crop coordinates and hashes are in `crop-manifest.json`. The source hash remains c2623551c7094d2caa60efbbd3dab674b49553c6a3e39d8407afe83cb36c8ad2.

## Caption and circuit context

- The power crop contains no auxiliary rails or isolated-sense circuits; captions should name the charge-pump branch, GaN half bridge, resonant/transformer path and secondary rectifier only.
- V2 sheet 4 shows gate commands at PA8/PB13 and burst enable at PA11, with PA0/PA1/PA2 sense signals. The previous V1.1 PA8/PA9/PA10 caption cannot be retained. This crop does not show the previous sheet’s analog-buffer region.
- V2 rectifier labels are D4/D5/D9/D10, S4D02120T. V2 sheet 3 input is the drawn 100 µH 7447480101 L2 element. Do not relabel these crops as the fitted V1 baseline or silently apply their component labels to earlier numerical tests.
- The V2 resonant drawing retains its drawn L4 SER1512-103MED and C26 component positions; the later leakage-only tank is a bench modification described separately.
- At approximately 234 mm landscape width the main power and USB views retain considerably more zoom detail than raster figures; MCU at 150 mm portrait width has small component labels (roughly 4–5 pt for the larger source text). They remain sharp on PDF zoom. Captions and prose should carry essential signal roles rather than require reading every schematic pin.

Reproduce with `python3 /workspace/tooling/v2-main-schematics/generate-crops.py`.
