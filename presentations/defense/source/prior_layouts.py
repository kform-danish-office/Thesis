"""Build the reviewed, editable 25-minute DTU defense."""
from pathlib import Path
import json, math
from deck_tools import *
from circuit_tools import wire, ground, cap, switch, dot, box, label
from chart_tools import separate_xy_columns
import legacy_layouts as legacy

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
NAME='Thesis_Defense_Supervisor_Story'

def content(p):
    v=p['visible_content']
    return v if isinstance(v,dict) else {b['id']:b.get('text',b) for b in v}
def vc(p,k):return content(p)[k]
def pic(s,f,x,y,w,h):return picture(s,ASSETS/f,x,y,w,h)
def tx(s,t,x,y,w,h=.6,size=27,**kw):return text(s,t,x,y,w,h,size=size,**kw)
def foot(s,t):return tx(s,t,.8,7.9,14.4,.35,19,fill=MUTED)
def crop(s,f,x,y,w,left=0,top=0,right=0,bottom=0,h=None):
    path=ASSETS/f
    with Image.open(path) as im:iw,ih=im.size
    ratio=ih*(1-top-bottom)/(iw*(1-left-right))
    sh=s.shapes.add_picture(str(path),Inches(x),Inches(y),width=Inches(w),height=Inches(h or w*ratio))
    sh.crop_left=left;sh.crop_top=top;sh.crop_right=right;sh.crop_bottom=bottom
    return record(s,sh,'Original source with native crop: '+f)
def adapt(p,mapping):
    return {**p,'visible_content':[{'id':k,'text':vc(p,v)} for k,v in mapping.items()]}

def s01(prs,p,i):
    s=prs.slides.add_slide(prs.slide_layouts[0]);clear_placeholders(s)
    tx(s,vc(p,'context'),.8,1.35,13.9,.6,27,fill=WHITE)
    tx(s,p['title'],.8,2.6,13.9,3.6,46,bold=True,fill=WHITE,spacing=1.07)
    tx(s,vc(p,'author'),.8,7.25,13.9,.7,31,bold=True,fill=WHITE)
    slide_number(s,i);return s

def s02(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p)
    photos=p['visual'].get('photos',[])
    for j,n in enumerate(['5w','20w','140w']):
        x=.8+j*4.95
        pic(s,'adapter_'+n+'.jpg',x+.4,2.35,3.65,3.5)
        caption=v.get(f'photo_{j+1}_caption','')
        tx(s,caption,x,5.82,4.45,.95,27,bold=True,align=PP_ALIGN.CENTER)
    line(s,.8,6.94,15.2,6.94,LINE,1.5)
    tx(s,v['body_1'],.8,7.18,8.5,.55,29,bold=True,fill=TEAL)
    tx(s,v['body_2'],9.4,7.18,5.8,.55,25,align=PP_ALIGN.RIGHT)
    for k in ['photo_note','photo_credit','credit','caption_note']:
        if k in v:foot(s,v[k]);break
    return s

def s03(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p);d=v['diagram_labels']
    box(s,d['frequency'],2.1,2.65,11.8,.85,c=PALE,size=32)
    for x in [4.25,11.75]:
        a=arrow(s,x-.36,3.75,.72,.32);a.rotation=90
    box(s,d['passives'],.8,4.45,6.6,1.05,size=31)
    box(s,d['loss'],8.6,4.45,6.6,1.05,size=31)
    tx(s,v['equation'],8.6,6.0,6.6,.72,35,bold=True,fill=TEAL,align=PP_ALIGN.CENTER)
    tx(s,d['condition'],8.6,6.9,6.6,.55,23,align=PP_ALIGN.CENTER)
    foot(s,v['caption']);return s

def s04(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p)
    tx(s,v['diagram_heading'],.8,2.12,14.4,.48,24,fill=MUTED)
    # Lower-device commutation with upper and lower output capacitances.
    x=2.05;switch(s,x,3.55);switch(s,x,5.12)
    wire(s,(x,2.9),(x,3.07));wire(s,(x,4.03),(x,4.64));wire(s,(x,5.6),(x,5.94))
    for yc,ya,yb in [(3.55,2.9,4.34),(5.12,4.34,5.94)]:
        wire(s,(x,ya),(3.1,ya),(3.1,yc-.4));cap(s,3.1,yc,True);wire(s,(3.1,yc+.4),(3.1,yb),(x,yb))
    dot(s,x,4.34);wire(s,(3.1,4.34),(4.15,4.34),c=TEAL);arrow(s,3.65,4.22,.65,.24)
    for t,xx,yy,ww in [('+VDC',1.1,2.53,1.7),('QH',.85,3.28,.9),('QL',.85,4.88,.9),('Coss,H',3.32,3.3,1.4),('Coss,L',3.32,4.9,1.4),('VSW',3.3,4.55,1.4),('iDT',3.66,3.77,.9),('0 V',1.2,6.1,1.6)]:label(s,t,xx,yy,ww,22)
    start=8.0;ww=6.85;t0=start+.28*ww;t1=start+.62*ww;t2=start+.78*ww;end=start+ww
    for xx in [t0,t2]:line(s,xx,2.82,xx,6.6,LINE,1)
    for lab,yy in [('High-side gate',3.05),('Low-side VDS',4.4),('Low-side gate',5.8)]:tx(s,lab,5.05,yy-.06,2.75,.75,23)
    wire(s,(start,3.0),(t0,3.0),(t0,3.55),(end,3.55),c=INK,width=2.6)
    wire(s,(start,4.34),(t0,4.34),(t1,4.94),(end,4.94),c=TEAL,width=2.6)
    wire(s,(start,6.35),(t2,6.35),(t2,5.8),(end,5.8),c='00805A',width=2.6)
    wire(s,(t0,2.95),(t0,2.7),(t2,2.7),(t2,2.95),c=MUTED,width=1.5)
    tx(s,'Dead time',t0,2.2,t2-t0,.45,22,align=PP_ALIGN.CENTER)
    tx(s,'Near zero',t1-.4,5.06,2.25,.42,21,fill=TEAL)
    tx(s,'Turn-on',t2-.2,6.52,1.8,.4,21,fill='00805A')
    tx(s,'Time →',13.9,6.98,1.1,.4,20)
    bullets(s,[v['body_1'],v['body_2']],.8,7.23,12.8,24,gap=.53)
    return s

def s05(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p);labs=v['block_labels']
    # Two rows allow readable functional blocks and keep the shared SW drive explicit.
    positions=[(.8,3.5,2.1),(3.3,3.5,2.6),(6.3,3.5,2.0),(8.7,3.5,2.65),(11.75,3.5,3.45),
               (11.75,5.75,3.45),(7.8,5.75,3.45),(3.85,5.75,3.45)]
    for t,(x,y,w) in zip(labs,positions):box(s,t,x,y,w,1.05,size=26)
    for xa,xb in [(2.9,3.3),(5.9,6.3),(8.3,8.7),(11.35,11.75)]:arrow(s,xa+.04,3.91,xb-xa-.08,.23)
    wire(s,(13.47,4.55),(13.47,5.75),c=TEAL);a=arrow(s,13.15,5.25,.64,.24);a.rotation=90
    for x in [11.31,7.36]:a=arrow(s,x,6.16,.38,.23);a.rotation=180
    dot(s,11.55,4.02,TEAL);wire(s,(11.55,4.02),(11.55,2.8),(4.6,2.8),(4.6,3.5),c=TEAL)
    a=arrow(s,4.34,3.1,.52,.22);a.rotation=90
    tx(s,v['feedback_arrow_label'],5.4,2.25,5.1,.5,25,fill=TEAL,align=PP_ALIGN.CENTER)
    tx(s,v['node_label'],11.28,4.6,.8,.45,21)
    tx(s,v['control_labels'][0],11.65,7.0,3.65,.85,25,align=PP_ALIGN.CENTER)
    tx(s,v['control_labels'][1],6.4,7.0,4.9,.85,25,align=PP_ALIGN.CENTER)
    foot(s,v['citation']);return s

def s06(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p)
    tx(s,v['pump_caption'],.8,2.22,6.9,.5,27,bold=True)
    crop(s,'schematic_pump_detail.png',.8,3.13,6.9,right=11/981)
    for j,k in enumerate(['pump_capacitor','pump_inductor','switch_node']):tx(s,v[k],.8,6.68+j*.47,7,.44,23)
    tx(s,v['charge_equation'],8.3,2.4,6.9,.6,35,bold=True,fill=TEAL)
    tx(s,v['current_equation'],8.3,3.2,6.9,.7,35,bold=True,fill=TEAL)
    tx(s,v['condition'],8.3,4.12,6.9,.9,21,fill=MUTED)
    bullets(s,[v[f'bullet_{k}'] for k in range(1,4)],8.3,5.03,6.9,25,gap=.82)
    tx(s,v['citation'],11.3,8.08,3.9,.30,17,fill=MUTED,align=PP_ALIGN.RIGHT);return s

def s07(prs,p,i):
    from circuit_tools import inductor,transformer,diode
    s=base(prs,p['title'],i,title_size=39);v=content(p)
    tx(s,v['caption'],.8,2.13,14.4,.4,21,fill=MUTED)
    y=4.35
    # Shared SW node and signed branch currents.
    wire(s,(.8,y),(2.0,y),(2.0,3.0),(3.0,3.0),c=TEAL)
    arrow(s,1.1,y-.1,.45,.2);dot(s,2.0,y,TEAL)
    arrow(s,2.42,2.9,.4,.2);box(s,'Charge pump',3.0,2.65,2.2,.72,size=23)
    tx(s,'ipump',2.0,2.51,1.05,.4,20);tx(s,'iSW',.8,3.77,.85,.4,20)
    tx(s,'VSW',1.5,4.76,1.15,.4,22)
    wire(s,(2.0,y),(2.7,y));arrow(s,2.18,y-.1,.4,.2)
    tx(s,'itank',2.12,3.77,1.05,.4,20)
    cap(s,3.1,y);wire(s,(3.5,y),(3.9,y));inductor(s,4.4,y)
    wire(s,(4.9,y),(5.3,y));inductor(s,5.8,y)
    wire(s,(6.3,y),(6.65,y),(6.65,3.85),(6.95,3.85))
    transformer(s,7.17,y);wire(s,(6.95,4.85),(6.95,5.9));ground(s,6.95,5.9)
    for t,x,w in [('C26',2.55,1.2),('L4',3.8,1.2),('Llk',5.25,1.2),('T1 (ideal)',6.35,1.75)]:label(s,t,x,3.4,w,23)
    # Full-wave bridge. Junction dots distinguish connected AC nodes from the wire crossing.
    xl,xr=8.9,10.35;yt,yb=3.25,5.9;mid=4.55
    for xx in [xl,xr]:
        wire(s,(xx,yt),(xx,3.47));diode(s,xx,3.9,True,True);wire(s,(xx,4.33),(xx,4.77));diode(s,xx,5.2,True,True);wire(s,(xx,5.63),(xx,yb))
    wire(s,(xl,yt),(11.5,yt));wire(s,(xl,yb),(12.65,yb));wire(s,(xr,yt),(xr,3.47));wire(s,(xr,5.63),(xr,yb))
    wire(s,(7.57,3.85),(8.1,3.85),(8.1,mid),(xl,mid));dot(s,xl,mid)
    # The lower transformer lead passes under the left bridge leg without a junction.
    wire(s,(7.57,4.85),(7.9,4.85),(7.9,6.45),(10.9,6.45),(10.9,6.03));wire(s,(10.9,5.77),(10.9,mid),(xr,mid));dot(s,xr,mid)
    # A white gap at the DC-return crossing makes the separate AC route explicit.
    wire(s,(10.9,5.77),(11.05,5.82),(11.05,5.98),(10.9,6.03),c=WHITE,width=7);wire(s,(10.9,5.77),(11.05,5.82),(11.05,5.98),(10.9,6.03))
    for xx in [xl,xr]:dot(s,xx,yt);dot(s,xx,yb)
    wire(s,(11.5,yt),(11.5,4.15));cap(s,11.5,4.55,True);wire(s,(11.5,4.95),(11.5,yb));ground(s,11.5,yb)
    wire(s,(11.5,yt),(12.65,yt),(12.65,3.72));box(s,'USB-C PD',12.3,3.72,2.6,1.0,size=25)
    wire(s,(12.65,4.72),(12.65,yb));wire(s,(14.9,4.22),(15.4,4.22),(15.4,4.95))
    tx(s,'VBUS',14.15,5.12,1.5,.45,23)
    tx(s,'Secondary rectifier',8.15,2.6,3.7,.48,24,bold=True)
    tx(s,'Vsec',11.65,2.78,1.2,.4,22);tx(s,'Cbulk',11.73,4.45,1.35,.5,21)
    tx(s,'Primary return',5.4,6.3,2.8,.4,21);tx(s,'Secondary return',11.5,6.38,3.5,.4,21)
    tx(s,'iSW = ipump + itank',.8,7.17,5,.5,28,bold=True,fill=TEAL)
    tx(s,v['regulation_labels'][0],.8,7.92,5,.4,22)
    tx(s,v['regulation_labels'][1],6.15,7.92,4,.4,22)
    tx(s,v['regulation_labels'][2],10.6,7.92,4.8,.4,22)
    return s

def s08(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p)
    tx(s,v['reference'],.8,2.55,2.15,.7,24)
    circle=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(3.0),Inches(2.6),Inches(.65),Inches(.65));circle.fill.solid();circle.fill.fore_color.rgb=color(WHITE);circle.line.color.rgb=color(INK)
    tx(s,v['sum_plus'],3.08,2.61,.2,.3,21);tx(s,v['sum_minus'],3.33,2.91,.2,.3,21)
    arrow(s,2.58,2.84,.36,.2)
    for key,x,w in [('controller',4.05,3.0),('burst',7.5,3.0),('half_bridge',10.95,4.05)]:box(s,v[key],x,2.52,w,.95,size=26)
    for x in [3.68,7.08,10.53]:arrow(s,x,2.87,.34,.22)
    box(s,v['power_stage'],10.95,4.4,4.05,.95,size=26)
    wire(s,(12.98,3.47),(12.98,4.4),c=TEAL);a=arrow(s,12.68,3.92,.6,.22);a.rotation=90
    box(s,v['bulk'],6.4,4.4,4.05,.95,size=26)
    a=arrow(s,10.51,4.77,.35,.22);a.rotation=180
    wire(s,(8.42,4.4),(8.42,3.93),(3.33,3.93),(3.33,3.25),c=TEAL)
    box(s,v['pd'],2.4,4.4,3.5,.95,size=25);a=arrow(s,5.96,4.77,.35,.22);a.rotation=180
    tx(s,v['vbus'],.8,5.78,4.9,.48,24)
    wire(s,(2.4,4.87),(1.6,4.87),(1.6,5.6),c=TEAL)
    bullets(s,[v[f'bullet_{k}'] for k in range(1,4)],.8,6.52,14.4,27,gap=.58)
    return s

def s09(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p)
    for j,name in enumerate(['v1_scope_5v_3a.png','v1_scope_20v_4a.png']):
        yy=2.95+j*2.65
        tx(s,v[f'figure_{j+1}_label'],.8,yy-.65,10.3,.5,27,bold=True)
        crop(s,name,.8,yy,10.25,left=100/1030,top=190/839,right=3/1030,bottom=(839-327)/839)
    bullets(s,[v[f'body_{k}'] for k in range(1,4)],11.65,2.6,3.55,26,gap=1.4)
    # Annotations are outside the measured plot, with pointer lines.
    tx(s,v['figure_1_annotations'][0],1.35,4.49,2,.30,17);tx(s,v['figure_1_annotations'][1],6.2,4.49,3.5,.30,17)
    foot(s,v['figure_legend']);return s

def s10(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p)
    tx(s,v['body_1'],.8,2.2,14.4,.5,28,bold=True)
    crop(s,'v1_scope_20v_4p7a.png',.8,3.0,9.9,top=144/843,bottom=(843-638)/843)
    tx(s,v['body_2'],11.25,3.25,3.95,1.6,31)
    tx(s,v['figure_condition'],11.25,5.3,3.95,1.6,24,fill=MUTED)
    foot(s,v['figure_legend']);return s

def s11(prs,p,i):
    return legacy.c11(prs,p,i)

def s12(prs,p,i):
    s=base(prs,p['title'],i,title_size=40);v=content(p);groups=p['visual']['series'];palette=[TEAL,'00805A',AMBER,INK]
    series=[(g['label'],[a for a,b in g['points']],[b for a,b in g['points']],c) for g,c in zip(groups,palette)]
    tx(s,v['chart_title'],.8,2.12,10.1,.45,24,bold=True)
    chart=xy_chart(s,series,.6,2.8,10.4,4.65,v['chart_x_axis'],v['chart_y_axis'],0,85,50,90).chart
    separate_xy_columns(chart,[{'name':g['label'],'points':[{'iout_a':a,'error_pct':b} for a,b in g['points']]} for g in groups])
    for trace,marker in zip(chart.series,[XL_MARKER_STYLE.CIRCLE,XL_MARKER_STYLE.SQUARE,XL_MARKER_STYLE.TRIANGLE,XL_MARKER_STYLE.DIAMOND]):trace.format.line.fill.background();trace.marker.style=marker;trace.marker.size=9
    chart.category_axis.major_unit=20;chart.value_axis.major_unit=10;chart.legend.font.size=Pt(22)
    tx(s,v['body_1'],11.5,3.0,3.7,1.8,28,bold=True)
    tx(s,v['body_2'],11.5,5.4,3.7,1.2,29,fill=TEAL)
    tx(s,v['chart_annotation'],.8,7.73,10.4,.5,25,bold=True,fill=TEAL)
    return s


def s13(prs,p,i):
    q=adapt(p,{'conditions':'conditions','result':'body_1'})
    q['visible_content'].append({'id':'efficiency','text':''})
    return legacy.b02(prs,q,i)

def s14(prs,p,i):
    from circuit_tools import inductor,transformer
    s=base(prs,p['title'],i,title_size=40);v=content(p)
    for pre,y in [('before',3.75),('after',6.15)]:
        x=1.1;tx(s,v[pre+'_heading'],.8,y-1.42,3,.45,28,bold=True,fill=TEAL)
        wire(s,(x,y),(x+.75,y));cap(s,x+1.15,y);wire(s,(x+1.55,y),(x+2,y))
        if pre=='before':inductor(s,x+2.5,y)
        else:wire(s,(x+2,y),(x+3,y))
        wire(s,(x+3,y),(x+3.6,y));inductor(s,x+4.1,y)
        wire(s,(x+4.6,y),(x+5.35,y),(x+5.35,y-.5),(x+5.8,y-.5))
        transformer(s,x+6.02,y);wire(s,(x+5.8,y+.5),(x+5.8,y+.87));ground(s,x+5.8,y+.87)
        wire(s,(x+6.42,y-.5),(x+7.15,y-.5));wire(s,(x+6.42,y+.5),(x+7.15,y+.5))
        label(s,v[pre+'_input'],x-.45,y-.7,1.3,19)
        label(s,v[pre+'_capacitor'],x+.2,y+.42,1.95,22)
        if pre=='before':tx(s,v['before_external'],x+1.48,y-1.45,2.3,1.1,18,align=PP_ALIGN.CENTER)
        tx(s,v[pre+'_leakage'],x+3.2,y+.42,2.2,.95,20,align=PP_ALIGN.CENTER)
        label(s,v[pre+'_transformer'],x+5.2,y-1.15,1.8,20)
        label(s,v[pre+'_output'],x+6.8,y-.2,1.7,20)
    bullets(s,[v[f'bullet_{k}'] for k in range(1,4)],10.2,2.65,5,28,gap=1.4)
    foot(s,v['diagram_caption']);return s

def s15(prs,p,i):
    s=base(prs,p['title'],i,title_size=38);v=content(p)
    tx(s,v['condition'],.8,2.12,14.4,.5,23,fill=MUTED)
    for j,d in enumerate(p['visual']['panels']):
        xs,ys=zip(*d['points']);chart=xy_chart(s,[(d['title'],xs,ys,TEAL)],.65+j*7.4,2.85,7.1,4.1,v['x_axis_voltage' if j==0 else 'x_axis_power'],v['voltage_panel' if j==0 else 'power_panel'],0,11,0,d['y_axis']['maximum'],False).chart
        chart.category_axis.major_unit=2;chart.value_axis.major_unit=d['y_axis']['major_unit']
        for k in [2,6]:chart.series[0].points[k].marker.size=11
    tx(s,v['body_1'],.8,7.1,7,.55,24,bold=True)
    tx(s,v['body_2'],8.2,7.1,7,.55,24,bold=True)
    foot(s,v['body_3']);return s

def s16(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p);d=p['visual']['chart_data']
    tx(s,v['chart_title'],.8,2.2,7,.45,25,bold=True)
    chart=xy_chart(s,[(v['legend_r1'],d['secondary_power_W'],d['R1_secondary_region_max_C'],TEAL),(v['legend_r3'],d['secondary_power_W'],d['R3_input_bridge_region_max_C'],AMBER)],.45,2.85,7.65,4.2,v['x_axis'],v['y_axis'],40,145,40,105).chart
    chart.legend.font.size=Pt(18);chart.category_axis.major_unit=20;chart.value_axis.major_unit=20
    chart.series[1].marker.style=XL_MARKER_STYLE.SQUARE
    tx(s,v['image_caption'],8.4,2.2,6.8,.8,24,bold=True)
    pic(s,'thermal_final.jpg',8.4,3.28,6.8,3.82)
    tx(s,v['r1_annotation'],6.25,3.43,1.65,.4,21,fill=TEAL,bold=True)
    tx(s,v['r3_annotation'],2.68,4.08,1.7,.4,21,fill=AMBER,bold=True)
    bullets(s,[v['bullet1'],v['bullet2']],.8,7.27,14.4,24,gap=.56)
    return s

def s17(prs,p,i):
    s=base(prs,p['title'],i,dark=True,title_size=42);v=content(p)
    bullets(s,[v[k] for k in ['contribution','connector','limit']],.8,2.75,14.4,35,gap=1.58,fill=WHITE)
    return s


def b01(prs,p,i):
    q={**p,'visual':{**p['visual'],'series':[{'name':g['name'],'points':[{'load_current_a':r['iout_a'],'error_percent':r['error_pct']} for r in g['points']]} for g in p['visual']['series']]}}
    s=legacy.b01(prs,q,i)
    from pptx.enum.chart import XL_TICK_LABEL_POSITION
    next(sh.chart for sh in s.shapes if sh.has_chart).category_axis.tick_label_position=XL_TICK_LABEL_POSITION.LOW
    return s

def b02(prs,p,i):
    s=base(prs,p['title'],i,title_size=40);v=content(p)
    tx(s,v['conditions'],.8,2.2,14.4,.45,23,fill=MUTED)
    sh=table(s,v['table_headers'],v['table_rows'],.8,3.0,14.4,4.6,[1.15,1.05,1.18,1.15,1.38,.7,1.3],24)
    for j,row in enumerate(sh.table.rows):row.height=Inches(1.08 if j==0 else .67)
    return s

def b03(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p);t=v['readings']
    tx(s,v['condition'],.8,2.2,14.4,.45,22,fill=MUTED)
    sh=table(s,t['columns'],t['rows'],.8,3.0,14.4,4.35,[1.15,1.15,1.2,1.8,1.8],24)
    for j,row in enumerate(sh.table.rows):
        row.height=Inches(1.1 if j==0 else .48)
        for cell in row.cells:
            cell.margin_top=Inches(.05);cell.margin_bottom=Inches(.04)
            if j:
                for para in cell.text_frame.paragraphs:para.alignment=PP_ALIGN.RIGHT
    foot(s,v['equilibrium']);return s

def b04(prs,p,i):
    s=base(prs,p['title'],i,title_size=40);v=content(p)
    tx(s,v['equation'],.8,2.3,14.4,.8,39,bold=True,fill=TEAL)
    for j,pre in enumerate(['original','modified']):
        x=.8+j*7.4
        tx(s,v[pre+'_heading'],x,3.55,7,.55,28,bold=True)
        line(s,x,4.3,x+7,4.3,TEAL,2)
        tx(s,v[pre+'_inductance'],x,4.6,7,.62,26)
        tx(s,v[pre+'_capacitance'],x,5.35,7,.55,28)
        tx(s,v[pre+'_result'],x,6.16,7,.6,36,bold=True,fill=TEAL)
    tx(s,v['carrier_label'],.8,7.27,14.4,.5,25,bold=True)
    foot(s,v['caption']);return s

def b05(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);v=content(p)
    pic(s,'v2_complete_power_schematic.png',.8,2.12,14.4,4.65)
    tx(s,v['figure_caption'],.8,6.93,14.4,.47,25,bold=True)
    tx(s,v['control_roles'],.8,7.49,14.4,.48,24)
    tx(s,v['citation'],.8,8.07,14.4,.32,18,fill=MUTED)
    return s

BUILDERS={k:v for k,v in list(globals().items()) if k[0] in 'sb' and len(k)==3 and callable(v)}

def main():
    prs=new_deck();manifest=json.loads((ROOT/'review/slide-manifest.json').read_text());built=[];timing=[];md=['# Defense speaker notes','']
    for item in manifest['slides']:
        sid=item['slide_id'];path=ROOT/'proposals'/f'{sid}.json'
        if not path.exists() or sid not in BUILDERS:continue
        p=json.loads(path.read_text());i=len(built)+1
        s=BUILDERS[sid](prs,p,i);notes(s,p)
        built.append({**item,'order':i,'title':p['title']})
        spoken=s.notes_slide.notes_text_frame.text
        timing.append({'slide_id':sid,'seconds':p['duration_seconds'],'words':len(spoken.split()),'backup':item['section']=='backup'})
        md.extend([f'## {i}. {p["title"]}',f'{p["duration_seconds"]} seconds','',spoken,''])
    prs.save(ROOT/(NAME+'.pptx'));(ROOT/'Speaker_Notes.md').write_text('\n'.join(md))
    (ROOT/'review/render-manifest.json').write_text(json.dumps({'slides':built},indent=2));(ROOT/'review/timing.json').write_text(json.dumps(timing,indent=2));(ROOT/'review/layout-bounds.json').write_text(json.dumps(BOUNDS,indent=2))
    print(f'Built {len(built)} slides')

if __name__=='__main__':main()
