from pathlib import Path
import json
root=Path('/workspace/thesis')
review=Path('/workspace/tooling/usb-pd-wording-review')
edits={
'Chapters/05_Modeling_Simulation/02_Uploaded_LTspice_Files.tex':[
('The predecessor regulates a high-voltage output; the prototype has separate isolated bulk and connector VBUS nodes. Model comparison requires corresponding nodes and power boundaries.','The predecessor regulates a high-voltage output; in the prototype, the isolated secondary bulk supply feeds the USB-C PD output stage. Comparisons must state where voltages and powers are measured and which stages and auxiliary supplies are included.')],
'Chapters/05_Modeling_Simulation/03_GaN_Model.tex':[
('At MHz frequency, transition-energy error directly affects calculated loss, so device-name substitution is insufficient.','At megahertz switching frequencies, transition-energy error directly affects calculated loss, so device-name substitution is insufficient.')],
'Chapters/05_Modeling_Simulation/05_Simulation_Cases.tex':[
("A fixed resistor at connector voltage does not reproduce the downstream regulator's bulk-bus demand.","An output resistor alone does not model the USB-C PD stage's input demand as its output voltage and load change.")],
'Chapters/05_Modeling_Simulation/07_Startup_NoLoad.tex':[
('Limited precharge establishes power for isolated feedback before voltage control.','Limited precharge is used to power the isolated feedback circuit before normal voltage control begins.')],
'Chapters/06_Magnetics_Integration/07_Isolation_Clearance.tex':[
('The functional isolation path does not establish these margins.','Functional isolation alone does not establish creepage, clearance, or dielectric strength.')],
'Chapters/06_Magnetics_Integration/10_Verification.tex':[
('Converter tests demonstrate assembled-path power transfer,','Converter tests demonstrate power transfer through the installed magnetics,')],
'Chapters/07_Hardware/06_Resonant_Output.tex':[
('This separates the resonant transfer function from the final connector voltage setting.','The USB-C PD stage regulates the output voltage from this bulk supply.')],
'Chapters/07_Hardware/07_USBC_Interface.tex':[
('The isolated bulk supply was connected to the USB-C connector through the MPQ4242GVE-0000-AEC1-P stage.','The MPQ4242GVE-0000-AEC1-P stage regulates the USB-C output voltage from the isolated bulk supply.'),
('The bulk and connector nodes are named separately as \\texttt{V\\_PW\\_OUTPUT\\_BULK} and \\texttt{USB\\_PD\\_OUT} in \\Cref{fig:schematic-usbc}.','In \\Cref{fig:schematic-usbc}, \\texttt{V\\_PW\\_OUTPUT\\_BULK} feeds the stage and \\texttt{USB\\_PD\\_OUT} supplies the USB-C output.'),
('The secondary bulk voltage is regulated by the front-end controller using the secondary-voltage feedback signal received at MCU input PA1. Connector VBUS also depends on the downstream power path and cable drop, so the measured node is stated with each result.','The MCU regulates the secondary bulk voltage using feedback at PA1. The USB-C PD stage regulates its output to the selected PD level. Voltage at the load can differ because of cable drop, so the measurement point is stated with each result.')],
'Chapters/07_Hardware/10_Auxiliary_Power.tex':[
('Bounded precharge bursts and settling intervals establish the secondary supply before normal control.','Bounded precharge bursts and settling intervals are used to power the secondary-side sensing before normal control.')],
'Chapters/07_Hardware/16_V2_F410.tex':[
('ADC1 continuously scans primary voltage at PA0, secondary-bulk voltage at PA1, and half-bridge current at PA2 through DMA2 Stream0 Channel0, independently of carrier phase.','ADC1 continuously scans primary voltage at PA0, secondary-bulk voltage at PA1, and half-bridge current at PA2 through DMA2 Stream0 Channel0 without synchronization to the carrier.'),
('USB-PD sheet 2 includes the MPQ4242GVE-0000-AEC1-P output stage and separate \\texttt{V\\_PW\\_OUTPUT\\_BULK}/\\texttt{USB\\_PD\\_OUT} nodes.','USB-PD sheet 2 includes the MPQ4242GVE-0000-AEC1-P output stage, fed from \\texttt{V\\_PW\\_OUTPUT\\_BULK} and supplying \\texttt{USB\\_PD\\_OUT}.')],
'Chapters/08_Control_Firmware/01_Control_Objectives.tex':[
('the downstream MPQ4242 sets connector VBUS.','the MPQ4242 USB-C PD stage regulates the output voltage to the selected PD level.')],
'Chapters/08_Control_Firmware/02_Architecture_Timing.tex':[
('Acquisition is free-running and independent of both carrier phase and the foreground loop.','The scan is free-running without synchronization to the carrier, and DMA acquisition continues while the foreground loop runs.')],
'Chapters/08_Control_Firmware/15_PWR_2_Port.tex':[
('The free-running ADC scan retains primary voltage, secondary-bulk voltage, and primary current, sampled sequentially and independently of carrier phase.','The free-running ADC scan samples primary voltage, secondary-bulk voltage, and primary current sequentially, without synchronization to the carrier.')],
'Backmatter/Appendices/C_Firmware_Documentation.tex':[
('The software request is aligned with a carrier boundary without an interrupt on every \\SI{1}{\\mega\\hertz} cycle. Interrupt latency and GPIO execution still affect the physical edge.','Polling attempts to align the software request with a carrier boundary without an interrupt on every \\SI{1}{\\mega\\hertz} cycle; it can time out without observing an update. Interrupt latency and GPIO execution still affect the physical edge.')],
'Backmatter/Appendices/G_Software_Tools.tex':[
('or delivered USB-C power. They are kept separate from the external\nload-current and VBUS measurements used for Chapter~\\ref{ch:results}.','or delivered USB-C power. The results in Chapter~\\ref{ch:results} use external\nload-current and VBUS measurements.'),
('The numerical module works independently.','The numerical module runs without the page interface.')]
}
rows=[]
for rel,changes in edits.items():
    p=root/rel;data=p.read_bytes()
    for old,new in changes:
        oldb=old.encode();newb=new.encode()
        assert data.count(oldb)==1,(rel,old)
        data=data.replace(oldb,newb)
        rows.append({'path':rel,'before':old,'after':new})
    p.write_bytes(data)
(review/'control-edits.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Edited',len(edits),'files with',len(rows),'local prose replacements')
