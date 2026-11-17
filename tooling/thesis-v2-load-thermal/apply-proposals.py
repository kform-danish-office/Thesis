from pathlib import Path
import json,collections
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-v2-load-thermal')
newsection=r'''\subsection{Secondary-Output Load and Thermal Tests}
\label{sec:res-v2-secondary-load}

The electronic load was connected to the V2 secondary output. At
approximately \SI{240}{\volt} AC and \SI{50}{\hertz}, increasing the load
current from \SI{1.86}{\ampere} to \SI{10.01}{\ampere} raised the calculated
secondary power from \SI{48.68}{\watt} to \SI{137.08}{\watt}. The secondary
voltage fell from \SI{26.14}{\volt} to \SI{13.69}{\volt} over this sequence
(\cref{tab:v2-secondary-load,fig:v2-secondary-load-performance}). At
\SI{20.07}{\volt}, the load drew \SI{4.29}{\ampere}, giving
\SI{86.17}{\watt}. The higher-power points were therefore reached with
increasing voltage droop.

\input{Data/measurements/v2_load_thermal/load_table}

The input-bridge region R3 reached \SI{83.9}{\celsius} near
\SI{70.75}{\watt}. Its maxima at the subsequent higher-power points were
lower, between \SI{68.2}{\celsius} and \SI{75.6}{\celsius}. The secondary
region R1 became progressively hotter, rising from \SI{50.3}{\celsius} to
\SI{98.3}{\celsius}. This sequence shows the lower bridge temperatures
observed at higher loads alongside increasing secondary heating.

None of the load points reached thermal equilibrium. The sequence includes
both load changes and continued heating, so the temperatures cannot be
treated as settled values for each power level. Diode selection and the
current and thermal paths around the rectifiers require further work.
The tests show that the leakage-only stage can transfer more than
\SI{100}{\watt} to a secondary load; voltage droop and heating still limit
sustained operation.

\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{Data/measurements/v2_load_thermal/load_performance.pdf}
\caption{Secondary voltage and thermal-region maxima during the increasing-load sequence. Lines connect successive readings. R3 covers the input bridge and R1 the secondary area.}
\label{fig:v2-secondary-load-performance}
\end{figure}
\FloatBarrier
'''
newpath='Chapters/10_Results/17_V2_Secondary_Load_Tests.tex'
assert not (root/newpath).exists()
newjudgements=[]
reasons={
'abstract-v2':'Introduces the new secondary-output result while keeping V1 connector measurements distinct.',
'abstract-outcome':'The output location is explicit and the maximum is not repeated.',
'intro-objectives':'Replaces the obsolete request for any paired V2 power measurements with the actual higher-load result and remaining thermal work.',
'intro-v3':'Connects the new higher-load observations to the V3 motivation.',
'discussion-findings':'Updates the V2 outcome without replacing the V1 connector data.',
'discussion-magnetics':'Retains the earlier current range as history and states that later loading exceeded it with voltage droop.',
'discussion-epr':'Keeps the reviewer question as higher-load discussion and names the remaining physical issues.',
'discussion-future':'Replaces the stale V1 comparison with the current higher-load behavior and targeted measurements.',
'discussion-plan':'The proposal refers ambiguously to power levels after listing power differences; identify the 100 W secondary point explicitly.',
'discussion-steps':'A higher secondary-output snapshot does not justify dropping the existing baseline conditions before planned endurance steps.',
'conclusion-summary':'Names the secondary region as a surface region, preserves voltage droop, and states that no new point reached equilibrium.',
'conclusion-rq5':'Updates the lessons from the earlier apparent current limit without asserting a proven transformer or via cause.',
'hardware-v2':'Updates the historical baseline with the later secondary-load work and retains dimensions and the earlier plan point.',
'hardware-v3':'Separates the earlier loading observation from subsequent higher-current operation.',
'compliance-intro':'The USB-C and secondary-output endpoints are explicit; continuous requirements remain open.',
'compliance-power':'Keep the no-equilibrium statement specific to V2; the earlier V1 thermal record is incomplete rather than equivalent.',
'compliance-thermal':'Updates the thermal status without assigning a region maximum to an individual diode junction.',
'plan-v2-result':'Separates the earlier CP setting from the later calculated secondary powers.',
'plan-ap01':'Updates the maximum while preserving the exact V1 number and its output terminal.',
'plan-ap03':'Keep the suspected interlayer restriction as an existing hypothesis rather than silently dropping it.',
'plan-ap05':'Adds the new region maximum and preserves the uncompleted thermal work.',
'v2-secondary-load-results':'Use calculated load power, show the intermediate bridge-temperature peak rather than a monotonic claim, and identify the secondary area as a region. Insert the table and numeric plot; original screenshot embedding is pending files.',
'methods-v2-efficiency':'The general equations already define efficiency. Add the actual V2 terminals and instrument sources without repeating the uncertainty discussion.',
'methods-v2-thermal':'Describe the confirmed regions and region emissivity. Keep the few-second image/reading offset local; global camera/footer metadata stays in the data record.',
'appendix-v2-sources':'Identifies the new supply/load dataset and thermal-region readings without changing earlier waveform data.',
}
for scope in ['results','methods','story']:
 for p in json.loads((r/f'proposals/{scope}.json').read_text()):
  final=p['new'];decision='Accept';scores=[2,2,2]
  if p['id']=='v2-secondary-load-results':
   decision='Revise';scores=[1,1,2];final=r'\input{Chapters/10_Results/17_V2_Secondary_Load_Tests}'+'\n\n'+p['old']
  elif p['id']=='methods-v2-efficiency':
   decision='Revise';scores=[1,2,1];final=p['old']+'\r\n'+r'''For the V2 secondary-load tests, the AC supply's reported real power was
paired with voltage and current at the electronic-load terminals. Their
product gives the secondary-load power used in the efficiency estimate.
Loss in the leads between the secondary output and load is included with
the converter losses; no cable-loss correction was applied.
'''.replace('\n','\r\n')
  elif p['id']=='methods-v2-thermal':
   decision='Revise';scores=[1,2,1];final=r'''For the V2 secondary-load sequence, region R3 covered the input bridge and
R1 the secondary area. The maximum surface temperature in each region was
read with the displayed region emissivity of 0.95. Thermal images and
electrical readings were paired in test order and were taken a few seconds
apart.

'''.replace('\n','\r\n')+p['old']
  elif p['id']=='appendix-v2-sources':
   decision='Revise';scores=[2,2,1];final=final.replace('The corresponding\r\nthermal images give the region maxima described in', 'The associated\r\nthermal-region readings are described in')
  elif p['id']=='abstract-v2':
   final=final.replace('Heating in the secondary region and at the input bridge require', 'Heating in the secondary region and at the input bridge requires');decision='Revise';scores=[1,2,2]
  elif p['id']=='discussion-findings':
   final=final.replace('The input bridge and secondary region were hot during loading. ', '');decision='Revise';scores=[1,2,1]
  elif p['id']=='discussion-plan':
   final=final.replace('Later V2 secondary-output tests exceeded these power levels',r'Later V2 secondary-output tests delivered more than \SI{100}{\watt}');decision='Revise';scores=[2,1,1]
  elif p['id']=='discussion-steps':
   final=p['old'];decision='Reject';scores=[2,1,1]
  elif p['id']=='compliance-power':
   final=final.replace('tests did not reach thermal equilibrium','V2 tests did not reach thermal equilibrium');decision='Revise';scores=[2,1,2]
  elif p['id']=='plan-ap03':
   final+='; suspected interlayer restriction remains under investigation';decision='Revise';scores=[2,2,1]
  newjudgements.append({**p,'assignment':scope,'decision':decision,'proposed_scores':dict(zip(['voice','technical_fidelity','flow'],scores)),
      'lead_reason':reasons[p['id']],'final_new':final,'final_scores':{'voice':2,'technical_fidelity':2,'flow':2} if decision!='Reject' else None})

# Two current summaries would otherwise still imply that all results come from V1 waveforms.
for ident,path,old,new,why in [
 ('lead-results-opening','Chapters/10_Results/chapter.tex',
  'The selected average output voltage was maintained up to the highest matched\r\nload. The remaining questions are how the supply behaved during detachment,\r\nand what input power, switching behavior, and heating accompanied that output.\r\nOperation is assessed from the waveforms, while power and temperature\r\nmeasurements are used to identify further tests and design changes.',
  'The V1 tests cover USB-C output regulation, load removal, switching behavior,\r\ninput power, and heating. Later V2 tests examine the modified resonant tank\r\nand loading at the secondary output. AC-supply and electronic-load readings\r\nare combined with thermal-region temperatures to describe the higher-load\r\nbehavior and the changes still needed for sustained operation.',
  'Defines the V1 and V2 measurements directly and avoids treating the excluded new scope rows as results.'),
 ('lead-v2-earlier','Chapters/10_Results/15_V2_Testing_Update.tex',
  'Secondary-winding heating and limited power increase were observed near',
  'During earlier V2 tests, secondary-winding heating and limited power increase were observed near',
  'Keeps the original observation as the earlier test stage, not a present maximum.')]:
 newjudgements.append({'id':ident,'path':path,'old':old,'new':new,'final_new':new,'assignment':'lead','decision':'Lead edit','lead_reason':why,'proposed_scores':None,'final_scores':{'voice':2,'technical_fidelity':2,'flow':2}})

replacements={}
for j in newjudgements:
 s=replacements.get(j['path'],(root/j['path']).read_bytes().decode());assert s.count(j['old'])==1,j['id'];replacements[j['path']]=s.replace(j['old'],j['final_new'])
for name,s in replacements.items():
 p=root/name
 if p.read_bytes()==s.encode():continue
 backup=r/'before'/name;backup.parent.mkdir(parents=True,exist_ok=True);assert not backup.exists();backup.write_bytes(p.read_bytes());p.write_bytes(s.encode())
(root/newpath).write_text(newsection)
(r/'new-section.tex').write_text(newsection)
(r/'judgements.json').write_text(json.dumps(newjudgements,indent=2)+'\n')
counts=collections.Counter(j['decision'] for j in newjudgements)
lines=['# V2 load and thermal integration: lead judgement','',
 'Four GPT-6.1 Terra agents checked the numbers and proposed the results, methods and narrative updates. The lead reviewed every proposal before changing the thesis. Original CSV files were imported unchanged; all scope rows are excluded from the analysis.','',
 '| Proposal | Decision | Reason |','|---|---|---|']
for j in newjudgements:lines.append(f'| {j["id"]} | {j["decision"]} | {j["lead_reason"]} |')
lines+=['','## Pending original images','','The seven thermal screenshots are visible in chat, and their region maxima have been transcribed and independently checked. Their original image files are not available in the workspace. They have been requested so the actual screenshots can be embedded. No replacement thermal images have been generated. The current source contains the measured-data table and derived plot.']
(r/'judgement.md').write_text('\n'.join(lines)+'\n')
print(dict(counts));print('Edited',sum((r/'before'/n).exists() for n in replacements),'files and added the V2 results subsection.')
