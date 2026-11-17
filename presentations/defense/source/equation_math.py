"""Editable PowerPoint Office Math equations, on deck_tools' 16 × 9 grid.

LibreOffice fits math to its text box, so preserve the default aspect ratio when
scaling. Each equation has an explicit baseline size and may be independently
edited in PowerPoint's equation editor.
"""
from pptx.util import Inches
from lxml import etree

SCALE = 5 / 6
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
A14 = 'http://schemas.microsoft.com/office/drawing/2010/main'

def tag(ns, local): return '{%s}%s' % (ns, local)
def node(local, *children, **attrs):
    e = etree.Element(tag(M, local))
    for k, v in attrs.items(): e.set(tag(M, k), v)
    e.extend(children)
    return e

def run(text, plain=False, color='171748', size=2800):
    r = node('r')
    if plain: r.append(node('rPr', node('nor')))
    rp = etree.SubElement(r, tag(A, 'rPr'), sz=str(size))
    fill = etree.SubElement(rp, tag(A, 'solidFill'))
    etree.SubElement(fill, tag(A, 'srgbClr'), val=color)
    t = node('t'); t.text = text; r.append(t)
    return r

def sub(base, label, color):
    if isinstance(base, str): base = run(base, color=color)
    return node('sSub', node('e', base), node('sub', run(label, plain=True, color=color)))

def bar(base, color):
    return node('bar', node('barPr', node('pos', val='top')), node('e', run(base, color=color)))

def equation_nodes(kind, color):
    if kind == 'rectifier':
        return [sub(bar('i', color), 'rec', color), run('≈', plain=True, color=color), run('b', color=color), sub('f','s',color), sub('C','P',color), sub('v','rec',color)]
    if kind == 'switching':
        return [sub('P','sw',color), run('≈',plain=True,color=color), sub('f','s',color), sub('E','sw',color)]
    if kind == 'resonance':
        root = node('rad',node('radPr',node('degHide',val='on')),node('deg'),node('e',sub('L','total',color),sub('C','s',color)))
        frac = node('f',node('fPr',node('type',val='bar')),node('num',run('1',plain=True,color=color)),node('den',run('2',plain=True,color=color),run('π',plain=True,color=color),root))
        return [sub('f','0',color),run('=',plain=True,color=color),frac]
    raise ValueError('Unknown equation: ' + str(kind))

# Coordinates use the same 16 × 9 grid as deck_tools. Height includes space for
# subscripts and accents; scaling by width preserves the tested aspect ratio.
DEFAULTS = {'rectifier': (4.7, 0.84), 'switching': (3.0, 0.84), 'resonance': (3.1, 1.15)}

def add_equation(slide, kind, x, y, width=None, color='171748', source_text=''):
    w0, h0 = DEFAULTS[kind]
    w = w0 if width is None else width
    h = h0 * w / w0
    shape = slide.shapes.add_textbox(Inches(x*SCALE), Inches(y*SCALE), Inches(w*SCALE), Inches(h*SCALE))
    shape.name = 'Equation: ' + kind
    shape._element.xpath('./p:nvSpPr/p:cNvPr')[0].set('descr', source_text)
    tf = shape.text_frame
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]._p
    p.get_or_add_pPr()
    wrapper = etree.Element(tag(A14, 'm'), nsmap={'a14':A14, 'm':M})
    math = node('oMath', *equation_nodes(kind, color))
    wrapper.append(math)
    p.append(wrapper)
    end = etree.SubElement(p, tag(A, 'endParaRPr'), sz='2800')
    fill = etree.SubElement(end, tag(A, 'solidFill'))
    etree.SubElement(fill, tag(A, 'srgbClr'), val=color)
    return shape
