"""One stable, editable V2 circuit view for the three operation slides."""
from deck_tools import *
from circuit_tools import wire,ground,cap,inductor,diode,switch,transformer,dot,box,label


def master_circuit(s,focus=None):
    first=len(s.shapes)
    # Stage highlights are backgrounds: all component positions stay fixed.
    if focus=='pump':rect(s,1.88,3.0,3.85,3.42,PALE)
    if focus=='tank':rect(s,7.4,3.55,3.95,2.9,PALE)
    for title,x,w in [('Charge pump',2.0,3.7),('GaN half bridge',5.4,2.45),('Resonant tank',7.85,2.5)]:label(s,title,x,2.56,w,23,c=TEAL)
    # Rectified line enters the charge-pump branch; the named SW and HV-link nets
    # are the same nodes as their labels on the half bridge.
    label(s,'AC input',.5,2.77,1.5,19)
    box(s,'Input bridge',.5,3.39,1.4,.82,size=19)
    wire(s,(1.9,3.8),(2.0,3.8));cap(s,2.4,3.8)
    wire(s,(2.8,3.8),(4.4,3.8));inductor(s,4.9,3.8);wire(s,(5.4,3.8),(5.76,3.8))
    label(s,'Cₚ',2.0,4.12,.8,20);label(s,'Lₚ',4.5,4.12,.8,20);label(s,'SW',5.08,3.15,.8,21)
    wire(s,(1.95,3.8),(1.95,4.9),(2.07,4.9));diode(s,2.5,4.9);wire(s,(2.93,4.9),(3.0,4.9))
    wire(s,(3.0,3.8),(3.0,3.92));diode(s,3.0,4.35,True);wire(s,(3.0,4.78),(3.0,5.15));cap(s,3.0,5.55,True);wire(s,(3.0,5.95),(3.0,6.12),(3.8,6.12))
    wire(s,(3.8,6.12),(3.8,4.95));diode(s,3.8,4.52,True,True);wire(s,(3.8,4.09),(3.8,3.8))
    for x,y in [(1.95,3.8),(3.0,3.8),(3.8,3.8),(3.0,4.9),(3.0,6.12)]:dot(s,x,y)
    ground(s,3.0,6.12);label(s,'HV link',1.9,5.22,.95,19)
    # Shared half bridge: exactly one midpoint excites both paths.
    x=6.6
    label(s,'HV link',5.9,3.08,1.4,20);wire(s,(x,3.47),(x,3.52));switch(s,x,4.0)
    switch(s,x,5.55);wire(s,(x,4.48),(x,5.07));wire(s,(x,6.03),(x,6.24));ground(s,x,6.24)
    label(s,'QH',6.83,3.65,.75,20);label(s,'QL',5.66,5.31,.75,20)
    dot(s,x,4.76);wire(s,(x,4.76),(7.45,4.76));label(s,'SW',6.76,4.15,.8,21)
    # Resonant path and isolated secondary. Transformer leakage is represented
    # inside the non-ideal transformer; Ls is the external series element.
    cap(s,7.85,4.76);wire(s,(8.25,4.76),(8.55,4.76));inductor(s,9.05,4.76)
    wire(s,(9.55,4.76),(9.9,4.76),(9.9,4.05),(10.45,4.05));transformer(s,10.67,4.55)
    wire(s,(10.45,5.05),(10.45,6.24));ground(s,10.45,6.24)
    label(s,'Cₛ',7.35,5.13,1.0,20);label(s,'Lₛ',8.56,5.13,1.0,20)
    label(s,'Transformer',9.65,3.18,2.1,20);label(s,'T1',10.05,3.68,1.1,20)
    wire(s,(11.07,4.05),(11.25,4.05),(11.25,4.4),(11.45,4.4))
    wire(s,(11.07,5.05),(11.25,5.05),(11.25,5.25),(11.45,5.25))
    box(s,'Secondary rectifier',11.45,4.0,1.65,1.5,size=18)
    wire(s,(13.1,4.43),(13.35,4.43),(13.35,5.0));cap(s,13.35,5.4,True)
    wire(s,(13.35,5.8),(13.35,6.06),(13.1,6.06),(13.1,5.25));ground(s,13.35,6.06)
    wire(s,(13.35,4.43),(13.65,4.43));box(s,'USB-C PD',13.65,4.0,1.55,.86,size=19)
    wire(s,(15.2,4.43),(15.55,4.43),(15.55,5.08));label(s,'USB-C output',14.25,5.26,1.4,19)
    label(s,'Secondary bulk',11.25,6.46,2.05,19)
    # Functional feedback is kept below the electrical circuit. Its arrows
    # begin at the bulk label, without drawing a conductor across isolation.
    box(s,'Isolated voltage feedback',9.0,7.02,3.8,.64,size=20)
    box(s,'MCU',5.5,7.02,1.5,.64,size=22)
    dot(s,13.35,4.43);wire(s,(13.35,4.43),(13.52,4.43),(13.52,7.34),(12.8,7.34),c=TEAL,width=1.6)
    a=arrow(s,12.82,7.24,.35,.20);a.rotation=180
    wire(s,(9.0,7.34),(7.0,7.34),c=TEAL,width=1.6)
    a=arrow(s,7.1,7.24,.4,.20);a.rotation=180
    wire(s,(5.5,7.34),(5.0,7.34),(5.0,6.75),(5.25,6.75),(5.25,4.0),(6.12,4.0),c=TEAL,width=1.6)
    label(s,'Burst enable',3.5,6.88,1.4,18,c=TEAL)
    a=arrow(s,5.84,3.9,.42,.20)
    label(s,'PGND',2.42,6.49,1.15,17);label(s,'SGND',14.4,6.79,1.2,17)
    # Compact the unscaled electrical drawing vertically, leaving a consistent
    # explanation band below it on all three circuit slides.
    for sh in list(s.shapes)[first:]:
        y=sh.top/Inches(1)
        sh.top=Inches(2.35+(y-2.35)*.86)
        sh.height=round(sh.height*.86)
