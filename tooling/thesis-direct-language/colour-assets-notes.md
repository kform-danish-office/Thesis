# Colour V2 schematic crops

The four current main-text display PDFs were regenerated from the approved `Schematic_V2_Colour.pdf`. The original source is unchanged at SHA-256 `7af67969cea32d270498dacdd244b937c2496f113b85038893dbc88260f8d031`. Existing grey schematic masters were compared with the frozen baseline and remain byte-identical.

The crop rectangles and page dimensions are identical to the previous grey display crops. All symbols, nets, labels and values remain original vector content; no drawing was redrawn, recoloured, rasterized or converted to grey. Each of the five output pages has exactly the same extracted word labels as its previous grey crop.

## Outputs

- `schematic_v2_power_stage_excerpt.pdf`: one page, complete charge-pump/resonant, GaN half-bridge and secondary-rectifier row.
- `schematic_v2_input_excerpt.pdf`: two pages, complete AC input/filter and mains-rectifier boxes.
- `schematic_v2_usb_excerpt.pdf`: one page, all functional USB-PD regions.
- `schematic_v2_controller_excerpt.pdf`: one page, complete MCU/power and control/sense-interface boxes.

All five preview pages were visually inspected. They preserve the original blue conductors/symbols, red net labels and highlighted component bodies. Colour-pixel counts at 144 dpi are nonzero for every crop (7.6%–11.7% of pixels differ materially between RGB channels). Rendering each derived page against the corresponding colour source region gives exact pixels for three crops; power and USB have only PDF-form subpixel antialias differences, with mean channel error below 0.001 on a 0–255 scale.

No raster image intersects any displayed crop. The source Altium-logo image resource is inherited inside the source page form outside the clipping rectangle. All shown electrical content is vector. Detailed source rectangles, output hashes, colour counts and render-comparison metrics are in `colour-crop-manifest.json`.

Reproduce with `python3 /workspace/tooling/thesis-direct-language/generate-colour-crops.py`. Previous review scripts/assets under `v2-main-schematics` were not modified. No TeX, source-change manifest, build, code, hardware or GitHub changes were made by this asset task. Root owns the appendix master-PDF switch and full-thesis build.
