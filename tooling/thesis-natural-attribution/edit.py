from pathlib import Path
import json,shutil
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-natural-attribution');edits=[]
# Contextual changes keep attribution without treating the supplied work as a legal category.
mapping={
'Frontmatter/Abstract.tex': [('an inherited charge-pump power-factor-correction (PFC) resonant topology','a charge-pump power-factor-correction (PFC) resonant topology from earlier DTU work')],
'Frontmatter/Approval.tex': [('identifies the inherited designs and the author\'s integration, control, and test work','describes the earlier designs and the integration, control, and test work completed in this project')],
'Chapters/01_Introduction/01_Motivation.tex': [('the inherited conversion principle','the original conversion principle')],
'Chapters/01_Introduction/02_Problem_Statement.tex': [('an inherited charge-pump PFC resonant converter','the DTU charge-pump PFC resonant converter')],
'Chapters/01_Introduction/03_Aim_Objectives.tex': [('the inherited charge-pump topology','the charge-pump topology from earlier DTU work')],
'Chapters/01_Introduction/04_Research_Questions.tex': [('the inherited charge-pump resonant circuit','the original charge-pump resonant circuit')],
'Chapters/01_Introduction/07_Thesis_Structure.tex': [('the inherited circuit','the original circuit'),('the inherited models','the supplied models')],
'Chapters/02_Background/04_Soft_Switching_GaN.tex': [('The inherited discrete-GaN and external-driver models','The supplied discrete-GaN and external-driver models')],
'Chapters/04_Topology_Analysis/08_ZVS.tex': [('the inherited model','the supplied model')],
'Chapters/04_Topology_Analysis/11_Design_Summary.tex': [('the inherited models','the supplied models')],
'Chapters/05_Modeling_Simulation/01_Objectives.tex': [('The inherited LTspice circuits','The supplied LTspice circuits')],
'Chapters/05_Modeling_Simulation/02_Uploaded_LTspice_Files.tex': [('Inherited LTspice Circuits','Supplied LTspice Circuits'),('The inherited \\sourcefile','The supplied \\sourcefile'),('Inherited simulation parameters','Reference simulation parameters'),('the inherited files','the supplied files')],
'Chapters/05_Modeling_Simulation/03_GaN_Model.tex': [('the inherited model','the supplied model')],
'Chapters/05_Modeling_Simulation/04_Simulation_Setup.tex': [('the inherited simulations','the supplied simulations'),('the inherited circuits','the supplied circuits')],
'Chapters/05_Modeling_Simulation/09_Loss_Estimation.tex': [('The inherited loss files','The supplied loss files')],
'Chapters/06_Magnetics_Integration/01_Provenance.tex': [('The inherited work covered','The earlier design work covered'),('Inherited component work','Earlier component design')],
'Chapters/06_Magnetics_Integration/02_Inherited_Specifications.tex': [('the supplied measurements for two inductor variants','the given measurements for two inductor variants')],
'Chapters/06_Magnetics_Integration/03_Integration_Requirements.tex': [('the inherited core spacing','the original core spacing')],
'Chapters/06_Magnetics_Integration/11_Limitations.tex': [('the inherited magnetics','the supplied magnetics')],
'Chapters/07_Hardware/chapter.tex': [('the inherited charge-pump resonant circuit','the charge-pump resonant circuit from earlier DTU work')],
'Chapters/07_Hardware/17_V3_Edge_Card_Plan.tex': [('The inherited planar magnetics','The supplied planar magnetics')],
'Chapters/10_Results/11_Simulation_Hardware.tex': [('The inherited LTspice studies','The supplied LTspice studies'),('the inherited models','the supplied models')],
'Chapters/10_Results/15_V2_Testing_Update.tex': [('The inherited leakage values','The given leakage-inductance measurements')],
'Chapters/11_Discussion/05_Magnetics_Integration.tex': [('sensing; the electromagnetic design was inherited.','sensing. The electromagnetic design came from earlier DTU work.'),('The inherited measurements','The given component measurements')],
'Chapters/11_Discussion/07_Limitations.tex': [('The inherited simulations','The supplied simulations')],
'Chapters/12_Conclusion/chapter.tex': [('the inherited converter','the original DTU converter')],
'Chapters/12_Conclusion/01_Project_Summary.tex': [('the inherited DTU charge-pump PFC resonant topology','the DTU charge-pump PFC resonant topology')],
'Chapters/12_Conclusion/02_Research_Questions.tex': [('The inherited charge-pump branch','The original charge-pump branch'),('The inherited electromagnetic design','The supplied planar magnetics')],
'Chapters/12_Conclusion/03_Contributions.tex': [('The inherited charge-pump PFC principle and planar-magnetic design were\r\nintegrated','The charge-pump PFC principle and planar-magnetic design from earlier DTU\r\nwork were integrated')],
'Backmatter/Appendices/D_Modeling_Files.tex': [('in inherited simulations','in the supplied simulations')],
'Backmatter/Appendices/F_Contribution_Provenance.tex': [('Project Contributions and Inherited Designs','Project Contributions and Earlier DTU Designs')],
'Backmatter/References.tex': [('in inherited planar-magnetics documentation','in the supplied planar-magnetics documentation')],
'README.md': [('the inherited converter','the original DTU converter'),('hardware, inherited\r\n','hardware, supplied\r\n')]
}
for name,pairs in mapping.items():
 p=root/name;b=p.read_bytes();s=b.decode();out=s
 for old,new in pairs:
  assert old in out,(name,old);out=out.replace(old,new);edits.append({'path':name,'old':old,'new':new})
 backup=r/'before'/name;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(b);p.write_bytes(out.encode())
(r/'edits.json').write_text(json.dumps(edits,indent=2)+'\n')
print(len(edits),'contextual replacements in',len(mapping),'files')
