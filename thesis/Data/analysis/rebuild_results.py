"""Rebuild thesis results from original records; source workbooks remain unchanged.

Run with the bundled Python runtime. All exported CSV columns retain source row
numbers. Power and voltage-error columns are independently recomputed, not read
from workbook formula caches. Raw waveforms are copied byte-for-byte and plotted
without filtering, amplitude normalization, or forcing a target power.
"""
from pathlib import Path
import csv, hashlib, json, math, os, re, shutil, sys
from inspect_measurements import read_xlsx

THESIS=Path(__file__).resolve().parents[2]
ROOT=THESIS
OUT=THESIS/'Data/measurements/processed_rewrite'
FIG=THESIS/'Pictures/Thesis/10_Results/Rebuilt'
OUT.mkdir(parents=True,exist_ok=True); FIG.mkdir(parents=True,exist_ok=True)
# Use an ordinary environment containing numpy and matplotlib.
# This optional fallback supports the original local workspace runtime.
legacy=THESIS.parents[1]/'tmp/efficiency_graph_20260804/pydeps'
if legacy.is_dir(): sys.path.insert(0,str(legacy))
os.environ['MPLCONFIGDIR']=str(Path(__file__).parent/'.mplconfig')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

BOOK=THESIS/'Data/measurements/Thesis_USB_PDO_3A_Limited_Test_Plan.xlsx'
source=read_xlsx(BOOK)['Load Data']
records=[]
for item in source:
    n=item['row']; c=item['cells']
    if n<5: continue
    g=lambda col:c.get(f'{col}{n}')
    note=str(g('Y') or '')
    coupling='AC detail' if 'AC-' in str(g('A')) else ('transient' if 'TO-NL' in str(g('A')) else 'DC')
    ithd=g('T') if isinstance(g('T'),(int,float)) else None
    match=re.search(r'iTHD\s+([\d.]+)%',str(g('T') or '')+'; '+note,re.I)
    if match: ithd=float(match.group(1))
    ihigh=any(x in str(g('A')) for x in ['PDO15-30W-2A-001','PDO15-45W-3A-001'])
    copied=g('A')=='PDO20-80W-001'
    status=g('W')
    actual=status in ('Measured','Recorded','Captured') and isinstance(g('K'),(int,float)) and coupling=='DC' and isinstance(g('O'),(int,float))
    eligible=actual and g('O')>0 and isinstance(g('P'),(int,float)) and not ihigh and not copied
    pout=g('K')*g('O') if actual else None
    rec={'test_id':g('A'),'source_workbook':BOOK.name,'source_sheet':'Load Data','source_row':n,'status':status,
        'firmware':g('D'),'input_condition':g('E'),'pdo_v':g('G'),'load_condition':g('H'),'iout_a':g('O'),
        'vbus_avg_v':g('K') if coupling=='DC' else None,'vbus_logged_pp_or_detail_v':g('L'),
        'secondary_avg_v':g('M') if coupling=='DC' else None,'secondary_logged_pp_or_detail_v':g('N'),
        'pin_w':g('P'),'pf':g('S'),'ithd_percent':ithd,'coupling':coupling,
        'pout_w_derived':pout,'voltage_error_percent_derived':100*(g('K')/g('G')-1) if actual else None,
        'efficiency_screening_included':eligible,'efficiency_percent_derived':100*pout/g('P') if eligible else None,
        'loss_w_derived':g('P')-pout if eligible else None,
        'exclusion':('planned row' if status=='Planned' else 'AC-coupled: no DC output' if coupling=='AC detail' else 'transient' if coupling=='transient' else 'instrument power disagreement' if ihigh else 'associated input-power record' if copied else 'no nonzero measured DC output/input power' if not eligible else ''),
        'notes':note}
    records.append(rec)

def write_csv(name, rows):
    if not rows:return
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

write_csv('all_workbook_rows.csv',records)
dc=[r for r in records if r['coupling']=='DC' and r['status']!='Planned' and r['pout_w_derived'] is not None]
eff=[r for r in records if r['efficiency_screening_included']]
ac=[r for r in records if r['coupling']=='AC detail']
pq=[r for r in records if r['pin_w'] is not None and r['status']!='Planned' and r['coupling']!='transient']
write_csv('dc_operating_points.csv',dc);write_csv('efficiency_screening.csv',eff);write_csv('ac_detail_statistics.csv',ac);write_csv('power_quality_logged.csv',pq)
high=[r for r in eff if r['pdo_v']==20 and r['iout_a']>=3.7]
headline={'source_workbook':str(BOOK.relative_to(ROOT)),'source_sheet':'Load Data','dc_point_count':len(dc),'screening_efficiency_point_count':len(eff),
    'highest_verified_dc_output':max(dc,key=lambda r:r['pout_w_derived']),
    'high_power_points':high,
    'highest_screening_efficiency':max(eff,key=lambda r:r['efficiency_percent_derived']),
    'maximum_loaded_absolute_voltage_error_percent':max(abs(r['voltage_error_percent_derived']) for r in dc if r['iout_a']>0),
    'limits':['Screening efficiency is computed from row-level records; channel simultaneity, auxiliary power, calibration and uncertainty are unresolved.',
              'Power-factor and current-THD entries may come from different instruments; do not infer displacement factor from their combination.',
              'AC-detail entries are often ranges of averaged-voltage statistics, not instantaneous waveform peak-to-peak ripple.',
              'The 4.7 A high-load record has no DC-coupled output voltage and cannot establish 94 W or an efficiency value.',
              'No stabilized thermal endurance run establishes a continuous 75 W rating.']}
(OUT/'headline_metrics.json').write_text(json.dumps(headline,indent=2),encoding='utf-8')

STYLE={5:('#0072B2','o'),9:('#009E73','s'),15:('#E69F00','D'),20:('#CC79A7','^')}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9.5,'axes.titlesize':10,
    'legend.fontsize':8.5,'xtick.labelsize':8,'ytick.labelsize':8,'pdf.fonttype':42,'svg.fonttype':'none',
    'axes.spines.top':False,'axes.spines.right':False,'axes.axisbelow':True,'savefig.facecolor':'white'})
manifest=[]
def finish(fig,name,sources,description):
    fig.savefig(FIG/(name+'.pdf'),bbox_inches='tight')
    fig.savefig(FIG/(name+'.png'),dpi=260,bbox_inches='tight')
    plt.close(fig)
    manifest.append({'figure':name,'description':description,'sources':sources})
def setup(ax,xlabel,ylabel,title):
    ax.set(xlabel=xlabel,ylabel=ylabel,title=title);ax.grid(axis='both',color='#d9dee3',lw=.55)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
def pdo_scatter(ax,rows,key):
    for pdo,(color,marker) in STYLE.items():
        selected=[r for r in rows if r['pdo_v']==pdo and r[key] is not None]
        if selected:ax.scatter([r['iout_a'] for r in selected],[r[key] for r in selected],c=color,marker=marker,s=42,label=f'{pdo} V',edgecolors='white',linewidths=.5,zorder=3)

fig,ax=plt.subplots(1,2,figsize=(7.2,3.45),layout='constrained')
pdo_scatter(ax[0],eff,'efficiency_percent_derived');pdo_scatter(ax[1],eff,'loss_w_derived')
setup(ax[0],'Logged output current (A)','Calculated efficiency (%)','(a) Row-level efficiency')
setup(ax[1],'Logged output current (A)','Input minus output power (W)','(b) Power difference')
ax[0].set_ylim(45,100);ax[1].set_ylim(bottom=0)
ax[0].legend(ncol=2,loc='lower right',frameon=True)
for a in ax:a.set_xlim(0,4.2)
finish(fig,'efficiency_and_loss',['efficiency_screening.csv'],'Eleven eligible row-level calculations; no fitted or interpolated curve.')

fig,ax=plt.subplots(1,2,figsize=(7.2,3.5),layout='constrained')
pdo_scatter(ax[0],dc,'voltage_error_percent_derived');pdo_scatter(ax[1],dc,'vbus_logged_pp_or_detail_v')
setup(ax[0],'Logged output current (A)','Average-voltage error (%)','(a) DC output average')
setup(ax[1],'Logged output current (A)','Workbook VBUS pp field (V)','(b) Original DC-capture entries')
ax[0].axhline(0,color='#555',lw=.7);ax[0].set_ylim(-.2,.7)
ax[1].set_yscale('log');ax[1].set_ylim(.25,20)
ax[0].legend(ncol=2,loc='upper right',frameon=True)
finish(fig,'regulation_and_logged_ripple',['dc_operating_points.csv'],'DC voltage error and original logged peak-to-peak fields, retaining anomalous entries.')

fig,ax=plt.subplots(figsize=(7.2,3.0),layout='constrained')
for pdo,(color,marker) in STYLE.items():
    selected=[r for r in ac if r['pdo_v']==pdo]
    currents=[]
    for r in selected:
        m=re.search(r'(\d+(?:\.\d+)?) A',r['load_condition'])
        current=0 if 'No load' in r['load_condition'] else float(m.group(1)) if m else r['iout_a']
        r['load_current_from_label_a']=current
    if selected:ax.scatter([r['load_current_from_label_a'] for r in selected],[1000*r['vbus_logged_pp_or_detail_v'] for r in selected],c=color,marker=marker,s=44,label=f'{pdo} V',edgecolor='white',lw=.6)
setup(ax,'Load current from condition label (A)','Logged AC-detail range (mV)','AC-coupled output-channel statistics')
ax.set_ylim(0,100);ax.set_xlim(-.1,4.9);ax.legend(ncol=3,loc='upper left')
write_csv('ac_detail_statistics.csv',ac)
finish(fig,'ac_detail_statistics',['ac_detail_statistics.csv'],'Logged AC-detail ranges; these are not independently validated instantaneous waveform ripple.')

fig,ax=plt.subplots(1,2,figsize=(7.2,3.5),layout='constrained')
pdo_scatter(ax[0],[r for r in pq if r['coupling']=='DC' and r['test_id']!='PDO20-80W-001'],'pf')
pdo_scatter(ax[1],[r for r in pq if r['coupling']=='DC' and r['test_id']!='PDO20-80W-001'],'ithd_percent')
high_ac=next(r for r in pq if r['test_id']=='PDO20-94W-47A-AC-001')
for a,key in [(ax[0],'pf'),(ax[1],'ithd_percent')]:a.scatter([4.7],[high_ac[key]],s=60,marker='^',facecolors='none',edgecolors=STYLE[20][0],linewidths=1.4,label='20 V high-load AC capture',zorder=4)
setup(ax[0],'Logged output current (A)','Logged power factor','(a) Power factor')
setup(ax[1],'Logged output current (A)','Logged input-current THD (%)','(b) Current THD')
ax[0].set_ylim(0,1.06);ax[1].set_ylim(0,90)
ax[0].legend(ncol=2,loc='lower right',fontsize=7.5)
finish(fig,'power_quality',['power_quality_logged.csv'],'Power factor and current THD at logged loads; instruments differ across records.')

harmonic_sources={
 'PDO20-76W-38A-001':('PDO20_76W_38A/itech_harmonic_current_20v_38a.png',[100,.2,.8,.2,.7,.1,.6,.1,.1,.1,.4,.1,.1,.1,.4,.1,.1,.2,.3,.1,.5,1.5,.8,1.2,.3,.2,.2,.1,.1,.1,.1,.1,0,.1,.1,0,.1,0,0,.1]),
 'PDO20-80W-40A-001':('PDO20_80W_40A/itech_harmonic_current_20v_40a.png',[100,2.6,2.3,1,1.2,.5,.8,.4,.3,.2,.5,.2,.2,.1,.3,.2,.2,0,.2,.3,.3,1.3,.5,1.3,.4,.3,.2,.1,.1,.1,.2,.1,.2,.1,.1,.1,.1,0,.1,0]),
 'PDO20-94W-47A-AC-001':('PDO20_94W_47A_AC/itech_current_harmonics_20v_4p7a.png',[100,.1,12.9,0,16.3,.1,14.7,.1,12.3,.1,9.3,.1,7.2,0,5.1,0,3.8,0,3.6,0,3.6,0,3.5,0,3.5,0,3.1,0,2.6,0,2.2,0,1.6,0,1.2,.1,1,.1,.8,.1])}
harmonic_rows=[]
fig,ax=plt.subplots(3,1,figsize=(7.2,6),sharex=True,layout='constrained')
for a,(test_id,(path,values)),label,color in zip(ax,harmonic_sources.items(),['(a) 20 V, 3.8 A','(b) 20 V, 4.0 A','(c) 20 V, 4.7 A high-load capture'],['#0072B2','#009E73','#D55E00']):
    assert len(values)==40
    for order,value in enumerate(values,1):harmonic_rows.append({'test_id':test_id,'harmonic_order':order,'current_percent_of_fundamental':value,'source_screenshot':'Data/measurements/evidence/'+path,'method':'Manual transcription visually checked against original ITECH current table'})
    a.bar(np.arange(2,41),values[1:],color=color,width=.73)
    a.set_ylim(0,3.1 if '3.8' in label or '4.0' in label else 18)
    setup(a,'','Current / fundamental (%)',label)
    a.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=10));a.set_xlim(1,41)
ax[-1].set_xlabel('Harmonic order (fundamental omitted)')
write_csv('current_harmonic_spectrum.csv',harmonic_rows)
harmonic_consistency=[]
for test_id,(path,values) in harmonic_sources.items():
    logged=next(r['ithd_percent'] for r in pq if r['test_id']==test_id)
    calculated=math.sqrt(sum(v*v for v in values[1:]))
    minimum=math.sqrt(sum(max(0,v-.05)**2 for v in values[1:]))
    maximum=math.sqrt(sum((v+.05)**2 for v in values[1:]))
    harmonic_consistency.append({'test_id':test_id,'logged_current_thd_percent':logged,'rss_orders_2_to_40_percent':calculated,'minimum_with_table_rounding_percent':minimum,'maximum_with_table_rounding_percent':maximum,'logged_thd_within_table_rounding_bounds':minimum<=logged<=maximum})
write_csv('harmonic_thd_consistency.csv',harmonic_consistency)
finish(fig,'current_harmonic_spectrum',['current_harmonic_spectrum.csv'],'Transcribed normalized current spectrum; panel scales intentionally differ; no assumed standards class.')

thermal=[]
for line in (Path(__file__).parent/'thermal_image_reference_table.md').read_text().splitlines():
    if not line.startswith('| Image #'):continue
    cells=[c.strip() for c in line.split('|')[1:-1]]
    pv=int(re.search(r'(\d+) V',cells[1]).group(1)); current=re.search(r'([\d.]+) A',cells[1])
    vals=re.search(r'Max/spot: ([\d.]+) C; cursor/center: ([\d.]+) C; marker: ([\d.]+) C',cells[3])
    thermal.append({'image_id':cells[0],'condition':cells[1],'pdo_v':pv,'load_current_a':float(current.group(1)) if current else 0,
        'displayed_max_c':float(vals.group(1)),'cursor_c':float(vals.group(2)),'reference_marker_c':float(vals.group(3)),
        'emissivity':.95,'source_image':cells[2].strip('`'),'stabilization_time_recorded':False})
write_csv('thermal_camera_readings.csv',thermal)
headline['thermal_maximum']=max(thermal,key=lambda r:r['displayed_max_c'])
headline['thermal_20v_4a']=next(r for r in thermal if r['pdo_v']==20 and r['load_current_a']==4)
(OUT/'headline_metrics.json').write_text(json.dumps(headline,indent=2),encoding='utf-8')
fig,ax=plt.subplots(figsize=(7.2,3.2),layout='constrained')
for pdo,(color,marker) in STYLE.items():
    rows=sorted([r for r in thermal if r['pdo_v']==pdo],key=lambda r:r['load_current_a'])
    if rows:ax.scatter([r['load_current_a'] for r in rows],[r['displayed_max_c'] for r in rows],color=color,marker=marker,s=46,label=f'{pdo} V',edgecolors='white',lw=.5)
setup(ax,'Load current from image label (A)','Displayed maximum surface temperature (°C)','Thermal-camera observations')
ax.set_ylim(20,115);ax.set_xlim(-.1,4.9);ax.legend(ncol=3,loc='upper left')
ax.annotate('102.9 °C',(4.7,102.9),xytext=(4.0,109),fontsize=8,arrowprops={'arrowstyle':'-','lw':.6})
finish(fig,'thermal_observations',['thermal_camera_readings.csv'],'Surface-temperature observations from labeled thermal screenshots; stabilization is unknown.')

rawdir=OUT/'raw_waveforms';rawdir.mkdir(exist_ok=True)
raw_index=[]
switch_records=[('00006','Overview A','C2i725 32.4W00006.csv'),('00007','Carrier detail A','C2i725 32.4W00007.csv'),('00008','Overview B','C2i725 32.4W00008.csv'),('00010','Carrier detail B','C2i725 32.4W00010.csv')]
fig,ax=plt.subplots(2,2,figsize=(7.2,5),layout='constrained')
waveform_metrics=[]
for a,(rid,label,name) in zip(ax.flat,switch_records):
    source_path=Path('C:/Users/multi/Downloads/Waveforms_Richard')/name
    target=rawdir/name
    if not source_path.exists(): source_path=target
    if source_path.resolve()!=target.resolve(): shutil.copy2(source_path,target)
    arr=np.loadtxt(target,delimiter=',',skiprows=5);t,v=arr[:,0],arr[:,1]
    assert np.all(np.diff(t)>0) and np.all(np.isfinite(arr))
    raw_index.append({'record_id':rid,'source':str(source_path),'archived_path':str(target.relative_to(THESIS)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'sample_count':len(t),'sample_interval_s':float(np.median(np.diff(t))),'t_min_s':float(t[0]),'t_max_s':float(t[-1]),'amplitude_transform':'none'})
    lo,hi=(0,.0003) if 'Overview' in label else (0,4e-6)
    selected=(t>=lo)&(t<=hi);scale=1e6
    a.plot(t[selected]*scale,v[selected],color='#534990',lw=.48)
    setup(a,'Time in source record (µs)','Recorded C2 amplitude (V)',label+f' (record {rid})')
    a.set_xlim(lo*scale,hi*scale);a.set_ylim(float(v[selected].min())-15,float(v[selected].max())+20)
    armed=False;edges=[]
    for i,value in enumerate(v):
        if value<50:armed=True
        elif armed and value>400:
            if not edges or t[i]-edges[-1]>.35e-6:edges.append(t[i])
            armed=False
    gaps=np.diff(edges);carrier=float(np.median(gaps[(gaps>.35e-6)&(gaps<2e-6)]))
    waveform_metrics.append({'record_id':rid,'median_carrier_period_s':carrier,'median_carrier_frequency_hz':1/carrier,'method':'Hysteretic rising transitions below 50 V then above 400 V; 0.35 us refractory interval; median spacing below 2 us'})
write_csv('raw_waveform_index.csv',raw_index);write_csv('switching_derived_metrics.csv',waveform_metrics)
finish(fig,'raw_switching_records',['raw_waveform_index.csv','switching_derived_metrics.csv'],'Unmodified source switching records with carrier and burst detail; no gate-source trace or matched test-ID metadata.')

# The earlier presentation CSVs were scaled to force target RMS voltage/power.
# Use the original LeCroy exports here. C1/C2 are shown as recorded amplitudes
# because probe scaling and C2 offset calibration are not established.
fig,ax=plt.subplots(3,2,figsize=(7.2,6),sharex=True,layout='constrained')
line_rows=[]
for col,folder,label in [(0,'lecory 7','Capture 7'),(1,'lecory 8','Capture 8')]:
    for row,name,ch,color in [(0,'C1.txt','C1','#0072B2'),(1,'C2.txt','C2','#D55E00'),(2,'C3-low.txt' if col==0 else 'C3-high.txt','C3','#009E73')]:
        source_path=Path('C:/Users/multi/Documents')/folder/name;target=rawdir/(folder.replace(' ','_')+'_'+name)
        if not source_path.exists(): source_path=target
        if source_path.resolve()!=target.resolve(): shutil.copy2(source_path,target)
        arr=np.loadtxt(target,delimiter=',',skiprows=5);t,v=arr[:,0],arr[:,1]
        selected=(t>=-.02)&(t<=.02)
        ax[row,col].plot(t[selected]*1000,v[selected],color=color,lw=.55)
        setup(ax[row,col],'Time (ms)' if row==2 else '',f'{ch} recorded amplitude',label if row==0 else '')
        ax[row,col].set_xlim(-20,20)
        raw_index.append({'record_id':folder+' '+ch,'source':str(source_path),'archived_path':str(target.relative_to(THESIS)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'sample_count':len(t),'sample_interval_s':float(np.median(np.diff(t))),'t_min_s':float(t[0]),'t_max_s':float(t[-1]),'amplitude_transform':'none'})
        for tt,vv in zip(t[selected],v[selected]):line_rows.append({'capture':folder,'channel':ch,'time_s':float(tt),'recorded_amplitude':float(vv),'source_archived':str(target.relative_to(THESIS))})
write_csv('line_waveform_plot_data.csv',line_rows);write_csv('raw_waveform_index.csv',raw_index)
finish(fig,'raw_line_records',['line_waveform_plot_data.csv','raw_waveform_index.csv'],'Original recorded channel amplitudes, without power-target scaling or smoothing; channel calibration unresolved.')

def f(v,d=3):return '--' if v is None else f'{v:.{d}f}' if isinstance(v,(float,int)) else str(v)
def idtex(value):return '\\sourcefile{'+str(value)+'}'
def tex_plain(value):
    replacements={'#':r'\#','&':r'\&','%':r'\%','_':r'\_','$':r'\$','{':r'\{','}':r'\}'}
    return ''.join(replacements.get(c,c) for c in str(value))
def table(name,caption,label,headers,rows,widths,landscape=False,size='scriptsize'):
    widths=[w*.88/sum(widths) for w in widths]
    spec='@{}'+' '.join('L{'+f'{w:.4f}'+'\\linewidth}' for w in widths)+'@{}'
    result=['% Automatically rebuilt from original records by rebuild_results.py.']
    if landscape:result.append('\\begin{landscape}')
    result+=['\\begingroup','\\'+size,'\\setlength{\\tabcolsep}{3pt}',r'\renewcommand{\arraystretch}{1.12}',r'\begin{longtable}{'+spec+'}',r'\caption{'+caption+'}\\label{'+label+r'}\\',r'\toprule',' & '.join(headers)+r'\\',r'\midrule',r'\endfirsthead',r'\toprule',' & '.join(headers)+r'\\',r'\midrule',r'\endhead']
    result+=[' & '.join(row)+r'\\' for row in rows]
    result+=[r'\bottomrule',r'\end{longtable}',r'\endgroup']
    if landscape:result.append(r'\end{landscape}')
    (OUT/name).write_text('\n'.join(result)+'\n',encoding='utf-8')

table('dc_complete_table.tex','DC operating-point measurements at 240 V, 50 Hz, with calculated output power and voltage error. VBUS pp keeps the original workbook label.','tab:appendix-dc-complete',
 ['Test ID', '$V_\\mathrm{set}$ (V)', '$I_\\mathrm{out}$ (A)', '$V_\\mathrm{BUS}$ (V)', 'Logged pp (V)', '$V_\\mathrm{sec}$ (V)', 'Sec. pp (V)', '$P_\\mathrm{in}$ (W)', '$P_\\mathrm{out}$ (W)', 'Error (\\%)'],
 [[idtex(r['test_id']),f(r['pdo_v'],0),f(r['iout_a'],2),f(r['vbus_avg_v'],5),f(r['vbus_logged_pp_or_detail_v']),f(r['secondary_avg_v'],4),f(r['secondary_logged_pp_or_detail_v'],4),f(r['pin_w']),f(r['pout_w_derived']),f(r['voltage_error_percent_derived'])] for r in dc],[.22,.07,.07,.09,.09,.09,.09,.08,.08,.07],True)
table('ac_complete_table.tex','AC-coupled measurements. Several workbook values describe the spread of average-voltage readings, not instantaneous peak-to-peak ripple. CH2 and CH3 do not show absolute DC voltage.','tab:ac-coupled-ripple-captures',
 ['Test ID', 'Setting (V)', 'Load (A)', 'VBUS detail (mV)', 'Secondary detail (V)', 'Interpretation'],
 [[idtex(r['test_id']),f(r['pdo_v'],0),f(r['load_current_from_label_a'],2),f(1000*r['vbus_logged_pp_or_detail_v'],3),f(r['secondary_logged_pp_or_detail_v'],5),'AC statistics/detail; no DC level'] for r in ac],[.31,.08,.08,.14,.14,.20],False)
table('efficiency_table.tex','Initial efficiency estimates from eleven measurements.','tab:efficiency-results',
 ['Test ID', '$I_\\mathrm{out}$ (A)', '$P_\\mathrm{out}$ (W)', '$P_\\mathrm{in}$ (W)', '$\\eta$ (\\%)', 'Difference (W)'],
 [[idtex(r['test_id']),f(r['iout_a'],2),f(r['pout_w_derived'],2),f(r['pin_w'],2),f(r['efficiency_percent_derived'],2),f(r['loss_w_derived'],2)] for r in eff],[.34,.12,.14,.14,.11,.14])
table('pq_complete_table.tex','Power factor and current THD from the instrument readings. The instruments or averaging intervals can differ. The 3.9 A entry is an associated record and is not used for the load trend.','tab:pq-results',
 ['Test ID', 'Setting / load', '$P_\\mathrm{in}$ (W)', 'PF', 'Current THD (\\%)', 'Instrument / record'],
 [[idtex(r['test_id']),f(r['pdo_v'],0)+' V / '+f(r['iout_a'],2)+' A',f(r['pin_w'],3),f(r['pf'],3),f(r['ithd_percent'],2),('Associated record' if r['test_id']=='PDO20-80W-001' else 'Siglent PF; ITECH THD' if r['pdo_v'] in (9,15) or r['coupling']=='AC detail' else 'ITECH entries')] for r in pq],[.31,.16,.12,.08,.12,.21])
hr=[]
for order in range(1,41):hr.append([str(order)]+[f(values[order-1],1) for path,values in harmonic_sources.values()])
table('harmonics_complete_table.tex','Input-current harmonics from the three ITECH tables. Order 1 is the fundamental. The 4.7 A entry uses an AC-coupled output capture.','tab:input-harmonics',
 ['Order','3.8 A: \\% of fundamental','4.0 A: \\% of fundamental','4.7 A: \\% of fundamental'],hr,[.12,.27,.27,.27])
table('thermal_complete_table.tex','Temperature readings from ten thermal images, using emissivity 0.95. The lower reference marker was not confirmed as ambient temperature.','tab:thermal-results',
 ['Image / condition', 'Maximum (°C)', 'Cursor (°C)', 'Reference (°C)'],
 [[tex_plain(r['image_id']+' / '+r['condition']),f(r['displayed_max_c'],1),f(r['cursor_c'],1),f(r['reference_marker_c'],1)] for r in thermal],[0.34, 0.18, 0.18, 0.18])
table('raw_waveform_source_table.tex','Waveform records, sample counts, and sampling intervals.','tab:raw-waveform-sources',
 ['Record', 'Samples', 'Interval (s)'],
 [[idtex(r['record_id']),str(r['sample_count']),f"{r['sample_interval_s']:.3g}"] for r in raw_index],[0.3562, 0.2619, 0.2619])
trans=[]
for item in source:
    n=item['row'];c=item['cells']
    if n not in (31,35):continue
    trans.append({'test_id':c[f'A{n}'],'source_row':n,'pdo_v':c[f'G{n}'],'event':c[f'H{n}'],
        'vbus_acquisition_average_v':c[f'K{n}'],'vbus_logged_pp_v':c[f'L{n}'],
        'secondary_acquisition_average_v':c[f'M{n}'],'secondary_logged_pp_v':c[f'N{n}'],
        'overshoot_from_pre_step_v':None,'recovery_time_s':None})
write_csv('transient_recorded_fields.csv',trans)
table('transient_complete_table.tex','Load-removal measurements from the workbook. Averages and pp span the whole capture and do not give the voltage rise from the pre-step level. Recovery time is not available. The 5 V and 20 V screenshots have no numerical worksheet row.','tab:appendix-transient-complete',
 ['Test ID', 'Setting (V)', 'VBUS avg (V)', 'VBUS pp (V)', 'Secondary avg (V)', 'Secondary pp (V)'],
 [[idtex(r['test_id']),f(r['pdo_v'],0),f(r['vbus_acquisition_average_v'],5),f(r['vbus_logged_pp_v']),f(r['secondary_acquisition_average_v'],4),f(r['secondary_logged_pp_v'],4)] for r in trans],[.30,.10,.14,.14,.15,.15])
complete=[r for r in records if r['status']!='Planned']
table('record_metadata_table.tex','Test status, firmware version, and use in the calculations. A dash means the firmware was not recorded. Efficiency estimates are preliminary because acquisition timing and inclusion of auxiliary power were not fully documented. AC-coupled statistics are not used to calculate DC power.','tab:appendix-record-metadata',
 ['Test ID', 'Recorded status', 'Firmware', 'Treatment'],
 [[idtex(r['test_id']),r['status'],tex_plain(r['firmware']) if r['firmware'] else '--',('Power comparison' if r['efficiency_screening_included'] else ('No nonzero DC input/output power pair' if r['exclusion']=='no nonzero measured DC output/input power' else r['exclusion']))] for r in complete],[.29,.15,.24,.30],True)

# A single appendix entry point is supplied for the main-document editor.
(OUT/'measurement_appendix.tex').write_text(r'''\section{Complete Measurement Records}
\label{app:rewritten-measurement-records}
The tables below include every completed steady-state DC point, the AC-coupled
detail entries, input-power-quality records, the three transcribed harmonic
spectra, and all ten thermal-camera observations used in Chapter~\ref{ch:results}.
A blank field indicates an unavailable measurement.
\input{Data/measurements/processed_rewrite/dc_complete_table}
\input{Data/measurements/processed_rewrite/ac_complete_table}
\input{Data/measurements/processed_rewrite/efficiency_table}
\input{Data/measurements/processed_rewrite/pq_complete_table}
\input{Data/measurements/processed_rewrite/harmonics_complete_table}
\input{Data/measurements/processed_rewrite/thermal_complete_table}
\input{Data/measurements/processed_rewrite/raw_waveform_source_table}
''',encoding='utf-8')

(OUT/'figure_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
write_csv('source_checksums.csv',[{'source':str(BOOK.relative_to(ROOT)),'sha256':hashlib.sha256(BOOK.read_bytes()).hexdigest()}])
for name,label in [('ac_complete_table','tab:ac-coupled-ripple-captures'),('efficiency_table','tab:efficiency-results'),('thermal_complete_table','tab:thermal-results')]:
    text=(OUT/(name+'.tex')).read_text(encoding='utf-8')
    (OUT/('appendix_'+name+'.tex')).write_text(text.replace(label,label+'-complete'),encoding='utf-8')
(OUT/'appendix_electrical_tables.tex').write_text(r'''\input{Data/measurements/processed_rewrite/dc_complete_table}
\input{Data/measurements/processed_rewrite/appendix_ac_complete_table}
\input{Data/measurements/processed_rewrite/appendix_efficiency_table}
\input{Data/measurements/processed_rewrite/pq_complete_table}
\input{Data/measurements/processed_rewrite/transient_complete_table}
\input{Data/measurements/processed_rewrite/record_metadata_table}
''',encoding='utf-8')
(OUT/'appendix_harmonic_tables.tex').write_text(r'''\input{Data/measurements/processed_rewrite/harmonics_complete_table}
''',encoding='utf-8')
(OUT/'appendix_thermal_tables.tex').write_text(r'''\input{Data/measurements/processed_rewrite/appendix_thermal_complete_table}
''',encoding='utf-8')
(OUT/'processing_provenance.txt').write_text('Primary electrical data: original workbook Load Data sheet; workbook not modified. Original recorded voltages/power retained, derived values recomputed.\nPrior presentation waveform exports in outputs/input_voltage_current_240v_10w and outputs/input_voltage_current_95w were filtered, offset-adjusted and rescaled by earlier scripts to force target power and/or RMS voltage. They were excluded. Raw waveform copies are byte-identical to original exports and have SHA-256 digests.\nHarmonic tables were manually transcribed and visually verified against original ITECH screenshots for all orders 1–40.\nAC detail columns often contain ranges of Vavg measurement statistics, not waveform peak-to-peak ripple. Labels preserve this distinction. The 15 V/1 A workbook field 27.3799 mV differs from the explicitly noted Vpp/detail 50.582 mV; neither is substituted.\nThermal figures use the maximum marker, separately from cursor and reference marker, from the retained reference table; no stabilization time or calibrated component identity is assumed.\n',encoding='utf-8')
assert len(dc)==17 and len(eff)==11 and len(ac)==12 and len(thermal)==10 and len(harmonic_rows)==120
assert abs(high[-1]['pout_w_derived']-79.8928)<1e-7
assert abs(high[-1]['efficiency_percent_derived']-76.512479)<1e-5
print(json.dumps({'figures':len(manifest),'dc_records':len(dc),'efficiency_records':len(eff),'ac_detail_records':len(ac),'raw_sources':len(raw_index),'headline_file':str(OUT/'headline_metrics.json')},indent=2))
write_csv('generated_output_checksums.csv',[{'output':str(p.relative_to(THESIS)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size_bytes':p.stat().st_size} for directory in (OUT,FIG) for p in sorted(directory.rglob('*')) if p.is_file() and p.name!='generated_output_checksums.csv'])
