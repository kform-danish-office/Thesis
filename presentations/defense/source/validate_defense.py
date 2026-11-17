"""Check text, notes, measurements, shared diagrams and the rendered PowerPoint."""
from pathlib import Path
from io import BytesIO
import csv,hashlib,json,re,unicodedata,zipfile
import math
from pptx import Presentation
from lxml import etree
import fitz
from equation_math import equation_nodes, M, A14
R=Path(__file__).resolve().parent;NAME='Thesis_Defense_Supervisor_Flow'
m=json.loads((R/'manifest.json').read_text());prs=Presentation(R/(NAME+'.pptx'));pdf=fitz.open(R/(NAME+'.pdf'))
assert len(prs.slides)==len(pdf)==len(m['slides'])==20
assert sum(x['section']=='main' for x in m['slides'])==16
assert len({x['assigned_agent'] for x in m['slides']})==20
judged={x['slide_id']:x for x in json.loads((R/'review/text-judgments.json').read_text())}
def norm(t):
    for a,b in {'V_SW':'VSW','Pₛw':'Psw','Eₒₙ':'Eon','Eₒff':'Eoff','Eₛw':'Esw','f₀':'f0','īᵣₑ꜀':'īrec','īᵣₑ꜀':'īrec','vᵣₑ꜀':'vrec','fₛ':'fs','Cₚ':'Cp','Lₚ':'Lp','Cₛ':'Cs','Lₛ':'Ls','Lₜₒₜₐₗ':'Ltotal','L_total':'Ltotal','C_s':'Cs','C_P':'CP','f_0':'f0'}.items():t=str(t).replace(a,b)
    return re.sub(r'\s+','',unicodedata.normalize('NFD',t)).lower()
def strings(x):
    if isinstance(x,str):return [x]
    if isinstance(x,list):return [s for v in x for s in strings(v)]
    if isinstance(x,dict):return [s for v in x.values() for s in strings(v)]
    return []
ids=[x['slide_id'] for x in m['slides']];missing=[];counts={'charts':0,'tables':0,'pictures':0,'text_shapes':0};elapsed=0;notes=['# Speaker notes','','25-minute speaking allocation, with four backup slides. Timing is an estimate for rehearsal.',''];hashes={}
for ix,(item,sl,page) in enumerate(zip(m['slides'],prs.slides,pdf)):
    sid=item['slide_id'];path=R/'proposals'/f'{sid}.json';p=json.loads(path.read_text());hashes[sid]=hashlib.sha256(path.read_bytes()).hexdigest()
    assert judged[sid]['decision']=='Accept' and (item.get('review_status') in ['text_accepted','Accept','accepted','complete'] or item.get('text_review_status')=='Accept')
    assert p['title'] in [s.text for s in sl.shapes if s.has_text_frame]
    expected=p['speaker_notes']
    if p.get('transition') and p['transition'] not in expected:expected+='\n\n'+p['transition']
    if p.get('references_note'):expected+='\n\n'+p['references_note']
    assert sl.notes_slide.notes_text_frame.text==expected,('Notes',sid)
    assert not re.search(r'/workspace/|sediment://|SHA-256|TRANSFER_MANIFEST',expected)
    t0=elapsed
    if item['section']=='main':elapsed+=p['duration_seconds']
    stamp=f'{t0//60:02}:{t0%60:02}–{elapsed//60:02}:{elapsed%60:02}' if item['section']=='main' else 'Backup'
    notes.extend([f'## {ix+1}. {p["title"]}',f'*{stamp}*','',expected,''])
    found=[]
    for sh in sl.shapes:
        counts['charts']+=int(sh.has_chart);counts['tables']+=int(sh.has_table);counts['pictures']+=int(sh.shape_type==13);counts['text_shapes']+=int(sh.has_text_frame)
        if sh.has_text_frame:found.append(sh.text)
        if sh.name.startswith('Equation: '):
            kind=sh.name.split(': ',1)[1]
            actual=sh._element.findall('.//{%s}oMath'%M)
            assert len(actual)==1
            tree=lambda e:(e.tag,dict(e.attrib),e.text,tuple(tree(c) for c in e))
            assert [tree(e) for e in actual[0]]==[tree(e) for e in equation_nodes(kind,'171748')],('Equation structure',sid)
            found.append(sh._element.xpath('./p:nvSpPr/p:cNvPr')[0].get('descr',''))
        if sh.has_table:found.extend(c.text for c in sh.table.iter_cells())
        if sh.has_chart:found.extend(sh.chart._chartSpace.itertext())
        if sh.has_text_frame or sh.has_table or sh.has_chart or sh.shape_type==13:
            assert sh.left>=0 and sh.top>=0 and sh.left+sh.width<=prs.slide_width+12700 and sh.top+sh.height<=prs.slide_height+12700,('Off canvas',sid)
    alltext=norm(' '.join(found));visible=p['visible_content']
    if isinstance(visible,list):visible={x['id']:x['text'] for x in visible}
    for key,vals in visible.items():
        if 'ticks' in key or key.startswith('scope_') or key.startswith('embedded_') or key=='low_embedded_camera_text':continue
        for t in strings(vals):
            if norm(t) not in alltext:missing.append((sid,key,t))
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                assert '\ufffd' not in span['text'] and '\u25a1' not in span['text'],('Missing glyph',sid,span['text'])
                x0,y0,x1,y1=span['bbox'];assert x0>=-1 and y0>=-1 and x1<=page.rect.width+1 and y1<=page.rect.height+1,('Off page',sid,span['text'])
(R/'review/missing-text.json').write_text(json.dumps(missing,indent=2))
assert not missing,missing
assert elapsed==1500
assert all('Axis Title' not in page.get_text() for page in pdf)
with zipfile.ZipFile(R/(NAME+'.pptx')) as z:
    assert z.testzip() is None
    media={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('ppt/media/')}
    with zipfile.ZipFile(R/'template/DTU_Blue_base.pptx') as t:
        parts=[n for n in t.namelist() if n.endswith('.xml') and n.startswith(('ppt/slideMasters/','ppt/slideLayouts/','ppt/theme/'))]
        canon=lambda b:etree.tostring(etree.fromstring(b),method='c14n')
        for n in parts:assert canon(z.read(n))==canon(t.read(n)),n
for n in ['original-digest-power-stage.png','adapter_5w.jpg','adapter_20w.jpg','adapter_140w.jpg','v1_scope_5v_3a.png','v1_scope_20v_4p7a.png','v1_thermal_20v_4p7a.png','v2_board.png','thermal_intermediate.jpg','thermal_final.jpg','v2_complete_power_schematic.png']:
    assert hashlib.sha256((R/'assets'/n).read_bytes()).hexdigest() in media,n
thermal_original=Path('/workspace/thesis/Pictures/Thesis/10_Results/image_001_20v_4p7a.png')
if thermal_original.exists():assert thermal_original.read_bytes()==(R/'assets/v1_thermal_20v_4p7a.png').read_bytes()
# Check excluded board photos by hash so the source package need not include them.
excluded_board_photos={
    'v1_board.png':'3e8ef27783be1222943428970da0f02596761e51fcf9c1a8ad65ee90f4c2f058',
    'v2_boards_crop.png':'2679f5d0fbec08ebe72ed959f995257c3b94091901a53c26ac93dd88f2446b41',
}
for n,digest in excluded_board_photos.items():
    assert digest not in media,n
title_photos=[sh for sh in prs.slides[0].shapes if sh.shape_type==13]
assert len(title_photos)==1
assert hashlib.sha256(title_photos[0].image.blob).hexdigest()=='ba76433a3c9d05356e519fbec261af4f3f6ee01953e7e5942e740005f2a54ba1'
thermal_photos=[sh for sh in prs.slides[ids.index('s14')].shapes if sh.shape_type==13]
assert len(thermal_photos)==2
assert hashlib.sha256((R/'assets/thermal_intermediate.jpg').read_bytes()).hexdigest()=='4efb78c7049aef2e463bc57f77718b66166051470c8aeec3a0067bc06d243edf'
calibration=json.loads((R/'assets/adapter-scale.json').read_text())
adapter_shapes={sh.name.split(': ',1)[1]:sh for sh in prs.slides[ids.index('s02')].shapes if sh.name.startswith('Scale-calibrated adapter: ')}
assert set(adapter_shapes)=={'5w','20w','140w'}
for item in calibration['adapters']:
    sh=adapter_shapes[item['id']];iw,ih=sh.image.size
    xscale=sh.width/(1-sh.crop_left-sh.crop_right)/iw
    yscale=sh.height/(1-sh.crop_top-sh.crop_bottom)/ih
    assert math.isclose(xscale,yscale,rel_tol=1e-5),('Photo aspect ratio',item['id'])
    edge_top,edge_bottom=item['reference_edge_y_px']
    actual_mm_scale=yscale*(edge_bottom-edge_top)/item['reference_body_height_mm']
    assert math.isclose(actual_mm_scale,calibration['design_units_per_mm']*762000,rel_tol=1e-5),('Physical scale',item['id'])
    actual_base=sh.top+yscale*(item['body_bottom_px']-item['crop_box_px'][1])
    assert abs(actual_base-calibration['body_bottom_y']*762000)<2,('Body baseline',item['id'])

def charts(sid):return [x.chart for x in prs.slides[ids.index(sid)].shapes if x.has_chart]
def cache(s,tag):return {int(p.get('idx')):float(p[0].text) for p in s._element.xpath(f'./c:{tag}/c:numRef/c:numCache/c:pt')}
with (R/'assets/v1_dc_operating_points.csv').open() as f:dc=list(csv.DictReader(f))
reg=charts('s09')[0];np=0
for s in reg.series:
    setting=float(s.name.split()[0]);expected={float(r['iout_a']):float(r['voltage_error_percent_derived']) for r in dc if float(r['pdo_v'])==setting and float(r['iout_a'])>0}
    xs,ys=cache(s,'xVal'),cache(s,'yVal');actual={xs[k]:y for k,y in ys.items()};assert actual==expected;np+=len(actual)
assert np==14
with zipfile.ZipFile(BytesIO(reg.part.chart_workbook.xlsx_part.blob)) as z:
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};sheet=etree.fromstring(z.read('xl/worksheets/sheet1.xml'))
    cells=[c for c in sheet.findall('.//s:c',ns) if c.get('r')[0] in 'BDFH' and c.get('r')[1:]!='1' and c.find('s:v',ns) is not None];assert len(cells)==14
by_id={r['test_id']:r for r in dc};selected=['PDO20-5W-001','PDO20-75W-001','PDO20-76W-38A-001','PDO20-80W-40A-001']
# The user requested the original APEC harmonic comparison, not reconstructed charts.
assert not charts('s11')
harmonic_meta=json.loads((R/'assets/iec-harmonic-figure.json').read_text())
harmonic_asset=R/'assets'/harmonic_meta['asset']
harmonic_hash=hashlib.sha256(harmonic_asset.read_bytes()).hexdigest()
assert harmonic_hash==harmonic_meta['asset_sha256']
harmonic_pics=[sh for sh in prs.slides[ids.index('s11')].shapes if sh.shape_type==13]
assert len(harmonic_pics)==1
hp=harmonic_pics[0]
assert hashlib.sha256(hp.image.blob).hexdigest()==harmonic_hash
left,top,right,bottom=harmonic_meta['crop_box_px'];iw,ih=harmonic_meta['image_size_px']
for actual,expected in zip([hp.crop_left,hp.crop_top,hp.crop_right,hp.crop_bottom],[left/iw,top/ih,(iw-right)/iw,(ih-bottom)/ih]):
 assert abs(actual-expected)<1e-5
assert math.isclose(hp.width/(right-left),hp.height/(bottom-top),rel_tol=1e-5)
original_digest=Path('/workspace/source-archives/APEC_2027_Digest_USB_PD.pdf')
if original_digest.exists():
 original_doc=fitz.open(original_digest)
 assert hashlib.sha256(original_doc.extract_image(harmonic_meta['image_xref'])['image']).hexdigest()==harmonic_hash
assert float(by_id['PDO20-80W-40A-001']['ithd_percent'])==harmonic_meta['legend_logged_current_THD_percent']
assert float(by_id['PDO20-80W-40A-001']['pout_w_derived'])==harmonic_meta['condition']['measured_USB_C_power_W']
with (R/'assets/v2_summary.csv').open() as f:v2=list(csv.DictReader(f))
for ch,key in zip(charts('s13'),['secondary_power_W','secondary_voltage_V']):
    xs,ys=cache(ch.series[0],'xVal'),cache(ch.series[0],'yVal')
    assert all(xs[k]==float(row['secondary_current_A']) and abs(ys[k]-float(row[key]))<1e-8 for k,row in enumerate(v2))
for s,key in zip(charts('s14')[0].series,['secondary_R1_max_C','bridge_R3_max_C']):
    xs,ys=cache(s,'xVal'),cache(s,'yVal');assert all(xs[k]==k+1 and ys[k]==float(row[key]) for k,row in enumerate(v2))
high=by_id['PDO20-80W-40A-001'];assert abs(float(high['vbus_avg_v'])*4-79.8928)<1e-9
assert round(100*79.8928/104.418,2)==76.51
# The three changed circuit slides must embed the original figure unchanged.
source_hash=hashlib.sha256((R/'assets/original-digest-power-stage.png').read_bytes()).hexdigest()
assert source_hash=='426d2c0b7f45b490504d6ec606119739da7680fbafd993f34402368c23f9e9c2'
for sid in ['s04','s05','s06']:
 sl=prs.slides[ids.index(sid)]
 pics=[sh for sh in sl.shapes if sh.shape_type==13]
 assert len(pics)==1 and hashlib.sha256(pics[0].image.blob).hexdigest()==source_hash
 assert not any(sh.has_text_frame and sh.text in ['HV link','QH','QL','PGND','SGND'] for sh in sl.shapes)
# Confirm the rest of the deck retained its accepted layout and appearance.
prior=R/'review/before-iec-comparison/Thesis_Defense_Supervisor_Flow.pdf'
unchanged_pages=[]
if prior.exists():
 old_pdf=fitz.open(prior)
 old_ids=[x['slide_id'] for x in json.loads((prior.parent/'manifest.json').read_text())['slides']]
 for ix,sid in enumerate(ids):
  if sid=='s11':continue
  # This revision changes the input-harmonic slide only; compare all other complete slides.
  rect=pdf[ix].rect
  old=old_pdf[old_ids.index(sid)].get_pixmap(matrix=fitz.Matrix(1,1),clip=rect);new=pdf[ix].get_pixmap(matrix=fitz.Matrix(1,1),clip=rect)
  assert old.samples==new.samples,('Unexpected slide change',sid)
  unchanged_pages.append(sid)

changes=[]
for rec in json.loads((R/'review/thesis-baseline.json').read_text()):
    p=Path('/workspace/thesis')/rec['path']
    if p.parent.exists() and (not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=rec['sha256']):changes.append(rec['path'])
assert not changes,changes
(R/'Speaker_Notes.md').write_text('\n'.join(notes))
equation_kinds={sid:[sh.name for sh in prs.slides[ids.index(sid)].shapes if sh.name.startswith('Equation: ')] for sid in ['s03','s05','b01']}
assert equation_kinds=={'s03':['Equation: switching'],'s05':['Equation: rectifier'],'b01':['Equation: resonance']}
result={'slides':20,'main_slides':16,'backups':4,'dedicated_writers':20,'main_duration_seconds':elapsed,'timing':'Estimated speaking allocation including walkthroughs and pauses; not a timed rehearsal','editable_objects':counts,'native_equations':equation_kinds,'template_parts_preserved':len(parts),'package_crc':'passed','accepted_text_and_notes_match':True,'original_digest_figure_unchanged':True,'unaffected_slides_visually_identical':unchanged_pages,'regulation_points_verified':14,'v2_points_verified':7,'original_iec_harmonic_figure_verified':True,'measurement_images_unaltered':True,'v2_board_photo_on_title':True,'adapter_common_scale_checked':True,'thesis_changes':changes,'rendering':'LibreOffice; metric-compatible Liberation Sans for Arial; Office Math equations','powerpoint_native_inspection':False,'proposal_sha256':hashes}
(R/'review/validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='proposal_sha256'},indent=2))
