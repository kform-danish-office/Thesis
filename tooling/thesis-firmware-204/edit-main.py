from pathlib import Path
import json,shutil,re
root=Path('/workspace/thesis');r=Path('/workspace/tooling/thesis-firmware-204');changes=[]
def write(name,s):
 p=root/name;b=r/'before'/name;b.parent.mkdir(parents=True,exist_ok=True)
 if not b.exists():shutil.copy2(p,b)
 p.write_bytes(s.encode());changes.append(name)
def replace(name,old,new):
 s=(root/name).read_bytes().decode();assert old in s,(name,old[:50]);write(name,s.replace(old,new))
replace('Chapters/08_Control_Firmware/chapter.tex','Archived V2 firmware & PWR-2.0.1 & MCU port with browser commands and logging.','V2 controller firmware & PWR-2.0.4 & Browser calibration, reference-load settings, and adjustable carrier frequency and dead time on V2.')
replace('Chapters/08_Control_Firmware/chapter.tex','main final test series and retained in the integrated V2 port.','main final test series and retained in the integrated V2 port. The later V2\nfirmware adds calibration and timing controls without changing the bulk-voltage\ncontrol law. These additions are described in Section~\\ref{sec:ctrl-pwr2-port}.')
p='Chapters/08_Control_Firmware/15_PWR_2_Port.tex';s=(root/p).read_text()
s=s.replace('The baseline voltage-control law was retained; browser control and UART logging were added after the hardware port.','The baseline voltage-control law was retained. Browser control and UART logging were followed by automatic calibration, editable reference-load settings, and adjustable carrier timing.')
s=s.replace('At a \\SI{100}{\\mega\\hertz} TIM1 clock, ARR \\(=50\\), CCR1 \\(=25\\), and DTG \\(=4\\) give the nominal \\SI{1}{\\mega\\hertz} carrier and \\SI{40}{\\nano\\second} programmed dead time through the complementary-output hardware \\cite{ststm32f410ds,ststm32f410rm}. Driver-input and switch-node timing remain to be measured on the assembled V2.','The complementary outputs share the TIM1 compare signal and hardware dead-time generator \\cite{ststm32f410ds,ststm32f410rm}. The earlier port used center-aligned counting; the adjustable implementation uses edge-aligned counting with equal reference pulse widths. The default remains a \\SI{1}{\\mega\\hertz} carrier with \\SI{40}{\\nano\\second} programmed dead time.')
s=s.replace('The saved boot preference was kept separate', 'Timing and calibration are saved together in a 488-byte record, giving 33 entries in the reserved sector. Existing settings from the earlier format load with default carrier timing and are not rewritten at startup. Older firmware cannot read the new record format.\n\nThe saved boot preference was kept separate')
s=s.replace('Blocking autotuning is excluded from the web interface, and a browser settings save requires OFF.','Calibration routines service UART commands and cancellation checks during their waits, allowing OFF and lease expiry to interrupt a run. A browser settings save requires OFF.')
start=s.index('\\subsection{V2 Software Checks and Remaining Tests}')
s=s[:start]+r'''\subsection{Automatic Calibration and Reference Loads}

Browser calibration was added for startup precharge, no-load operation, and three reference loads. The existing coarse and fine duty search is used to find a burst duty from the measured secondary-bulk voltage. The burst-enable frequency remains fixed during this search. This makes the earlier terminal routines accessible from the setup interface without adding a separate control algorithm.

Each reference load is connected by the operator, and its resistance is entered in the setup page. The resistance entry describes the connected load; it does not set an electronic load or switch a resistor. Selecting a calibrated slot applies its stored profile. No-load duty, scan step and interval, and startup precharge settings can also be read and adjusted with output OFF. Current-zero and primary-voltage-reference capture are available for sensor calibration.

A calibration run starts with output OFF and leaves it OFF after completion. OFF, communication-lease expiry, a fault, or the \SI{180}{\second} timeout cancels the run; interrupted or failed runs restore the previous settings. Successful browser changes remain in RAM until explicitly saved with the output disabled.

\subsection{Adjustable Carrier Frequency and Dead Time}
\label{sec:ctrl-v2-adjustable-timing}

Carrier frequency and dead time were made adjustable so that switching could be set relative to the modified resonant tank and the commutation interval could be varied without rebuilding the firmware. Both values are applied together through \texttt{TIMING} while output is OFF and startup and calibration are inactive. Burst duty continues to regulate the secondary bulk voltage. The separate \texttt{FEN} setting controls the burst-enable frequency; the tank's natural resonant frequency is set by its inductance and capacitance.

The command accepts carrier requests from \SI{500}{\kilo\hertz} to \SI{2}{\mega\hertz} and dead-time requests from \SI{20}{\nano\second} to \SI{200}{\nano\second}. These are timer-setting limits; the usable converter range must be established from switching and thermal measurements. TIM1 uses an even period count for balanced reference pulses, and dead time is rounded up to a timer count. At a \SI{100}{\mega\hertz} timer clock, period increments are \SI{20}{\nano\second} and dead-time increments are \SI{10}{\nano\second}. Frequency steps therefore depend on the selected period.

For timer clock \(f_t\), period count \(N_p\), and dead-time count \(N_d\), the applied settings are
\begin{equation}
 f_s=\frac{f_t}{N_p},\qquad t_d=\frac{N_d}{f_t},\qquad 4N_d<N_p.
 \label{eq:ctrl-v2-carrier-timing}
\end{equation}
The last condition rejects pairs that leave insufficient pulse time. A request of \SI{950}{\kilo\hertz} and \SI{53}{\nano\second}, for example, gives \(N_p=106\) and \(N_d=6\): approximately \SI{943.396}{\kilo\hertz} and \SI{60}{\nano\second}. The browser displays the applied values from MCU readback, and burst scheduling uses the actual clock and period counts.

Changing either applied timer count clears the three learned load profiles and tuning results. Reference resistances, sensor calibration, and applied duty settings are retained. Calibration must then be repeated before using learned profiles at the new timing. Browser timing changes require an explicit save while OFF; the terminal retains its existing automatic save after a \SI{1.5}{\second} quiet interval while OFF, unless a configuration import is active.

The programmed interval is the separation between timer output commands. Driver delay and switch-node commutation determine the effective transistor dead time, which must be measured on the assembled board. Automatic calibration does not search carrier frequency or establish zero-voltage switching.

\subsection{Software Verification}

The V2 firmware, protocol tests, settings-storage tests, and browser tests were built and checked. These checks cover timer rounding and pair rejection, application with output disabled, learned-profile clearing, calibration cancellation, and saved-settings recovery after interrupted writes. The complete source and build results are included in Appendices~\ref{app:firmware} and \ref{app:full-embedded-source}.

Powered validation of the adjustable implementation remains to be completed. The V1.0 measurements and later V2 thermal observations in Chapter~\ref{ch:results} describe the earlier test configurations. Switching waveforms and matched electrical and thermal measurements are needed to assess the new timing controls on the converter.
'''
write(p,s)
replace('Chapters/01_Introduction/08_V2_Prototype.tex','Archived timing & Nominal \\SI{1}{\\mega\\hertz} carrier and \\SI{40}{\\nano\\second} programmed dead time in the archived V2 controller code','Carrier timing & Default \\SI{1}{\\mega\\hertz} carrier and \\SI{40}{\\nano\\second} programmed dead time; both adjustable with output disabled (\\cref{sec:ctrl-v2-adjustable-timing})')
replace('Chapters/07_Hardware/16_V2_F410.tex','The fixed \\SI{1}{\\mega\\hertz} carrier and burst-enable control were retained from the earlier DMA-based controller (\\cref{ch:control}). Board-dependent peripherals were ported before browser telemetry and commands were added. The common source supports both MCUs. Each test needs the MCU, fitted parts, and firmware settings recorded together.','The nominal \\SI{1}{\\mega\\hertz} carrier and burst-enable control were retained from the earlier DMA-based controller (\\cref{ch:control}). Board-dependent peripherals were ported before browser telemetry and commands were added. The later V2 firmware adds output-OFF adjustment of carrier frequency and dead time (\\cref{sec:ctrl-v2-adjustable-timing}).')
replace('Chapters/07_Hardware/16_V2_F410.tex','The archived V2 source configures center-aligned TIM1','The earlier V2 port configures center-aligned TIM1')
replace('Chapters/05_Modeling_Simulation/08_Parameter_Sweeps.tex','The included controller has a fixed carrier; frequency and dead-time experiments require their own recorded configuration.','The later V2 firmware allows carrier frequency and dead time to be changed with output disabled (\\cref{sec:ctrl-v2-adjustable-timing}), allowing these parameters to be varied separately from the tank components.')
p='Backmatter/Appendices/H_Full_Embedded_Source.tex';s=(root/p).read_text().replace('PWR-2.0.1','PWR-2.0.4').replace('PWR_2_0_1','PWR_2_0_4').replace('pwr201','pwr204').replace('4,848','5,348')
s=s.replace('the later V2 controller source for F410 and G071 targets, including\nthe browser protocol.','the later V2 controller source with browser calibration, reference-load settings,\nand adjustable carrier timing. The same file builds the G071 target as\nPWR-2.0.3 with its fixed carrier.')
s=s.replace('Complete PWR-2.0.4 controller source for V2 F410 and G071 targets.','Complete V2 controller source: PWR-2.0.4 for F410 and PWR-2.0.3 for G071.')
write(p,s)
# Update existing full supporting listings and add the new runtime/tests.
p='Backmatter/Appendices/I_Full_Supporting_Source.tex';s=(root/p).read_text();a=s.index('The listings also include');b=s.index('Generated build outputs')
s=s[:a]+'The browser files include the monitoring dashboard, calibration and setup controls, and resonant-tank calculator.\n\n'+s[b:];s=s.replace('PWR_2_0_1','PWR_2_0_4')
s=re.sub(r'(\\noindent\\sourcefile\{([^}]+)\}; )\d+( physical lines\.)',lambda m:m[1]+str(len((root/m[2]).read_bytes().splitlines()))+m[3],s)
extra=[('firmware/test_carrier_storage.py','Carrier settings storage tests'),('web/resonance-ui.js','Resonant-tank calculator interface'),('web/resonance-presets.js','Measured magnetic component presets'),('web/tests/resonance-presets.test.mjs','Magnetic component preset tests')]
for i,(path,title) in enumerate(extra,24):
 path='Code/PWR_2_0_4/'+path;n=len((root/path).read_bytes().splitlines())
 s+=f'\n\\Needspace{{10\\baselineskip}}\n\\section{{{title}}}\n\\noindent\\sourcefile{{{path}}}; {n} physical lines.\n\n\\lstinputlisting[language={{}},style=fullsource,caption={{{title}: complete source.}},label={{lst:full-support-{i}}}]{{{path}}}\n'
s=s.replace('Archived calculator styling','Calculator styling').replace('Archived calculator page','Calculator page')
write(p,s)
write('Code/README.md', '''# Thesis firmware and software\n\nThe current V2 snapshot is `PWR_2_0_4`: firmware, linker/build tools, protocol and storage tests, browser runtime and tests, fonts, and supporting documentation. The F410 build identifies as PWR-2.0.4; the G071 build remains PWR-2.0.3 with fixed carrier timing. `source_manifest.json` lists the exact source hashes and `software_verification.json` records software checks.\n\n`PWR_2_0_1` is retained as a historical snapshot, including its original manifest and software verification. The separate `thesi_power_control_PWR_1_9_20.ino` remains the measured V1.0 baseline. Earlier test results are not relabelled as current-firmware tests.\n\nThe new snapshot adds browser calibration, editable reference-load/setup settings and output-OFF carrier/dead-time adjustment. The physical test load is connected separately. Powered verification remains necessary; no board is flashed by the browser application.\n''')
(r/'main-edited-files.json').write_text(json.dumps(changes,indent=2)+'\n')
