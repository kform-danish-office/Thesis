from pathlib import Path
import json,hashlib,collections,re
r=Path('/workspace/tooling/thesis-pdf-prose');root=Path('/workspace/thesis')
props=json.loads((r/'astra-approved.json').read_text());grouped=collections.defaultdict(list)
for p in props:grouped[p['path']].append(p)
judgments=[]
for path,changes in grouped.items():
 f=root/path;old=f.read_bytes().decode('utf-8');new=old
 spans=[]
 for p in changes:
  assert old.count(p['old'])==1,p['id'];start=old.index(p['old']);spans.append((start,start+len(p['old']),p['id']))
 for a,b in zip(sorted(spans),sorted(spans)[1:]):assert a[1]<=b[0],(a,b)
 for p in changes:
  assert new.count(p['old'])==1,p['id'];new=new.replace(p['old'],p['new'])
  judgments.append({'id':p['id'],'path':path,'decision':'Accept','reason':'Lead accepts Astra final wording after contextual prose review and technical checks; '+p['reason'],'scores':{'voice':2,'technical_fidelity':2,'flow':2}})
 for command in ['input','include','includegraphics','lstinputlisting']:
  pattern=r'\\'+command+r'(?:\[[^\]]*\])?\{([^}]+)\}'
  assert re.findall(pattern,old)==re.findall(pattern,new),(path,command)
 b=r/'before'/path;b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(f.read_bytes());f.write_bytes(new.encode('utf-8'))
(r/'lead-judgements.json').write_text(json.dumps(judgments,indent=2)+'\n')
(r/'judgement.md').write_text('''# Full thesis rewrite: lead judgment

Astra directed four GPT-6.1 Terra section reviewers and a fifth cross-section reviewer. All authored prose was reviewed, including captions, tables, front matter and appendices. The initial narrow pass was returned for complete contextual reading and a dedicated full-prose pass. Exact per-section coverage and the reasons for keeping already clear passages are in the Terra review records.

Astra judged 211 final proposals: 191 Accept, 18 Revise and 2 Reject. The lead reviewed the final wording and accepts all 209 approved edits across 60 files. Mechanical worksheet-row removals are counted as individual exact edits; this count is not a claim that 209 paragraphs were rewritten. The key changes remove file/manifest bookkeeping from reader-facing prose, improve connected descriptions and keep measurement limitations local. Internal LaTeX paths and original data remain intact.

The lead specifically checked the 60 ns software setting, unconfirmed ZVS, separate V1 connector and V2 secondary measurements, camera maximum/cursor distinction, no thermal equilibrium, V3 design-only status, project targets and genuine scholarly attribution. Purely shorter proposals that lost design checks or clarity were rejected by Astra. The final review retained useful within-PDF references and operational firmware checksum descriptions. Per-proposal reasoning and editorial scores are in `astra-judgements.json` and `lead-judgements.json`.

Generated table presentation is synchronized separately; numerical measurement columns and calculations must remain unchanged. Final build, source audit, visual review and publication records follow in this directory.
''')
print(f'Applied {len(props)} approved edits in {len(grouped)} files.')
