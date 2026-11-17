"""Assemble the revised defense from exact, independently judged slide proposals."""
from pathlib import Path
import json,csv
from deck_tools import *
from circuit_tools import wire,box,label
from chart_tools import separate_xy_columns
from master_circuit import master_circuit
from equation_math import add_equation
import prior_layouts as old

ROOT=Path(__file__).resolve().parent;ASSETS=ROOT/'assets';NAME='Thesis_Defense_Focused'
def v(p):
    a=p['visible_content'];return a if isinstance(a,dict) else {b['id']:b.get('text',b) for b in a}
def tx(s,t,x,y,w,h=.6,size=27,**kw):return text(s,t,x,y,w,h,size=size,**kw)
def foot(s,t):return tx(s,t,.8,8.0,14.4,.35,19,fill=MUTED)
def s01(prs,p,i):return old.s01(prs,p,i)

def s02(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);d=v(p)
    for j in range(4):
        x=.8+j*3.7
        tx(s,d[f'state_{j+1}'],x,2.65,3.1,1.0,29,bold=True,align=PP_ALIGN.CENTER)
        if j<3:arrow(s,x+3.15,3.01,.48,.22)
    line(s,.8,4.0,15.2,4.0,LINE,1.4)
    tx(s,d['target'],.8,4.45,14.4,.68,32,bold=True,fill=TEAL)
    bullets(s,[d[f'contribution_{j}'] for j in range(1,4)],.8,5.7,14.4,30,gap=.82)
    return s

def shared(prs,p,i,focus=None):
    s=base(prs,p['title'],i,title_size=41);master_circuit(s,focus);return s

def s03(prs,p,i):
    s=shared(prs,p,i);d=v(p)
    tx(s,d['concept'],.8,2.06,14.4,.38,19,fill=MUTED)
    tx(s,d['bulk_control'],.8,7.47,6.85,.83,25,bold=True)
    tx(s,d['pd_control'],8.15,7.47,7.05,.83,25,bold=True)
    return s

def s04(prs,p,i):
    s=shared(prs,p,i,'pump');d=v(p)
    tx(s,d['equation'],.8,7.25,6.7,.65,34,bold=True,fill=TEAL)
    tx(s,d['legend'],.8,8.0,6.7,.35,21,fill=MUTED)
    tx(s,d['body_2'],8.2,7.35,7,1.0,29,bold=True)
    return s

def s05(prs,p,i):
    s=shared(prs,p,i,'tank');d=v(p)
    tx(s,d['body_1'],.8,7.45,6.6,.9,29,bold=True,fill=TEAL)
    tx(s,d['body_2'],8.0,7.45,7.2,.9,27,bold=True)
    return s

def s06(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);d=v(p)
    # The closed functional loop remains directly beside the measured burst.
    labs=d['loop_labels']
    positions=[(.8,2.65,2.8),(3.95,2.65,3.2),(7.5,2.65,1.6),(9.45,2.65,2.4),(12.2,2.65,3.0)]
    for name,(x,y,w) in zip(labs,positions):box(s,name,x,y,w,.9,size=24)
    for x,w in [(3.65,.24),(7.2,.24),(9.15,.24),(11.9,.24)]:arrow(s,x,3.0,w,.2)
    wire(s,(13.7,3.55),(13.7,3.95),(2.2,3.95),(2.2,3.55),c=TEAL,width=1.5)
    tx(s,d['trace_condition'],.8,4.37,9.5,.47,26,bold=True)
    old.crop(s,'v1_scope_5v_3a.png',.8,5.0,9.5,left=100/1028,top=193/843,right=1/1028,bottom=(843-327)/843)
    tx(s,d['trace_annotations'][1],.95,6.65,3.0,.4,20)
    tx(s,d['trace_annotations'][0],5.4,6.65,4.9,.4,20)
    bullets(s,[d[f'body_{j}'] for j in range(1,4)],11.0,4.5,4.2,25,gap=1.02)
    tx(s,' · '.join(d['trace_scales']),.8,7.33,9.5,.42,23)
    foot(s,d['trace_legend']);return s

def s07(prs,p,i):
    from pptx.enum.chart import XL_TICK_LABEL_POSITION
    s=base(prs,p['title'],i,title_size=41);d=v(p)
    tx(s,d['test_condition'],.8,2.17,14.4,.42,22,fill=MUTED)
    with (ASSETS/'v1_dc_operating_points.csv').open() as f:rows=list(csv.DictReader(f))
    groups=[]
    for n in [5,9,15,20]:
        groups.append({'name':f'{n} V','points':[{'iout_a':float(r['iout_a']),'error_pct':float(r['voltage_error_percent_derived'])} for r in rows if float(r['pdo_v'])==n and float(r['iout_a'])>0]})
    palette=[TEAL,'00805A',AMBER,INK]
    chart=xy_chart(s,[(g['name'],[a['iout_a'] for a in g['points']],[a['error_pct'] for a in g['points']],c) for g,c in zip(groups,palette)],.55,2.79,14.85,4.32,d['chart_x_axis'],d['chart_y_axis'],0,4.2,-.2,.7).chart
    separate_xy_columns(chart,groups)
    for ser,m in zip(chart.series,[XL_MARKER_STYLE.CIRCLE,XL_MARKER_STYLE.SQUARE,XL_MARKER_STYLE.TRIANGLE,XL_MARKER_STYLE.DIAMOND]):ser.format.line.fill.background();ser.marker.style=m;ser.marker.size=9
    chart.category_axis.major_unit=1;chart.value_axis.major_unit=.2;chart.category_axis.tick_label_position=XL_TICK_LABEL_POSITION.LOW;chart.legend.font.size=Pt(21)
    tx(s,d['body_1'],.8,7.15,14.4,.5,25)
    tx(s,d['body_2'],.8,7.71,14.4,.5,26,bold=True,fill=TEAL)
    return s

def s08(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);d=v(p)
    tx(s,d['test_condition'],.8,2.17,14.4,.5,23,fill=MUTED)
    box(s,d['input_label'],.8,3.25,4.2,1.2,size=32)
    arrow(s,5.15,3.69,1.25,.32)
    box(s,d['connector_label'],6.55,3.25,8.65,1.2,size=34)
    tx(s,d['measurement'],6.55,4.75,8.65,.65,28,align=PP_ALIGN.CENTER)
    line(s,.8,5.68,15.2,5.68,LINE,1.5)
    tx(s,d['efficiency_label'],.8,6.15,14.4,.8,39,bold=True,fill=TEAL)
    tx(s,d['difference_label'],.8,7.29,14.4,.65,30)
    return s


def s09(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);d=v(p);pts=p['visual']['points']
    tx(s,d['condition'],.8,2.15,14.4,.45,23,fill=MUTED)
    for j,(field,title,hi,unit) in enumerate([('power_factor','pf_panel_title',1,.2),('current_thd_percent','thd_panel_title',100,20)]):
        x=.7+j*7.4;tx(s,d[title],x+.1,2.8,7,.5,28,bold=True)
        chart=xy_chart(s,[(d[title],[a['load_current_a'] for a in pts],[a[field] for a in pts],TEAL if j==0 else INK)],x,3.45,7.1,3.45,d['x_axis_label'],d[title],0,4.2,0,hi,False).chart
        chart.series[0].format.line.fill.background();chart.series[0].marker.size=9;chart.category_axis.major_unit=1;chart.value_axis.major_unit=unit
        tx(s,d['pf_endpoint_label' if j==0 else 'thd_endpoint_label'],x+.1,7.05,7,.5,31,bold=True,fill=TEAL)
    foot(s,d['body_1']);return s

def s10(prs,p,i):
    from circuit_tools import cap,inductor,transformer,ground
    s=base(prs,p['title'],i,title_size=41);d=v(p)
    for pre,y in [('before',3.8),('after',6.1)]:
        tx(s,d[pre+'_label'],.8,y-1.6,4.5,.45,27,bold=True,fill=TEAL)
        x=2.0
        wire(s,(x,y),(x+.75,y));cap(s,x+1.15,y);wire(s,(x+1.55,y),(x+2,y))
        if pre=='before':inductor(s,x+2.5,y)
        else:wire(s,(x+2,y),(x+3,y))
        wire(s,(x+3,y),(x+3.6,y));inductor(s,x+4.1,y)
        wire(s,(x+4.6,y),(x+5.35,y),(x+5.35,y-.5),(x+5.8,y-.5));transformer(s,x+6.02,y)
        wire(s,(x+5.8,y+.5),(x+5.8,y+.87));ground(s,x+5.8,y+.87)
        wire(s,(x+6.42,y-.5),(x+7.15,y-.5));wire(s,(x+6.42,y+.5),(x+7.15,y+.5))
        tx(s,d[pre+'_switch_node'],.8,y-.22,1.1,.4,23)
        tx(s,d[pre+'_capacitor'],x+.15,y+.4,2.0,.55,23,align=PP_ALIGN.CENTER)
        if pre=='before':tx(s,d['before_external_inductor'],x+1.9,y-1.1,2.1,.9,22,align=PP_ALIGN.CENTER)
        tx(s,d[pre+'_leakage'],x+3.2,y+.4,2.35,.8,22,align=PP_ALIGN.CENTER)
        tx(s,d[pre+'_transformer'],x+5.05,y-1.2,3.2,.5,22,align=PP_ALIGN.CENTER)
        tx(s,d[pre+'_secondary'],x+7.3,y-.28,3.9,.7,24)
    tx(s,d['body_1'],.8,7.6,6.5,.55,27,bold=True)
    tx(s,d['body_2'],8.1,7.6,7.1,.7,25,bold=True)
    return s

def s11(prs,p,i):
    s=base(prs,p['title'],i,title_size=40);d=v(p);pts=p['visual']['points']
    tx(s,d['condition'],.8,2.12,14.4,.4,23,fill=MUTED)
    for j,(field,key,hi,major) in enumerate([('secondary_power_W','power_axis_label',150,50),('secondary_voltage_V','voltage_axis_label',30,10)]):
        yy=2.8+j*2.6
        chart=xy_chart(s,[(d[key],[a['secondary_current_A'] for a in pts],[a[field] for a in pts],TEAL)],.6,yy,10.4,2.55,d['current_axis_label'] if j else '',d[key],0,11,0,hi,False).chart
        chart.category_axis.major_unit=2;chart.value_axis.major_unit=major
        if j==0:chart.category_axis.has_title=False
        for ix in [2,6]:chart.series[0].points[ix].marker.size=11
        for k,t in enumerate(d['power_callouts' if j==0 else 'voltage_callouts']):tx(s,t,11.45,yy+.4+k*.92,3.75,.8,25,bold=True,fill=TEAL if k else INK)
    return s

def s12(prs,p,i):
    s=base(prs,p['title'],i,title_size=40);d=v(p);pts=p['visual']['chart_data']
    tx(s,d['condition'],.8,2.1,14.4,.4,22,fill=MUTED)
    tx(s,d['image_caption'],.8,2.75,7.1,.6,24,bold=True)
    picture(s,ASSETS/'thermal_final.jpg',.8,3.45,7.1,4.15)
    tx(s,d['chart_title'],8.45,2.75,6.75,.62,23,bold=True)
    chart=xy_chart(s,[(d['chart_legend'][0],[a['point'] for a in pts],[a['secondary_r1_max_c'] for a in pts],TEAL),(d['chart_legend'][1],[a['point'] for a in pts],[a['input_bridge_r3_max_c'] for a in pts],AMBER)],8.1,3.55,7.25,3.5,d['chart_x_axis'],d['chart_y_axis'],1,7,40,105).chart
    chart.legend.font.size=Pt(18);chart.category_axis.major_unit=1;chart.value_axis.major_unit=20;chart.series[1].marker.style=XL_MARKER_STYLE.SQUARE
    tx(s,d['body_1'],8.45,7.15,6.75,.44,23)
    tx(s,d['body_2'],8.45,7.68,6.75,.44,23,bold=True)
    foot(s,d['equilibrium_caption']);return s

def s13(prs,p,i):
    s=base(prs,p['title'],i,dark=True,title_size=41);d=v(p)
    for j in range(1,4):
        yy=2.65+(j-1)*1.62
        tx(s,d[f'row_{j}_label'],.8,yy,4.4,.9,27,bold=True,fill=WHITE)
        tx(s,d[f'row_{j}_text'],5.4,yy,9.8,1.12,32,fill=WHITE)
    return s


def b01(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);d=v(p)
    tx(s,d['condition'],.8,2.2,14.4,.45,25,bold=True)
    old.crop(s,'v1_scope_20v_4p7a.png',.8,2.95,9.2,left=100/1028,top=150/843,bottom=(843-640)/843)
    for j,k in enumerate(['legend_1','legend_2','legend_3']):tx(s,d[k],11.25,3.13+j*1.25,3.95,1.15,23)
    tx(s,d['time_scale'],11.25,7.02,3.95,.55,24,bold=True)
    foot(s,d['body_1']);return s

def b02(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);d=v(p)
    rows=[d[k] for k in ['table_external_inductance','table_transformer_leakage','table_series_total','table_capacitance','table_frequency']]
    sh=table(s,d['table_column_labels'],rows,.8,2.55,14.4,3.9,[1.5,1,1],25)
    for j,row in enumerate(sh.table.rows):row.height=Inches(.72 if j==0 else .61)
    record(s,add_equation(s,'resonance',.8,6.55,width=3.35,source_text=d['equation']),'Native resonance equation')
    tx(s,d['caption'],.8,8.03,14.4,.42,22,fill=MUTED)
    return s

def b03(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);d=v(p)
    tx(s,d['caption'],.8,2.18,14.4,.45,23,fill=MUTED)
    rows=[d[f'table_row_{j}'] for j in range(1,8)]
    sh=table(s,d['table_headers'],rows,.8,2.97,14.4,4.4,[.6,1.15,1.15,1.15,1.6,1.6],23)
    for j,row in enumerate(sh.table.rows):
        row.height=Inches(1.1 if j==0 else .48)
        for cell in row.cells:cell.margin_top=Inches(.05);cell.margin_bottom=Inches(.04)
    foot(s,d['condition']);return s

def b04(prs,p,i):
    s=base(prs,p['title'],i,title_size=41);d=v(p)
    picture(s,ASSETS/'v2_complete_power_schematic.png',.8,2.2,14.4,4.7)
    tx(s,d['caption'],.8,7.02,14.4,.42,25,bold=True)
    tx(s,d['citation_1'],.8,7.6,14.4,.35,21,fill=MUTED)
    tx(s,d['citation_2'],.8,8.1,14.4,.35,21,fill=MUTED)
    return s

BUILDERS={k:x for k,x in list(globals().items()) if len(k)==3 and k[0] in 'sb' and callable(x)}

def main():
    prs=new_deck();m=json.loads((ROOT/'manifest.json').read_text());built=[];timing=[];md=['# Defense speaker notes','']
    for item in m['slides']:
        sid=item['slide_id'];path=ROOT/'proposals'/f'{sid}.json'
        if not path.exists() or sid not in BUILDERS:continue
        p=json.loads(path.read_text());ix=len(built)+1
        slide=BUILDERS[sid](prs,p,ix);notes(slide,p)
        built.append({**item,'order':ix,'title':p['title']});spoken=slide.notes_slide.notes_text_frame.text
        timing.append({'slide_id':sid,'seconds':p['duration_seconds'],'notes_words':len(spoken.split()),'backup':item['section']=='backup'})
        md.extend([f'## {ix}. {p["title"]}',f'{p["duration_seconds"]} seconds','',spoken,''])
    prs.save(ROOT/(NAME+'.pptx'));(ROOT/'Speaker_Notes.md').write_text('\n'.join(md))
    (ROOT/'review/render-manifest.json').write_text(json.dumps({'slides':built},indent=2));(ROOT/'review/timing.json').write_text(json.dumps(timing,indent=2));(ROOT/'review/layout-bounds.json').write_text(json.dumps(BOUNDS,indent=2))
    print(f'Built {len(built)} slides')
if __name__=='__main__':main()
