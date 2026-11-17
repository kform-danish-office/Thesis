from pathlib import Path
import hashlib,json,shutil
r=Path('/workspace/thesis'); out=Path('/workspace/tooling/v2-photos-95w'); e=r/'Data/measurements/v2_results/evidence'
a=Path('/tmp/codex-remote-attachments/01a16ff1-9f0d-7412-a0eb-85e7a0573057/ac7785f9-13c5-48c5-a917-807ce14d7ca5')
changed=[]; records=[]
for src,name,description in [('1-1000048184.jpg','v2_board_overview_original.jpg','V2 board overview'),('2-1000048178.jpg','v2_bridge_thermal_original.jpg','Thermal image; user identifies this as a 95 W run'),('3-1000048153.jpg','v2_thermal_setup_original.jpg','V2 bench and thermal-camera arrangement'),('4-1000048144.jpg','v2_board_detail_original.jpg','V2 board component-side detail')]:
 p=e/name
 if p.exists(): assert p.read_bytes()==(a/src).read_bytes()
 else: shutil.copy2(a/src,p); changed.append(p)
 records.append(dict(path=str(p.relative_to(r)),source_filename=src,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),description=description,modified=False))
p=e/'v2_photos_provenance.json'; p.write_text(json.dumps(dict(user_statement='V2 pictures. Thermal is from a 95w run',photos=records,reported_thermal_run_power_W=95,power_measurement_basis='Not specified: setpoint versus measured power not confirmed',limits='Board photos are not confirmed to show the exact thermal-run configuration.'),indent=2)+'\n'); changed.append(p)
p=e/'v2_bridge_thermal_provenance.json'; d=json.loads(p.read_text()); d['user_report']['earlier_load_setpoint_W']=d['user_report'].pop('load_setpoint_W'); d['user_report']['thermal_image_run_power_W']=95; d['user_report']['thermal_run_power_basis']='User correction; setpoint versus measured output unspecified'; d['power_correction']='Latest user identifies this thermal image as a 95 W run, superseding its previous association with a 100 W setpoint. Earlier temperature-rise reports are retained as historical observations; exact run association is unconfirmed.'; d['interpretation_limits'][0]='95 W is the user-reported thermal run power; independently measured delivered power and continuous rating are not established'; d['conditional_calculations']['scope']='Historical 100 W examples only; not calculations for this corrected 95 W image'; p.write_text(json.dumps(d,indent=2)+'\n'); changed.append(p)
p=r/'Chapters/10_Results/15_V2_Testing_Update.tex'; s=p.read_text(); s=s.replace('Earlier V2 thermal image supplied with the load-test observations.',r'V2 thermal image from a run reported as \SI{95}{\watt}.'); s=s.replace('\\begin{figure}[htbp]',r'''The thermal image in Figure~\ref{fig:v2-bridge-thermal-observation}
was subsequently identified as a \SI{95}{\watt} run. The basis of this
power value, whether a load setting or a measured output, was not specified.
The earlier \SI{100}{\watt} setpoint and temperature-rise account are
retained as separate reported observations; their exact association with
this image has not been confirmed.

\begin{figure}[htbp]''',1)
s+=r'''

\subsection{V2 Board and Test-Setup Photographs}

The V2 assembly and thermal-camera arrangement are documented in
Figure~\ref{fig:v2-board-test-photos}. The original photographs have been
retained. Their exact configuration relative to the \SI{95}{\watt}
thermal run has not been recorded.

\begin{figure}[p]
\centering
\includegraphics[height=0.34\textheight]{Data/measurements/v2_results/evidence/v2_board_overview_original.jpg}
\hspace{0.03\linewidth}
\includegraphics[height=0.34\textheight]{Data/measurements/v2_results/evidence/v2_thermal_setup_original.jpg}

\vspace{0.8em}
\includegraphics[width=0.86\linewidth]{Data/measurements/v2_results/evidence/v2_board_detail_original.jpg}
\caption{V2 assembly overview (upper left), thermal-camera bench arrangement (upper right), and component-side detail (lower). The photographs document the supplied hardware and setup; a common test configuration across all images has not been verified.}
\label{fig:v2-board-test-photos}
\end{figure}
\FloatBarrier
'''; p.write_text(s); changed.append(p)
p=r/'Data/project_records/V2_Testing_Update.txt'; p.write_text(p.read_text()+'\nLater photo clarification (verbatim):\nV2 pictures\nThermal is from a 95w run\n\nThis corrects the thermal image run-power attribution to 95 W. Whether this is a setpoint or measured output was not specified. See evidence/v2_photos_provenance.json for original photo hashes.\n'); changed.append(p)
p=r/'README.md'; b=p.read_bytes(); b+=b'\r\nLatest V2 photo clarification: the thermal image is from a user-reported 95 W run.\r\nIts earlier association with the 100 W setting is superseded; whether 95 W is\r\na setpoint or measured output is unspecified. Three original board/setup photos\r\nare included in Section 10.15 and retained with the V2 evidence.\r\n'; p.write_bytes(b); changed.append(p)
m=Path('/workspace/tooling/thesis-change-manifest.json'); rows=json.loads(m.read_text()); by={x['path']:x for x in rows}
for p in changed:
 key=str(p.relative_to(r)); row=by.get(key)
 if row is None: row={'path':key,'original_sha256':None}; rows.append(row)
 row['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
m.write_text(json.dumps(rows,indent=2)+'\n'); (out/'changed-files.json').write_text(json.dumps([str(p.relative_to(r)) for p in changed],indent=2)+'\n')
print('Updated',len(changed),'files; originals verified')
