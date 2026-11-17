from pathlib import Path
import json,shutil
root=Path('/workspace/thesis');review=Path('/workspace/tooling/thesis-direct-results');edits=[]
m={
'Chapters/02_Background/chapter.tex': [('The reference converters establish this operating principle; the USB-C adaptation adds','The reference converters use this operating principle; the USB-C adaptation adds')],
'Chapters/02_Background/04_Soft_Switching_GaN.tex': [('separately from established switching','separately from switching within an active burst')],
'Chapters/03_Requirements_Architecture/05_Safety_Protection.tex': [('Precharge applies limited excitation to establish the isolated feedback supply.','Precharge applies limited excitation to power the isolated feedback circuit.')],
'Chapters/04_Topology_Analysis/02_Switching_Cycle.tex': [('within an established burst','during an active burst')],
'Chapters/04_Topology_Analysis/05_Pump_Inductor.tex': [('In-circuit waveforms are required to establish the timing margin.','In-circuit waveforms show how much time remains between charge-transfer completion and the next transition.')],
'Chapters/04_Topology_Analysis/06_DC_Link.tex': [('Measured bus mean, ripple, and maximum establish capacitor-voltage margin and half-bridge excitation.','Measured bus mean, ripple, and maximum are used to calculate capacitor-voltage margin and half-bridge excitation.')],
'Chapters/04_Topology_Analysis/08_ZVS.tex': [
('The charge condition must be met with the required polarity and before turn-on; charge magnitude alone does not establish ZVS.','The charge condition must be met with the required polarity and before turn-on.'),
('Near-carrier resonance does not establish ZVS across the operating range. Tolerances shift resonance, pump current falls near line zero crossings, and idle intervals can remove circulating current. These conditions require separate switching captures even at fixed dead time.','Tolerances shift resonance, pump current falls near line zero crossings, and idle intervals can remove circulating current. Switch-node transitions therefore need checking near line zero crossings and at burst restart, even with fixed dead time.')],
'Chapters/04_Topology_Analysis/09_Device_Stress.tex': [('Nominal passive values and supplied magnetic measurements establish the starting design; the waveforms determine the stresses reached in the tested circuit.','The initial calculations use nominal passive values and supplied magnetic measurements. The waveforms give the stresses reached in the tested circuit.')],
'Chapters/06_Magnetics_Integration/07_Isolation_Clearance.tex': [(' A full insulation check also requires the transformer spacing, material group, and standardized dielectric tests. Functional isolation alone does not establish creepage, clearance, or dielectric strength.',' The full insulation check includes transformer spacing, material group, and standardized dielectric tests.')],
'Chapters/07_Hardware/16_V2_F410.tex': [
('Driver-input and switch-node captures are required to establish effective dead time and enable alignment.','Effective dead time and enable alignment are measured from driver-input and switch-node captures.'),
('The reported \\SI{85}{\\watt} point and matched \\SI{79.89}{\\watt} point do not demonstrate sustained operation at the \\SI{100}{\\watt} target.','The reported \\SI{85}{\\watt} point and matched \\SI{79.89}{\\watt} point are intermediate loads below the \\SI{100}{\\watt} target.')],
'Chapters/08_Control_Firmware/15_PWR_2_Port.tex': [
('The port retains the earlier conversion defaults. The repeated \\SI{6.2}{\\mega\\ohm} schematic labels do not establish the assumed divider ratios; fitted resistors and measured gains must be verified before using the displayed voltage, current, or protection thresholds.','The port retains the earlier conversion defaults. The repeated \\SI{6.2}{\\mega\\ohm} schematic labels need checking against the fitted resistors. The voltage, current, and protection scales must use the measured circuit gains.'),
('These are timer-setting limits; the usable converter range must be established from switching and thermal measurements.','These are timer-setting limits. The converter operating range still needs switching and thermal measurements.'),
('Automatic calibration does not search carrier frequency or establish zero-voltage switching.','The duty-search calibration holds carrier frequency fixed.')],
'Chapters/09_Experimental_Methods/06_Test_Matrix.tex': [('Bring-up established switching and power transfer, followed by loaded and','Switching and power transfer were checked during bring-up, followed by loaded and')],
'Chapters/09_Experimental_Methods/10_Thermal.tex': [('Incomplete ambient, airflow, warm-up, and camera-setup records prevent a\r\nthermal steady-state assessment. The images guide instrumented monitoring\r\nbut do not establish a continuous power rating.','Ambient, airflow, warm-up, and camera setup were not fully recorded.\r\nThe images locate hotspots for temperature monitoring during longer runs.')],
'Chapters/09_Experimental_Methods/12_Revised_Plan_Validation.tex': [
('firmware source, saved settings, and live mode. Version, status, and validated\nconfiguration exports are required; a successful build does not verify powered\noperation.','firmware source, saved settings, and live mode. Version, status, and\nconfiguration exports are recorded with the test.'),
('Establish regulation, power quality, efficiency, stress, and heating','Measure regulation, power quality, efficiency, stress, and heating'),
('transitions, and limit behavior; fixed-voltage records do not verify PPS.','transitions, and limit behavior.')],
'Backmatter/Appendices/C_Firmware_Documentation.tex': [
('The command does not switch output OFF or establish zero current. Zero primary current must be established before use; sensor gain is not calibrated.','The operator must switch output OFF and check for zero primary current before using the terminal command. This captures the offset; gain calibration uses a separate reference.'),
('The operator must first establish zero primary current; the command does not enforce OFF.','Switch output OFF and check for zero primary current before the terminal command; OFF is not enforced automatically.'),
('These are timer limits; the usable converter range must be established from switching and thermal measurements.','These are timer limits. The converter operating range still needs switching and thermal measurements.')],
'Backmatter/Appendices/G_Software_Tools.tex': [('stated hysteretic thresholds and median edge spacing; single-node\nrecords still cannot establish gate timing or ZVS. The scripts save source and','stated hysteretic thresholds and median edge spacing. The scripts save source and')],
'Backmatter/Appendices/H_Full_Embedded_Source.tex': [('follows those definitions. A successful build does not verify fitted\ndivider ratios, gate timing, or powered-converter performance.','follows those definitions.')]
}
for name,pairs in m.items():
 p=root/name;before=p.read_bytes();text=before.decode()
 for old,new in pairs:
  assert old in text,(name,old);text=text.replace(old,new);edits.append({'path':name,'old':old,'new':new})
 backup=review/'before'/name;backup.parent.mkdir(parents=True,exist_ok=True)
 assert not backup.exists(),name
 backup.write_bytes(before);p.write_bytes(text.encode())
(review/'technical-edits.json').write_text(json.dumps(edits,indent=2)+'\n')
(review/'technical-files.json').write_text(json.dumps(list(m),indent=2)+'\n')
print(len(edits),'replacements in',len(m),'files')
