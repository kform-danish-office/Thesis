# V2 PCB export inspection

Source: `Documentation/PCB Print/_SCH DWG NO__SCH.PDF` from the user-supplied ZIP. The PDF is a 31-page Altium PCB print export for `thesis_sml.PcbDoc`. All pages are 1069 × 515 PDF points. Those are print-page dimensions, not board dimensions.

## Defensible specifications

- Four copper-layer prints are supplied: Top Layer (page 1), Int1 (GND) (page 2), Int2 (PWR) (page 3), and Bottom Layer (page 4). This supports describing the exported V2 board as a four-layer PCB with the internal layers named GND and PWR.
- The file contains two-sided component/silkscreen, solder/paste-mask, and through-board drill information. It shows components assigned to both sides. Pages 5 and 6 are the top and bottom silkscreen prints in the source's common projection; the bottom is not a standalone mirrored bottom photograph.
- Top silkscreen page 5 locates the AC connector P3, L2, C25/C28, U3 and pump network toward the input end; the planar-magnetic terminal outlines occupy the central region; J1 USB-C and its output-stage components are at the opposite end.
- Bottom silkscreen page 6 and the supplied bottom 3D render show the bottom-side controller/sensing/auxiliary circuitry and the external resonant inductor L4. The 3D render is a design view; it does not establish that L4 remained fitted during the later leakage-only bench test.
- The two inline user images are 3D design renders, not laboratory photographs. They show upright planar-magnetic assemblies, top-side bulk capacitors and USB-C connector, and bottom-side L4/controller circuitry. The ZIP does not contain those raster renders as image files: all 31 PDF pages are vector layer prints with zero embedded raster images.
- No dimensioned mechanical drawing, explicit print scale, finished board dimensions, assembled height, thickness stackup, copper weights, board volume, clearance certification, or verified continuous output rating is provided by this PCB PDF. Do not calculate V2 size or power density from the PDF page size, or substitute the old V1.0 outline. A four-layer print set does not specify finished copper thickness or isolation rating.
- Shared layer overlays/holes/pads appear on many pages. Their appearance must not be taken to mean every layer has the same copper or a component is fitted on every layer.

## Page inventory

- Page 1: Top Layer.
- Page 2: Int1 (GND).
- Page 3: Int2 (PWR).
- Page 4: Bottom Layer.
- Page 5: Top Silkscreen Overlay.
- Page 6: Bottom Silkscreen Overlay.
- Page 7: Top Paste Mask Print.
- Page 8: Bottom Paste Mask Print.
- Page 9: Top Solder Mask Print.
- Page 10: Board.
- Page 11: Top Tenting.
- Page 12: Bottom Tenting.
- Page 13: Bottom Component Center.
- Page 14: Route Tool Path.
- Page 15: Top 3D Body.
- Page 16: Bottom 3D Body.
- Page 17: Top Component Center.
- Page 18: Top Component Outline.
- Page 19: Bottom Component Outline.
- Page 20: Top Coating.
- Page 21: Bottom Coating.
- Page 22: Top Assembly.
- Page 23: Bottom Assembly.
- Page 24: Top Courtyard.
- Page 25: Bottom Courtyard.
- Page 26: Top Designator.
- Page 27: Bottom Designator.
- Page 28: Top Pad Master.
- Page 29: Bottom Pad Master.
- Page 30: Drill Drawing For (Top Layer - Bottom Layer).
- Page 31: Drill Guide For (Top Layer - Bottom Layer).

## Useful figures and retained review artifacts

- Pages 1 and 4: top/bottom copper routing overview; retain original colors and label the selected layer explicitly.
- Pages 2 and 3: internal GND/PWR layer overview.
- Pages 5 and 6: top/bottom silkscreen and component location overview; not assembly photographs.
- Page 30: drill drawing, useful if hole documentation is needed.
- `pcb-previews/contact-sheet.png`: all 31 pages at overview scale.
- `pcb-previews/page-01.png`, `page-04.png`, `page-05.png`, `page-06.png`, `page-30.png`, `page-31.png`: high-resolution representative previews.
- `pcb-previews/layers.json`: layer/page bookmark inventory.
- `pcb-top-bottom-copper.pdf`: vector page extraction of source pages 1 and 4.
- `pcb-top-bottom-silkscreen.pdf`: vector page extraction of source pages 5 and 6.

The original PDF was opened through PyMuPDF for static inspection. Embedded JavaScript was not executed. No thesis source was changed by this inspection.
