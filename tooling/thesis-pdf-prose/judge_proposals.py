import json,re,collections
from pathlib import Path
out=Path('/workspace/tooling/thesis-pdf-prose'); root=Path('/workspace/thesis')
names=['terra-front-ch1-6','terra-ch7-9','terra-ch10-12','terra-backmatter-tables','terra-cross-section']
items=[x for n in names for x in json.loads((out/(n+'.json')).read_text())]
for i,c in enumerate(json.loads((out/'terra-backmatter-table-cells.json').read_text()),1):
 if not c.get('merged_into'):
  items.append({'id':f'back-cell-{i:03d}','path':c['path'],'old':c['old_cell'],'new':c['new_cell'],'reason':'Remove spreadsheet row number from the PDF while retaining its test identifier.','facts_preserved':['Test identifier and every numerical measurement cell unchanged.'],'checklist':['PDF-only reader','technical fidelity','meaningful table labels']})
rev={
'front-01':("A planar inductor and transformer from earlier DTU work by Bima Nugraha Sanusi and the DTU Power Electronics group were used in this converter. The components were measured by M\\'ani Gautason.\n",'Retain earlier-work attribution without turning package identification into a stronger sole-design claim.'),
'front-02':(None,'Retain explicit two-circuit count while removing filenames.'),
'front-06':(None,'Keep assembly identification as well as fitted components; these are test conditions, not archival clutter.'),
'front-08':("AP-08 & Determine whether V3 is ready for testing, identify the tests that can be completed, and state the remaining work. If V3 is not ready, use the completed V2 tests with matched operating conditions as the hardware results.\\\\\n",'Preserve conditional V2 fallback and scope of feasible V3 tests; original proposal shortened substantive requirements.'),
'ch79-04':("Firmware version, calibration, thresholds, loaded/no-load settings, and timing affect the control response and should be recorded with each test. Appendix~\\ref{app:firmware} gives the command reference.",'Preserve firmware identification as a relevant test variable while removing contradictory-note administration and generic results navigation.'),
'ch79-06':(None,'Preserve firmware version and controller target as test variables without requiring export-file inventory.'),
'10-03':("\\caption{C2 waveforms showing burst overviews (00006 and 00008) and carrier detail (00007 and 00010).}",'Place incomplete setup attribution once in the adjacent frequency discussion, not again in the caption.'),
'10-04':("approximately \\SI{1.03}{\\mega\\hertz}. This is the frequency measured in the C2\r\nwaveforms; the configured timer frequency and test conditions were not recorded.",'Keep waveform-derived frequency separate from timer configuration, with the missing setup stated locally.'),
'10-06':("After the tank was modified and the software dead time was set to about\n\\SI{60}{\\nano\\second}, half-bridge heating decreased. Turn-on voltage\nand current measurements are still needed to check ZVS.",'Use direct authorial test wording requested by root; retain approximate software setting and unverified ZVS.'),
'10-05':("PR-09 & Link results to configuration & Test identifiers and instrument readings & Setup details incomplete\\\\",'Avoid inventing full identification of hardware/test conditions from the original archive linkage statement.'),
'12-01':(None,'Preserve completed software-check status while removing archive inventory.'),
'10-10':("Loaded and load-removal tests show the response of the combined controller;\r\nthe contributions of individual changes were not measured separately. The\r\nrequested \\texttt{MAXRATE} period is \\SI{20}{\\micro\\second}; the achieved\r\nperiod and jitter have not been measured.",'Keep the local attribution limit: combined response must not imply individually measured gains.'),
'back-061':("Serve the application locally or prepare a static build using an explicit list of application files.",'Retain the explicit allowlist behavior, a software design fact, while removing directory narration.')
}
reject={'front-07':'The revised proposal now preserves DRC and release status, but check the design-rule checks is less direct than the existing wording; retain the original substantive design requirements.', 'ch79-14':'The original three sentences already explain tank effects, fitted-inductor context and the needed measurement. The new compound sentence is harder to read and adds no useful content.'}
rev.update({
'front-16':("The supplied analysis and LTspice circuits allow circuit relationships and approximate component values to be checked. Chapter~\\ref{ch:simulation} describes the calculations and the changes needed to model the final board and firmware.\r\n",'Preserve the original scope of what can be checked; do not turn conditional capability into a newly claimed completed validation.'),
'10-12':(None,'Correct 39.7 degrees C to cursor temperature: the reference value in the table is 24.9 degrees C.'),
'10-13':(None,'Name V1.0 so its 79.89 W maximum cannot be confused with later 137.1 W secondary-output tests.'),
'11-03':(None,'Keep the high-power electrical/efficiency result explicitly attached to V1.0.'),
'11-04':(None,'Name the secondary bulk supply and USB-C PD stage instead of the ambiguous both output stages.')
})
approved=[];judgments=[];spans=collections.defaultdict(list)
for p in items:
 s=(root/p['path']).read_bytes().decode('utf-8'); assert s.count(p['old'])==1,(p['id'],s.count(p['old']))
 pos=s.index(p['old']);
 for a,b,i in spans[p['path']]: assert pos+len(p['old'])<=a or pos>=b,(p['id'],i)
 spans[p['path']].append((pos,pos+len(p['old']),p['id']))
 q=dict(p);status='Accept';why=p['reason'];scores={'voice':2,'technical_fidelity':2,'flow':2}
 if p['id'] in reject:
  status='Reject';why=reject[p['id']];scores={'voice':1,'technical_fidelity':2,'flow':1}
 elif p['id'] in rev:
  status='Revise';new,why=rev[p['id']]
  if new is not None:q['new']=new
  elif p['id']=='front-02':q['new']=q['new'].replace('The supplied LTspice circuits','The two supplied LTspice circuits')
  elif p['id']=='front-06':q['new']=q['new'].replace('State the fitted parts','State the assembly, fitted parts')
  elif p['id']=='ch79-06':q['new']=q['new'].replace('controller settings and mode','controller target, firmware version, settings and mode')
  elif p['id']=='10-12':q['new']=q['new'].replace('reference marker','cursor')
  elif p['id']=='10-13':q['new']=q['new'].replace('The highest calculated output was','The highest calculated V1.0 output was')
  elif p['id']=='11-03':q['new']=q['new'].replace('high-power measurements gave','V1.0 high-power measurements gave')
  elif p['id']=='11-04':q['new']=q['new'].replace('both output stages and heating','the secondary bulk supply, USB-C PD stage, and heating')
  elif p['id']=='12-01':q['new']=q['new'] if 'passed software checks' in q['new'] else q['new'].replace('The four-layer circuit and layout integrate these functions on V2.','The four-layer circuit and layout integrate these functions on V2.\r\nThe firmware and supporting software passed software checks.')
  q['reason']=p['reason']+' Lead revision: '+why
 if status!='Reject': approved.append(q)
 judgments.append({'id':p['id'],'path':p['path'],'judgment':status,'reason':why,'scores':scores,'proposed_new':p['new'],'final_new':q['new'] if status!='Reject' else None})
# Simulate replacements and check internal source/data paths remain.
for path in spans:
 s=(root/path).read_bytes().decode('utf-8'); t=s
 for p in approved:
  if p['path']==path:t=t.replace(p['old'],p['new'],1)
 pattern=r'\\(?:input|include|includegraphics|lstinputlisting)(?:\[[^\]]*\])?\{[^}]*\}'
 assert re.findall(pattern,s)==re.findall(pattern,t),('internal path changed',path)
(out/'astra-approved.json').write_text(json.dumps(approved,ensure_ascii=False,indent=2)+'\n')
(out/'astra-judgements.json').write_text(json.dumps(judgments,ensure_ascii=False,indent=2)+'\n')
print('proposals',len(items),'approved',len(approved),'judgments',dict(collections.Counter(x['judgment'] for x in judgments)),'files',len(spans))
