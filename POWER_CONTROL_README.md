# Bang-Bang Converter Controller Quick README

Current firmware version: `PWR-1.9.8`

Version notes:

- `PWR-1.9.8`: calibrated load slots are now live reference points. When the no-load/high-impedance guard is active, the firmware estimates apparent load resistance from PA1/PA2 and interpolates between tuned `CALLOAD 1..3` duties. Lower resistance than the lowest tuned reference extrapolates to `DMAX`, so lower-resistance loads are no longer trapped at the no-load cap. Live status prints `AREF` when the adaptive reference is active. EEPROM magic is now `PWR18`.
- `PWR-1.9.7`: `AUTOBANG` now tunes the no-load soft-switch cap `NLDUTY`, not loaded full-power `BHIGH`. Loaded sag demand uses `DMAX` directly, so if Vsec is below `VON` or the no-load sag escape trips, the firmware commands true full EN even if a previous no-load calibration found 26-32 percent. Live status prints `FDEM` when full-power demand is active. EEPROM magic is now `PWR17`.
- `PWR-1.9.6`: loaded operation now turns on at `VON`, default 28 V, instead of waiting for `VMIN=10 V`. This lets real loads demand full `BHIGH=100` whenever Vsec is below setpoint. Load profiles no longer reduce `BHIGH` below the current value, so `LOAD n` cannot silently cap full power. High-impedance load slots can still enable the no-load soft-switch guard through `NLSLOT=1`, but only when measured current is consistent with that slot. EEPROM magic is now `PWR16`.
- `PWR-1.9.5`: tightens low-load operation to 23-28 V by default with `VSET=28` and `NLDROP=5`. The full-power escape is now latched: if Vsec stays below `VSET - NLDROP` for `NLFULL` cycles, the controller bypasses the no-load cap and commands full `BHIGH` until `VMAX`, so a real load cannot get trapped in the low-load guard. Default loop is now ultra-fast `CPER=25 us`. EEPROM magic is now `PWR15`.
- `PWR-1.9.4`: fixes high-power load sagging while stuck in no-load guard. No-load guard now uses a set/cal voltage window: low threshold is `VSET - NLDROP`, release is `VSET`. Defaults are `VSET=28`, `VMIN=10`, `VMAX=32`, `OVP=36`, `NLDROP=10`, and `NLFULL=3`. If PA1 stays below the no-load low threshold for `NLFULL` control cycles, the guard cap is bypassed and the loop commands full `BHIGH` until `VSET`. EEPROM magic is now `PWR14`.
- `PWR-1.9.3`: improves 220 V/high-line no-load stability. The high-to-low cutoff and OVP now use the fresh raw PA1 Vsec sample, no-load guard also engages for light configured load slots, and no-load defaults are more conservative: `NLDUTY=5`, `NLBAND=1`, `NLI=0.35`, `NLR=30`, `VSTAU=0.8`. EEPROM magic is now `PWR13`.
- `PWR-1.9.2`: fixes deep dips during full-demand recovery. If raw or filtered Vsec is below `VMIN`, the loop bypasses no-load guard and commands full `BHIGH` immediately. Static 100 percent EN also drives PA10 high immediately instead of waiting for the next TIM3 period.
- `PWR-1.9.1`: adds a no-load guard for high-line/no-load operation. When output current/apparent load indicates no load, EN high duty is capped by `NLDUTY` and the controller releases at `VMIN + NLBAND` instead of waiting for `VMAX`. EEPROM magic is now `PWR12`.
- `PWR-1.9.0`: removes power-feedback control/limiting from the active loop. Closed-loop mode now uses PA1 secondary voltage only: EN goes high below `VMIN` and low above `VMAX`; OVP still latches at `OVP`. Defaults are `BHIGH=100`, `DMAX=100`, `STATIC=1`, `LOAD1=50`, current trip/foldback off, and EEPROM magic `PWR11`.
- `PWR-1.8.3`: allows true 100 percent PA10 EN duty by default (`STATIC=1`, `DMAX=100`), changes default `LOAD1` to 50 ohms, and adds light-load voltage-band behavior so the controller can sit near `VMIN` instead of chasing power up to `VMAX`. EEPROM magic is now `PWR10`.
- `PWR-1.8.2`: recovery build. Restores the direct TIM3 PA10 EN switching path from the working versions. `GATECYC` still sets minimum burst width; `GATELEAD` is not used in this recovery path.
- `PWR-1.8.1`: keeps the TIM1 1 MHz carrier running like the working builds and synchronizes only PA10 EN edges to carrier update boundaries. `GATELEAD` now defaults to 0. EEPROM magic is now `PWR9`.
- `PWR-1.8.0`: synchronizes PA10 EN bursts to the 1 MHz TIM1 carrier, holds the carrier idle during a separate `GATELEAD` wake-up blanking time, then emits complete carrier cycles. EEPROM magic is now `PWR8`.
- `PWR-1.7.2`: makes the minimum nonzero EN burst adjustable with `GATECYC`. Default is 8 full 1 MHz carrier cycles to ride through the first partial/soft switching cycles seen at low load. EEPROM magic is now `PWR7`.
- `PWR-1.7.1`: enforces a carrier-cycle minimum EN high time. Any nonzero PA10 EN pulse is at least long enough for one complete 1 MHz half-bridge high/low cycle, with phase margin.
- `PWR-1.7.0`: removes blocking `analogRead()` from feedback. PA0/PA1/PA2 are sampled by ADC1 DMA in a circular scan buffer, and the control loop only reads the latest DMA values.
- `PWR-1.6.0`: scraps PI power control and uses fixed-frequency bang-bang control. `AUTOBANG` scans EN duty only at the current `FEN`; it does not sweep EN frequency. EEPROM magic is now `PWR6`.
- `PWR-1.5.2`: makes `SEC_V_I` the default feedback source because PA2 is proportional to secondary output current. EEPROM magic is now `PWR5`, so old saved `PRI_V_I` settings will not persist by accident.
- `PWR-1.5.1`: fixes UART command entry in terminals such as Tera Term by accepting CR, LF, and CRLF line endings.
- `PWR-1.5.0`: adds selectable power feedback source. Use `PFBPRI` / `SET PFBSRC 0` for PA0 primary voltage times PA2 current, or `PFBSEC` / `SET PFBSRC 1` for PA1 secondary voltage times PA2 current feedback.
- `PWR-1.4.0`: defers EEPROM writes while output is active so UART `SET` commands cannot stall the control loop or EN timing during flash programming.
- `PWR-1.3.0`: hardens the EN pulse-skip state, bounds UART input, limits serial work per loop while active, and adds the `TURBO` loop preset.
- `PWR-1.2.0`: changes startup precharge default to true 0.1 percent average duty, adds `AUTOPRE`, and stops power autotune duty scans when secondary voltage exceeds `VMAX`.
- `PWR-1.1.0`: adds firmware version reporting and startup secondary-feedback precharge.

## Serial

- UART is hardware serial on PC5 RX and PC4 TX at 115200 baud.
- Command entry accepts Enter as CR, LF, or CRLF, so Tera Term's default transmit newline works.
- `SET NAME VALUE` applies immediately. If output is OFF, it saves immediately; if output is ON, EEPROM save is deferred until `OFF` or `SAVE` while output is OFF.
- Type `?` or `STATUS` for live settings, ADC readings, loop timing, and load-slot status.
- Type `VER` or `VERSION` for the firmware version.
- Type `PARAMS` for the firmware's SET-able parameter list.

## Control Mode

- PA8 / PA9 stay as the fixed 1 MHz gate carrier.
- PA10 EN is a fixed-frequency bang-bang throttle. The firmware switches EN between `BLOW` and `BHIGH`.
- PA10 EN is driven directly by TIM3 update/compare interrupts in this recovery build. Any nonzero PA10 pulse is still forced to at least the `GATECYC` minimum width.
- ADC feedback is DMA-only. PA0, PA1, and PA2 are continuously sampled by ADC1 DMA; the loop never calls blocking `analogRead()`.
- Default EN frequency is 10 kHz. `AUTOBANG` does not sweep frequency; set `FEN` first if you want a different fixed EN rate.
- Active feedback is PA1 secondary voltage only. PA0/PA2 and `Pdiag` are displayed for diagnostics, but they do not limit the closed loop by default.
- PA1 secondary voltage band defaults to 10 V to 32 V, with OVP at 36 V.
- Loaded voltage bang-bang turns high when `Vsec <= VON`, default 28 V, and returns low when `Vsec >= VMAX`, default 32 V.
- No-load guard is on by default. When active, it caps high EN duty to `NLDUTY` and uses the smaller no-load window from `VSET - NLDROP` to `VSET`. With defaults, that is 23 V to 28 V.
- If Vsec drops below `VMIN`, or stays below `VSET - NLDROP` for `NLFULL` loop cycles, no-load guard is bypassed and the loop uses full `BHIGH` until `VMAX`.
- `BONMS` and `BOFFMS` set minimum high/low dwell time in milliseconds.
- Above `OVP`, EN shuts off and latches a fault. Current trip/foldback are off by default in `PWR-1.9.0`.
- On `ON`, boot, and `AUTOBANG`, the firmware first gives PA10 a tiny startup precharge burst so the secondary-side isolated feedback device has enough power to wake up before PA1 is trusted.

## Startup Precharge

Default precharge settings:

```text
PRECHEN   1
PREDUTY   0.1
PREMS     3
PRESETTLE 80
PREMAX    4
PREV      4.0
PREAUTOMAX 2.0
PRETRIES   20
```

With the default 10 kHz EN frequency and `MINEDGE=2`, a literal 0.1 percent high time is below the timer edge limit. Firmware `PWR-1.2.0` and newer preserves the average by pulse skipping: it emits one minimum-width EN pulse and skips enough EN periods to average back down to the requested duty. After each try, EN is turned off for `PRESETTLE` ms while PA1 is sampled. It repeats until PA1 reads at least `PREV` volts or `PREMAX` tries have happened, then normal open-loop or power-loop startup takes over.

To make it even gentler at 10 kHz:

```text
SET PREMS 1
SET PREMAX 2
```

To auto-tune the initial burst after the secondary output has discharged:

```text
AUTOPRE
```

`AUTOPRE` starts at `PREDUTY`, repeats tiny bursts, and increases duty only up to `PREAUTOMAX`. It saves the first result that reaches `PREV`. If PA1 rises above `VMAX`, it stops instead of continuing upward.

To disable this path:

```text
SET PRECHEN 0
```

## PA0 Primary Voltage Divider

Firmware formula:

```text
PA0 = Vpri * Rbottom / (Rtop + Rbottom)
Vpri = PA0 * (Rtop + Rbottom) / Rbottom
```

Recommended population for your stated 450 V peak primary bus:

```text
Rtop total = 1.50 Mohm
Rbottom   = 10.0 kohm
Firmware: SET VPRITOP 1500
Firmware: SET VPRIBOT 10
PA0 at 450 V peak ~= 2.98 V
```

Practical ladder options:

| Bus range | Rtop total | Rbottom | PA0 at max | Notes |
|---|---:|---:|---:|---|
| 400 V max only | 1.24 Mohm | 10.0 kohm | 3.20 V at 400 V | Do not use this at 450 V; PA0 would be about 3.60 V |
| 450 V peak | 1.50 Mohm | 10.0 kohm | 2.98 V at 450 V | Firmware default and recommended |
| 450 V peak, more ADC range | 1.43 Mohm | 10.0 kohm | 3.13 V at 450 V | Less headroom; only use with tight bus limits |
| 500 V abs with margin | 1.58 Mohm | 10.0 kohm | 3.15 V at 500 V | Use if 450 V peak may be exceeded |
| 600 V abs | 1.82 Mohm | 10.0 kohm | 3.28 V at 600 V | Use if bus can go this high |

For 1.50 Mohm, populate the top as series high-voltage resistors, for example `499k + 499k + 499k`, then set the actual measured total with `VPRITOP`. With 450 V across 1.50 Mohm, the divider current is about 0.30 mA and the top string dissipates about 0.135 W total, so split the voltage and power across multiple rated parts.

## Typical Bring-Up

```text
DEFAULTS
SET VPRITOP 1500
SET VPRIBOT 10
SET FEN 10000
SET VMIN 10
SET VMAX 32
SET VSET 28
SET VON 28
SET OVP 36
SET BLOW 0
SET BHIGH 100
SET NLGUARD 1
SET NLDUTY 5
SET NLDROP 5
SET NLFULL 3
SET NLSLOT 1
SET NLI 0.35
SET NLR 30
SET GATECYC 8
SET GATELEAD 0
SET STATIC 1
SET DMAX 100
SET LOAD1 50
FULL
VSB
ON
```

To set the fixed EN frequency:

```text
SET FEN 10000
```

## Main Commands

| Command | Meaning |
|---|---|
| `ON` / `OFF` | Enable or disable system output |
| `OPEN` | Open-loop EN duty mode |
| `BANG` / `VSB` / `VOLT` | Closed voltage bang-bang mode |
| `POWER` | Legacy alias for `BANG` |
| `PFBPRI` | Select diagnostic PA0*PA2 power display source; not used for control |
| `PFBSEC` | Select diagnostic PA1*PA2 power display source; not used for control |
| `VER` | Print firmware version |
| `AUTOPRE` | Tune the initial secondary-feedback precharge burst |
| `AUTOBANG` | Calibrate no-load soft-switch cap `NLDUTY` at the current fixed `FEN`; keeps loaded `BHIGH=100` |
| `SET NAME VALUE` | Change parameter now; EEPROM save defers while output is ON |
| `SAVE` | Save now if output is OFF; otherwise mark EEPROM save pending |
| `P 50` | Legacy shortcut for `SET PTARGET 50`; not used by voltage-only loop |
| `D 10` | Shortcut for `SET OD 10` |
| `F 10000` | Shortcut for `SET FEN 10000` |
| `ZEROI` | Average PA2 and store current-sensor zero offset |
| `CLR` | Clear latched fault |
| `FAST` | Sets `CPER=100`; ADC remains DMA-only |
| `TURBO` | Sets `CPER=50`, faster filters, and slower serial status; ADC remains DMA-only |
| `ULTRA` | Sets `CPER=25`, fastest filters, and slower serial status; ADC remains DMA-only |
| `FULL` | Sets `BHIGH=100`, `DMAX=100`, `STATIC=1`, `VON=VSET`, and zero bang-bang dwell |
| `SAFE` | Sets conservative duty/current safety defaults |
| `DIVIDER` | Prints PA0 ladder options |
| `DEFAULTS` | Restore defaults and save |

## Autotune Commands

| Command | What it does |
|---|---|
| `AUTOBANG` or `CAL` | Fixed-frequency bang-bang duty calibration using the active load slot |
| `AUTOBANG 1` | Calibrate using load slot 1 |
| `CALLOAD 2` | Calibrate and save profile for load slot 2 |
| `CAL3` | Prompts for three physical loads, then tunes slots 1, 2, and 3 |
| `LOAD 1` | Selects saved reference slot 1 and its saved frequency |

`AUTOBANG` holds `FEN` fixed. It scans duty from `max(DMIN, BLOW)` to `AUTOMAX` in `AUTOSTEP` increments, then fine scans around the best point using `AUTOFINE`. It scores each point by PA1 secondary voltage only, preferring the no-load release voltage near `VSET`. It saves the best duty as `NLDUTY` for high-impedance/no-load soft switching, keeps `BLOW` as the low/off duty, and leaves loaded `BHIGH` at `DMAX`.

`CALLOAD 1..3` stores reference resistance and tuned duty points. Live control treats them as a curve, not rigid modes: if PA1/PA2 indicate a load between two references, the no-load cap is interpolated; if the load is lower resistance than the lowest tuned point, the cap rises to `DMAX`.

During bang-bang calibration, if PA1 exceeds `VMAX`, EN is turned off for that point and the firmware stops trying higher duty. OVP still latches if PA1 exceeds `OVP`.

## Min / Max Settings

| Parameter | Range | Units / notes |
|---|---:|---|
| `PFBSRC` | 0 or 1 | diagnostic `Pdiag` display source only |
| `PTARGET` | 0.5 to 2000 | W, legacy/diagnostic; not used by voltage-only loop |
| `VREF` | 1.0 to 3.6 | V, default 3.3 |
| `VPRITOP` | 1 to 10000 | kohm |
| `VPRIBOT` | 0.1 to 1000 | kohm |
| `VPRIGAIN` | 0.1 to 10 | multiplier |
| `VPRIOFF` | -100 to 100 | V |
| `AMCREF` | 1.0 to 5.0 | V |
| `AMCVCLIP` | 0.5 to 3.0 | V |
| `VSECTOP` | 1 to 10000 | kohm, default 390 |
| `VSECBOT` | 0.1 to 1000 | kohm, default 10 |
| `VSECGAIN` | 0.1 to 10 | multiplier |
| `VSECOFF` | -20 to 20 | V |
| `CSRES` | 1 to 10000 | ohm, default 820 |
| `CSGAIN` | 0.000001 to 0.1 | current-sensor scale |
| `CSOFF` | -1 to 1 | V |
| `IABS` | 0 or 1 | absolute current mode |
| `ITRIP` | 0.1 to 100 | A |
| `ITRIPEN` | 0 or 1 | current trip enable |
| `ISOFT` | 0 to 100 | A |
| `IFOLDEN` | 0 or 1 | current foldback enable |
| `IFOLD` | 0 to 100 | percent duty per amp |
| `PRECHEN` | 0 or 1 | startup precharge enable |
| `PREDUTY` | 0 to 100 | precharge EN command percent |
| `PREMS` | 1 to 500 | ms per tiny burst |
| `PRESETTLE` | 1 to 2000 | ms pause/read time after each burst |
| `PREMAX` | 1 to 20 | max precharge burst tries |
| `PREV` | 0 to 80 | Vsec ready threshold; 0 means do not wait for PA1 voltage |
| `PREAUTOMAX` | 0 to 100 | max precharge autotune duty percent |
| `PRETRIES` | 1 to 50 | max precharge autotune burst attempts per duty |
| `FEN` | `FMIN` to `FMAX` | Hz |
| `FMIN` | 1000 to 50000 | Hz |
| `FMAX` | 1000 to 50000 | Hz |
| `FPREF` | 1000 to 50000 | Hz, default 10000 |
| `FPEN` | 0 to 1000 | score penalty toward `FPREF` |
| `MINEDGE` | 1 to 20 | us, minimum low-time margin used by the EN scheduler |
| `GATECYC` | 1 to 40 | minimum full 1 MHz carrier drive cycles for any nonzero burst; default 8 |
| `GATELEAD` | 0 to 40 | saved but inactive in the direct TIM3 EN path; default 0 |
| `STATIC` | 0 or 1 | allow true 100 percent EN; default 1 |
| `DMIN`, `DMAX`, `OD`, `BIAS`, `PWRDUTY` | 0 to 100 | percent |
| `BLOW` | 0 to 100 | low bang-bang EN duty percent; usually 0 |
| `BHIGH` | 0 to 100 | high voltage-bang EN duty percent; default 100 |
| `BHYST` | 0 to 1000 | legacy, not used by voltage-only loop |
| `BONMS`, `BOFFMS` | 0 to 1000 | ms, minimum high/low dwell |
| `CPER` | 20 to 20000 | us, requested control-loop period |
| `STATUSMS` | 100 to 5000 | ms |
| `PTAU`, `VPTAU`, `VSTAU`, `ITAU` | 0.1 to 500 | ms filter time constant |
| `KP`, `KI`, `DB`, `SLEW`, `IMIN`, `IMAX` | see firmware | legacy PI-power fields, not used by voltage-only loop |
| `VMIN` | 0 to 80 | V, default 10 |
| `VMAX` | `VMIN + 0.5` to 80 | V, default 32 |
| `VSET` / `VCAL` | `VMIN + 0.2` to `VMAX` | V, no-load release/set voltage, default 28 |
| `VON` / `LOADON` | `VMIN` to `VMAX` | V, loaded-loop turn-on threshold, default 28 |
| `OVP` | `VMAX` to 80 | V, default 36 |
| `OVPEN` | 0 or 1 | OVP enable |
| `NLGUARD` | 0 or 1 | no-load guard enable; default 1 |
| `NLDUTY` | 0 to 100 | max high EN duty while no-load guard active; default 5 |
| `NLDROP` / `NLBAND` | 0.2 to 60 | V below `VSET` for no-load low threshold; default 5 |
| `NLFULL` / `NLCYC` | 0 to 100 | loop cycles below `VSET - NLDROP` before full-power escape; default 3; 0 disables this escape |
| `NLSLOT` | 0 or 1 | let high-impedance active load slots use no-load guard; default 1 |
| `NLI` | 0 to 10 | A threshold for no-load detection; default 0.35 |
| `NLR` | 1 to 100000 | ohm apparent-load threshold for no-load detection; default 30 |
| `VBOOST`, `VFOLD` | 0 to 100 | legacy power-loop fields, not used by voltage-only loop |
| `MAXFAULTEN` | 0 or 1 | legacy max-duty power fault; not called by voltage-only loop |
| `MAXFAULTMS` | 50 to 10000 | ms |
| `MAXFAULTERR` | 0 to 1000 | W |
| `AUTOMAX` | 0 to 100 | percent |
| `AUTOSTEP` | 0.5 to 25 | percent |
| `AUTOFINE` | 0.1 to 10 | percent |
| `AUTOSETTLE` | 20 to 3000 | ms |
| `AUTOMEAS` | 20 to 2000 | ms |
| `AUTOTEST` | 0.5 to 15 | percent |
| `LOAD1`, `LOAD2`, `LOAD3` | 0 to 100000 | ohm; `LOAD1` default is 50 ohm |

## Loop-Speed Notes

- `CPER` min is 20 us, which requests a 50 kHz control loop.
- Default is 25 us, or 40 kHz requested.
- `FAST` sets 100 us, or 10 kHz, and reduces ADC averaging.
- `TURBO` sets 50 us, or 20 kHz requested. `ULTRA` sets 25 us, or 40 kHz requested. Use `STATUS` and watch `Control period last/max/overruns`; if overruns climb, back off to `TURBO`, `FAST`, or raise `CPER`.
- Actual speed depends mostly on loop work and serial activity. ADC is DMA-only, so `ADC block last/max` should reflect a fast DMA snapshot instead of blocking conversion time.
- PA10 EN scheduling uses TIM3, but the actual burst edge/drive sequence is aligned by the TIM1 carrier update interrupt. The TIM1 ISR only runs during a burst.
- UART input is bounded to 96 characters and limited to 32 bytes per loop while the system is active so pasted commands cannot starve the control loop.
- EEPROM writes are deferred while output is active. This avoids flash-program stalls during live control; `STATUS` shows `EEPROM pending save: YES` until it flushes.
- At 50 kHz EN, the nominal period is 20 us. The smallest nonzero burst envelope is `GATELEAD + GATECYC + 1 tail cycle` plus the `MINEDGE` low-time margin. If that does not fit, firmware stretches the EN period rather than creating partial pulses.
