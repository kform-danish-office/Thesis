# Converter test bench

Browser control and experiment logging for the current thesis converter firmware.
The app is a dependency-free static website for Vercel. USB communication runs on
the computer viewing the website; Vercel does not open the serial port. Session
records stay in that browser's IndexedDB and can be downloaded as CSV or JSON.
There is no cloud database, remote access to the bench, or account requirement.

**Live app:** <https://thesis-power-lab.vercel.app>

V2 timing controls require matching F410 firmware, available as the
[PWR-2.0.4 pre-release](https://github.com/kform-danish-office/Thesis/releases/tag/pwr-2.0.4); powered bench validation remains pending. Updating the browser app does not flash a board.

## Resonant-tank calculator

Open **Calculator** in the navigation. It opens in a separate tab so USB control
and recording can continue in the monitor. Pick a schematic/document preset,
choose frequency, discrete inductance, or equivalent capacitance as the unknown,
then edit the other inputs. Results update immediately. Reload preset restores
its starting values.

Five presets cover the tested V1.0 thesis model, supplied transformer A,
the latest F410 drawing, an explicitly assumed F410 comparison, and V1.1.
Unvalued C26 and unspecified transformer leakage stay blank. A blank leakage
field is explicitly assumed zero; enter the primary-referred value when known.
The 1 nF thesis value is an equivalent tank capacitance, not an inferred physical
capacitor population. Magnetizing L is excluded from series L.

The optional transformer reference applies measured leakage and magnetizing
inductance together for transformer A or B as a comparison; installed identity
is unknown. Lm is a parallel branch, so it does not change the series-resonance
equation. The diagram and separate branch results show Xm, Lm/Lr and an ideal
open-secondary LC frequency with explicit assumptions. This is not loaded
converter gain, operating frequency or a ZVS prediction. Unknown Lm stays blank.

The calculator supports series/parallel capacitor entries, editable design
ranges, reactance or positive-R normalized current plots, E12/E24 comparisons,
and CSV/JSON calculation records. The separate charge-pump panel uses the
thesis triangular-current sizing relation. These calculations do not apply
settings to hardware. See [source evidence and equations](../docs/calculator-evidence.md).

## Start

From this folder, run `node server.mjs`, then open <http://localhost:4173> in
desktop Chrome or Edge. Click **Demo** to inspect the interface with synthetic
data. Demo sessions are marked `demo` in the app and exports.

V2 carrier/deadtime controls require **PWR-2.0.4 on F410** and the advertised
`carrier_timing_v1` capability. **G071 remains PWR-2.0.3** with its fixed carrier;
its existing monitor, calibration and bench-settings features remain available.
Build the appropriate target and follow its bench bring-up procedure separately:

```powershell
cd C:\Users\multi\Documents\Thesis
.\firmware\build.ps1 -Target F410
# Or: .\firmware\build.ps1 -Target G071
```

Build outputs are `arduino-build-f410/` and `arduino-build-g071/`. For F410,
use the HEX and custom linker from the build script; a BIN spans the reserved
settings sector. Follow [the existing board notes](../docs/stm32f410-port.md)
for flashing and board verification. The app does not flash hardware.

Connect an appropriate **isolated USB-to-3.3 V-UART interface** when the
controller is referenced to the live primary side. An unisolated PC USB ground
must not be connected to a mains-powered primary ground. With the bench
appropriately de-energized, wire:

| Adapter | F410 schematic-12 board | Original G071 |
| --- | --- | --- |
| RX | PA9 TX (J3 pin 5) | PC4 TX |
| TX | PA10 RX (J3 pin 6) | PC5 RX |
| Isolated UART-side reference | Board signal reference | Board signal reference |

Use **115200 baud, 8 data bits, no parity, 1 stop bit, no flow control**.
Close other serial monitors before clicking **Connect USB** and selecting the
adapter's serial port. These boards expose a UART command path; plugging in a
USB cable alone does not add native USB CDC to the firmware.

## Workspace views and device setup

- **Monitor** shows live measurements, the scope, output and mode controls.
- **Setup** contains voltage limits and physical load references. V2 switching/
  carrier timing, duty/EN timing, calibration-scan settings, startup precharge,
  wiring help and the terminal use expandable sections.
- **Calibration** contains the hardware auto-calibration workflow.
- **Sessions** contains recording and saved experiments. Recording continues when
  changing views; the global recording bar provides Stop and save.

Navigation preserves the USB connection. Output OFF remains available in every
view. The calculator opens separately so it does not interrupt recording.

Load references and the extended tuning controls require a board advertising
`bench_settings_v1` (PWR-2.0.3). Controls use reported values; unsupported or missing
readback remains disabled. Demo provides clearly marked synthetic settings for
trying the interface; it cannot calibrate real hardware.

With output OFF, enter each physical reference resistance in **Setup**, then
**Apply changes** and check readback. `LOAD1`–`LOAD3` accept 0–100000 Ω; 0 means
unconfigured, not a short circuit. These entries describe physical loads that
the operator connects; the app does not set or switch an electronic load.
Selecting a reference slot uses its stored settings when a profile exists. The
reported slot is not proof of valid calibration or of the attached load.

The expandable controls cover no-load duty, tune duty limit/coarse/fine steps,
measurement settling/window, and startup burst timing/count. Their ranges match
[the protocol specification](../docs/web-protocol.md#pwr-203-bench-settings-capability).
The existing calibration scan can raise a low tune limit to meet its minimum duty
and step rules; DMAX remains the output ceiling. Advanced settings and slot
selection require output OFF. Ordinary voltage controls retain their existing
behavior. Apply updates RAM; **Save to device** with output OFF writes settings
to device flash. **Reset edits** discards unsent form changes.

Open the collapsed **V2 switching/carrier timing** section in Setup to edit the
carrier and complementary-gate deadtime together. It requires fresh, validated
timing and telemetry readbacks, output OFF, an idle startup/calibration state
and no conflicting form edits. Apply or reset other setting/mode/slot edits
first. Output OFF remains available and cancels queued timing commands.

Enter whole numbers from **500000–2000000 Hz** and **20–200 ns**. These are timer
bounds, not an electrically validated operating range. TIM1 uses even
edge-aligned period ticks for balanced CH1/CH1N; deadtime rounds up to a tick.
At a 100 MHz timer clock, requesting 950000 Hz / 53 ns produces 106 period ticks /
6 deadtime ticks, reported as 943396 Hz / 60 ns. At 2 MHz the maximum accepted
deadtime is 120 ns; 130 ns is rejected. The separate draft preview is not device
readback. Apply succeeds only after its acknowledgement and matching timing
readback agree. Stale or incomplete data keeps the controls locked.

A change to actual timing clears the three learned load profiles, tuned
metadata and previous calibration-completion state. Physical `LOAD1`–`LOAD3`
resistances are retained; retune explicitly. Web timing changes stay in RAM
until **Save to device** with output OFF persists timing and calibration together.
The default is still 1 MHz / 40 ns, but F410 changes from center- to edge-aligned
carrier timing; steady waveforms and first-pulse phase need scope verification.
Natural LC resonance is set by the circuit components. `FEN` is a separate EN
burst frequency. See [candidate notes](../firmware/releases/pwr-2.0.4.md) before
flashing or downgrading.

## Hardware auto-calibration

The Calibration view includes startup precharge, no-load cap, individual load-slot tuning,
current-zero and line-reference controls. These require a connected board
advertising `calibration_v1` in firmware PWR-2.0.2 or newer; legacy boards and Demo cannot
start hardware calibration. Prepare the physical reference, turn output OFF,
apply/reset any pending edits, choose the routine/slot and confirm before Start.

Stop / output OFF remains available. The firmware services UART and the lease
inside calibration waits and cancels after180 seconds, lease loss, faults or OFF.
All outcomes leave output OFF; unsuccessful runs restore the pre-run settings.
Successful results stay in RAM until explicitly saved. Repeat one physical load
slot at a time, changing loads only while output is OFF. The browser cannot
switch physical loads. Current zero requires no sensed current. Line capture
records the primary reference and enables line feed-forward.

A configured positive reference resistance is required for load-slot calibration
when bench-settings readback is available. See [current build notes](../firmware/releases/pwr-2.0.3.md). Software/native tests
use mocks for physical measurement steps; powered bench performance, actual stop
latency, calibration quality and on-board flash behavior remain unverified. This
web update does not flash a board or make PWR-2.0.1 calibration-capable.

## Control and logging

- Connection negotiates the web protocol, arms a 5-second communication lease,
  and requests telemetry every 500 ms. Connection does not send ON or apply
  preset settings. Forms use values reported by the board.
- ON requires a negotiated connection, fresh telemetry, a live lease, and no
  reported fault. Commands report rejection/timeout instead of claiming success.
  Device telemetry confirms output and settings; firmware remains authoritative.
- OFF takes priority over queued app commands. Disconnect requests OFF before
  closing the port. On cable removal, tab closure, or suspended browser,
  heartbeat loss causes the firmware to turn output OFF within the active
  lease (normally 5 seconds). This software timeout is not a physical emergency
  disconnect and has not been validated electrically on a powered converter.
- Setting changes apply in RAM. Use explicit SAVE with output OFF to persist
  them in the board's nonvolatile storage. The firmware keeps its existing
  validation/clamping and protections. Legacy raw tuning and boot-setting commands
  remain unavailable in web sessions; supported calibration uses the dedicated CAL dispatcher; the UART
  terminal retains those workflows.
- Name a session, enter bench notes, then record. Local sessions include host
  receipt times, device uptime, measurements, settings, source, firmware, and
  command events. Each sample also carries the fresh timing readback available
  at capture; missing/stale timing stays blank. CSV adds `requestedcarrier_Hz`,
  `actualcarrier_Hz`, `requesteddeadtime_ns`, `actualdeadtime_ns`, `timer_clock_Hz`,
  `period_ticks`, `dead_ticks`, `timing_revision`, `timing_received_at` and
  `timing_source`. JSON also includes timing changes as events and metadata.
  Earlier samples are never backfilled from later session metadata.
  Export important sessions: browser storage can be cleared or evicted and is
  specific to this browser and website origin.
- PA2 is half-bridge current feedback. The displayed current and derived power
  are **diagnostics**, not calibrated secondary load current/output power.
  The 100 W label is the thesis design target, not a measured performance claim.

Web Serial needs a supported desktop browser and HTTPS or localhost. A browser
without Web Serial can still run Demo and manage local logs. An embedded app
preview may restrict serial access: use the deployment URL in desktop Chrome
or Edge for the actual USB connection.

## Build and deploy to Vercel

```powershell
cd C:\Users\multi\Documents\Thesis\web
node --test tests/*.test.mjs
node build.mjs
```

In Vercel, select **web** as the project root, framework **Other**, build
`node build.mjs`, and output directory `dist`. No install step, secrets,
environment variables, database, or paid integration is required. Alternatively
run the Vercel CLI from this folder using your authorized team/account.
Only the app's static files and licensed local fonts are included in `dist`; thesis documents,
firmware source, logs, local credentials, and test tools are not deployed.

`vercel.json` supplies a restrictive content policy, local-origin serial
permission, and cache revalidation. The same headers are used locally.

## Implementation

- `app.js`, `index.html`, `styles.css`: dashboard, controls, charts and sessions.
- `serial.js`: real Web Serial transport, correlated acknowledgments, stale-data
  interlock, lease heartbeat, command queue and clearly labeled simulator.
- `protocol.js`: bounded line framing and validated protocol parsing.
- `storage.js`: IndexedDB sessions and spreadsheet-safe CSV export.
- `calculator.html`, `calculator.css`, `resonance-ui.js`: editable calculator UI.
- `resonance.js`: SI-only LC/RLC and separate charge-pump mathematics.
- `resonance-presets.js`: source-backed starting values and explicit unknowns.
- [Protocol specification](../docs/web-protocol.md): firmware commands and frames.

See [verification results](VERIFICATION.md) for the checks actually completed.
