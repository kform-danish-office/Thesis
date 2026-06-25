# UART Command Quick Reference

Firmware: `PWR-1.9.13`

UART is hardware serial on PC5 RX and PC4 TX at 115200 baud. Commands accept CR, LF, or CRLF line endings.

## Basic Flow

```text
VER
FULL
MAXRATE
VSBONLY
ON
STATUS
OFF
```

Use `SET NAME VALUE` for parameters. If the output is OFF, settings save immediately. If the output is ON, the firmware applies the setting in RAM and defers the EEPROM write until `OFF` or `SAVE` while OFF.

## Main Commands

| Command | Meaning |
|---|---|
| `ON` / `OFF` | Enable or disable PA10 EN power transfer |
| `STATUS` / `?` | Print measured values, mode, timing, faults, PA10 sync counters, and settings |
| `VER` | Print firmware version |
| `PARAMS` | Print supported `SET` names |
| `EXPORT` / `COMPS` | Print paste-ready calibration and compensation settings |
| `BEGINCFG` / `ENDCFG` | Defer EEPROM writes during a pasted config block, then save once |
| `OPEN` | Open-loop EN duty from `OD` |
| `VSB` / `BANG` / `VOLT` | PA1 secondary-voltage bang-bang mode |
| `VSBONLY` | PA1 secondary-voltage bang-bang only; disables PA0 feed-forward |
| `LINEFF` | PA1 bang-bang with PA0 primary-voltage duty cap |
| `LFFCAL` | Store current PA0 primary voltage as `LFFREF` and enable `LINEFF` |
| `FULL` | Set `BHIGH=100`, `DMAX=100`, `STATIC=1`, `VON=VSET`, zero dwell |
| `MAXRATE` / `FASTEST` | Request fastest 20 us control loop preset |
| `ULTRA` | Request 25 us control loop preset |
| `TURBO` | Request 50 us control loop preset |
| `FAST` | Request 100 us control loop preset |
| `AUTOPRE` | Tune startup precharge burst |
| `AUTOBANG` / `CAL` | Tune no-load soft-switch cap at current fixed EN frequency |
| `CALLOAD 1..3` | Tune a load reference slot |
| `CAL3` | Prompt through all three load reference slots |
| `LOAD 1..3` | Select a saved load reference slot |
| `ZEROI` | Store current-sensor zero offset |
| `CLR` | Clear latched fault |
| `SAVE` | Save if output is OFF; otherwise leave save pending |
| `DEFAULTS` | Restore defaults and save |
| `DIVIDER` | Print PA0 divider suggestions |

## Copy Calibration Between Boards

On the board with the good tune:

```text
EXPORT
```

Copy the whole block into the other board's UART terminal. The export starts with `OFF` and `BEGINCFG`, prints `SET ...` commands for sensor scaling, line feed-forward, EN timing, voltage/no-load settings, and load-slot reference calibrations, then ends with `ENDCFG`. EEPROM writes are deferred during the block and saved once at the end.

This firmware ignores exported `#` comment lines, so the whole block can be pasted as-is.

## Common Settings

| Setting | Typical / Range |
|---|---|
| `FEN` | EN frequency, default 10000 Hz |
| `BLOW` | Low bang-bang duty, usually 0 percent |
| `BHIGH` | High bang-bang duty, default 100 percent |
| `DMAX` | Maximum duty, default 100 percent |
| `STATIC` | Allow true 100 percent EN, default 1 |
| `VSET` | No-load release/set voltage, default 28 V |
| `VON` | Loaded turn-on threshold, default 28 V |
| `VMIN` | Undervoltage/full-demand threshold, default 10 V |
| `VMAX` | Bang-bang release/high threshold, default 32 V |
| `OVP` | Latched overvoltage threshold, default 36 V |
| `NLGUARD` | Enable no-load guard |
| `NLDUTY` | No-load high-duty cap |
| `NLDROP` | Low end of no-load window is `VSET - NLDROP` |
| `NLFULL` | Cycles below no-load floor before full-demand escape |
| `NLI` / `NLR` | No-load current / apparent-resistance thresholds |
| `NLSOVPEN` | Enable soft no-load OVP holdoff, default 1 |
| `NLSOVP` | Soft no-load OVP trip voltage, default 33.5 V |
| `NLSOVPR` | Soft no-load OVP rearm/reset voltage, default 23 V |
| `LFFEN` | PA0 line feed-forward enable |
| `LFFREF` | PA0 primary voltage reference captured by `LFFCAL` |
| `LFFMINV` | PA0 voltage below which feed-forward is ignored |
| `LFFMINS` | Minimum PA0 duty scale |
| `LFFMAXS` | Maximum PA0 duty scale, default 1.0 |
| `CPER` | Control period, 20 to 20000 us |
| `STATUSMS` | Live status print interval |
| `ACTIVELOAD` | Active saved load reference slot, 1 to 3 |
| `L1FEN`, `L1DUTY`, etc. | Internal load-slot calibration import fields printed by `EXPORT` |

Full parameter ranges are in [power-control.md](power-control.md).

## High-Line Workflow

Tune or verify at low line first, then capture PA0:

```text
OFF
LINEFF
LFFCAL
SAVE
ON
```

When `LINEFF` is active, live status shows `mode=VSB+VIN` and `LFF=<scale>`. If the primary bus doubles, the high duty is roughly halved unless limited by `LFFMINS`. At high-line no/light load, `NLSOVP` may also show in live status while EN is held low until `NLSOVPR`.

## Fastest Loop

```text
MAXRATE
STATUS
```

Watch `Control period last/max/overruns`. If overruns climb, use `ULTRA`, `TURBO`, `FAST`, or set a larger `CPER`.

Live status includes `BTPS=<n>` for bang-bang transitions per second. Full `STATUS` also prints PA10 EN sync rise/drive/fall/abort counts.
