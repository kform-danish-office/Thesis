"""Display-only vector crops of the approved V2 schematic; no drawing edits."""
from pathlib import Path
import fitz
import hashlib
import json
import numpy as np

root = Path('/workspace/thesis')
review = Path('/workspace/tooling/v2-main-schematics')
source = root / 'Pictures/Thesis/07_Hardware/Schematic_V2_F410_2026-10-27.pdf'
destination = root / 'Pictures/Thesis/07_Hardware/Rebuilt'
previews = review / 'crop-previews'
previews.mkdir(exist_ok=True)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
original_sha = sha(source)

# Page numbers below are one-based source sheet numbers; bounds are source
# PDF points. Each selected rectangle contains complete functional boxes.
specifications = {
    'power_stage': [
        {'sheet': 3, 'clip': [22, 261, 1662, 629],
         'scope': 'Complete resonant/transformer, GaN half-bridge, and secondary rectifier/output boxes, including the charge-pump branch.'},
    ],
    'input': [
        {'sheet': 3, 'clip': [22, 49, 748, 247],
         'scope': 'Complete AC input / EMI filter box.'},
        {'sheet': 3, 'clip': [762, 31, 957, 247],
         'scope': 'Complete mains rectifier box.'},
    ],
    'usb': [
        {'sheet': 2, 'clip': [87, 65, 1200, 655],
         'scope': 'All functional USB-PD sheet regions, including bulk/output filtering, status, I2C service, controller/power stage/USB-C, and ground filter.'},
    ],
    'controller': [
        {'sheet': 4, 'clip': [381, 89, 1230, 657],
         'scope': 'Complete MCU/power and control/sense-interface boxes; STLINK and status-LED boxes outside this crop remain on the full appendix sheet.'},
    ],
}

src = fitz.open(source)
manifest = {'source': str(source.relative_to(root)),
            'source_sha256': original_sha,
            'method': 'PyMuPDF show_pdf_page, unit-scale rectangular clip; no redraw or rasterization',
            'outputs': []}
for name, specs in specifications.items():
    out = fitz.open()
    for spec in specs:
        clip = fitz.Rect(spec['clip'])
        page = out.new_page(width=clip.width, height=clip.height)
        page.show_pdf_page(page.rect, src, spec['sheet']-1, clip=clip)
    path = destination / f'schematic_v2_{name}_excerpt.pdf'
    out.set_metadata({'title': f'V2 schematic {name.replace("_", " ")} display crop',
                      'subject': 'Original vector schematic content; display crop only',
                      'creator': 'PyMuPDF vector clipping'})
    out.save(path, garbage=4, deflate=True)
    out.close()
    check = fitz.open(path)
    pages = []
    for index, spec in enumerate(specs):
        page = check[index]
        assert page.get_xobjects(), 'Vector source object absent'
        visible_images = [x for x in page.get_image_info() if (fitz.Rect(x['bbox']) & page.rect).get_area() > 0]
        assert not visible_images, 'Unexpected visible raster content'
        scale = 2
        original = src[spec['sheet']-1].get_pixmap(matrix=fitz.Matrix(scale, scale), clip=fitz.Rect(spec['clip']))
        actual = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        assert original.width == actual.width and original.height == actual.height
        aa = np.frombuffer(original.samples, dtype=np.uint8).astype(np.int16)
        bb = np.frombuffer(actual.samples, dtype=np.uint8).astype(np.int16)
        mean_difference = float(np.abs(aa-bb).mean())
        differing_fraction = float(np.count_nonzero(aa != bb) / aa.size)
        # PDF form matrix serialization can move sub-pixel antialias samples.
        # Keep numerical tolerances far below visible geometry/label changes.
        match = mean_difference < 0.02 and differing_fraction < 0.005
        assert match, (name, index, mean_difference, differing_fraction)
        page.get_pixmap(matrix=fitz.Matrix(1500/page.rect.width, 1500/page.rect.width)).save(previews/f'{name}-{index+1}.png')
        pages.append({**spec, 'output_page': index+1,
                      'output_dimensions_pt': [page.rect.width, page.rect.height],
                      'vector_xobjects': len(page.get_xobjects()),
                      'visible_raster_images': len(visible_images),
                      'inherited_off_crop_image_resources': len(page.get_images(full=True)),
                      'render_matches_original_region_with_antialias_tolerance_144dpi': match,
                      'mean_channel_difference_0_to_255': mean_difference,
                      'fraction_of_differing_channels': differing_fraction})
    manifest['outputs'].append({'path': str(path.relative_to(root)),
                                'sha256': sha(path), 'pages': pages})
assert sha(source) == original_sha
(review/'crop-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({'source_unchanged': True, 'outputs': len(manifest['outputs']),
                  'pages': sum(len(x['pages']) for x in manifest['outputs']),
                  'all_vector': True, 'all_crop_renders_match_original_with_subpixel_antialias_tolerance': True}, indent=2))
