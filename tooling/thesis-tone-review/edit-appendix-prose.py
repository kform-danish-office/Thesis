from pathlib import Path
root=Path('/workspace/thesis/Backmatter/Appendices')
edits={
'A_Analytical_Equations.tex':[
("These are different circuit nodes. I use the connector voltage when calculating power delivered to the load; the controller's bulk-voltage reading is upstream of the output stage.","These voltages refer to different circuit nodes. I calculate power delivered to the load from the connector voltage. The controller reads bulk voltage upstream of the output stage."),
("The analyzer's THD reading can differ from the value calculated from an exported spectrum if the two use different harmonic ranges or averaging windows. The cause of the present difference is unresolved, so I report both values.","The analyzer's THD reading and the value calculated from an exported spectrum can differ when they use different harmonic ranges or averaging windows. I report both values because the cause of the present difference is unresolved."),
("An instantaneous peak-to-peak voltage is", "Instantaneous peak-to-peak voltage is"),
("Protection margins need the actual test configuration and timed waveforms.","Assessing the protection margins requires the actual test configuration and timed waveforms.")],
'B_Hardware_Documentation.tex':[
("The drawings below let the reader follow those circuit connections and compare them with the later V1.1 changes.","The drawings below show those circuit connections and the later V1.1 changes."),
("I include them as vector pages so the component labels remain readable when zoomed.","I include vector pages so the component labels remain readable when zoomed.")],
'C_Firmware_Documentation.tex':[
("The controller development has two software baselines.","Two software baselines document the controller development."),
("These definitions choose the command UART, gate pins, enable pin, LEDs, enable timer, and settings backend.","These definitions select the command UART, gate pins, enable pin, LEDs, enable timer, and settings backend."),
("Small negative voltage indications are also clamped near zero as specified in the source.","The source also clamps small negative voltage indications near zero."),
("Closed control runs from this background loop.","The background loop runs closed control."),
("It detects damaged/incomplete records, not every possible error.","It detects damaged or incomplete records, but cannot detect every possible error."),
("The active voltage loop does not call these helpers. Their settings remain for compatibility, but setting", "The active voltage loop does not call these helpers. Their settings are retained for compatibility, but setting"),
("The map below covers the sketch's functions in source order. Related helpers share a row so their role can be read beside the control path.","The map below lists the sketch's functions in source order. Related helpers share a row to show how they fit into the control path.")],
'D_Modeling_Files.tex':[
("The device choice is one important difference: the supplied model represents a GS66502B, and I used an integrated LMG2652 half bridge.","The device choice differs: the supplied model represents a GS66502B, while I used an integrated LMG2652 half bridge."),
("Predicting the installed stage's switching loss and temperature therefore needs its own device and circuit model.","Predicting switching loss and temperature in the installed stage therefore requires a model of its devices and circuit.")],
'E_Experimental_Data.tex':[
("This lets the reader follow a plotted point back to the measurement\nused in the calculation.","Each plotted point can therefore be traced back to the measurement\nused in its calculation."),
("Other selected rows\nstill contain differing instrument readings, so their calculated efficiencies\nremain screening values.","Some selected rows\nstill have differing instrument readings, so their calculated efficiencies\nremain screening values."),
("Assigning a junction temperature or continuous rating would\nalso need component identification, a thermal model, and a stabilized run.","A junction-temperature estimate or continuous rating would\nalso require component identification, a thermal model, and a stabilized run.")],
'F_Contribution_Provenance.tex':[
("The table below\nshows how those contributions fit together and credits the original designs.","The table below\nseparates my work from the original designs and credits their authors."),
("The operating-point measurements give\nthe starting point for the continuous-power, full-range, and conformance tests", "The operating-point measurements provide\na starting point for the continuous-power, full-range, and conformance tests")],
'G_Software_Tools.tex':[
("This appendix explains how those tools fit\ntogether.","This appendix explains how the tools work\ntogether."),
("The telemetry fields also need the same interpretation as the firmware.","The telemetry fields have the meanings defined in the firmware."),
("Starting from the board's reported values avoids changing an\nexisting bench configuration merely by connecting the interface.","Using the board's reported values avoids changing an\nexisting bench configuration just by connecting the interface."),
("These bounds\nkeep a long session from growing indefinitely.","These limits\nkeep a long session from growing indefinitely."),
("Successful file\nserving or a static build establishes that the interface files are available;\nit does not establish UART communication with a real board.","Serving the files or completing a static build confirms that the interface\nfiles are available. It does not verify UART communication with a real board."),
("I include them because they were present\nat source capture, while keeping their integration status explicit.","I include them because they were present\nat source capture, and state where their integration was incomplete."),
("The separated layout prevents ordinary\napplication sections from occupying the settings sector.","This layout keeps ordinary\napplication sections out of the settings sector."),
("Keeping row and cell identifiers makes a processed value easier\nto check against its original worksheet.","Row and cell identifiers make each processed value easier\nto check against its original worksheet."),
("Reproducing\nthose outputs checks the processing path.","Reproducing\nthose outputs checks that the processing steps can be repeated.")],
'H_Full_Embedded_Source.tex':[
("Keeping both files makes the changes traceable without assigning\nthe earlier measurements to the newer code.","Including both files makes the changes traceable without attributing\nthe earlier measurements to the newer code.")],
'I_Full_Supporting_Source.tex':[
("The original files and checksums\nare included in the editable package.","The editable package includes the original files and checksums.")],
'J_Revised_Plan_Integration.tex':[
("The repeat needs the V2 hardware, controller, settings, and raw files identified together.","The repeat needs a record that identifies the V2 hardware, controller, settings, and raw files together."),
("That keeps the final test period focused on the released design.","This keeps the final test period focused on the released design.")]
}
changed=[]
for name,pairs in edits.items():
 p=root/name;raw=(Path('/workspace/tooling/thesis-tone-review/original-source/Backmatter/Appendices')/name).read_bytes();s=raw.decode('utf-8')
 for old,new in pairs:
  if s.count(old)!=1:
   old=old.replace('\n','\r\n');new=new.replace('\n','\r\n')
  assert s.count(old)==1,(name,old,s.count(old));s=s.replace(old,new)
 p.write_bytes(s.encode('utf-8'));changed.append({'file':name,'edits':len(pairs)})
print(changed)
