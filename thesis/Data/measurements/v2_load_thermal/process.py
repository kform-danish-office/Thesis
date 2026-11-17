"""Extract AC-supply/load snapshots and visually transcribed thermal regions.

Scope rows are excluded before numeric conversion. No waveform quantities are
used. Original CSVs are kept unchanged in raw/.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
import csv, hashlib, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
AC = '4c5d43a8-3948-432f-9320-a8eeab4d5849'
LOAD = 'd80f4f53-4f7c-44ee-8ce0-d5860477faa7'
# Read directly from the supplied screenshots; H/L/M are ROI max/min/mean.
THERMAL = {
 '015': ('20:24:39',(65.1,24.7,37.7),(50.3,23.8,36.2)),
 '017': ('20:25:54',(83.9,26.1,42.5),(57.2,26.1,40.7)),
 '018': ('20:26:46',(68.2,25.1,42.2),(59.7,25.6,41.1)),
 '019': ('20:27:11',(73.2,26.5,45.1),(69.4,27.0,44.8)),
 '020': ('20:27:33',(74.5,27.4,47.4),(81.6,27.9,47.7)),
 '021': ('20:27:54',(75.6,28.8,49.2),(88.7,28.8,51.1)),
 '022': ('20:28:17',(73.7,27.0,48.5),(98.3,27.4,52.0)),
}

def rounded(value, places):
    return str(Decimal(str(value)).quantize(Decimal(10)**-places,rounding=ROUND_HALF_UP))

records,manifest=[],[]
for path in sorted((ROOT/'raw').glob('*.csv')):
    capture=path.stem.split()[1]
    with path.open(newline='') as f:
        rows=[row for row in csv.DictReader(f) if row['device'] in {AC,LOAD}]
    assert len(rows)==2 and {r['device'] for r in rows}=={AC,LOAD}
    ac=next(row for row in rows if row['device']==AC)
    load=next(row for row in rows if row['device']==LOAD)
    assert ac['timestamp']==load['timestamp']
    assert all(r['status']=='online' and not r['error'] for r in rows)
    pin=Decimal(ac['power_W']);v=Decimal(load['voltage_V']);i=Decimal(load['current_A']);power=v*i
    assert abs(power-Decimal(load['power_W']))<Decimal('1e-10')
    eta=100*power/pin
    clock,r3,r1=THERMAL[capture]
    time=datetime.fromisoformat(ac['timestamp'])
    image_time=datetime.fromisoformat(time.date().isoformat()+'T'+clock+'+00:00')
    gap=(time+timedelta(hours=1)-image_time).total_seconds()
    assert 2 < gap < 5
    record={'capture':capture,'source_csv':path.name,'timestamp_utc':ac['timestamp'],
      'ac_voltage_V':float(ac['voltage_V']),'ac_current_A':float(ac['current_A']),
      'input_real_power_W':float(pin),'ac_frequency_Hz':float(ac['frequency_Hz']),
      'secondary_voltage_V':float(v),'secondary_current_A':float(i),
      'secondary_power_W':float(power),'efficiency_estimate_percent':float(eta),
      'input_minus_load_power_W':float(pin-power),'camera_clock':clock,
      'clock_gap_after_one_hour_offset_s':gap,'bridge_R3_max_C':r3[0],
      'bridge_R3_min_C':r3[1],'bridge_R3_mean_C':r3[2],'secondary_R1_max_C':r1[0],
      'secondary_R1_min_C':r1[1],'secondary_R1_mean_C':r1[2],
      'region_emissivity':0.95,'display_footer_emissivity':0.97,
      'thermal_equilibrium_reached':False,
      'ac_values_inconsistent':pin>Decimal(ac['voltage_V'])*Decimal(ac['current_A'])}
    records.append(record)
    manifest.append({'path':'raw/'+path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                     'used_devices':[AC,LOAD],'excluded_scope_rows':1})

assert len(records)==7 and sum(r['ac_values_inconsistent'] for r in records)==1
(ROOT/'summary.json').write_text(json.dumps(records,indent=2)+'\n')
with (ROOT/'summary.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
(ROOT/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

lines=[r'\begin{table}[htbp]',r'\centering',r'\small',r'\setlength{\tabcolsep}{4pt}',
 r'\caption{AC input, secondary-load readings, and thermal-region maxima during the V2 load sequence. Input voltage was approximately \SI{240}{\volt} at \SI{50}{\hertz}.}',
 r'\label{tab:v2-secondary-load}',r'\begin{tabular}{@{}rrrrrrrr@{}}',r'\toprule',
 r'Capture & $P_{\mathrm{in}}$ & $V_{\mathrm{sec}}$ & $I_{\mathrm{sec}}$ & $P_{\mathrm{sec}}$ & $\eta$ & Bridge R3 & Secondary R1\\',
 r' & (W) & (V) & (A) & (W) & (\%) & ($^\circ$C) & ($^\circ$C)\\',r'\midrule']
for r in records:
    star=r'\textsuperscript{*}' if r['ac_values_inconsistent'] else ''
    vals=[r['capture'],rounded(r['input_real_power_W'],3)+star,rounded(r['secondary_voltage_V'],2),
          rounded(r['secondary_current_A'],2),rounded(r['secondary_power_W'],2),
          rounded(r['efficiency_estimate_percent'],1)+star,rounded(r['bridge_R3_max_C'],1),rounded(r['secondary_R1_max_C'],1)]
    lines.append(' & '.join(vals)+r'\\')
lines += [r'\bottomrule',r'\end{tabular}',r'\par\vspace{0.4em}',
 r'\begin{minipage}{\linewidth}\footnotesize',
 r'$P_{\mathrm{sec}}$ is calculated from the electronic-load voltage and current; $\eta=100P_{\mathrm{sec}}/P_{\mathrm{in}}$ is an estimate.',
 r'\textsuperscript{*}Capture 017 reports \SI{95.142}{\watt} input, while its \SI{239.99}{\volt} and \SI{0.39}{\ampere} readings give \SI{93.60}{\volt\ampere}. The input reading and associated efficiency need checking.',
 r'\end{minipage}',r'\end{table}']
(ROOT/'load_table.tex').write_text('\n'.join(lines)+'\n')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,
                     'axes.titlesize':10,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
power=[r['secondary_power_W'] for r in records]
fig,ax=plt.subplots(2,1,figsize=(5.9,5.2),sharex=True,layout='constrained')
ax[0].plot(power,[r['secondary_voltage_V'] for r in records],'-o',color='#205a83',lw=1.5,ms=4)
ax[0].set_ylabel('Secondary voltage (V)');ax[0].set_title('(a) Secondary-output voltage',loc='left')
ax[1].plot(power,[r['bridge_R3_max_C'] for r in records],'-s',color='#bb482b',lw=1.5,ms=4,label='Input bridge, R3')
ax[1].plot(power,[r['secondary_R1_max_C'] for r in records],'-o',color='#205a83',lw=1.5,ms=4,label='Secondary, R1')
ax[1].set_ylabel('Region maximum (°C)');ax[1].set_xlabel('Calculated secondary output power (W)')
ax[1].set_title('(b) Surface temperatures during the load sequence',loc='left');ax[1].legend(frameon=False,loc='upper left')
for a in ax:a.grid(alpha=.22);a.set_xlim(43,143)
fig.savefig(ROOT/'load_performance.pdf');fig.savefig(ROOT/'load_performance.png',dpi=180);plt.close(fig)
print('Processed 7 AC/load pairs, excluding all 7 scope rows; generated table and plots.')
