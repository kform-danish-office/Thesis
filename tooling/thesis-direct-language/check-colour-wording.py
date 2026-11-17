from pathlib import Path
import fitz,json,numpy as np,re

review=Path('/workspace/tooling/thesis-direct-language')
doc=fitz.open('/workspace/thesis-build/main.pdf')
offset=next(x[2] for x in doc.get_toc() if x[0]==1 and x[1].startswith('1 '))-1
aux='\n'.join(p.read_text(errors='replace') for p in Path('/workspace/thesis-build').rglob('*.aux'))
def page_for(label):
    m=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^{}]*\}\{(\d+)\}',aux)
    assert m,label
    return int(m[1])+offset

labels=['fig:analysis-power-stage','fig:hw-input-schematic','fig:schematic-power-stage','fig:schematic-usbc','fig:schematic-mcu']+[f'fig:app-v2-oct27-schematic-{n}' for n in range(1,5)]
colours={}
out=review/'page-previews';out.mkdir(exist_ok=True)
for label in labels:
    number=page_for(label);page=doc[number-1]
    pix=page.get_pixmap(colorspace=fitz.csRGB)
    arr=np.frombuffer(pix.samples,np.uint8).reshape(-1,3)
    count=int((arr.max(axis=1).astype(int)-arr.min(axis=1).astype(int)>25).sum())
    assert count>50,(label,count)
    colours[label]={'physical_page':number,'non_gray_pixels_at_72dpi':count}
    page.get_pixmap(matrix=fitz.Matrix(1300/page.rect.width,1300/page.rect.width)).save(out/(label.replace(':','-')+'.png'))

targets={'tab:intro-controller-signals':'mcu-pins','tab:analysis-design-summary':'calculation-parameters','tab:ctrl-version-identity':'control-stage-table','sec:ctrl-comparison':'control-development','ch:simulation':'models-opening'}
for label,name in targets.items():
    number=page_for(label)
    doc[number-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(out/(name+'.png'))

clean=lambda text:re.sub(r'\s+',' ',text.replace('-\n',''))
intro=' '.join(clean(p.get_text()) for p in list(doc)[offset:offset+12])
assert 'MCU pin assignments for the original controller and V2.' in intro
assert "MCU’s perspective" not in intro and "MCU's perspective" not in intro
stage_page=page_for('sec:ctrl-comparison')
stage=' '.join(clean(p.get_text()) for p in list(doc)[stage_page-1:stage_page+3])
assert all(word in stage for word in ['Improvement','Blocking','DMA','precharge'])
assert 'Matched tests were not performed to isolate the performance effect' not in stage
models=clean(doc[page_for('ch:simulation')-1].get_text())
assert 'Charge transfer, resonant gain and phase, and component sensitivity are examined' in models
result={'pages':len(doc),'colour_schematic_pages':colours,'pin_caption_updated':True,'control_improvement_table_present':True,'models_opening_describes_calculations':True,'selected_pages':{name:page_for(label) for label,name in targets.items()}}
(review/'colour-and-wording-pdf-check.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: all five main V2 figures and four full V2 sheets render in colour; direct captions and firmware-stage improvements present')
