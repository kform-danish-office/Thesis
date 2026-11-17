from pathlib import Path
import hashlib,json,re,zipfile
root=Path('/workspace');out=root/'local-handoff'
cacheparts={'.git','node_modules','__pycache__','.pio','.platformio','.venv','venv','.next','.cache','.vercel'}
blockedtools={'apt','arduino-data','arduino-downloads','arduino-user','bin','downloads','npm-cache','tex-packages','xdg-cache','xdg-data','tex-smoke'}
reviewskip={'before','verified-downloads','page-previews','autocal-originals','magnetizing-revision-originals','ui-originals','final-review-before'}
secret=re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
files=[];excluded=[]
for folder in ['thesis','working-source','skills','tooling','source-archives']:
 for p in (root/folder).rglob('*'):
  if not p.is_file() or p.is_symlink():continue
  rel=p.relative_to(root);parts=rel.parts
  if any(x in cacheparts for x in parts):continue
  if p.name.startswith('.env') and p.name not in {'.env.example','.env.sample','.env.template'}:excluded.append(str(rel));continue
  if p.name in {'hosts.yml','.npmrc','.netrc','credentials','credentials.json','id_rsa','id_ed25519'}:excluded.append(str(rel));continue
  if folder=='tooling':
   if len(parts)>1 and parts[1] in blockedtools:continue
   if any(x in reviewskip for x in parts):continue
   if p.suffix.lower() in {'.zip','.pdf','.png','.jpg','.jpeg','.webp','.exe','.deb','.tar','.gz','.xz','.elf','.o','.a','.so'}:continue
  data=p.read_bytes()
  if secret.search(data):excluded.append(str(rel));continue
  if p.suffix.lower()=='.zip':
   with zipfile.ZipFile(p) as z:
    if any(secret.search(z.read(i)) for i in z.infolist() if not i.is_dir() and i.file_size<15000000):excluded.append(str(rel));continue
  files.append((p,str(rel)))
for p in [root/'AGENTS.md']:
 if p.exists():files.append((p,p.name))
readme='''# Local project handoff

Extract this archive into a new folder. Current work is in thesis/ and working-source/. Imported user skills are in skills/. Original approved source archives are in source-archives/. Tooling scripts and review notes are in tooling/; downloaded toolchains, caches, dependency folders, credentials and redundant compiled review PDFs are omitted.

Do not extract over an existing local project without comparing it first. The selected GitHub main checkout was not changed by this export.

## Latest V2 work

The completed V2 secondary-output load/thermal section, table, performance plot and seven thermal images are included in thesis/ and in Thesis_V1_V2_V3.pdf. The source retains all seven CSV captures and eight original thermal JPEG files (the two Capture 022 copies are byte-identical). The latest full-thesis prose pass was directed by Astra with five GPT-6.1 Terra reviewers. The lead applied the judged rewrites, removed reader-facing file/worksheet bookkeeping and checked the complete PDF. Current proposals, section coverage, judgments and validation records are in tooling/thesis-pdf-prose/. Earlier V2 data checks remain in tooling/thesis-v2-load-thermal/.

Only AC-supply and electronic-load rows from the new CSVs are used; their scope rows are excluded. Historical V1 oscilloscope results are retained. R3 covers the input bridge and R1 the secondary area. Calculated secondary power reaches 137.08 W at 13.69 V and 10.01 A, with voltage droop. No point reached thermal equilibrium. Capture 017 has inconsistent AC power/current/voltage readings, flagged in the table; the original readings are preserved.

Read tooling/thesis-voice-guide.md and tooling/thesis-agent-voice-checklist.md. Keep the author's practical engineering voice, V2 colour schematics and current figure sequence. The project target remains 100 W continuous, with a 65 W minimum; the new transient secondary result is not a continuous USB-C rating.

## Local tools

Install XeLaTeX, latexmk and PDF tools (manual bibliography, no Biber), Python with matplotlib and PyMuPDF, Node/npm for the web app, and Arduino CLI with STM32 core 2.8.1 for firmware. See tooling/setup-report.md and the build/test scripts for exact prior versions/commands. Reinstall web dependencies from its package lock file; node_modules is omitted.

The cloud build script uses absolute /workspace paths and a bundled TeX package path. Adapt those paths locally. Its main command is:

    latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex

Create mirrored build subdirectories for included chapter auxiliaries if necessary, as done in tooling/build-thesis.sh. Validate the full thesis, references and appendices and inspect the new table/plot/image pages. No hardware settings should be changed for this handoff.

This ZIP is the current local-work handoff. GitHub's automatic source-code ZIP remains the older main checkout.
'''
(out/'LOCAL_START.md').write_text(readme)
files.append((out/'LOCAL_START.md','LOCAL_START.md'))
pdf=root/'thesis-build/main.pdf'
if pdf.exists():files.append((pdf,'Thesis_V1_V2_V3.pdf'))
manifest=[{'path':name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p,name in sorted(files,key=lambda x:x[1])]
(out/'CONTENTS_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');files.append((out/'CONTENTS_SHA256.json','CONTENTS_SHA256.json'))
zpath=out/'Thesis_Local_Handoff.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p,name in files:z.write(p,name)
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for item in manifest:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
sha=hashlib.sha256(zpath.read_bytes()).hexdigest();(out/'LOCAL_HANDOFF_SHA256.txt').write_text(sha+'  '+zpath.name+'\n')
(out/'package-report.json').write_text(json.dumps({'files':len(files),'bytes':zpath.stat().st_size,'sha256':sha,'excluded_sensitive_files':excluded},indent=2)+'\n')
print(json.dumps({'files':len(files),'bytes':zpath.stat().st_size,'sha256':sha,'excluded_sensitive_files':excluded},indent=2))
