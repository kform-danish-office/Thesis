from pathlib import Path
import re,json
root=Path('/workspace/thesis');review=Path('/workspace/tooling/thesis-firmware-204')
files=['Backmatter/Appendices/C_Firmware_Documentation.tex','Backmatter/Appendices/G_Software_Tools.tex']
texts={}
for name in files:
 p=root/name;b=p.read_bytes();q=review/'before'/name;q.parent.mkdir(parents=True,exist_ok=True)
 assert not q.exists();q.write_bytes(b);texts[name]=b.decode().replace('\r\n','\n')
c=texts[files[0]]
c=c.replace('The two archived controller programs are described in \\cref{sec:ctrl-firmware-identities}. The PWR numbers name firmware revisions. PWR-1.9.20 is the baseline voltage-control firmware; the test tables state which runs used it. PWR-2.0.1 is its V2 hardware port with browser communication and can target either MCU. Reproducing a test also requires the board, calibration, and saved settings.', 'The baseline voltage-control firmware and current V2 firmware are described in \\cref{sec:ctrl-firmware-identities}. PWR-1.9.20 was used for the main V1.0 test series. The V2 firmware was extended to PWR-2.0.4 with browser calibration, reference-load settings, and adjustable carrier timing. The G071 target in the same source remains PWR-2.0.3 with a fixed carrier.')
c=c.replace('PWR_2_0_1','PWR_2_0_4').replace('lst:full-pwr201','lst:full-pwr204')
c=c.replace('PWR-1.9.20 contains 4207 lines; PWR-2.0.1 contains 4848. The line ranges below refer to the archived V2 sketch, including comments and blank lines.','PWR-1.9.20 contains 4207 lines; the current V2 sketch contains 5348 lines. The earlier V2 port is retained under \\sourcefile{Code/PWR_2_0_1}.')
c=c.replace('PWR-2.0.1 & Opt-in JSON UART, bounded transmit work, link lease, and browser diagnostics\\\\','PWR-2.0.1 & Opt-in JSON UART, bounded transmit work, link lease, and browser diagnostics\\\\\nPWR-2.0.2 & Browser calibration with progress, cooperative stop handling, and rollback after interruption\\\\\nPWR-2.0.3 & Reference-load, tuning, and precharge settings with device readback\\\\\nPWR-2.0.4 & V2 carrier-frequency and dead-time adjustment while output is OFF; timing readback and saved timing/calibration records\\\\')
c=c.replace('F410 / PWR-2.0.1 target','F410 / PWR-2.0.4 target')
start=c.index('Both targets are configured for a fixed')
end=c.index('\nIn the enable scheduler',start)
c=c[:start]+r'''The G071 retains the fixed \SI{1}{\mega\hertz} center-aligned TIM1 CH1/CH2 carrier. V2 uses edge-aligned CH1/CH1N with the TIM1 dead-time unit, leaving PA9 free for USART1. The default remains \SI{1}{\mega\hertz} with \SI{40}{\nano\second} programmed dead time. At the \SI{100}{\mega\hertz} timer clock, the default period is 100 ticks, with ARR \(=99\), CCR1 \(=50\), and DTG \(=4\). CH2 is disabled. Carrier frequency and dead time are applied together while output is OFF; their adjustment is described below.''' +c[end:]
start=c.index('The aligned record is 472 bytes')
end=c.index('\nOnly one sector',start)
c=c[:start]+r'''V2 saves a 488-byte record containing the unchanged 471-byte settings payload, a version marker, an alignment byte, requested carrier frequency and dead time, and an outer checksum. The reserved sector holds 33 new records. The loader also scans the earlier 472-byte-stride records, retaining their settings and loading the default carrier timing without writing flash at startup. New records are appended after occupied or interrupted records; the latest complete valid record is recovered after an interrupted append.

The older firmware cannot read the new record format. A downgrade can therefore load older settings or defaults. The configuration must be exported before changing back to an earlier firmware.''' +c[end:]
c=c.replace('Settings can be written only with output OFF, no autotune, and no active startup.','Settings can be written only with output OFF, no autotune, no calibration transaction, and no active startup.')
c=c.replace('Some earlier tests have no complete settings export. Their missing settings remain unknown.','For V2, \\texttt{TIMING} also prints the requested pair and exact timer ratios.')
c=c.replace('Terminal command families in the archived V2 firmware.','Terminal command families in the V2 firmware.')
c=c.replace('\\texttt{ON}, \\texttt{OFF} & Change live state.', '\\texttt{TIMING}; \\texttt{TIMING Hz ns} & V2 only: read the current carrier pair or apply a new pair while OFF and idle.\\\\\n\\texttt{ON}, \\texttt{OFF} & Change live state.')
c=c.replace('parser bounds, and archived V2 defaults','parser bounds, and V2 defaults')
c=c.replace('\\texttt{AUTOMAX} & Tune maximum duty 0--100\\%, default 100, limited by DMAX.','\\texttt{AUTOMAX} & Scan-range setting 0--100\\%, default 100, limited by DMAX. Minimum-duty and step rules can raise scan points above a low AUTOMAX; DMAX remains the duty ceiling.')
c=c.replace('\\texttt{ACTIVELOAD} & Profile 1--3;', '\\texttt{ACTIVELOAD} & Profile 1--3;')
c=c.replace('Firmware, board, baud, maximum line length, and the lease requirement are reported.','Firmware, board, baud, maximum line length, lease requirement, and supported capabilities are reported. The V2 build advertises \\texttt{calibration\\_v1}, \\texttt{bench\\_settings\\_v1}, and \\texttt{carrier\\_timing\\_v1}; the last capability is V2-only.')
c=c.replace('Enter quiet JSON mode; or acknowledge and queue one telemetry frame.','Enter quiet JSON mode; or acknowledge and queue telemetry with V2 timing readback.')
c=c.replace('Apply validated RAM settings or profile 1--3. Boot-preference changes are terminal-only.','Apply validated RAM settings or profile 1--3. Reference-load, tuning, precharge, and slot changes require OFF. Boot-preference changes are terminal-only.')
c=c.replace('\\texttt{BEGINCFG}; \\texttt{ENDCFG}; \\texttt{SAVE} & Group changes;', '\\texttt{CAL PRECHARGE}, \\texttt{CAL NOLOAD}, \\texttt{CAL LOAD n} & Queue startup or duty tuning, with output initially OFF and an active lease.\\\\\n\\texttt{CAL ZERO}; \\texttt{CAL LINE} & Queue current-offset or line-reference capture.\\\\\n\\texttt{TIMING Hz ns} & V2 only: apply an OFF-state carrier/dead-time pair and return matching timing readback.\\\\\n\\texttt{BEGINCFG}; \\texttt{ENDCFG}; \\texttt{SAVE} & Group changes;')
c=c.replace('Blocking autotuning, current-zero capture, presets, defaults, and the large export are not web commands.','Calibration is requested through the queued \\texttt{CAL} commands. Terminal presets, defaults, \\texttt{CAL3}, and the large text export are not web commands.')
c=c.replace('Periodic telemetry is queued only while two slots remain free, leaving room for acknowledgments and events.','Periodic V2 telemetry and timing frames are queued together only when two further slots remain free for acknowledgments and events.')
c=c.replace('selected validated settings, lease/stream state, pending settings, and control timing.','selected validated settings, calibration state, lease/stream state, pending settings, and control timing.')
start=c.index('\\section{Function Map and Build Dependencies}')
end=c.index('\nThe sketch is built',start)
c=c[:start]+r'''\section{Browser Calibration and Reference Loads}
\label{sec:app-fw-web-calibration}

The browser calibration commands reuse the precharge, duty-scan, current-offset, and line-reference routines. Commands are queued first and run outside the serial parser. Serial input, telemetry, faults, and the communication lease continue to be serviced during measurement waits. The browser can therefore stop an active scan without waiting for the complete tuning sequence.

Calibration starts with output OFF, valid feedback, no fault, and an active lease. Precharge and duty tuning then energize the converter; current-zero and line-reference capture keep output OFF. OFF, lease expiry, a fault, lost acquisition, or the \SI{180}{\second} limit cancels the run. Every outcome leaves output OFF. Cancellation or failure restores the previous settings; successful results remain in RAM until an explicit save. The stored boot preference and previous control mode are retained.

The three resistance entries describe the physical loads connected by the operator. Entering \texttt{LOAD1}, \texttt{LOAD2}, or \texttt{LOAD3} does not switch a resistor or command an electronic load. Zero means the reference is unconfigured. \texttt{LOAD n} selects a slot and applies its stored profile when valid; \texttt{ACTLOAD} reports the selected slot. Each physical load is connected with output OFF before its calibration is started.

The browser also exposes the no-load duty, coarse/fine scan steps, measurement and settling intervals, and startup burst/settle timing. These settings are populated from MCU readback. Their edits and reference-slot changes require output OFF, so setup changes do not silently alter an active tuning run.

\section{Adjustable V2 Carrier Timing}
\label{sec:app-fw-carrier-timing}

\texttt{TIMING Hz ns} accepts carrier requests from \SI{500}{\kilo\hertz} to \SI{2}{\mega\hertz} and dead-time requests from \SI{20}{\nano\second} to \SI{200}{\nano\second}. These are timer limits; the usable converter range must be established from switching and thermal measurements. The command is rejected during output, startup, autotuning, or queued/running calibration. Frequency and dead time are applied atomically with enable held low.

With prescaler zero, the period is rounded to an even number of timer ticks, and dead time is rounded up to a whole tick. At \SI{100}{\mega\hertz}, the period grid is \SI{20}{\nano\second} and the dead-time grid is \SI{10}{\nano\second}. The pair must satisfy \(4N_{\mathrm{dead}}<N_{\mathrm{period}}\). For example, a request of \SI{950}{\kilo\hertz} and \SI{53}{\nano\second} gives 106 period ticks and six dead-time ticks: approximately \SI{943.396}{\kilo\hertz} and \SI{60}{\nano\second}. At \SI{2}{\mega\hertz}, \SI{120}{\nano\second} is accepted but \SI{130}{\nano\second} is rejected.

\texttt{FEN} remains the separate burst-enable frequency. Carrier adjustment changes the excitation frequency; the tank's natural resonance remains set by its inductance and capacitance. An effective change to period or dead-time ticks clears all three learned load profiles and tuned metadata. Physical resistance entries, sensor calibration, and applied duty settings are retained. The profiles must be retuned for the new timing.

A dedicated timing frame reports requested and actual values, timer clock, period/dead-time ticks, output/busy state, and a volatile revision counter. The browser requires fresh OFF/idle readback and a matching acknowledgment before confirming an applied pair. A register-verification failure inhibits output. Browser timing changes remain pending until SAVE while OFF; terminal changes before \texttt{WEB HELLO} retain the existing deferred auto-save after \SI{1.5}{\second} of quiet OFF operation.

\section{Function Map and Build Dependencies}
\label{sec:app-fw-functions}

The principal functions are listed by task. Complete implementations are in Listing~\ref{lst:full-pwr204}; the earlier voltage-control baseline is Listing~\ref{lst:full-pwr1920}.
\begingroup
\small
\begin{longtable}{@{}L{0.25\linewidth}L{0.67\linewidth}@{}}
\caption{V2 firmware functions.}\label{tab:app-fw-function-map}\\
\toprule Task & Functions\\\midrule
\endfirsthead
\toprule Task & Functions\\\midrule
\endhead
Settings and profiles & \nolinkurl{setDefaults}, \nolinkurl{validateSettings}, \nolinkurl{loadProfileValid}, \nolinkurl{storeLoadProfile}, \nolinkurl{applyLoadProfile}\\
Saved settings & \nolinkurl{loadSettings}, \nolinkurl{validCarrierRecord}, \nolinkurl{safeToWriteEepromNow}, \nolinkurl{saveSettingsNow}, \nolinkurl{flushPendingSettingsSave}\\
Carrier timing & \nolinkurl{calculateCarrierTiming}, \nolinkurl{calculateGateTiming}, \nolinkurl{setupGatePWM}, \nolinkurl{applyCarrierTiming}\\
Burst scheduling & \nolinkurl{updateEnableTimingNoInterruptLock}, \nolinkurl{applyEnableTimerNoInterruptLock}, \nolinkurl{enPeriodISR}, \nolinkurl{enCompareISR}\\
Acquisition and conversion & \nolinkurl{setupAdcDma}, \nolinkurl{readPrimaryVoltageRaw}, \nolinkurl{readSecondaryVoltageRaw}, \nolinkurl{readPrimaryCurrentRaw}, \nolinkurl{updateAnalogFilters}\\
Startup and voltage control & \nolinkurl{beginStartupPrecharge}, \nolinkurl{handleStartupPrecharge}, \nolinkurl{handlePowerLoop}, \nolinkurl{loadedSteadyDutyX10}\\
Fault handling & \nolinkurl{checkFaults}, \nolinkurl{latchFault}, \nolinkurl{serviceNoLoadSoftOvp}\\
Tuning and calibration & \nolinkurl{autoTunePrecharge}, \nolinkurl{autoTunePower}, \nolinkurl{zeroCurrentOffset}, \nolinkurl{runWebCalibration}, \nolinkurl{serviceWebCalibrationWait}\\
UART and web protocol & \nolinkurl{processCommand}, \nolinkurl{processWebCommand}, \nolinkurl{webQueueTelemetry}, \nolinkurl{serviceWebTelemetry}, \nolinkurl{serviceWebLease}, \nolinkurl{serviceWebTx}\\
Foreground execution & \nolinkurl{setup}, \nolinkurl{loop}\\
\bottomrule
\end{longtable}
\endgroup
''' +c[end:]
start=c.index('Both archived V2 firmware targets were rebuilt')
c=c[:start]+r'''The V2 build and the G071 regression target were compiled, and the firmware image, protocol, saved-settings journal, and browser tests were checked. Powered switching, sensing accuracy, and on-board persistence still require bench verification.

\begin{table}[htbp]
\centering
\small
\caption{Software checks for the current firmware and browser.}
\label{tab:app-fw-software-checks}
\begin{tabularx}{\textwidth}{@{}L{0.25\textwidth}Y@{}}
\toprule Check & Result\\\midrule
V2 build & Passed; 90,268 program bytes of 98,304; 6,868 static RAM bytes of 32,768\\
G071 regression build & Passed; 130,424 program bytes of 131,072; 9,544 static RAM bytes of 32,768\\
V2 HEX layout & Passed; 90,752 programmed bytes; valid vectors and reserved settings sector excluded\\
Host protocol & Passed; 131 JSON frames with mocked hardware\\
Saved-settings journal & Passed; legacy migration, corruption, torn records, and 122 interrupted-append boundaries\\
Browser tests & Passed; 76 automated tests\\
\bottomrule
\end{tabularx}
\end{table}

Program size and HEX programmed-byte count use different counting methods. Static RAM excludes later stack and heap demand. These checks exercise software and image layout; the measured converter results remain those described in Chapter~\ref{ch:results}.
'''
(root/files[0]).write_text(c)
g=texts[files[1]].replace('PWR_2_0_1','PWR_2_0_4').replace('PWR-2.0.1','PWR-2.0.4')
g=g.replace('the archived V2 interface still needs testing with the powered converter.','the current V2 interface adds calibration, reference-load setup, and carrier timing.')
g=g.replace('The archived PWR-2.0.4','The current PWR-2.0.4')
g=g.replace('Page structure, controls, status labels, and responsive layout.','Monitor, Setup, Calibration, and Sessions views, global OFF controls, status labels, and responsive layout.')
g=g.replace('CSV and download helpers.','CSV and download helpers, including per-sample carrier timing.')
g=g.replace('\\sourcefile{server.mjs}, \\sourcefile{build.mjs} &','\\sourcefile{resonance.js}, \\sourcefile{resonance-ui.js}, \\sourcefile{resonance-presets.js} & Tank and pump calculations, calculator controls, and component presets.\\\\\n\\sourcefile{server.mjs}, \\sourcefile{build.mjs} &')
g=g.replace('No \\texttt{ON} or preset settings are sent, so connecting the\ninterface leaves the existing bench configuration unchanged.','No \\texttt{ON} or preset settings are sent when connecting.')
needle='\\texttt{DeviceLink.startDemo} uses a separate synthetic device'
idx=g.index(needle)
g=g[:idx]+r'''The Setup view adds physical reference-load resistance entries, profile selection, no-load duty, tuning steps and waits, and precharge timing. The resistances describe loads attached by the operator; they do not command or switch the load. These settings require output OFF and the \texttt{bench\_settings\_v1} capability.

The Calibration view queues precharge, no-load, individual load-slot, current-zero, and line-reference routines. Progress and completion come from MCU telemetry. Each reference load is connected with output OFF before its slot is started. OFF cancels the run, and successful calibration still requires an explicit save. The firmware's \texttt{calibration\_v1} capability and fresh state determine whether these controls are available.

V2 carrier controls apply switching frequency and dead time as one OFF-state pair. The draft preview is kept separate from actual device readback. The interface confirms the change only after receiving both its acknowledgment and matching timing frame; stale or mismatched readback leaves the operation unconfirmed. The timer limits and quantization are given in \cref{sec:app-fw-carrier-timing}. A timing change invalidates learned load profiles, which must be retuned.

''' +g[idx:]
g=g.replace('The interface, controls, and exports can be tested without the\ngenerated values being presented as converter measurements.','The display, basic controls, synthetic timing, and exports can be checked without a connected board. Demo cannot run physical calibration.')
g=g.replace('JSON export keeps the complete session, including events and metadata','Each sample includes only fresh verified carrier timing. The CSV adds requested/actual carrier and dead time, timer clock, period and dead-time ticks, timing revision, receipt time, and source. Stale or missing timing fields remain blank; later metadata is not copied back into earlier samples. JSON export keeps the complete session, including events and metadata')
g=g.replace('checks and copies the six bench-interface\nfiles','checks and copies 15 application and font\nfiles').replace('The archived\ninterface can','The current\ninterface can')
start=g.index('\\section{Unfinished Calculator Page}')
end=g.index('\\section{Firmware Builds and HEX Checks}',start)
g=g[:start]+r'''\section{Resonant-Tank and Pump Calculator}
\label{sec:app-calculator-snapshot}

The calculator is included in the local server and static build. \sourcefile{resonance-ui.js} connects the page controls to the numerical routines; \sourcefile{resonance-presets.js} supplies nominal component sets and the transformer A/B measurements used for comparison.

\texttt{toSI} and \texttt{fromSI} handle explicit units. \texttt{equivalentCapacitance} combines series and parallel banks, and \texttt{equivalentSeriesInductance} sums uncoupled series inductors. \texttt{analyzeTank} solves the ideal series-LC frequency, inductance, or capacitance, with reactance, characteristic impedance, tolerance corners, and optional series-loss quantities. Leakage is referred to the resonant side and included once.

Magnetizing inductance is treated as a separate branch. \texttt{analyzeMagnetizingBranch} calculates its reactance, the magnetizing-to-series inductance ratio, and an ideal open-secondary resonance. Magnetizing inductance is therefore not added to the loaded series-resonance calculation. The pump calculator uses the approximate triangular-current sizing relationship \(L_p=1/(16C_p f_s^2)\), separately from the series-LC resonance equation.

\texttt{preferredCandidates} returns E12/E24 values, and \texttt{generateFrequencyResponse} plots the normalized series-RLC current for an entered series resistance. These models support component and operating-point comparisons; complete-converter gain, loss, and ZVS still require the full circuit and measurements. Calculator edits do not change MCU settings.

''' +g[end:]
g=g.replace('and HEX programmed-byte', 'and HEX programmed-byte')
g=g.replace('\\sourcefile{firmware/test_web_protocol.py} & Production firmware dispatcher and serializer with mocked UART, timing, settings, and control dependencies.\\\\','\\sourcefile{firmware/test_web_protocol.py} & Production dispatcher, timing math and application, scheduler, calibration cancellation, lease and queue behavior with mocked hardware.\\\\\n\\sourcefile{firmware/test_carrier_storage.py} & Production journal loader/writer, legacy records, corruption, torn writes, and interrupted appends with mocked flash.\\\\')
g=g.replace('\\sourcefile{web/tests/resonance.test.mjs} & Unit conversion, bank topology, inverse LC solves, leakage handling, tolerance corners, reactance, series-loss response, preferred values, and invalid inputs.','\\sourcefile{web/tests/resonance.test.mjs}, \\sourcefile{web/tests/resonance-presets.test.mjs} & Unit conversion, bank topology, inverse LC solves, leakage and magnetizing branches, pump sizing, tolerance corners, preferred values, and presets.')
start=g.index('All 38 Node tests passed')
end=g.index('\\section{Checking Measurements',start)
g=g[:start]+r'''All 76 Node tests passed, including protocol, timing/readback, calibration transport, session export, and calculator checks. The firmware harness extracts production code and runs it with mocked hardware. Its 131 JSON frames cover command dispatch, timing-pair quantization and rejection, OFF/busy conditions, calibration cancellation and rollback, lease expiry, bounded transmission, and readback failure. Journal tests cover legacy migration and all 122 interrupted-append word boundaries. The Linux host checks were run with a native C++ compiler; the Windows/MSVC runner was not executed.

Powered tests must check UART wiring, sensing gains, gate and enable timing, calibration response, on-board persistence, and link-loss stop behavior.

''' +g[end:]
(root/files[1]).write_text(g)
print('Updated two appendices')
