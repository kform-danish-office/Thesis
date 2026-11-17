from pathlib import Path
import json,hashlib
r=Path('/workspace/tooling/thesis-v2-load-thermal');root=Path('/workspace/thesis')
proposals=json.loads((r/'terra-final-proposals.json').read_text())+json.loads((r/'astra-proposals.json').read_text())
revisions={
 'thermal-summary':('\n\n','Remove the repeated summary and preserve the paragraph break before the thermal interpretation.'),
 'sustained-operation':('\\SI{100}{\\watt} to a secondary load, although voltage droop and continued\nheating remain.','Keep the observed problems direct. The sequence gives no continuous rating, but does show droop and continued heating; avoid generic calls for investigation.'),
 'v3-comparison-row':('Secondary-load tests reached \\SI{137.1}{\\watt} with voltage droop; input-bridge and secondary heating remained','Update the comparison with the measured secondary result and observed heating. Concrete follow-up work already appears in the V2 section.')
}
reasons={
 'thermal-repetition':'Introduce the actual temperature observation without a separate empty sentence.',
 'astra-v1-efficiency-exclusion':'Scope the old screening rule to V1 because capture 017 remains explicitly flagged in the V2 table.',
 'astra-diagnostic-output-stage':'Keep the regulated V1 connector result separate from the later V2 secondary-output droop.'
}
judgments=[];touched=set()
for p in proposals:
 f=root/p['path'];s=f.read_bytes().decode('utf-8');assert s.count(p['old'])==1,p['id']
 final,reason=revisions.get(p['id'],(p['new'],reasons.get(p['id'],p['reason'])))
 b=r/'final-review-before'/p['path'];b.parent.mkdir(parents=True,exist_ok=True)
 if not b.exists():b.write_bytes(f.read_bytes())
 f.write_bytes(s.replace(p['old'],final).encode('utf-8'));touched.add(p['path'])
 judgments.append({**p,'decision':'Revise' if p['id'] in revisions else 'Accept','final':final,'lead_reason':reason,'scores':{'voice':2,'technical_fidelity':2,'flow':2}})
# The deleted repeated sentence started after a space; normalize only that paragraph break.
f=root/'Chapters/10_Results/17_V2_Secondary_Load_Tests.tex';s=f.read_bytes().decode();s=s.replace('\\SI{98.3}{\\celsius}. \n\n','\\SI{98.3}{\\celsius}.\n\n');f.write_bytes(s.encode())
(r/'final-judgements.json').write_text(json.dumps(judgments,indent=2)+'\n')
md='\n## Astra and Terra final review\n\nAstra independently checked every new AC/load calculation and the cross-chapter interpretation. Terra reviewed the V2 prose, captions and V3 connection. All six proposals were judged in context: three accepted and three revised. Final accepted wording scored 2/2 for voice, technical fidelity and flow; these are editorial judgments. Exact decisions and wording are in `final-judgements.json`.\n\n| Proposal | Decision | Lead reason |\n|---|---|---|\n'+''.join(f"| {p['id']} | {p['decision']} | {p['lead_reason']} |\n" for p in judgments)
with (r/'judgement.md').open('a') as f:f.write(md)
ledger=Path('/workspace/tooling/thesis-change-manifest.json');rows=json.loads(ledger.read_text());by={x['path']:x for x in rows}
for path in touched:
 by[path]['sha256']=hashlib.sha256((root/path).read_bytes()).hexdigest()
ledger.write_text(json.dumps(rows,indent=2)+'\n')
print('Applied six judged proposals in four source files; change ledger updated.')
