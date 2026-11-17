# Browser control and logging protocol

The root `thesi_power_control.ino` builds `PWR-2.0.4` for V2 / STM32F410 and
`PWR-2.0.3` for the original G071. The opt-in UART web session was introduced in
`PWR-2.0.1`; later features are negotiated by capability. F410 alone adds
adjustable switching-carrier/deadtime timing. A browser connection never enables
the converter automatically. The F410 build is a software-validated pre-release with powered bench verification pending.

## USB connection

The F410 build uses a **USB-to-3.3 V UART adapter**, not native USB firmware.
Use 115200 baud, 8 data bits, no parity, one stop bit, no flow control.

| Board | Adapter RX connects to | Adapter TX connects to |
| --- | --- | --- |
| STM32F410CBU6 | PA9 TX, J3 pin 5 | PA10 RX, J3 pin 6 |
| STM32G071 | PC4 TX | PC5 RX |

Connect the adapter reference ground to the board's UART ground only through
the appropriate bench isolation arrangement. The F410 UART is on the primary
MCU domain; a normal USB-UART adapter does not provide galvanic isolation. Do
not connect a computer ground to an energized, nonisolated mains-referenced
primary. Use a suitably rated isolated UART/USB interface and the bench's
established isolation procedure. Do not feed a 5 V UART signal into these pins.
See `stm32f410-port.md` for the existing divider-population verification notes.

The web app uses Web Serial in desktop Chrome or Edge in a secure context
(Vercel HTTPS or localhost). The user selects and grants access to the serial
port in the browser. USB bytes flow directly between browser and adapter;
Vercel hosts the application and does not connect to a USB port itself.

## Framing and session

Send one ASCII command per line, accepting LF, CR, or CRLF. A command line may
contain at most 96 characters excluding its terminator. Overlong or invalid
lines are rejected in full rather than executed after truncation. Replies are
newline-delimited JSON objects. Ignore terminal boot text and echo before the
first JSON hello.

```text
WEB HELLO
WEB c1 SNAPSHOT
WEB c2 STREAM 500
WEB c3 LEASE 5000
WEB c4 PING
```

`WEB HELLO` enters a quiet web session that persists until reset. It does not
change output, stream settings, boot settings, or the lease. If an earlier
terminal session enabled output, a hello does not turn that existing output off.
The browser must inspect the snapshot and explicitly apply the intended action.

```json
{"type":"hello","protocol":1,"fw":"PWR-2.0.4","board":"STM32F410CBU6","baud":115200,"max_line":96,"lease_required":true,"capabilities":["calibration_v1","bench_settings_v1","carrier_timing_v1"]}
```

Use `WEB <id> <command>` for commands after hello. IDs are 1–24 ASCII letters,
digits, hyphens, or underscores. Use a new ID for each command and serialize
commands: await the matching acknowledgement before sending the next one.
For `TIMING`, also await the matching-ID timing readback described below.

```json
{"type":"ack","protocol":1,"id":"c3","ok":true,"code":"lease_armed","settings_pending":false}
```

`ok` reports execution of that supported operation. An accepted SET reports
`applied_pending`, meaning applied in RAM using the existing validation/clamps;
request a snapshot to read the effective settings. It does not mean that the
requested value was stored exactly or saved to flash. Validation and unsupported
commands produce `ok:false` with a reason. Timeout means unknown completion;
resynchronize with SNAPSHOT and never automatically retry ON or a mutation.

For terminal diagnostics, `WEB SNAPSHOT`, `WEB STREAM <ms>`, `WEB LEASE <ms>`,
and `WEB PING` also work without an ID and return an empty acknowledgement ID.

## Supported web commands

| Command | Behavior |
| --- | --- |
| `SNAPSHOT` | Acknowledgement followed by telemetry; F410 also sends a matching-ID timing frame |
| `STREAM 500` | Set periodic telemetry interval; valid 250–5000 ms |
| `STREAM 0` | Stop periodic telemetry |
| `LEASE 5000` | Explicitly arm a 1000–10000 ms link lease; renew with PING |
| `LEASE 0` | Disarm lease only while output is OFF; otherwise reject |
| `PING` | Renew an already armed lease; cannot rearm an expired lease |
| `ON` | Require live lease, no latched fault, working ADC/gate/storage initialization; begin existing nonblocking startup |
| `OFF` | Disable through existing output-off path, without flash writes |
| `OPEN`, `VSB`, `BANG`, `VSBONLY`, `LINEFF` | Apply existing mode behavior in RAM |
| `CLR` | Clear fault only while OFF and required hardware initialization is healthy |
| `SET NAME number` | Existing setting parser and limits, strict finite numeric input, apply in RAM |
| `LOAD 1..3` | Apply existing selected load profile in RAM |
| `TIMING Hz ns` | F410 `carrier_timing_v1` only: atomically apply an OFF-state carrier/deadtime pair and return timing readback |
| `BEGINCFG` | Begin explicit configuration import |
| `ENDCFG` | End import and save with output OFF; report save failure |
| `SAVE` | Save with output OFF and import completed; report save failure |

Negative values are accepted only for signed offsets, integral limits, and
stored secondary-voltage measurements. Boot-on parameters are terminal-only.
Autotuning, ZEROI, large textual exports, presets, and defaults are not exposed
through this bounded web dispatcher. They return `unsupported_web_command`.
After entering web mode, other plain terminal commands are rejected. A plain
`OFF` remains available as an emergency command. Reset restores terminal mode.

Web changes do not automatically write flash while idle. Output OFF and lease
expiry do not save pending settings. Use explicit SAVE or ENDCFG while OFF.
`settings_pending` remains true after a failed save. On the F410, actual save
success is based on the existing flash writer's result; on the G071 it retains
the existing EEPROM driver's reporting limitations. Frequent saves are not
required for logging.

## Link lease

Only LEASE arms the watchdog. Hello, snapshots, and stream setup do not arm it.
Renew at approximately 1000 ms for a 5000 ms lease. If renewals stop, firmware
calls the existing output-off path and forces EN low before any serial output,
sets stream interval to zero, disarms the lease, and queues:

```json
{"type":"event","protocol":1,"event":"lease_expired","ms":25000,"enabled":false}
```

The session remains quiet. To resume, explicitly arm a new lease and enable
output again. Browser tab suspension/background timer throttling can expire a
lease. The browser should also stop renewing if telemetry becomes stale or its
serial connection fails. Graceful disconnect should request OFF before closing;
the lease covers abrupt USB removal or browser termination after it was armed.

This is a loop-serviced communications guard, not an independent hardware
watchdog or emergency stop. Hardware faults, CPU stalls, and external power
circuit behavior require the existing independent bench protections.

## Telemetry

```json
{"type":"telemetry","protocol":1,"ms":12000,"enabled":false,"mode":"VSB","fault":"NONE","feedback_valid":true,"vpri":155.000,"vsec":28.000,"current":0.150,"power":4.200,"duty":0.000,"adc":[1274,1160,180],"settings":{"VSET":28.000,"VON":28.000,"VMIN":10.000,"VMAX":32.000,"OVP":36.000,"OVPEN":1,"DMAX":100.000,"OD":0.000,"BHIGH":100.000,"STATIC":1,"FEN":10000},"lease_ms":4500,"lease_duration_ms":5000,"stream_ms":500,"settings_pending":false,"control_dt_us":25,"control_max_us":140,"control_overruns":3}
```

- `ms` is MCU uptime in milliseconds and wraps at 2^32. Timestamp logs on the
  computer too, and create a new session after an MCU reset.
- Voltages are V; `current` is PA2-derived half-bridge/primary current in A;
  `power` is the selected diagnostic V×I proxy in W. Neither current nor power
  is a calibrated secondary-output current/power measurement or efficiency.
- `duty` is the effective EN duty percentage from firmware state, not a measured
  oscilloscope duty. `adc` is the raw PA0/PA1/PA2 12-bit ADC sample array.
- Measurements are `null` when ADC/filters are unavailable or a value is
  nonfinite/out of the serializer's numerical range. Missing values must remain
  missing in saved data rather than becoming zero.
- `enabled` is the software enable request. A latched fault inhibits output even
  if that flag is true; always interpret it with `fault` and `duty`.
- `lease_ms` is remaining time; `lease_duration_ms` is configured duration.
  Both are zero once disarmed. `stream_ms` is zero when stopped.
- `settings` contains actual validated values at capture, and timing values are
  diagnostics in microseconds. Requested loop rate is not a hardware guarantee.
- Fault transitions queue `{"type":"event","protocol":1,"event":"fault",...}`.

Transmit work is bounded to at most 16 bytes per loop and guarded by
`availableForWrite()`. Four fixed 1024-byte frame slots preserve whole JSON
lines. Periodic samples are dropped when congested, leaving slots for replies
and events. Mutations are not executed when there is insufficient room to queue
an acknowledgement. A client should tolerate skipped samples and command
timeouts. Firmware never waits for the host to read telemetry.

## Build verification

Use `firmware/build.ps1 -Target F410` or `-Target G071`. Optional
`-BuildDirectory .\arduino-build-f410-web` selects a fresh build location if an
older build cache or directory cannot be reused. Check the generated sketch
contains `PWR-2.0.4` for F410 or `PWR-2.0.3` for G071; stale generated source
must not count as verification.

No automatic flashing or physical USB connection is performed by this update.
Compilation and HEX layout verification do not establish electrical correctness,
safe populated divider values, serial timing under load, or measured loop timing.

Current candidate verification uses STM32 Arduino core 2.8.1:

| Target | Program storage | Static RAM |
| --- | --- | --- |
| F410 PWR-2.0.4 | 90,268 / 98,304 bytes | 6,868 / 32,768 bytes |
| G071 PWR-2.0.3 | 130,424 / 131,072 bytes | 9,544 / 32,768 bytes |

G071 has only 648 bytes of remaining program space; its compiled behavior stays
at PWR-2.0.3. The F410 HEX verifier passes checksums, stack/reset vectors and
settings-sector exclusion. The native host harness
(`python3 /workspace/tooling/test-working-protocol-linux.py`, using the repository
harness) passes 131 JSON frames, exercising
production dispatch, timing math, retimed EN scheduling, atomic application,
readback failures, calibration invalidation, lease/queue handling and bounded
writes. Maximum tested telemetry/timing frames are 913/350 wire bytes, within
1024-byte slots. `python3 firmware/test_carrier_storage.py` exercises the
production loader/writer with mocked HAL flash, including legacy migration,
corruption and all 122 interrupted-append word boundaries. These are software
checks; actual USB, waveforms and on-board persistence remain unverified.

## PWR-2.0.2 calibration capability

The PWR-2.0.2 build advertises `capabilities:["calibration_v1"]` in HELLO. The
browser never infers support from a version string alone and requires fresh
calibration-state telemetry. Older boards remain usable for the original
monitor/control protocol; they cannot run these CAL commands. Demo is excluded.

| Command body | Routine |
| --- | --- |
| `CAL PRECHARGE` | Existing AUTOPRE startup-burst tuner |
| `CAL NOLOAD` | Existing AUTOBANG no-load-cap tuner without a load-slot write |
| `CAL LOAD 1` .. `CAL LOAD 3` | Existing tuner applied to the selected physical reference slot |
| `CAL ZERO` | Existing current-sensor offset capture; output stays OFF |
| `CAL LINE` | Capture primary reference and enable line feed-forward; output stays OFF |
| `OFF` | Cancel queued/running calibration and disable output |

CAL requires an active lease, output OFF, primed ADC feedback, ready hardware,
no fault and no config import. It acknowledges `calibration_queued`, not success.
The runner starts outside the serial parser. Existing legacy algorithms service
serial, lease, telemetry and faults inside their measurement waits, suppressing
human serial printouts to avoid interleaving JSON frame chunks. Normal legacy
terminal behavior before WEB HELLO remains available.

Telemetry adds `calibration` with integer `state` (0idle,1queued,2running,3complete,
4stopped,5failed), `kind` (1precharge,2no-load/load,3zero,4line), `slot` (0none,
1–3reference), last test `duty`, current `nlduty`/`preduty`, current-zero `offset`
and `line_ref`. Duty values are percent; voltage references are V. Fields report
device values, not physical calibration certification. State/progress can skip
intermediate phases when a routine completes between telemetry samples.

During a queued/running tune, non-monitoring mutations are rejected with
`calibration_busy_use_off`; OFF, lease/stream controls, PING and SNAPSHOT remain
serviceable. OFF is executed even if no reply queue slot remains. Lease expiry,
fault, unavailable ADC/gate hardware, OFF or the180s duration limit cancel the
run. Every outcome disables output and gates; cancellation/failure restores the
pre-run settings. A fault stays latched. Boot preference and prior control mode
are preserved. Successful results remain dirty in RAM; algorithm save attempts
cannot write flash while the calibration transaction is active. Explicit SAVE
with output OFF commits successful settings afterward.

CAL3 is intentionally not an autonomous web command. The operator must switch
physical loads while output is OFF and explicitly start each slot. No raw
terminal mode bypasses the web lease. The native harness tests protocol/runner
logic with mocked physical routines; actual powered behavior and stop latency
must be bench-validated before relying on this build on hardware.

## PWR-2.0.3 bench settings capability

HELLO additionally advertises `bench_settings_v1`. The ordinary telemetry
`settings` object now reports the following device values, allowing the browser
to populate forms from readback instead of inventing defaults:

| Key | Unit / accepted range | Notes |
| --- | --- | --- |
| `LOAD1`, `LOAD2`, `LOAD3` | Ω, 0–100000 | Physical reference-load configuration; 0 means unconfigured |
| `ACTLOAD` | integer 1–3 | Read-only selected reference-slot index; not proof of valid calibration |
| `NLDUTY` | %, 0–100 | No-load soft-switch cap |
| `AUTOMAX` | %, 0–100 | Firmware also limits this to the current DMAX |
| `AUTOSTEP` | %, 0.5–25 | Coarse duty step, quantized to 0.1% |
| `AUTOFINE` | %, 0.1–10 | Fine duty step, quantized to 0.1% |
| `AUTOSETTLE` | ms, integer 20–3000 | Settle interval before each measurement |
| `AUTOMEAS` | ms, integer 20–2000 | Measurement interval |
| `PREMS` | ms, integer 1–500 | Startup precharge burst duration |
| `PRESETTLE` | ms, integer 1–2000 | Startup precharge settle interval |
| `PREMAX` | count, integer 1–20 | Maximum startup bursts |

Use `SET <key> <value>` for editable values; use `LOAD 1` .. `LOAD 3` to select
and apply a reference profile. `ACTLOAD` is telemetry only. Setting these
resistances does not change or switch any physical resistor/electronic load.
They describe the loads connected by the operator. Selecting a slot does not
establish that its profile is valid or that the expected load is attached.

`LOAD n` and web SET mutations of load/profile, no-load duty, auto-tune and
precharge settings require output OFF (`turn_off_first`). Existing web live
voltage/duty controls retain their prior behavior. The calibration-busy guard
continues to reject all conflicting mutations while a run is queued/running.
Successful bench edits stay pending in RAM under the existing web SET wrapper;
explicit SAVE while output OFF persists them. Existing authoritative firmware
clamping/quantization and default values are unchanged.

The native harness exercises actual command dispatch/readback and OFF/busy
preconditions with mocked physical SET/profile routines. Maximum supported
bench settings, long measurements and saturated diagnostic counters serialize
as a 913-byte wire JSON frame, below the existing 1024-byte frame buffer. Both
board builds pass; G071 has limited remaining flash headroom. No powered bench
operation or new physical-load control is established by these software checks.

## PWR-2.0.4 carrier timing capability

Only V2 / F410 advertises `carrier_timing_v1`; G071 remains PWR-2.0.3 with its
fixed carrier. Clients must check the capability and validated readback rather
than infer support from a firmware string. The carrier drives PA8/PB13 TIM1
CH1/CH1N. `FEN` still controls the separate EN burst frequency; changing the
carrier does not change the circuit's natural LC resonance.

```text
WEB t1 TIMING 950000 53
```

`TIMING` accepts exactly two unsigned decimal integers, in Hz and ns:

| Quantity | Accepted request | Timer result |
| --- | --- | --- |
| Switching carrier | 500000–2000000 Hz | Nearest even edge-aligned period tick count, prescaler 0 |
| Complementary-gate deadtime | 20–200 ns | Rounded up to a timer tick; linear DTG encoding |
| Pair constraint | Both requests in range | `4 * dead_ticks < period_ticks`; otherwise reject the whole pair |

These bounds describe timer representability, not an electrically validated
operating range. At a 100 MHz timer clock, frequency uses a two-tick period grid
(about 20 kHz steps near 1 MHz), and deadtime uses 10 ns ticks. At 2 MHz, 120 ns
is the maximum accepted deadtime: 130 ns, or a request that rounds to 130 ns,
is rejected. Do not treat the two independent request ranges as all valid pairs.

Firmware rejects an enabled output, active startup, autotune or queued/running
calibration. It checks OFF/idle again under an interrupt lock, keeps EN low and
applies ARR, CCR1 and DTG together. Register verification failure inhibits output
and reports `timing_readback_failed`. Invalid pairs leave the old timing intact.
Successful application reports `timing_applied_pending` and sends a timing frame
with the same command ID. Relevant errors include `use_timing_hz_ns_integers`,
`timing_pair_not_representable`, `turn_off_first`, `hardware_not_ready` and
`calibration_busy_use_off`.

```json
{"type":"timing","protocol":1,"id":"t1","ms":12000,"timing":{"requested_hz":950000,"actual_hz":943396,"requested_dead_ns":53,"actual_dead_ns":60,"timer_hz":100000000,"period_ticks":106,"dead_ticks":6,"min_hz":500000,"max_hz":2000000,"min_dead_ns":20,"max_dead_ns":200,"revision":1,"enabled":false,"busy":false}}
```

The dedicated `timing` frame keeps the ordinary telemetry frame bounded.
F410 sends it after `SNAPSHOT`, after successful `TIMING`, and alongside periodic
stream samples. Protocol is 1; `id` is optional to clients and empty on the
firmware's periodic frames. A command reply uses its matching ID. Congested
periodic pairs are dropped together, reserving two queue slots for replies/events.

All nested numeric fields are integers. `requested_hz`/`requested_dead_ns` retain
the accepted requests. `timer_hz`, `period_ticks` and `dead_ticks` expose the
actual register timing: exact frequency is `timer_hz / period_ticks`, and exact
deadtime is `dead_ticks * 1000000000 / timer_hz` ns. `actual_hz` rounds the former
to the nearest Hz; `actual_dead_ns` rounds the latter up to a whole ns. The four
`min_`/`max_` fields report the request limits. `revision` is a volatile uint32
counter incremented on each successful application, not a saved calibration
identifier. `enabled` and `busy` report output/startup/tuning state.

The browser validates the complete math and limits before using a timing frame.
It requires fresh telemetry, a confirmed lease and timing readback younger than
2.5 seconds showing output OFF and idle. It rechecks queued requests at send
time, requires a new OFF/idle timing readback after an ON request, and gives OFF
priority. A mutation completes only after both its successful ACK and matching-ID
readback confirm the requested OFF-state pair, in either arrival order. Missing
or mismatched readback leaves completion unconfirmed; do not retry automatically.

Only a change to the actual period/deadtime ticks invalidates the three learned
load profiles, tuned metadata and prior web calibration-completion state. Physical
load resistances, sensor calibration and currently applied duty settings remain.
Retune explicitly before relying on learned profiles. Web changes remain in RAM
until SAVE with output OFF; timing and calibration persist together in the
[new F410 journal wrapper](stm32f410-port.md#saved-settings). Before WEB HELLO,
terminal `TIMING` reads the exact current pair, and `TIMING Hz ns` applies it;
the existing terminal auto-save still runs after 1.5 s quiet while OFF unless
BEGINCFG holds an import. SAVE/ENDCFG can also persist those terminal edits.

The default remains 1 MHz / 40 ns. F410 changes from center-aligned to
edge-aligned operation to provide balanced CH1/CH1N reference pulses on the
two-tick grid. Steady complementary waveforms, deadtime, first-pulse phase and
EN alignment require scope verification; no powered validation is claimed.

Recordings attach only fresh verified timing to each sample. CSV includes
`requestedcarrier_Hz`, `actualcarrier_Hz`, `requesteddeadtime_ns`,
`actualdeadtime_ns`, `timer_clock_Hz`, `period_ticks`, `dead_ticks`,
`timing_revision`, `timing_received_at` and `timing_source`; fields stay blank
when timing is unavailable/stale. JSON retains per-sample timing and change
events. Later session metadata cannot establish timing for earlier samples.
