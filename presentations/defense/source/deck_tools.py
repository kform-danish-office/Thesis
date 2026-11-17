"""Editable PowerPoint primitives used by build_defense.py."""
from pathlib import Path
import re
from PIL import Image
from pptx import Presentation
from pptx.util import Inches as NativeInches, Pt as NativePt

# The existing diagrams use a 16-by-9 design grid; the supplied DTU master is 13 1/3 by 7 1/2 inches.
SCALE = 5 / 6
def Inches(value): return NativeInches(value * SCALE)
def Pt(value): return NativePt(value * SCALE)
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import XyChartData, CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_MARK, XL_MARKER_STYLE

FONT = 'Arial'
INK = '171748'
MUTED = '4C4C59'
RED = '990000'
TEAL = '2F3EEA'
BLUE = '171748'
PALE = 'F0F1FF'
LINE = 'D9DCEC'
WHITE = 'FFFFFF'
AMBER = '8B4B10'
BOUNDS = []

def color(value):
    return RGBColor.from_string(value)

def new_deck():
    template = Path(__file__).resolve().parent / 'template/DTU_Blue_base.pptx'
    prs = Presentation(template)
    # Remove the example/help slides while retaining every original master and layout.
    for entry in list(prs.slides._sldIdLst):
        prs.part.drop_rel(entry.rId)
        prs.slides._sldIdLst.remove(entry)
    prs.core_properties.author = 'Richard Xu'
    prs.core_properties.title = 'Charge-Pump PFC USB-C Power Supply — Thesis Defense'
    prs.core_properties.subject = '25-minute MSc thesis defense'
    return prs

def clear_placeholders(slide):
    for shape in list(slide.shapes):
        if shape.is_placeholder:
            element=shape._element
            element.getparent().remove(element)

def slide_number(slide,index):
    # The DTU footer and university name are inherited from its master.
    text(slide,str(index),15.10,8.61,.55,.22,size=11,fill=WHITE,align=PP_ALIGN.RIGHT)


def record(slide, shape, label):
    BOUNDS.append({'slide': slide.slide_id, 'label': label,
                   'x': float(shape.left / Inches(1)), 'y': float(shape.top / Inches(1)),
                   'w': float(shape.width / Inches(1)), 'h': float(shape.height / Inches(1))})
    return shape

INLINE_MATH={'V_SW':('V','SW'),'Pₛw':('P','sw'),'Eₒₙ':('E','on'),'Eₒff':('E','off'),'Eₛw':('E','sw'),'f₀':('f','0'),'īᵣₑ꜀':('ī','rec'),'vᵣₑ꜀':('v','rec'),'fₛ':('f','s'),'Cₚ':('C','p'),'Lₚ':('L','p'),'Cₛ':('C','s'),'Lₛ':('L','s'),'īᵣₑ꜀':('ī','rec'),'Ltotal':('L','total'),'Lₜₒₜₐₗ':('L','total'),'L_total':('L','total'),'C_s':('C','s'),'C_P':('C','P'),'f_0':('f','0')}

def inline_runs(paragraph,value,size,fill=INK,bold=False):
    """Keep prose sans-serif and render mathematical symbols with true subscripts."""
    paragraph.clear()
    for part in re.split('('+'|'.join(map(re.escape,INLINE_MATH))+')',str(value)):
        if not part:continue
        if part in INLINE_MATH:
            base,sub=INLINE_MATH[part]
            r=paragraph.add_run();r.text=base
            r.font.name='Cambria Math';r.font.size=Pt(size);r.font.italic=True;r.font.bold=False;r.font.color.rgb=color(fill)
            r=paragraph.add_run();r.text=sub
            r._r.get_or_add_rPr().set('baseline','-25000')
            r.font.name='Cambria Math';r.font.size=Pt(size*.72);r.font.italic=False;r.font.bold=False;r.font.color.rgb=color(fill)
        else:
            r=paragraph.add_run();r.text=part
            r.font.name=FONT;r.font.size=Pt(size);r.font.bold=bold;r.font.color.rgb=color(fill)

def rect(slide, x,y,w,h, fill=PALE, stroke=None, radius=False):
    sh=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                              Inches(x),Inches(y),Inches(w),Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb=color(fill)
    if stroke: sh.line.color.rgb=color(stroke); sh.line.width=Pt(1)
    else: sh.line.fill.background()
    if radius: sh.adjustments[0]=0.08
    for effect in sh._element.xpath('.//a:effectRef'):effect.set('idx','0')
    return record(slide,sh,'panel')

def text(slide, value, x,y,w,h, size=26, fill=INK, bold=False, align=PP_ALIGN.LEFT,
         valign=MSO_ANCHOR.TOP, margin=0, spacing=1.12):
    if str(value)=='': return None
    sh=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=sh.text_frame; tf.word_wrap=True
    tf.margin_left=tf.margin_right=Inches(margin)
    tf.margin_top=tf.margin_bottom=Inches(margin)
    tf.vertical_anchor=valign
    for i,line in enumerate(str(value).split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        inline_runs(p,line,size,fill,bold)
        p.alignment=align; p.space_before=Pt(0); p.space_after=Pt(5)
        p.line_spacing=spacing
    return record(slide,sh,str(value)[:75])

def line(slide,x1,y1,x2,y2,fill=LINE,width=1.5,dash=None):
    sh=slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2))
    sh.line.color.rgb=color(fill); sh.line.width=Pt(width)
    if dash is not None:sh.line.dash_style=dash
    for effect in sh._element.xpath('.//a:effectRef'):effect.set('idx','0')
    return sh

def arrow(slide,x,y,w,h=.25,fill=TEAL):
    sh=slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,Inches(x),Inches(y),Inches(w),Inches(h))
    sh.fill.solid();sh.fill.fore_color.rgb=color(fill);sh.line.fill.background()
    for effect in sh._element.xpath('.//a:effectRef'):effect.set('idx','0')
    return sh

def picture(slide,path,x,y,w,h):
    path=Path(path)
    with Image.open(path) as im:iw,ih=im.size
    scale=min(w/iw,h/ih); dw,dh=iw*scale,ih*scale
    sh=slide.shapes.add_picture(str(path),Inches(x+(w-dw)/2),Inches(y+(h-dh)/2),width=Inches(dw),height=Inches(dh))
    return record(slide,sh,'image '+path.name)

def base(prs,title,index,kicker='',dark=False,title_size=38.4):
    # Use the supplied DTU title-only layout for the body and blue Front A for the conclusion.
    slide=prs.slides.add_slide(prs.slide_layouts[0 if dark else 7])
    clear_placeholders(slide)
    # The native title anchor matches the template's title placeholder exactly.
    text(slide,title,2.328,.564,12.216,1.272,size=title_size,
         fill=WHITE if dark else INK,bold=True,spacing=1.02)
    slide_number(slide,index)
    return slide

def bullets(slide,items,x,y,w,size=26,gap=.92,fill=INK):
    from PIL import ImageFont
    font=ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',round(size*SCALE*2))
    top=y
    for item in items:
        if not str(item).strip(): continue
        count=0
        for explicit in str(item).split('\n'):
            current=''; count+=1
            for word in explicit.split():
                candidate=(current+' '+word).strip()
                if current and font.getlength(candidate)>(w-.24)*60*2:
                    count+=1;current=word
                else:current=candidate
        h=max(.4,count*size/72*1.17+.1)
        rect(slide,x,top+.12,.07,.20,WHITE if fill==WHITE else TEAL)
        text(slide,item,x+.24,top,w-.24,h,size=size,fill=fill)
        top+=max(gap,h+.18)


def metric(slide,value,label,x,y,w=3.5,value_color=TEAL,dark=False):
    text(slide,value,x,y,w,.82,size=48,bold=True,fill=value_color)
    text(slide,label,x,y+1.01,w,1.1,size=22,fill=WHITE if dark else MUTED)

def callout(slide,value,x,y,w,h=.8,fill=PALE,fg=INK,size=23):
    rect(slide,x,y,w,h,fill)
    rect(slide,x,y,.06,h,TEAL)
    text(slide,value,x+.23,y+.14,w-.46,h-.2,size=size,fill=fg)

def table(slide,headers,rows,x,y,w,h,widths=None,size=21):
    shp=slide.shapes.add_table(len(rows)+1,len(headers),Inches(x),Inches(y),Inches(w),Inches(h))
    tb=shp.table
    if widths:
        for col,frac in zip(tb.columns,widths):col.width=Inches(w*frac/sum(widths))
    for r,vals in enumerate([headers]+rows):
        for c,val in enumerate(vals):
            cell=tb.cell(r,c);cell.text=str(val)
            cell.margin_left=Inches(.12);cell.margin_right=Inches(.10)
            cell.margin_top=Inches(.12);cell.margin_bottom=Inches(.07)
            cell.vertical_anchor=MSO_ANCHOR.MIDDLE
            cell.fill.solid();cell.fill.fore_color.rgb=color(INK if r==0 else (PALE if r%2 else WHITE))
            for p in cell.text_frame.paragraphs:
                if any(token in p.text for token in INLINE_MATH):inline_runs(p,p.text,size if r else size-1,WHITE if r==0 else INK,r==0)
                p.space_before=Pt(0);p.space_after=Pt(0)
                for run in p.runs:
                    if run.font.name!='Cambria Math':
                        run.font.name=FONT;run.font.size=Pt(size if r else size-1)
                        run.font.bold=(r==0);run.font.color.rgb=color(WHITE if r==0 else INK)
    return record(slide,shp,'table')

def xy_chart(slide,series,x,y,w,h,x_label,y_label,x_min=None,x_max=None,y_min=None,y_max=None,legend=True):
    cd=XyChartData()
    for name,xs,ys,series_color in series:
        s=cd.add_series(name)
        for xv,yv in zip(xs,ys):s.add_data_point(xv,yv)
    sh=slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_LINES,Inches(x),Inches(y),Inches(w),Inches(h),cd)
    chart=sh.chart;chart.has_title=False;chart.has_legend=legend and len(series)>1
    if chart.has_legend:
        chart.legend.position=XL_LEGEND_POSITION.TOP;chart.legend.include_in_layout=False
        chart.legend.font.name=FONT;chart.legend.font.size=Pt(15)
    for s,(_,xs,ys,c) in zip(chart.series,series):
        s.format.line.color.rgb=color(c);s.format.line.width=Pt(2.6)
        s.marker.style=XL_MARKER_STYLE.CIRCLE;s.marker.size=7
        s.marker.format.fill.solid();s.marker.format.fill.fore_color.rgb=color(c)
        s.marker.format.line.color.rgb=color(c)
        s.smooth=False
    for axis,label,lo,hi in [(chart.category_axis,x_label,x_min,x_max),(chart.value_axis,y_label,y_min,y_max)]:
        axis.has_title=True;axis.axis_title.text_frame.text=label
        for p in axis.axis_title.text_frame.paragraphs:
            for r in p.runs:r.font.name=FONT;r.font.size=Pt(18);r.font.color.rgb=color(INK)
        axis.tick_labels.font.name=FONT;axis.tick_labels.font.size=Pt(16);axis.tick_labels.font.color.rgb=color(MUTED)
        axis.major_tick_mark=XL_TICK_MARK.NONE;axis.minor_tick_mark=XL_TICK_MARK.NONE
        axis.format.line.color.rgb=color(LINE)
        if lo is not None:axis.minimum_scale=lo
        if hi is not None:axis.maximum_scale=hi
    chart.value_axis.has_major_gridlines=True
    chart.value_axis.major_gridlines.format.line.color.rgb=color(LINE)
    chart.category_axis.has_major_gridlines=False
    chart.chart_style=2
    return record(slide,sh,'editable chart')

def notes(slide,proposal):
    body=proposal.get('speaker_notes','')
    if not isinstance(body,str):body='\n\n'.join(body)
    transition=proposal.get('transition')
    if transition and transition not in body:body+='\n\n'+transition
    if proposal.get('references_note'):body+='\n\n'+proposal['references_note']
    slide.notes_slide.notes_text_frame.text=body
