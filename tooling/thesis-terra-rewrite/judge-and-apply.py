from pathlib import Path
import json, collections

root = Path('/workspace/thesis')
r = Path('/workspace/tooling/thesis-terra-rewrite')
# Scores are voice / technical fidelity / paragraph flow, each out of two.
decisions = {
'opening-01': ('Accept',[2,2,2],'Removes repeated V1 attribution while keeping the reported V2 point separate from the measured V1 result.'),
'opening-02': ('Accept',[2,2,2],'Connects the V2 tank change to series-inductor heating, as described in the testing section.'),
'opening-03': ('Accept',[2,2,2],'Explains the power path once, in circuit order, with the two regulators and PA1 feedback correctly assigned.'),
'opening-04': ('Accept',[2,2,2],'States the continuous-test conditions directly and gives the load-removal controls their physical purpose.'),
'opening-05': ('Revise',[2,2,1],'The proposed sentence can attach loaded/no-load operation to startup precharge as well as duty limits. Separate those functions.'),
'opening-06': ('Accept',[2,2,2],'Organizes hardware and firmware work by development stage and explains the tank-change trigger.'),
'opening-07': ('Accept',[2,2,2],'Separates the repeat test, later tank tests and volume comparison without dropping requirements.'),
'circuit-01': ('Accept',[2,2,2],'Links heat paths and thermal images to the longer temperature measurements needed for sustained operation.'),
'circuit-02': ('Accept',[2,2,2],'Keeps the V1 and V2 fitted-component distinction while removing a redundant explanatory aside.'),
'circuit-03': ('Accept',[2,2,2],'Combines repeated statements about the reported 85 W point into its test conditions and planned repeat.'),
'circuit-04': ('Revise',[1,1,2],'Some thermal behavior has already been observed. Describe the remaining checks without implying that no thermal measurements exist, and retain the pre-installation origin of the given values.'),
'circuit-05': ('Accept',[2,2,2],'Groups the available calculations and inputs before the switched-model and calibration work still needed.'),
'circuit-06': ('Revise',[2,1,2],'Waveform comparisons are planned model checks. Keep that prospective status instead of implying that bulk ripple and commutation have already been checked.'),
'circuit-07': ('Accept',[2,2,2],'Connects heat generation, transfer and removal to what the surface images show and the temperature histories needed.'),
'control-01': ('Accept',[2,2,2],'Explains DMA through the removed foreground wait, retaining the exact ADC sample setting.'),
'control-02': ('Reject',[2,2,1],'The original already explains the calibration search and browser interface clearly. The rearrangement adds little and does not justify another edit.'),
'control-03': ('Accept',[2,2,2],'Expands the ambiguous interval shorthand and distinguishes software diagnostics from measured jitter.'),
'control-04': ('Revise',[1,2,2],'The measurement list is useful, but PA10 should be identified by its burst-enable function in the rewritten sentence.'),
'control-06': ('Revise',[2,1,2],'Keep the original possibility of delayed duty adjustment; the prose should not imply a separately measured timing effect.'),
'control-07': ('Revise',[2,1,2],'Minimum scheduled burst duration does not guarantee complete physical carrier cycles. The baseline polling can time out; describe the intended reduction in partial cycles.'),
'control-08': ('Accept',[2,2,2],'Groups programming recovery and erase recovery by operation, preserving the remaining erase-interruption failure and output-OFF fallback.'),
'control-09': ('Revise',[1,1,1],'The proposed where-clause suggests selective error bars, whereas the source omits them. State the missing uncertainty inputs directly and retain the actual presentation choice.'),
'results-open': ('Accept',[2,2,2],'Maps each mean voltage to its error and removes a duplicate conclusion without changing values.'),
'results-v2-secondary': ('Accept',[2,2,2],'Separates the comparable output observation from the heating sequence and keeps the winding cause suspected.'),
'results-v3': ('Revise',[1,2,2],'Replace the vague ending about assessment with the concrete layout and build status. Keep the external USB-PD stage in the complete-supply comparison.'),
'results-summary-v3': ('Accept',[2,2,2],'Corrects the ambiguous grammar that could read as removal of secondary rectification. The layout-only status stays explicit.'),
'results-firmware-development': ('Revise',[2,1,2],'The source confirms bounded optional PA0 feed-forward in particular control branches. Use can cap rather than an unconditional duty relationship and name pins by function.'),
'results-failures': ('Revise',[2,2,1],'The problem-to-change sequence is stronger, but retain the original load-classification contribution and identify its PA2 role.'),
'results-contribution-firmware': ('Accept',[2,2,2],'Groups control features by operating role and explains why V2 needed timer and ADC remapping.'),
'results-lessons-hotspot': ('Revise',[1,2,2],'The causal sequence is useful. Replace remains suspect with a direct description of the possible restriction.'),
'results-summary-v2-target': ('Revise',[1,2,2],'The new conclusion still repeats a broad comparison disclaimer. State the V2 change and result directly, retain the missing temperature history beside the 95 W run, and make the repeat-test work concrete. Routine component model names are unnecessary here.'),
}
judgements = []
coverage = {}
for scope in ['opening','circuit','control','results']:
    proposals = json.loads((r/f'proposals/{scope}.json').read_text())
    files = json.loads((r/f'{scope}-files.json').read_text())
    report = (r/f'proposals/{scope}-review.md').read_text()
    assert all(p in report for p in files)
    coverage[scope] = {'model':'gpt-6.1-terra','reviewed_files':len(files),'proposal_count':len(proposals),'files':files,'missing_from_inventory':[]}
    for p in proposals:
        decision,score,reason = decisions[p['id']]
        new = p['new']
        if p['id']=='opening-05':
            new = new.replace('Startup precharge and separate burst-duty limits were used for loaded and no-load operation.', 'Startup precharge was implemented alongside separate burst-duty limits for loaded and no-load operation.')
        if p['id']=='circuit-04':
            new = r'The given electrical measurements were taken before installation and used in the converter calculations. Power was transferred through the installed magnetics during converter tests. The remaining checks on installed parameters, temperature, and isolation are listed in \Cref{tab:mag-verification-actions}.'
        if p['id']=='circuit-06':
            new = new.replace('This checks bulk ripple and commutation current as well as mean VBUS.', 'Both comparisons are needed to assess bulk ripple and commutation current as well as mean VBUS.')
        if p['id']=='control-04':
            new = new.replace('output rise and peak, PA10, inhibition', 'output rise and peak, the burst-enable signal (PA10), inhibition')
        if p['id']=='control-06':
            new = new.replace('other work, delaying opportunities to adjust duty.', 'other work, which could delay the next duty adjustment.')
        if p['id']=='control-07':
            new = new.replace('to avoid truncating individual carrier cycles', 'to reduce partial carrier cycles')
        if p['id']=='control-09':
            new = r'The setup information and repeated measurements needed for a numerical uncertainty budget are incomplete. Values are therefore kept at the workbook precision, and no error bars are given. Characterizing worst-case transients requires repeated events with a defined acceptance band; thermal equilibrium requires a temperature history, and jitter requires timing measurements. These limits apply throughout Chapter~\ref{ch:results}.'
        if p['id']=='results-v3':
            new = 'The V3 edge-card layout retained secondary rectification and removed the\nUSB-PD section, giving an estimated net volume reduction of approximately\n'+r'\SI{8}{\percent}.'+' External regulation and USB-PD remain necessary for a\ncomplete USB-C supply. Replacement planar magnetics were not installed,\nand the smaller layout still needs to be built and tested.'
        if p['id']=='results-firmware-development':
            new = new.replace('PA2 measures half-bridge current', 'The current-sense pin PA2 measures half-bridge current').replace('replaced by PA1 secondary-voltage regulation', 'replaced by secondary-voltage regulation using PA1').replace('Optional PA0 feed-forward caps\r\nPA10 duty as the sensed primary voltage rises.', 'Optional feed-forward from the primary-voltage input PA0 can cap\r\nthe burst-enable duty requested at PA10 as primary voltage rises.')
        if p['id']=='results-failures':
            start = new.index('Measurement review')
            new = 'The control changes addressed the problems found during bring-up. PA1\r\nvoltage regulation replaced the incorrect power feedback, with PA2 retained\r\nfor load classification. Complete-cycle scheduling addressed irregular\r\npulses, and no-load guarding limited charging after load removal. '+new[start:]
        if p['id']=='results-lessons-hotspot':
            new = new.replace('A possible\r\nsingle-via connection between layers remains suspect:', 'One possible\r\nrestriction is a single-via connection between layers:')
        if p['id']=='results-summary-v2-target':
            new = r'''V2 integrated the MCU, GaN stage, isolated sensing, and USB-C PD
circuit on a four-layer PCB, documented in \cref{sec:app-v2-oct27}.
The external series inductor was removed after excessive heating, and the
tank was changed to use transformer leakage with approximately
\SI{1.66}{\nano\farad}. Half-bridge heating decreased after the tank and
timing changes, while input-bridge heating persisted. The thermal image
shows surface heating during a \SI{95}{\watt} run; a temperature history
is still needed to assess continuous operation.

The revised plan retains \SI{100}{\watt} continuous as the target and
\SI{65}{\watt} continuous as the minimum \cite{projectOctoberPlan}.
Defined-duration tests with temperature histories are still needed at these
levels and at the earlier \SI{75}{\watt} milestone. The reported
approximately \SI{85}{\watt} V2 point should be repeated with the board,
firmware, settings, power readings, and temperatures recorded together.
This earlier V2 point is separate from the measured \SI{79.89}{\watt}
V1.0 result above.'''.replace('\n','\r\n')
        if p['id']=='results-firmware-development': new=new.replace('multiplying it by secondary voltage','multiplying its current indication by secondary voltage')
        if p['id']=='results-summary-v2-target': new=new.replace('separate from the measured ', 'separate from the calculated ')
        if decision=='Reject': new=p['old']
        # Match surrounding newline conventions and retain the original terminal CR.
        if p['old'].endswith('\r') and not new.endswith('\r'): new+='\r'
        judgements.append({**p,'assignment':scope,'decision':decision,'proposed_scores':dict(zip(['voice','technical_fidelity','flow'],score)),'lead_reason':reason,'final_new':new,'final_scores':{'voice':2,'technical_fidelity':2,'flow':2} if decision!='Reject' else None})

assert set(decisions)=={j['id'] for j in judgements}
counts = collections.Counter(j['decision'] for j in judgements)
(r/'coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
(r/'judgements.json').write_text(json.dumps(judgements,indent=2)+'\n')
# Validate every replacement before writing any source.
replacements = {}
for j in judgements:
    path = root/j['path']
    text = replacements.get(j['path'],path.read_bytes().decode())
    assert text.count(j['old'])==1,j['id']
    replacements[j['path']] = text.replace(j['old'],j['final_new'])
for name,text in replacements.items():
    path=root/name
    if text.encode()==path.read_bytes(): continue
    backup=r/'before'/name;backup.parent.mkdir(parents=True,exist_ok=True)
    assert not backup.exists(),name
    backup.write_bytes(path.read_bytes());path.write_bytes(text.encode())

lines=['# Lead judgement: second Terra rewrite','',f'Four GPT-6.1 Terra agents read 162 authored TeX files. The final proposals contain {len(judgements)} rewrites: {counts["Accept"]} accepted, {counts["Revise"]} rewritten by the lead, and {counts["Reject"]} rejected. Scores are editorial judgements, not a language metric. Each accepted final passage was checked for voice, technical fidelity and flow.','',
'The first pass was returned for deeper paragraph work. A punctuation-only thermal edit and a synonym-only results edit were withdrawn. The second pass connects design changes to their reasons and results, while preserving the original introduction and useful existing explanations.','',
'| Proposal | Decision | Proposed V/T/F | Lead judgement |','|---|---|---|---|']
for j in judgements:
    score='/'.join(str(v) for v in j['proposed_scores'].values())
    lines.append(f'| {j["id"]} | {j["decision"]} | {score} | {j["lead_reason"]} |')
lines+=['','## Lead rewrites','']
for j in judgements:
    if j['decision']=='Revise':
        lines += [f'### {j["id"]}', '', '> '+j['final_new'].replace('\r','').replace('\n',' '),'']
lines += ['## Technical checks','',
'The optional PA0 feed-forward relationship was checked against the baseline source at `Code/thesi_power_control_PWR_1_9_20.ino`: the bounded reference/primary-voltage scale is calculated near line 2444 and applied in the relevant control branches near line 2704. Carrier-boundary polling can time out near lines 1131–1161; the rewrite therefore describes minimum burst duration as reducing partial cycles, not guaranteeing measured full cycles.','',
'The [voice checklist](/workspace/tooling/thesis-agent-voice-checklist.md), [assignment](/workspace/tooling/thesis-terra-rewrite/AGENT_TASK.md), complete inventories and original agent proposals are retained. Build and source verification results will be added after compilation.']
(r/'judgement.md').write_text('\n'.join(lines)+'\n')
print(dict(counts));print('Changed files:',sum((r/'before'/n).exists() for n in replacements))
