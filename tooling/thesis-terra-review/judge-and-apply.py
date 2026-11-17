from pathlib import Path
import json,shutil
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-terra-review')
notes={
'opening-01':('Accept',[2,2,2],'The same paragraph already states 65 W and 100 W. Combining the 75 W milestone with its citation removes repetition while retaining all three power levels in context.'),
'opening-02':('Accept',[2,2,2],'AP-05 already requires a temperature history and defined-duration stability run. The additional statement about what a photograph cannot show adds no test requirement.'),
'circuit-01':('Accept',[2,2,2],'The caption already identifies the circuit blocks and revision. The sentence about named nets is generic and provides no useful circuit explanation.'),
'circuit-02':('Accept',[2,2,2],'The missing installed-inductance measurement explains the estimate. The missing rework log is an unnecessary administrative aside here.'),
'circuit-03':('Revise',[2,1,1],'Measurements are made on hardware, while V3 is still a layout. State that assembly and testing are next; do not imply the layout is ready for measurement.'),
'circuit-04':('Accept',[2,2,2],'The caption now describes the two copper layers and their orientation directly. The adjacent text already describes the testing changes.'),
'control-001':('Accept',[2,2,2],'The first paragraph already identifies surface hotspots. The replacement links those locations to longer temperature runs and retains the missing setup information.'),
'results-01':('Accept',[2,2,2],'The caption still names the plotted quantities as initial estimates. The surrounding paragraphs retain acquisition/power-path uncertainty and explain the need for intermediate-stage readings.'),
'results-02':('Revise',[2,1,2],'The proposal makes recovery of old measurements a prerequisite for repeating the test. The existing text requires the hardware and settings for the repeat; new measurements are collected during that repeat.'),
'results-03':('Accept',[2,2,2],'The paragraph makes no claim that loss fell. The prototype table still reports persistent bridge heating, and the next sentence requires comparable power, thermal conditions and output hardware.'),
'results-04':('Accept',[2,2,2],'The preceding sentence already states that original waveform amplitudes and offsets were retained. Deleting the defensive repetition does not change the processing description.')}
judgements=[]
for assignment in ['opening','circuit','control','results']:
 for p in json.loads((r/f'proposals/{assignment}.json').read_text()):
  decision,scores,why=notes[p['id']];final=p['new']
  if p['id']=='circuit-03':final='The operating prototypes retained the supplied magnetics; replacement planar parts were not installed within the project time. The smaller V3 layout still needs to be built and tested.'
  if p['id']=='results-02':final='Repeating the reported \\SI{85}{\\watt} V2 point requires its original\nhardware, firmware, and settings.'
  judgements.append({**p,'assignment':assignment,'decision':decision,'proposed_scores':dict(zip(['voice','technical_fidelity','flow'],scores)),'lead_reason':why,'final_new':final,'final_scores':{'voice':2,'technical_fidelity':2,'flow':2}})
(r/'judgements.json').write_text(json.dumps(judgements,indent=2)+'\n')
lines=['# Lead judgement of the Terra prose review','','Four GPT-6.1 Terra agents reviewed 162 authored TeX files. Every file in the assigned scope appears in the review inventories. They made 11 proposals: 9 accepted and 2 rewritten by the lead. No proposal was applied without this review. Good existing passages, including the introduction, were retained.','','Scores are editorial judgements on voice, technical fidelity and flow, each out of 2. Any factual failure blocks direct acceptance. Both revised proposals were rechecked after the lead rewrote them.','','| Proposal | Scope | Decision | Proposed score V/T/F | Reason |','|---|---|---|---|---|']
for j in judgements:
 s=j['proposed_scores'];lines.append(f"| {j['id']} | {j['assignment']} | {j['decision']} | {s['voice']}/{s['technical_fidelity']}/{s['flow']} | {j['lead_reason']} |")
lines+=['','## Lead rewrites','']
for j in judgements:
 if j['decision']=='Revise':lines += [f"### {j['id']}",'','Proposed:', '', '> '+j['new'].replace('\n',' '),'','Applied:', '', '> '+j['final_new'].replace('\n',' '),'',j['lead_reason'],'']
lines+=['## Agent judgement','','- Opening: both proposals accepted; preserved the original framing and did not invent a larger rewrite. The inventory covers 36 files; the initial chat summary incorrectly said 37, which the lead corrected from the file list.','- Circuit: three accepted; one rewritten to keep the unbuilt V3 status explicit. Good caption and attribution edits; the physical object of a proposed measurement needed more care.','- Control: one accepted; correctly kept the detailed firmware behavior and local limits rather than simplifying away technical content.','- Results: three accepted; one rewritten because the proposed prerequisite for a repeat test was stronger than the original. Redundant qualifications were removed without promoting estimates into measurements.','','The checklist is `/workspace/tooling/thesis-agent-voice-checklist.md`. Assignment instructions and original agent proposals are retained in this directory. Source integrity, full compilation and PDF checks follow application.']
(r/'judgement.md').write_text('\n'.join(lines)+'\n')
for j in judgements:
 p=root/j['path'];b=p.read_bytes();s=b.decode();assert s.count(j['old'])==1,j['id'];backup=r/'before'/j['path'];backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():backup.write_bytes(b)
 p.write_bytes(s.replace(j['old'],j['final_new']).encode())
print('Applied 9 accepted proposals and 2 lead rewrites in 10 files.')
