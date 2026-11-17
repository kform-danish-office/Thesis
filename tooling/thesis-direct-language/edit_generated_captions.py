from pathlib import Path
import ast,json
root=Path('/workspace/thesis')
base=root/'Data/measurements/processed_rewrite'
caption_map={
'Completed DC operating-point records. Voltages and input power are logged values; output power and error are calculated. The original VBUS pp field is retained without correction. All rows use the logged 240 V, 50 Hz input condition. Source: \\texttt{Load Data} in \\sourcefile{Thesis_USB_PDO_3A_Limited_Test_Plan.xlsx}.':
'DC operating-point measurements at 240 V, 50 Hz, with calculated output power and voltage error. VBUS pp keeps the original workbook label. Source: \\texttt{Load Data} in \\sourcefile{Thesis_USB_PDO_3A_Limited_Test_Plan.xlsx}.',
'Complete AC-coupled detail records. Values reproduce the workbook fields. Several entries are ranges of averaged-voltage statistics rather than instantaneous waveform peak-to-peak ripple. CH2 and CH3 cannot provide absolute DC voltage.':
'AC-coupled measurements. Several workbook values describe the spread of average-voltage readings, not instantaneous peak-to-peak ripple. CH2 and CH3 do not show absolute DC voltage.',
'Screening calculations from eleven eligible row-level records. Source rows refer to the original \\texttt{Load Data} sheet. Results are rounded to the precision justified for comparison.':
'Initial efficiency estimates from eleven measurements. Row numbers refer to the original \\texttt{Load Data} sheet.',
'Logged power-quality results. PF and current THD may originate from different instruments or averaging intervals. The associated 3.9 A record is retained for provenance but excluded from trend interpretation.':
'Power factor and current THD from the instrument readings. The instruments or averaging intervals can differ. The 3.9 A entry is an associated record and is not used for the load trend.',
'Input-current harmonic percentages transcribed and visually checked against the three retained ITECH current tables. Order 1 is the reference fundamental. The 4.7 A point is an AC-coupled output capture.':
'Input-current harmonics from the three ITECH tables. Order 1 is the fundamental. The 4.7 A entry uses an AC-coupled output capture.',
'Readings from all ten labeled thermal screenshots at emissivity 0.95. The lower reference marker is not a documented ambient-temperature measurement.':
'Temperature readings from ten thermal images, using emissivity 0.95. The lower reference marker was not confirmed as ambient temperature.',
'Original waveform exports included with the rewritten results. Files are copied without changing samples; SHA-256 digests and complete acquisition metadata appear in \\sourcefile{raw_waveform_index.csv}.':
'Waveform files, sample counts, and intervals. SHA-256 checksums and acquisition details are listed in \\sourcefile{raw_waveform_index.csv}.',
'Recorded numerical fields for completed transient rows. Acquisition-wide pp and averages are not the overshoot relative to the pre-step output; recovery time is unavailable. The 5 V and 20 V removal screenshots have no numerical worksheet row.':
'Load-removal measurements from the workbook. Averages and pp span the whole capture and do not give the voltage rise from the pre-step level. Recovery time is not available. The 5 V and 20 V screenshots have no numerical worksheet row.',
'Status, firmware attribution and efficiency-selection rule for every completed workbook record. A missing firmware entry is not assigned to the final release. AC-statistic rows are excluded from DC power calculation.':
'Test status, firmware version, and use in the calculations. A dash means the firmware was not recorded. AC-coupled statistics are not used to calculate DC power.'
}
header_map={'Evidence / calculation treatment':'Use in calculations','Power-quality provenance':'Instrument / record'}
log=[]
for p in sorted(base.glob('*.tex')):
    data=p.read_bytes();count=0
    for old,new in caption_map.items():
        a=old.encode();b=new.encode()
        if a in data:
            assert data.count(a)==1,(p.name,old);data=data.replace(a,b);log.append({'path':p.relative_to(root).as_posix(),'kind':'caption','before':old,'after':new});count+=1
    for old,new in header_map.items():
        a=old.encode();b=new.encode()
        if a in data:
            n=data.count(a);assert n==2,(p.name,n);data=data.replace(a,b);log.append({'path':p.relative_to(root).as_posix(),'kind':'header','before':old,'after':new,'count':n});count+=1
    if count:p.write_bytes(data)
p=root/'Data/analysis/rebuild_results.py';data=p.read_bytes();text=data.decode();tree=ast.parse(text)
all_map={**caption_map,**header_map};replaced=[]
for node in ast.walk(tree):
    if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value in all_map:
        segment=ast.get_source_segment(text,node)
        assert segment and data.count(segment.encode())==1,(node.value,segment)
        old=node.value;new=all_map[old];data=data.replace(segment.encode(),repr(new).encode());replaced.append({'before':old,'after':new})
assert {x['before'] for x in replaced}==set(all_map),(set(all_map)-{x['before'] for x in replaced})
p.write_bytes(data)
Path('/workspace/tooling/thesis-direct-language/generated-caption-edits.json').write_text(json.dumps({'table_edits':log,'generator_path':p.relative_to(root).as_posix(),'generator_string_replacements':replaced},indent=2)+'\n')
print('Table-caption/header files changed:',len({x['path'] for x in log}),'generator presentation strings:',len(replaced))
