"""Render the actual PowerPoint and create slide previews with LibreOffice."""
from pathlib import Path
import os, json, shutil, subprocess
import fitz
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parent
renderer=shutil.which('soffice') or shutil.which('libreoffice')
if not renderer:raise SystemExit('LibreOffice is required for PDF/slide rendering.')
cache=root/'review/cache';cache.mkdir(parents=True,exist_ok=True)
subprocess.run([renderer,'-env:UserInstallation=file:///tmp/defense-supervisor-flow-lo-profile','--headless','--convert-to','pdf','--outdir',str(root),str(root/'Thesis_Defense_Supervisor_Flow.pptx')],check=True,env={**os.environ,'XDG_CACHE_HOME':str(cache)})
manifest=json.loads((root/'review/render-manifest.json').read_text())
doc=fitz.open(root/'Thesis_Defense_Supervisor_Flow.pdf')
assert len(doc)==len(manifest['slides'])
(root/'rendered').mkdir(exist_ok=True)
for page,item in zip(doc,manifest['slides']):
    page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(root/'rendered'/f"{item['slide_id']}.png")
for start in range(0,len(doc),6):
    subset=manifest['slides'][start:start+6];rows=(len(subset)+1)//2
    canvas=Image.new('RGB',(1440,rows*440),'#dce3e7');draw=ImageDraw.Draw(canvas)
    for j,item in enumerate(subset):
        im=Image.open(root/'rendered'/f"{item['slide_id']}.png");im.thumbnail((704,396))
        x=(j%2)*720+8;y=(j//2)*440+25
        canvas.paste(im,(x,y));draw.text((x,y-20),f"{item['order']} · {item['slide_id']}",fill='black')
    canvas.save(root/'review'/f'contact-{start//6+1:02}.jpg')
(root/'review/pdf-text.txt').write_text('\n\n'.join(f'SLIDE {i+1}\n{p.get_text()}' for i,p in enumerate(doc)))
print(f'Rendered {len(doc)} slides using the DTU 16:9 slide size.')
