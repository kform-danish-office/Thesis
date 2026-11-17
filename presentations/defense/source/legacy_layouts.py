"""Assemble the reviewed circuit-led DTU defense as an editable PowerPoint."""
from pathlib import Path
import json, re, math
from deck_tools import *
from circuit_tools import wire, ground, cap, inductor, switch, transformer, dot, box, label, tank, full_power_circuit

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
NAME='Thesis_Defense_Circuit_Story_Revised'

def vc(p,key):
    return next(b['text'] for b in p['visible_content'] if b['id']==key)

def content(p):
    return {b['id']:b.get('text',b) for b in p['visible_content']}

def seq(value):return value if isinstance(value,list) else [value]

def pic(s,f,x,y,w,h):return picture(s,ASSETS/f,x,y,w,h)

def heading(s,t,x,y,w,size=29):text(s,t,x,y,w,.7,size=size,bold=True,fill=TEAL)

def footer(s,t):text(s,t,.8,7.82,14.4,.42,size=19,fill=MUTED)

def c01(prs,p,i):
    s=prs.slides.add_slide(prs.slide_layouts[0]);clear_placeholders(s)
    text(s,vc(p,'context'),.8,1.4,13.8,.55,size=27,fill=WHITE)
    text(s,p['title'],.8,2.6,13.8,3.25,size=47,bold=True,fill=WHITE,spacing=1.08)
    text(s,vc(p,'subtitle'),.8,6.15,13.8,.75,size=29,fill=WHITE)
    text(s,vc(p,'author'),.8,7.35,13.8,.55,size=30,bold=True,fill=WHITE)
    slide_number(s,i);return s

def adapter(s,x,y,w,h):
    rect(s,x,y,w,h,PALE,TEAL,True)
    line(s,x-.34,y+h*.3,x,y+h*.3,TEAL,5);line(s,x-.34,y+h*.7,x,y+h*.7,TEAL,5)
    rect(s,x+w-.32,y+h*.36,.12,h*.28,INK)

def c02(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    adapter(s,3.6,2.95,2.6,1.8)
    line(s,6.2,3.75,11.15,3.75,TEAL,2.5)
    rect(s,11.15,2.85,3.25,1.9,WHITE,INK);line(s,10.85,4.92,14.7,4.92,INK,4)
    label(s,vc(p,'adapter_label'),2.9,5.02,4.0,25)
    label(s,vc(p,'load_label'),10.8,5.1,4.1,25)
    text(s,vc(p,'power_target'),.8,5.65,7,.55,size=32,bold=True,fill=TEAL)
    text(s,vc(p,'power_minimum'),.8,6.3,7,.55,size=25,fill=MUTED)
    bullets(s,[vc(p,'benefit'),vc(p,'tradeoff')],8.0,6.18,7.2,size=26,gap=.85)
    return s

def c03(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    for x,prefix in [(.8,'earlier'),(8.2,'project')]:
        heading(s,vc(p,prefix+'_heading'),x,2.7,6.4,31)
        line(s,x,3.5,x+6.4,3.5,TEAL,3)
        items=vc(p,prefix+'_circuit').split('\n')+[vc(p,prefix+'_load')]
        bullets(s,items,x,4.03,6.4,33,gap=1.0)
    footer(s,vc(p,'citation'));return s

def c04(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    full_power_circuit(s,{'pump':'pump path','input':'rectified input','cp':'Cp','lp':'Lp','sw':'SW',
        'vdc':'DC link','cdc':'Cdc','halfbridge':'shared half bridge','qh':'QH','ql':'QL',
        'output_path':'resonant path','cs':'Cs','ls':'Ls','transformer':'T1',
        'rectifier':'Rectifier','pd':'USB-C PD','bulk':'secondary bulk Vsec','usb':'VBUS','pgnd':'PGND','sgnd':'SGND'})
    label(s,'D8',1.55,4.0,1,18);label(s,'D6',2.42,3.78,.7,18);label(s,'D7',4.0,4.06,.8,18)
    label(s,'Cout',13.52,5.52,1.05,18)
    label(s,'transformer',9.1,6.45,2.5,20)
    footer(s,vc(p,'circuit_caption'));return s

def c05(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    x=3.45;wire(s,(x,2.9),(x,3.1));switch(s,x,3.58);switch(s,x,5.15)
    wire(s,(x,4.06),(x,4.67));dot(s,x,4.38);wire(s,(x,5.63),(x,5.95))
    label(s,vc(p,'rail_high'),1.3,2.26,3.4,21);label(s,vc(p,'rail_low'),1.4,6.06,4.1,24)
    label(s,vc(p,'high_switch'),2.0,3.35,.9,24);label(s,vc(p,'low_switch'),2.0,4.95,.9,24)
    wire(s,(x,4.38),(5.1,4.38),(5.1,3.4),(6.9,3.4),c=TEAL)
    wire(s,(5.1,4.38),(5.1,5.45),(6.9,5.45),c=TEAL)
    label(s,vc(p,'switch_node'),3.8,4.53,1.1,24)
    label(s,vc(p,'pump_branch'),4.45,2.75,3.25,21)
    label(s,vc(p,'isolated_branch'),4.6,5.72,3.1,24)
    arrow(s,5.8,3.29,.65,.21);arrow(s,5.8,5.34,.65,.21)
    label(s,vc(p,'pump_current'),5.8,3.65,.7,21);label(s,vc(p,'tank_current'),5.8,4.77,.7,21)
    bullets(s,[vc(p,k) for k in ['carrier','branches','deadtime']],8.15,2.75,7.05,31,gap=1.52)
    text(s,vc(p,'diagram_type'),.8,7.25,7,.4,size=20,fill=MUTED)
    footer(s,vc(p,'current_reference'));return s

def c06(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    heading(s,vc(p,'pump_caption'),.8,2.3,6.6,27)
    pic(s,'schematic_pump_detail.png',.6,3.13,7.3,3.95)
    text(s,vc(p,'pump_capacitor'),.8,7.25,6.85,.4,size=24)
    text(s,vc(p,'pump_inductor'),.8,7.8,6.85,.4,size=24)
    text(s,vc(p,'equation'),8.15,2.45,7.05,.8,size=44,bold=True,fill=TEAL)
    text(s,vc(p,'equation_condition'),8.15,3.4,7.05,.7,size=22,fill=MUTED)
    bullets(s,[vc(p,f'bullet_{n}') for n in range(1,4)],8.15,4.5,7.05,29,gap=1.02)
    text(s,vc(p,'citation'),11.4,7.83,3.8,.4,size=19,fill=MUTED,align=PP_ALIGN.RIGHT)
    return s

def c07(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    y=3.8
    wire(s,(.9,y),(1.6,y));cap(s,2.0,y);wire(s,(2.4,y),(2.8,y));inductor(s,3.3,y)
    wire(s,(3.8,y),(4.4,y));inductor(s,4.9,y);wire(s,(5.4,y),(6.3,y),(6.3,3.3),(6.8,3.3))
    transformer(s,7.02,3.8);wire(s,(6.8,4.3),(6.8,5.55));ground(s,6.8,5.55)
    wire(s,(7.42,3.3),(7.9,3.3),(7.9,3.65),(8.4,3.65));wire(s,(7.42,4.3),(7.9,4.3),(7.9,4.6),(8.4,4.6))
    box(s,'secondary rectifier',8.4,3.3,2.1,1.65,size=24)
    wire(s,(10.5,3.65),(11.2,3.65),(11.2,4.35));cap(s,11.2,4.75,True)
    wire(s,(11.2,5.15),(11.2,5.55),(10.5,5.55),(10.5,4.6));ground(s,11.2,5.55)
    wire(s,(11.2,3.65),(12.5,3.65));box(s,'MPQ4242 USB-PD',12.5,3.22,2.7,1.2,size=25)
    for t,x,w in [('SW',.5,.9),('Cs (C26)',1.3,1.5),('Ls (L4)',2.65,1.6),('Llk',4.4,1.0),('T1',6.5,1.3),('Vsec',10.55,1.3)]:label(s,t,x,2.55,w,24)
    wire(s,(15.2,3.65),(15.55,3.65),(15.55,4.55))
    label(s,'VBUS',14.35,4.75,1.25,25)
    label(s,'Cbulk',11.4,4.65,1.1,22)
    label(s,'transformer leakage',4.0,4.5,2.0,23)
    label(s,'isolation and step-down',5.15,6.05,3.85,22)
    label(s,'energy buffer',9.9,6.08,2.6,24)
    # Control is conceptual and isolated, not an electrical conductor across the barrier.
    box(s,'MCU: bulk regulation',.8,6.95,6.1,.72,size=25)
    box(s,'PD: selected USB-C voltage',8.05,6.95,7.15,.72,size=25)
    footer(s,vc(p,'caption'));return s

def waveform(s,x,y,w,windows,pulses=32):
    dx=w/pulses
    for row in range(2):
        yy=y+row*.57;pts=[(x,yy+.3)]
        for k in range(pulses):
            xx=x+k*dx;on=any(a<=k<b for a,b in windows)
            if row==0:
                level=yy if on else yy+.3
                pts.extend([(xx,pts[-1][1]),(xx,level),(xx+dx,level)])
            elif on:pts.extend([(xx,yy+.3),(xx,yy),(xx+dx*.5,yy),(xx+dx*.5,yy+.3),(xx+dx,yy+.3)])
            else:pts.append((xx+dx,yy+.3))
        wire(s,*pts,c=TEAL if row else INK,width=1.6)

def c08(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    text(s,vc(p,'concept'),.8,2.10,14.4,.4,size=20,fill=MUTED)
    for n,key,windows in [(0,'low',[(2,5),(19,22)]),(1,'high',[(2,13),(19,30)])]:
        yy=2.95+n*1.65
        text(s,vc(p,key),.8,yy,2.8,.48,size=27,bold=True)
        text(s,vc(p,'enable'),.8,yy+.54,2.8,.35,size=20)
        text(s,vc(p,'carrier'),.8,yy+1.10,2.8,.43,size=20)
        waveform(s,3.7,yy+.45,5.2,windows)
    text(s,vc(p,'high_level'),3.7,2.65,2.0,.3,size=17)
    text(s,vc(p,'low_level'),6.9,2.65,2.0,.3,size=17)
    text(s,vc(p,'time'),7.6,6.27,1.4,.3,size=19)
    text(s,vc(p,'frequency'),.8,6.5,8.1,.4,size=23,bold=True)
    bullets(s,[vc(p,f'bullet{k}') for k in range(1,4)],9.65,3.0,5.55,28,gap=1.15)
    for j,k in enumerate(['power','cap','pd','load']):
        x=.8+j*3.7;box(s,vc(p,k),x,7.15,3.2,.68,size=19)
        if j<3:arrow(s,x+3.24,7.39,.4,.18)
    text(s,vc(p,'flow'),.8,7.93,4,.32,size=17,fill=MUTED)
    return s

def c09(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    # Large feedback loop; sensor and acquisition labels remain distinct.
    rect(s,5.9,2.45,9.3,2.9,WHITE,LINE)
    text(s,'MCU',6.12,2.52,1,.4,size=22,fill=TEAL,bold=True)
    nodes=[('Power stage',.8,3.05,2.0),('Secondary bulk voltage',3.2,3.05,2.3),('Isolated feedback',3.2,4.45,2.3),
           ('ADC + circular DMA',6.15,3.05,2.55),('Voltage control',9.1,3.05,2.3),('Bounded burst duty',11.8,3.05,2.95)]
    for t,x,y,w in nodes:box(s,t,x,y,w,.9,size=23)
    arrow(s,2.82,3.4,.30,.2);wire(s,(4.35,3.95),(4.35,4.45),c=TEAL)
    wire(s,(5.5,4.9),(5.8,4.9),(5.8,3.5),(6.15,3.5),c=TEAL)
    arrow(s,8.73,3.4,.3,.2);arrow(s,11.43,3.4,.3,.2)
    box(s,'Load classification',6.15,4.35,3.8,.65,size=21)
    wire(s,(7.4,3.95),(7.4,4.35),c=TEAL);wire(s,(9.95,4.67),(10.25,4.67),(10.25,3.95),c=TEAL)
    box(s,'Burst enable',11.8,4.35,2.95,.65,size=22)
    wire(s,(13.27,3.95),(13.27,4.35),c=TEAL)
    wire(s,(13.27,5.0),(13.27,5.72),(1.8,5.72),(1.8,3.95),c=TEAL)
    text(s,'Primary half-bridge current',.8,2.23,4.2,.47,size=22)
    wire(s,(4.95,2.45),(7.45,2.45),(7.45,3.05),c=TEAL)
    bullets(s,vc(p,'body'),.8,6.15,14.4,27,gap=.65)
    return s

def c10(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    footer(s,vc(p,'diagram_caption'))
    for j,k in enumerate(['precharge','loaded','light']):
        x=.8+j*4.95
        heading(s,vc(p,k),x,2.75,4.4,30)
        line(s,x,3.6,x+4.4,3.6,TEAL,3)
        bullets(s,[vc(p,k+'_action'),vc(p,k+'_benefit')],x,4.15,4.4,30,gap=1.4)
    arrow(s,8.6,6.9,1.4,.25)
    sh=arrow(s,8.6,7.25,1.4,.25);sh.rotation=180
    text(s,vc(p,'load_changes'),6.9,7.08,1.65,.6,size=20)
    return s

def c11(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    text(s,vc(p,'result'),.8,2.75,6.0,1.5,size=44,bold=True,fill=TEAL)
    text(s,vc(p,'calculation'),.8,4.6,5.5,1.05,size=28)
    text(s,vc(p,'conditions'),.8,6.0,5.5,1.1,size=23,fill=MUTED)
    b=next(b for b in p['visible_content'] if b['id']=='table')
    table(s,b['columns'],b['rows'],6.55,2.75,8.65,3.9,[.33,.32,.35],27)
    if b.get('title'):text(s,b['title'],6.55,7.0,8.65,.6,size=22,fill=MUTED)
    bs=[b['text'] for b in p['visible_content'] if b['id'].startswith('bullet')]
    if bs:bullets(s,bs,.8,7.5,14.4,size=22,gap=.45)
    return s

def scope_view(s,name,x,y,w):
    path=ASSETS/name
    with Image.open(path) as im:iw,ih=im.size
    top,bottom=144,638
    sh=s.shapes.add_picture(str(path),Inches(x),Inches(y),width=Inches(w),height=Inches(w*(bottom-top)/iw))
    sh.crop_top=top/ih;sh.crop_bottom=(ih-bottom)/ih
    return record(s,sh,'Original waveform with native crop')

def c12(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    for x,k,f in [(.8,'panel_5v','v1_scope_5v_3a.png'),(8.2,'panel_20v','v1_scope_20v_4a.png')]:
        heading(s,vc(p,k),x,2.65,7,30)
        scope_view(s,f,x,3.55,7)
    for k,x,c in [('legend_yellow',.8,'C5A100'),('legend_green',6.35,'008746'),('legend_blue',11.15,'175CC6')]:
        rect(s,x,7.02,.12,.3,c);text(s,vc(p,k),x+.24,6.95,min(4.8,15.4-x-.24),.78,size=23)
    footer(s,vc(p,'coupling'));return s

def resonant_path(s,x,y,after=False):
    wire(s,(x,y),(x+.75,y));cap(s,x+1.15,y);wire(s,(x+1.55,y),(x+2.0,y))
    if not after:inductor(s,x+2.5,y)
    else:wire(s,(x+2.0,y),(x+3.0,y))
    wire(s,(x+3.0,y),(x+3.6,y));inductor(s,x+4.1,y)
    wire(s,(x+4.6,y),(x+5.35,y),(x+5.35,y-.5),(x+5.8,y-.5))
    transformer(s,x+6.02,y);wire(s,(x+5.8,y+.5),(x+5.8,y+.87));ground(s,x+5.8,y+.87)
    wire(s,(x+6.42,y-.5),(x+7.15,y-.5));wire(s,(x+6.42,y+.5),(x+7.15,y+.5))
    label(s,'Switch node',x-.45,y-.75,1.3,20)
    label(s,'Cₛ ≈ 1.66 nF' if after else 'Cₛ',x+.25,y+.4,1.85,22)
    if not after:
        label(s,'external series inductor',x+1.5,y-1.25,2.3,18)
        label(s,'≈ 9.4 µH',x+1.6,y-.65,2.1,20)
    label(s,'transformer leakage',x+3.3,y+.4,1.95,20)
    label(s,'transformer',x+5.15,y-1.24,1.75,20)
    label(s,'secondary',x+6.9,y-.2,1.6,20)

def c13(prs,p,i):
    s=base(prs,p['title'],i,title_size=39)
    heading(s,vc(p,'before_heading'),.8,2.25,2,27);resonant_path(s,1.2,3.8)
    heading(s,vc(p,'after_heading'),.8,5.15,2,27);resonant_path(s,1.2,6.5,True)
    bullets(s,[vc(p,f'bullet{k}') for k in range(1,4)],10.1,2.85,5.1,29,gap=1.5)
    footer(s,vc(p,'diagram_caption'));return s

def c14(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    text(s,vc(p,'condition'),.8,2.2,14.4,.5,size=22,fill=MUTED)
    for j,panel in enumerate(p['visual']['panels']):
        xs,ys=zip(*panel['points'])
        x=.65+j*7.4
        shape=xy_chart(s,[(panel['title'],xs,ys,TEAL)],x,2.95,7.1,3.95,
             vc(p,'x_axis_voltage' if j==0 else 'x_axis_power'),vc(p,'voltage_panel' if j==0 else 'power_panel'),
             0,11,panel['y_axis']['minimum'],panel['y_axis']['maximum'],False)
        shape.chart.category_axis.major_unit=2;shape.chart.value_axis.major_unit=panel['y_axis']['major_unit']
    bullets(s,[vc(p,'result'),vc(p,'limit')],.8,7.08,14.4,25,gap=.55)
    return s

def c15(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);d=p['visual']['chart_data']
    text(s,vc(p,'chart_title'),.8,2.22,7.1,.5,size=26,bold=True)
    series=[(vc(p,'legend_r1'),d['secondary_power_W'],d['R1_secondary_region_max_C'],TEAL),
            (vc(p,'legend_r3'),d['secondary_power_W'],d['R3_input_bridge_region_max_C'],'A85B19')]
    chart=xy_chart(s,series,.5,2.8,7.5,4.1,vc(p,'x_axis'),vc(p,'y_axis'),40,145,40,105).chart
    chart.legend.font.size=Pt(18)
    pic(s,'thermal_final.jpg',8.35,2.85,6.85,4.1)
    text(s,vc(p,'image_caption'),8.35,2.2,6.85,.6,size=23,bold=True)
    text(s,vc(p,'chart_point_r1'),.8,7.03,3.5,.42,size=21,fill=TEAL)
    text(s,vc(p,'chart_point_r3'),4.5,7.03,3.5,.42,size=21,fill='A85B19')
    bs=[b['text'] for b in p['visible_content'] if b['id'].startswith('bullet')]
    bullets(s,bs,.8,7.65,14.4,size=24,gap=.5)
    return s

def c17(prs,p,i):
    s=base(prs,p['title'],i,dark=True,title_size=42)
    bullets(s,[vc(p,k) for k in ['contribution','measured_results','target']],.8,2.6,14.4,36,gap=1.65,fill=WHITE)
    return s

def b01(prs,p,i):
    from chart_tools import separate_xy_columns
    s=base(prs,p['title'],i,title_size=41)
    text(s,vc(p,'condition'),.8,2.1,14.4,.45,size=21,fill=MUTED)
    groups=p['visual']['series'];palette=[TEAL,'00805A','A85B19',INK]
    series=[(g['name'],[r['load_current_a'] for r in g['points']],[r['error_percent'] for r in g['points']],c) for g,c in zip(groups,palette)]
    shape=xy_chart(s,series,.6,2.75,14.8,4.45,vc(p,'x_axis'),vc(p,'y_axis'),0,4.2,-.2,.7)
    chart=shape.chart
    separate_xy_columns(chart,[{'name':g['name'],'points':[{'iout_a':r['load_current_a'],'error_pct':r['error_percent']} for r in g['points']]} for g in groups])
    for trace,marker in zip(chart.series,[XL_MARKER_STYLE.CIRCLE,XL_MARKER_STYLE.SQUARE,XL_MARKER_STYLE.TRIANGLE,XL_MARKER_STYLE.DIAMOND]):
        trace.format.line.fill.background();trace.marker.style=marker;trace.marker.size=9
    chart.category_axis.major_unit=1;chart.value_axis.major_unit=.1
    text(s,vc(p,'legend'),.8,2.55,14.4,.4,size=20)
    text(s,vc(p,'result'),.8,7.33,14.4,.5,size=25,bold=True,fill=TEAL)
    footer(s,vc(p,'formula'));return s

def b03(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    text(s,vc(p,'condition'),.8,2.2,14.4,.45,size=22,fill=MUTED)
    b=next(b for b in p['visible_content'] if b['id']=='readings')
    shape=table(s,b['columns'],b['rows'],.8,3.0,14.4,4.3,[.9,1.05,1.05,1.1,2.0,2.0],21)
    for j,row in enumerate(shape.table.rows):
        row.height=Inches(1.05 if j==0 else .46)
        for cell in row.cells:
            cell.margin_top=Inches(.07);cell.margin_bottom=Inches(.04)
            for par in cell.text_frame.paragraphs:
                for run in par.runs:run.font.size=Pt(19 if j==0 else 21)
    footer(s,vc(p,'equilibrium'));return s

def b02(prs,p,i):
    from pptx.enum.chart import XL_DATA_LABEL_POSITION
    s=base(prs,p['title'],i,title_size=41)
    text(s,vc(p,'conditions'),.8,2.1,14.4,.45,size=22,fill=MUTED)
    for j,desc in enumerate(p['visual']['charts']):
        data=CategoryChartData();data.categories=[str(v) for v in desc['categories_a']]
        vals=desc.get('values',desc.get('values_percent'));data.add_series(desc['title'],vals)
        x=.8+j*7.4
        text(s,desc['title'],x,2.7,7,.5,size=27,bold=True)
        sh=s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(x),Inches(3.3),Inches(7),Inches(3.7),data)
        chart=sh.chart;chart.has_title=False;chart.has_legend=False;chart.chart_style=2
        trace=chart.series[0];trace.format.fill.solid();trace.format.fill.fore_color.rgb=color(TEAL if j==0 else INK)
        trace.format.line.fill.background()
        chart.plots[0].has_data_labels=True;dl=chart.plots[0].data_labels
        dl.position=XL_DATA_LABEL_POSITION.OUTSIDE_END;dl.font.name=FONT;dl.font.size=Pt(21)
        for pt,t in zip(trace.points,desc['data_labels']):
            pt.data_label.text_frame.text=t
            for par in pt.data_label.text_frame.paragraphs:
                for r in par.runs:r.font.name=FONT;r.font.size=Pt(21)
        for axis,txt in [(chart.category_axis,desc['x_axis']),(chart.value_axis,desc['y_axis']['label'])]:
            axis.has_title=True;axis.axis_title.text_frame.text=txt
            for par in axis.axis_title.text_frame.paragraphs:
                for r in par.runs:r.font.name=FONT;r.font.size=Pt(19)
            axis.tick_labels.font.name=FONT;axis.tick_labels.font.size=Pt(19)
            axis.major_tick_mark=XL_TICK_MARK.NONE
        chart.value_axis.minimum_scale=0;chart.value_axis.maximum_scale=desc['y_axis']['maximum']
        chart.value_axis.major_unit=desc['y_axis']['major_unit']
        record(s,sh,'Editable input-quality chart')
    bullets(s,[vc(p,'result'),vc(p,'efficiency')],.8,7.25,14.4,size=24,gap=.56)
    return s

def b04(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    text(s,vc(p,'formula'),.8,2.3,14.4,.8,size=39,bold=True,fill=TEAL)
    for j,pre in enumerate(['original','modified']):
        x=.8+j*7.4
        heading(s,vc(p,pre+'_heading'),x,3.55,7,27)
        line(s,x,4.25,x+7,4.25,TEAL,2)
        text(s,vc(p,pre+'_values').replace('; ', ';\n').replace('1 nF','1\u00a0nF'),x,4.55,7,1.1,size=27)
        text(s,vc(p,pre+'_result'),x,5.75,7,.65,size=36,bold=True)
    text(s,vc(p,'leakage_caption'),.8,6.7,14.4,.45,size=21,fill=MUTED)
    bullets(s,[vc(p,'bullet1'),vc(p,'bullet2')],.8,7.27,14.4,size=24,gap=.55)
    return s

def b05(prs,p,i):
    s=base(prs,p['title'],i,title_size=41)
    pic(s,'schematic_v2_power_stage_excerpt.png',.8,2.45,14.4,3.65)
    text(s,vc(p,'schematic_caption'),.8,6.2,14.4,.48,size=25,bold=True)
    text(s,vc(p,'roles'),.8,6.85,14.4,.62,size=23)
    text(s,vc(p,'citation_2020'),.8,7.53,14.4,.36,size=20,fill=MUTED)
    text(s,vc(p,'citation_2021'),.8,7.99,14.4,.36,size=20,fill=MUTED)
    return s

BUILDERS={f'c{i:02}':globals()[f'c{i:02}'] for i in range(1,18) if i!=16}
BUILDERS.update({f'b{i:02}':globals()[f'b{i:02}'] for i in range(1,6)})

def main():
    prs=new_deck();manifest=json.loads((ROOT/'review/slide-manifest.json').read_text())
    built=[];timing=[];notes_md=['# Defense speaker notes','']
    for item in manifest['slides']:
        sid=item['slide_id'];path=ROOT/'proposals'/f'{sid}.json'
        if not path.exists() or sid not in BUILDERS:continue
        p=json.loads(path.read_text());i=len(built)+1
        s=BUILDERS[sid](prs,p,i);notes(s,p)
        built.append({**item,'order':i,'title':p['title']})
        spoken=s.notes_slide.notes_text_frame.text
        timing.append({'slide_id':sid,'seconds':p['duration_seconds'],'words':len(spoken.split()),'backup':item['section']=='backup'})
        notes_md.extend([f'## {i}. {p["title"]}',f'{p["duration_seconds"]} seconds','',spoken,''])
    prs.save(ROOT/(NAME+'.pptx'))
    (ROOT/'Speaker_Notes.md').write_text('\n'.join(notes_md))
    (ROOT/'review/render-manifest.json').write_text(json.dumps({'slides':built},indent=2))
    (ROOT/'review/timing.json').write_text(json.dumps(timing,indent=2))
    (ROOT/'review/layout-bounds.json').write_text(json.dumps(BOUNDS,indent=2))
    print(f'Built {len(built)} slides')

if __name__=='__main__':main()
