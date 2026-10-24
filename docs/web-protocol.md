# Browser control and logging protocol

Active firmware: `PWR-2.0.1` in the root `thesi_power_control.ino`.
This adds an opt-in web session to the existing UART interface. Existing boot
defaults, hardware pins, control law, calibration, and protection settings remain
unchanged. A browser connection never enables the converter automatically.

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
{"type":"hello","protocol":1,"fw":"PWR-2.0.1","board":"STM32F410CBU6","baud":115200,"max_line":96,"lease_required":true}
```

Use `WEB <id> <command>` for commands after hello. IDs are 1–24 ASCII letters,
digits, hyphens, or underscores. Use a new ID for each command and serialize
commands: await the matching acknowledgement before sending the next one.

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
| `SNAPSHOT` | Acknowledgement followed by one telemetry sample |
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
contains `PWR-2.0.1`; stale generated source must not count as verification.

No automatic flashing or physical USB connection is performed by this update.
Compilation and HEX layout verification do not establish electrical correctness,
safe populated divider values, serial timing under load, or measured loop timing.

Verification completed on October 19, 2026 with STM32 Arduino core 2.8.1:

| Target | Program storage | Static RAM |
| --- | --- | --- |
| F410 | 85,184 / 98,304 bytes (86%) | 6,820 / 32,768 bytes (20%) |
| G071 | 127,340 / 131,072 bytes (97%) | 9,524 / 32,768 bytes (29%) |

G071 has only 3,732 bytes of remaining program space. The F410 HEX verifier
passed record checksums, stack/reset vector checks, and settings-sector exclusion.
The native host harness (`python firmware/test_web_protocol.py`) passed 46 JSON
frames covering malformed numbers, unknown parameters, save failures, enable
interlocks, lease expiry including uptime wrap, queue congestion, missing sensor
values, and bounded writes. It extracts the production dispatcher rather than
reimplementing its behavior. UART, hardware state changes, and persistence are
stubbed, so this does not verify physical hardware operation. No flashing or
hardware-port access occurred.
