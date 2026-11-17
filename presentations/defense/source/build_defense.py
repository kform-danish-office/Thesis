"""Build the supervisor-led defense from independently reviewed slide proposals."""
from pathlib import Path
import json
from deck_tools import *
from circuit_tools import box,wire
from equation_math import add_equation
import focused_layouts as focused
import prior_layouts as prior
ROOT=Path(__file__).resolve().parent
NAME='Thesis_Defense_Supervisor_Flow'

def vc(p):
 d=p['visible_content'];return d if isinstance(d,dict) else {x['id']:x.get('text',x) for x in d}
def tx(s,t,x,y,w,h=.55,size=27,**kw):return text(s,t,x,y,w,h,size=size,**kw)
def phase(s,p):
 d=vc(p)
 if d.get('phase_label'):tx(s,d['phase_label'],.8,1.86,14.4,.25,13,fill=WHITE if p['slide_id']=='s15' else MUTED)

def title_with_v2(prs,p,i):
 s=prs.slides.add_slide(prs.slide_layouts[0]);clear_placeholders(s);d=vc(p)
 tx(s,d['context'],.8,1.35,10.1,.6,27,fill=WHITE)
 tx(s,p['title'],.8,2.6,10.1,4.0,42,bold=True,fill=WHITE,spacing=1.07)
 tx(s,d['author'],.8,7.25,10.1,.7,31,bold=True,fill=WHITE)
 sh=picture(s,ROOT/'assets/v2_board.png',11.15,1.8,3.8,6.1)
 sh._element.xpath('./p:nvPicPr/p:cNvPr')[0].set('descr','V2 prototype; crop of the original board photograph')
 slide_number(s,i)
 return s

def scaled_adapters(prs,p,i):
 s=base(prs,p['title'],i,title_size=41);d=vc(p)
 calibration=json.loads((ROOT/'assets/adapter-scale.json').read_text())
 for j,item in enumerate(calibration['adapters']):
  source=ROOT/'assets'/item['file']
  with Image.open(source) as im:iw,ih=im.size
  left,top,right,bottom=item['crop_box_px']
  edge_top,edge_bottom=item['reference_edge_y_px']
  units_per_px=calibration['design_units_per_mm']*item['reference_body_height_mm']/(edge_bottom-edge_top)
  w=(right-left)*units_per_px;h=(bottom-top)*units_per_px
  column_x=.8+j*4.95
  x=column_x+(4.45-w)/2
  y=calibration['body_bottom_y']-(item['body_bottom_px']-top)*units_per_px
  sh=s.shapes.add_picture(str(source),Inches(x),Inches(y),width=Inches(w),height=Inches(h))
  sh.crop_left=left/iw;sh.crop_top=top/ih;sh.crop_right=(iw-right)/iw;sh.crop_bottom=(ih-bottom)/ih
  sh.name='Scale-calibrated adapter: '+item['id']
  sh._element.xpath('./p:nvPicPr/p:cNvPr')[0].set('descr','Apple '+item['id']+' adapter at approximate common body scale; original product photograph')
  record(s,sh,'Approximate common scale: '+item['id'])
  tx(s,d[f'photo_{j+1}_caption'],column_x,calibration['captions_y'],4.45,.65,27,bold=True,align=PP_ALIGN.CENTER)
 line(s,.8,6.94,15.2,6.94,LINE,1.5)
 tx(s,d['body_1'],.8,7.18,8.5,.55,29,bold=True,fill=TEAL)
 tx(s,d['body_2'],9.4,7.18,5.8,.55,25,align=PP_ALIGN.RIGHT)
 tx(s,d['photo_note'],.8,7.9,14.4,.35,19,fill=MUTED)
 return s

def frequency(prs,p,i):
 s=base(prs,p['title'],i,title_size=40);d=vc(p)
 tx(s,d['frequency_heading'],.8,2.45,14.4,.62,34,bold=True,fill=TEAL)
 line(s,.8,3.25,15.2,3.25,LINE)
 # Read left to right: the compactness benefit raises a heat problem,
 # which the resonant commutation mechanism addresses.
 for k,(head,body) in enumerate([('compactness_heading','compactness_body'),('loss_heading','loss_equation'),('soft_switching_heading','soft_switching_body')]):
  xx=.8+k*4.95
  tx(s,d[head],xx,3.72,4.25,.94,29,bold=True)
  if k==1:record(s,add_equation(s,'switching',xx,5.02,width=3.1,source_text=d[body]),'Native switching-loss equation')
  else:tx(s,d[body],xx,5.02,4.25,1.18,27,fill=TEAL if k==2 else INK)
  if k<2:arrow(s,xx+4.36,4.65,.43,.24)
 line(s,.8,6.65,15.2,6.65,LINE)
 tx(s,d['regulation_bridge'],.8,7.1,14.4,.92,28,bold=True)
 tx(s,d['concept_caption'],.8,8.15,14.4,.27,15,fill=MUTED)
 return s

def digest_figure(s, crop_box, x=.8, y=2.4, w=14.4, h=4.6):
 # Keep the exact extracted image bytes. Enlarge using native PowerPoint crop.
 source=ROOT/'assets/original-digest-power-stage.png'
 with Image.open(source) as im:iw,ih=im.size
 left,top,right,bottom=crop_box
 scale=min(w/(right-left),h/(bottom-top))
 dw,dh=(right-left)*scale,(bottom-top)*scale
 pic=s.shapes.add_picture(str(source),Inches(x+(w-dw)/2),Inches(y+(h-dh)/2),width=Inches(dw),height=Inches(dh))
 pic.crop_left=left/iw;pic.crop_top=top/ih
 pic.crop_right=(iw-right)/iw;pic.crop_bottom=(ih-bottom)/ih
 return record(s,pic,'Original digest Fig. 1; native crop')

def whole(prs,p,i):
 s=base(prs,p['title'],i,title_size=40);d=vc(p)
 tx(s,d['concept'],.8,2.15,14.4,.31,17,fill=MUTED)
 digest_figure(s,[25,115,1970,650],.65,2.4,14.7,4.6)
 tx(s,d['contribution_heading'],.8,7.35,2.6,.95,26,bold=True,fill=TEAL)
 tx(s,d['contribution_1'],3.65,7.35,5.6,.95,26)
 tx(s,d['contribution_2'],9.6,7.35,5.6,.95,26)
 return s

def pump(prs,p,i):
 s=base(prs,p['title'],i,title_size=41);d=vc(p)
 digest_figure(s,[25,115,1260,650],.8,2.3,14.4,4.7)
 record(s,add_equation(s,'rectifier',.8,7.12,width=4.65,source_text=d['equation']),'Native rectifier-current equation')
 tx(s,d['legend'],.8,8.0,6.7,.35,21,fill=MUTED)
 tx(s,d['body_2'],8.2,7.35,7,1.0,29,bold=True)
 return s

def resonant(prs,p,i):
 s=base(prs,p['title'],i,title_size=41);d=vc(p)
 digest_figure(s,[665,125,1495,650],.8,2.3,14.4,4.7)
 tx(s,d['body_1'],.8,7.45,6.6,.9,29,bold=True,fill=TEAL)
 tx(s,d['body_2'],8.0,7.45,7.2,.9,27,bold=True)
 return s

def regulation(prs,p,i):
 s=focused.s07(prs,p,i);d=vc(p)
 for sh in s.shapes:
  if sh.has_chart:sh.height=Inches(3.95)
  if sh.has_text_frame and sh.text==d['body_1']:sh.top=Inches(6.94)
  if sh.has_text_frame and sh.text==d['body_2']:sh.top=Inches(7.49)
 tx(s,d['power_callout'],.8,8.05,14.4,.35,22,bold=True)
 return s

def input_harmonics(prs,p,i):
 s=base(prs,p['title'],i,title_size=40);d=vc(p)
 tx(s,d['condition'],.8,2.15,14.4,.4,23,fill=MUTED)
 metadata=json.loads((ROOT/'assets/iec-harmonic-figure.json').read_text())
 source=ROOT/'assets'/metadata['asset'];iw,ih=metadata['image_size_px']
 left,top,right,bottom=metadata['crop_box_px']
 x,y,w,h=.45,2.65,10.5,5.8
 scale=min(w/(right-left),h/(bottom-top));dw=(right-left)*scale;dh=(bottom-top)*scale
 sh=s.shapes.add_picture(str(source),Inches(x+(w-dw)/2),Inches(y+(h-dh)/2),width=Inches(dw),height=Inches(dh))
 sh.crop_left=left/iw;sh.crop_top=top/ih;sh.crop_right=(iw-right)/iw;sh.crop_bottom=(ih-bottom)/ih
 sh.name='Original digest harmonic comparison'
 sh._element.xpath('./p:nvPicPr/p:cNvPr')[0].set('descr','Original harmonic-current graph at 80 W USB-C output against IEC 61000-3-2 Class A limits; native crop only')
 record(s,sh,'Original digest Fig. 3(e); native crop')
 tx(s,d['standard_label'],11.05,3.05,4.15,1.2,27,bold=True,fill=TEAL)
 line(s,11.05,4.48,15.2,4.48,LINE)
 tx(s,d['body_1'],11.05,4.85,4.15,1.9,29,bold=True)
 tx(s,d['metric'],11.05,7.02,4.15,1.15,23,fill=MUTED)
 return s

def thermal(prs,p,i):
 s=base(prs,p['title'],i,title_size=40);d=vc(p);pts=p['visual']['chart_data']
 tx(s,d['condition'],.8,2.15,14.4,.4,21,fill=MUTED)
 tx(s,d['low_image_caption'],.8,2.75,4.35,.7,23,bold=True)
 tx(s,d['image_caption'],5.4,2.75,4.35,.7,23,bold=True)
 picture(s,ROOT/'assets/thermal_intermediate.jpg',.8,3.62,4.35,3.15)
 picture(s,ROOT/'assets/thermal_final.jpg',5.4,3.62,4.35,3.15)
 tx(s,d['chart_title'],10.0,2.75,5.2,.7,23,bold=True)
 ch=xy_chart(s,[(d['chart_legend'][0],[a['point'] for a in pts],[a['secondary_r1_max_c'] for a in pts],TEAL),(d['chart_legend'][1],[a['point'] for a in pts],[a['input_bridge_r3_max_c'] for a in pts],AMBER)],10.0,3.55,5.2,3.25,d['chart_x_axis'],d['chart_y_axis'],1,7,40,105).chart
 ch.legend.font.size=Pt(18);ch.category_axis.major_unit=1;ch.value_axis.major_unit=20;ch.series[1].marker.style=XL_MARKER_STYLE.SQUARE
 tx(s,d['body_1'],.8,6.98,4.35,.6,22,bold=True,fill=AMBER)
 tx(s,d['body_2'],5.4,6.98,4.35,.6,22,bold=True,fill=TEAL)
 tx(s,d['equilibrium_caption'],.8,7.62,14.4,.36,20,fill=MUTED)
 tx(s,d['design_response'],.8,8.04,14.4,.35,19,bold=True)
 return s

def v1_thermal(prs,p,i):
 s=base(prs,p['title'],i,title_size=41);d=vc(p)
 tx(s,d['condition'],.8,2.15,14.4,.4,23,fill=MUTED)
 picture(s,ROOT/'assets/v1_thermal_20v_4p7a.png',1.2,2.95,6.2,5.05)
 tx(s,d['temperature'],8.35,3.65,6.85,1.05,59,bold=True,fill=TEAL)
 tx(s,d['temperature_label'],8.35,4.92,6.85,.7,26)
 line(s,8.35,5.95,15.2,5.95,LINE)
 tx(s,d['body_1'],8.35,6.45,6.85,1.2,30,bold=True)
 return s

def usb_table(prs,p,i):
 s=base(prs,p['title'],i,title_size=40);d=vc(p)
 tx(s,d['condition'],.8,2.15,14.4,.4,23,fill=MUTED)
 rows=d['table_rows']
 tb=table(s,d['table_headers'],rows,.8,2.95,14.4,4.6,None,24)
 for j,row in enumerate(tb.table.rows):row.height=Inches(.85 if j==0 else .57)
 tx(s,d['power_caption'],.8,7.9,14.4,.48,24,bold=True,fill=TEAL)
 return s

BUILDERS={
 's01':title_with_v2,'s02':scaled_adapters,'s03':frequency,'s04':whole,
 's05':pump,'s06':resonant,'s07':focused.s06,'s08':focused.b01,
 's09':regulation,'s10':focused.s08,'s11':input_harmonics,'s12':focused.s10,
 's11a':v1_thermal,'s13':focused.s11,'s14':thermal,'s15':focused.s13,'b01':focused.b02,
 'b02':focused.b03,'b03':focused.b04,'b04':usb_table}

def main():
 prs=new_deck();m=json.loads((ROOT/'manifest.json').read_text());built=[];timing=[];md=['# Defense speaker notes','']
 for item in m['slides']:
  sid=item['slide_id'];path=ROOT/'proposals'/f'{sid}.json'
  if not path.exists():continue
  p=json.loads(path.read_text());ix=len(built)+1
  slide=BUILDERS[sid](prs,p,ix);phase(slide,p);notes(slide,p)
  built.append({**item,'order':ix,'title':p['title']});spoken=slide.notes_slide.notes_text_frame.text
  timing.append({'slide_id':sid,'seconds':p['duration_seconds'],'notes_words':len(spoken.split()),'backup':item['section']=='backup'})
  md.extend([f'## {ix}. {p["title"]}',f'{p["duration_seconds"]} seconds','',spoken,''])
 prs.save(ROOT/(NAME+'.pptx'));(ROOT/'Speaker_Notes.md').write_text('\n'.join(md))
 (ROOT/'review/render-manifest.json').write_text(json.dumps({'slides':built},indent=2));(ROOT/'review/timing.json').write_text(json.dumps(timing,indent=2));(ROOT/'review/layout-bounds.json').write_text(json.dumps(BOUNDS,indent=2))
 print(f'Built {len(built)} slides')
if __name__=='__main__':main()
