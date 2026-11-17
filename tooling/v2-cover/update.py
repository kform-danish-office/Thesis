from pathlib import Path
import json,hashlib
r=Path('/workspace/thesis'); changed=[]
p=r/'Frontmatter/Frontpage.tex'; s=p.read_text().replace('frontpage_project_prototype.png','frontpage_v2_right_cleaned.png').replace('yshift=-2.9mm','yshift=9mm').replace('height=18.9cm','height=16.5cm'); p.write_text(s); changed.append(p)
p=r/'Frontmatter/Copyright.tex'; b=p.read_bytes(); b=b.replace(b"Author's photograph of the assembled laboratory prototype used during final testing.",b"AI-assisted edited illustration of the right-hand V2 prototype, based on the author's photograph. Fine details may differ from the original."); p.write_bytes(b); changed.append(p)
p=r/'Pictures/Thesis/frontpage_v2_right_cleaned.png'; changed.append(p)
p=r/'Pictures/Thesis/frontpage_v2_right_cleaned_provenance.json'; p.write_text(json.dumps({'type':'AI-assisted cover illustration, not technical evidence','tool':'built-in image_gen','original':'Data/measurements/v2_results/evidence/v2_board_overview_original.jpg','subject':'Right-hand V2 board with amber tape','limitations':'Generated cleanup redraws fine markings and circuitry. Original evidence remains unchanged. Requested transparent background was rendered as a green photographic background.'},indent=2)+'\n'); changed.append(p)
m=Path('/workspace/tooling/thesis-change-manifest.json'); rows=json.loads(m.read_text()); by={x['path']:x for x in rows}
original=json.loads(Path('/workspace/tooling/thesis-source-manifest.json').read_text())
for p in changed:
 key=str(p.relative_to(r)); row=by.get(key)
 if row is None:
  old=next((x.get('sha256') for x in original if x.get('path')==key),None) if isinstance(original,list) else None
  row={'path':key,'original_sha256':old}; rows.append(row)
 row['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
m.write_text(json.dumps(rows,indent=2)+'\n')
