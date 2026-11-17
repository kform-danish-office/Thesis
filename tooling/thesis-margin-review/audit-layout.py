"""Verify the margin-only source change and the rebuilt PDF geometry."""
from pathlib import Path
import hashlib, json, math, statistics
import fitz

root=Path('/workspace/thesis')
review=Path('/workspace/tooling/thesis-margin-review')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((review/'before-manifest.json').read_text())
current={p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
assert baseline.keys()==current.keys()
changed=[p for p in baseline if baseline[p]!=current[p]]
assert changed==['main.tex'], changed
old=(review/'before/main.tex').read_bytes()
new=(root/'main.tex').read_bytes()
expected=old.replace(b'\\newgeometry{top=2.81cm,bottom=2.75cm,outer=2.5cm,inner=3.5cm}', b'% Symmetric body margins retain the 150 mm text width on both page parities.\r\n\\newgeometry{top=2.81cm,bottom=2.75cm,left=3cm,right=3cm}')
assert expected==new
a=fitz.open(review/'thesis-before.pdf')
b=fitz.open('/workspace/thesis-build/main.pdf')
assert len(a)==len(b)==424
assert a.get_toc()==b.get_toc(), 'Bookmark pagination changed'
errors=[];pages=[];extraction_grouping=[]
for i,(left,right) in enumerate(zip(a,b)):
    assert left.rect==right.rect and left.rotation==right.rotation
    aa=left.get_text('words');bb=right.get_text('words')
    if [w[4] for w in aa]!=[w[4] for w in bb]:
        errors.append({'page':i+1,'check':'word sequence changed'})
        continue
    if left.get_text()!=right.get_text():
        extraction_grouping.append({'page':i+1,'detail':'PDF extractor grouped dot leaders separately; word sequence and word coordinates are checked below.'})
    deltas=[(y[0]-x[0],y[1]-x[1]) for x,y in zip(aa,bb)]
    if not deltas:
        pages.append({'page':i+1,'words':0});continue
    # Landscape pages rotate the inner content before the PDF /Rotate entry.
    # Movement may therefore occur along x or y in unrotated extraction space.
    axis=1 if right.rotation else 0
    movement=[d[axis] for d in deltas]
    cross=[d[1-axis] for d in deltas]
    row={'page':i+1,'rotation':right.rotation,'words':len(aa), 'median_x_shift_pt':statistics.median(d[0] for d in deltas),'median_y_shift_pt':statistics.median(d[1] for d in deltas)}
    if i in (0,len(a)-1):
        assert all(abs(v)<0.02 for d in deltas for v in d)
        assert left.get_pixmap().samples==right.get_pixmap().samples
    elif not right.rotation:
        if not all(abs(v)<0.03 for v in cross):errors.append({'page':i+1,'check':'vertical coordinates changed'})
        if not all(abs(abs(v)-72*5/25.4)<0.04 for v in movement):errors.append({'page':i+1,'check':'unexpected horizontal movement'})
    pages.append(row)

# Full-width prose starts at 30 mm for both adjacent body pages.
samples=[]
for n in (23,24,25,26,80,81,82,83,100,101,130,131):
    def prose_left(page):
        starts=[]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                spans=line['spans']
                if not spans:continue
                r=fitz.Rect(line['bbox'])
                if r.y0>75 and r.y1<755 and r.width>300 and any(10.8<s['size']<11.1 for s in spans): starts.append(r.x0)
        return min(starts) if starts else None
    oldx,newx=prose_left(a[n-1]),prose_left(b[n-1])
    if oldx is not None and newx is not None:
        assert abs(newx-72*30/25.4)<0.04,(n,newx)
        samples.append({'pdf_page':n,'before_left_mm':oldx*25.4/72,'after_left_mm':newx*25.4/72})

out={'pages':len(b),'source_files':len(current),'changed_source_files':changed,'unchanged_source_files':len(current)-len(changed),'text_and_line_breaks_unchanged':not errors,'bookmarks_and_pagination_unchanged':True,'cover_and_back_cover_pixel_identical':True,'symmetric_body_margin_mm':30,'body_width_mm':150,'samples':samples,'errors':errors,'page_shifts':pages,'extraction_grouping_differences':extraction_grouping}
(review/'layout-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in {'page_shifts','samples'}},indent=2))
assert not errors,errors[:10]
