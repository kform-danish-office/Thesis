"""Editable electrical symbols derived from the V2 circuit connections."""
import math
from deck_tools import *

def wire(s,*pts,c=INK,width=2):
    for a,b in zip(pts,pts[1:]):line(s,*a,*b,fill=c,width=width)

def dot(s,x,y,c=INK):
    sh=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x-.045),Inches(y-.045),Inches(.09),Inches(.09))
    sh.fill.solid();sh.fill.fore_color.rgb=color(c);sh.line.fill.background()

def ground(s,x,y,c=INK):
    for i,w in enumerate([.38,.24,.10]):line(s,x-w/2,y+i*.09,x+w/2,y+i*.09,c,1.7)

def cap(s,x,y,vertical=False,c=INK,length=.8):
    if vertical:
        wire(s,(x,y-length/2),(x,y-.08),c=c);wire(s,(x,y+.08),(x,y+length/2),c=c)
        line(s,x-.23,y-.08,x+.23,y-.08,c,2);line(s,x-.23,y+.08,x+.23,y+.08,c,2)
    else:
        wire(s,(x-length/2,y),(x-.08,y),c=c);wire(s,(x+.08,y),(x+length/2,y),c=c)
        line(s,x-.08,y-.23,x-.08,y+.23,c,2);line(s,x+.08,y-.23,x+.08,y+.23,c,2)

def inductor(s,x,y,length=1.0,vertical=False,c=INK):
    pts=[]
    for j in range(65):
        u=j/64
        a=(u-.5)*length;b=-.18*abs(math.sin(u*4*math.pi))
        pts.append((x+b,y+a) if vertical else (x+a,y+b))
    wire(s,*pts,c=c)

def diode(s,x,y,vertical=False,reverse=False,c=INK):
    # Anode is left/top; cathode is right/bottom unless reversed.
    def tr(u,v):
        if reverse:u=-u
        return (x+v,y+u) if vertical else (x+u,y+v)
    wire(s,tr(-.43,0),tr(-.18,0),c=c);wire(s,tr(.18,0),tr(.43,0),c=c)
    wire(s,tr(-.18,-.20),tr(-.18,.20),tr(.18,0),tr(-.18,-.20),c=c)
    wire(s,tr(.18,-.23),tr(.18,.23),c=c)

def switch(s,x,y,c=INK):
    wire(s,(x,y-.48),(x,y-.22),c=c)
    wire(s,(x,y+.22),(x,y+.48),c=c)
    wire(s,(x,y-.22),(x+.22,y+.18),c=c)
    dot(s,x,y-.22,c);dot(s,x,y+.22,c)

def transformer(s,x,y,c=INK):
    inductor(s,x-.22,y,1,True,c);inductor(s,x+.4,y,1,True,c)
    line(s,x+.03,y-.55,x+.03,y+.55,c,1);line(s,x+.11,y-.55,x+.11,y+.55,c,1)

def label(s,t,x,y,w=1.8,size=21,c=INK):
    text(s,t,x,y,w,.65,size=size,fill=c,align=PP_ALIGN.CENTER)

def box(s,t,x,y,w,h=.82,c=PALE,size=22):
    rect(s,x,y,w,h,c)
    text(s,t,x+.08,y+.10,w-.16,h-.14,size=size,align=PP_ALIGN.CENTER,valign=MSO_ANCHOR.MIDDLE)

def tank(s,x,y,w,labels,external=True):
    """Primary-referred series tank; labels supplied by accepted proposal."""
    cy=y+.9
    wire(s,(x,cy),(x+1.0,cy));cap(s,x+1.4,cy)
    wire(s,(x+1.8,cy),(x+2.2,cy))
    if external:inductor(s,x+2.7,cy)
    else:wire(s,(x+2.2,cy),(x+3.2,cy))
    wire(s,(x+3.2,cy),(x+3.6,cy));inductor(s,x+4.1,cy)
    wire(s,(x+4.6,cy),(x+w,cy))
    for key,px,pw in [('input',x,1),('cap',x+.8,1.5),('external',x+2.0,1.6),('leakage',x+3.5,2.0)]:
        if labels.get(key):label(s,labels[key],px,y if key!='external' or external else y+1.3,pw,23)

def full_power_circuit(s,L):
    """Simplified topology, with node names linking separated drawing branches.

    Pump and GaN branches are connected by named Vdc/SW/0V nets, as in the
    source schematic. This avoids false junctions in an overpacked overview.
    """
    # Pump branch: rectified input, capacitor/inductor, steering diodes, DC link.
    y=3.1
    label(s,L['pump'],.75,2.05,4.6,25,c=TEAL)
    label(s,L['input'],.65,2.55,2.2,19)
    wire(s,(1.1,y),(2.0,y));cap(s,2.4,y);wire(s,(2.8,y),(3.8,y))
    inductor(s,4.3,y);wire(s,(4.8,y),(5.2,y))
    label(s,L['cp'],1.85,3.45,1.2);label(s,L['lp'],3.7,3.45,1.2)
    label(s,L['sw'],4.65,2.57,.8)
    wire(s,(1.2,y),(1.2,4.65),(1.75,4.65));diode(s,2.18,4.65);wire(s,(2.61,4.65),(3.2,4.65))
    wire(s,(3.2,y),(3.2,3.72));diode(s,3.2,4.15,True);wire(s,(3.2,4.58),(3.2,4.65))
    wire(s,(3.2,4.65),(3.2,5.12));cap(s,3.2,5.52,True);wire(s,(3.2,5.92),(3.2,6.05),(3.8,6.05))
    wire(s,(3.8,6.05),(3.8,4.58));diode(s,3.8,4.15,True,True);wire(s,(3.8,3.72),(3.8,3.1))
    label(s,L['vdc'],2.1,4.87,1.0);label(s,L['cdc'],3.45,5.2,1.3)
    ground(s,3.2,6.05)
    label(s,L['pgnd'],2.6,6.35,1.2,17)
    for x,yy in [(1.2,y),(3.2,y),(3.2,4.65),(3.2,6.05)]:dot(s,x,yy)
    # Shared half bridge.
    x=6.45
    label(s,L['halfbridge'],5.05,2.05,3.2,23,c=TEAL)
    label(s,L['vdc'],5.9,2.65,1.1)
    switch(s,x,3.55);switch(s,x,5.2)
    wire(s,(x,4.03),(x,4.72));dot(s,x,4.37)
    wire(s,(x,5.68),(x,6.05));ground(s,x,6.05)
    label(s,L['qh'],5.5,3.35,.7);label(s,L['ql'],5.5,5.0,.7)
    wire(s,(x,4.37),(7.45,4.37));label(s,L['sw'],6.57,3.83,.8)
    # Isolated tank and output, simplified functional rectifier and PD blocks.
    label(s,L['output_path'],8.1,2.05,6.8,25,c=TEAL)
    cap(s,7.85,4.37);wire(s,(8.25,4.37),(8.55,4.37));inductor(s,9.05,4.37)
    wire(s,(9.55,4.37),(9.9,4.37),(9.9,3.7),(10.45,3.7))
    transformer(s,10.67,4.2)
    wire(s,(10.45,4.7),(10.45,6.05));ground(s,10.45,6.05)
    wire(s,(11.07,3.7),(11.4,3.7),(11.4,4.05),(11.65,4.05))
    wire(s,(11.07,4.7),(11.4,4.7),(11.4,4.65),(11.65,4.65))
    box(s,L['rectifier'],11.65,3.8,1.2,1.1,size=18)
    wire(s,(12.85,4.07),(13.35,4.07),(13.35,4.62));cap(s,13.35,5.02,True)
    wire(s,(13.35,5.42),(13.35,5.8),(12.85,5.8),(12.85,4.65))
    ground(s,13.35,5.8)
    label(s,L['sgnd'],14.05,5.9,1.2,17)
    wire(s,(13.35,4.07),(13.65,4.07));box(s,L['pd'],13.65,3.67,1.55,.85,size=19)
    label(s,L['cs'],7.3,4.83,1.1);label(s,L['ls'],8.5,4.83,1.3)
    label(s,L['transformer'],10.0,2.95,1.5,20);label(s,L['bulk'],12.35,6.45,2.1,18)
    wire(s,(15.2,4.07),(15.55,4.07),(15.55,4.65))
    label(s,L['usb'],14.35,4.83,1.25,20)
