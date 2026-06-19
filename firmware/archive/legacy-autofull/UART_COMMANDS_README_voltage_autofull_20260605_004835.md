# thesi_closed_loop UART command quick readme

UART: `115200 baud`, `PC5 = MCU RX`, `PC4 = MCU TX`, common ground.

Most settings save to EEPROM immediately when changed with `SET`, `FB`, mode commands, or presets. Use `SAVE` if you want to force-save the current live state.

## Basic commands

`?` or `STATUS`
: Print full status, feedback mode, fault state, ADC readings, control loop timing, and tunable parameter list.

`PARAMS`
: Print the SET-able parameter names.

`ON`
: Enable the system. PA8/PA9 carrier stays running; PA10 EN controls power transfer.

`OFF`
: Disable power transfer by pulling PA10 EN low.

`OPEN` or `MO`
: Open-loop mode. PA10 EN duty is set by `OD`.

`CLOSED` or `MC`
: Closed-loop mode. PA10 EN duty/frequency are controlled by selected feedback path.

`CLR`
: Clear a latched fault.

`DEFAULTS`
: Restore default settings and save them to EEPROM.

`SAVE`
: Save current settings/state to EEPROM.

`FAST`
: Fast-loop preset: `CPER=250 us`, lower ADC sample counts, faster filters.

`SAFE`
: Safer preset: max duty 90%, static 100% disabled, max-duty and current trip enabled.

`CAL` or `AUTOTUNE`
: Run the faster normal autotune.

`AUTOFULL` or `CALFULL`
: Run the exhaustive autotune for the active load slot. This scans the full duty range at every EN frequency candidate and does not assume voltage rises monotonically with duty.

`AUTOFULL 1`, `AUTOFULL 2`, `AUTOFULL 3`
: Run exhaustive autotune for load slot 1, 2, or 3.

`CALLOAD 1`, `CALLOAD 2`, `CALLOAD 3`
: Same as `AUTOFULL n`; calibrates the selected physical load slot.

`CAL3`
: Interactive three-load calibration. It asks you to install each physical load, then type `GO`, `SKIP`, or `ABORT`.

`LOAD 1`, `LOAD 2`, `LOAD 3`
: Select a saved load slot and apply its stored tuned profile if it has one.

`ZEROI` or `IZERO`
: Measure and save current-sense zero offset on PA2.

## Feedback path

`FB 0`
: Secondary voltage only, PA1 ADC.

`FB 1`
: Secondary voltage plus primary current feedback/trip, PA1 ADC + PA2 ADC.

`FB 2`
: Comparator voltage path using PA1 and DAC threshold.

`FB 3`
: Comparator voltage path plus primary current feedback/trip.

## SET syntax

Use:

```text
SET NAME VALUE
```

Examples:

```text
SET TARGET 12.0
SET DMAX 95
SET CPER 250
SET ITRIPEN 0
SET IFOLDEN 0
SET LOAD1 10
SET LOAD2 5
SET LOAD3 2.5
```

## Common setup examples

Voltage-only closed loop:

```text
OFF
FB 0
SET TARGET 12.0
SET DMAX 80
CLOSED
ON
```

Voltage plus current protection:

```text
OFF
FB 1
SET ITRIP 5.5
SET ITRIPEN 1
SET ISOFT 4.5
SET IFOLDEN 1
CLOSED
ON
```

Comparator voltage path:

```text
OFF
FB 2
SET TARGET 12.0
SET COMPOFF 0
SET COMPHYST 1
CLOSED
ON
```

Disable current feedback/protection:

```text
FB 0
SET ITRIPEN 0
SET IFOLDEN 0
```

Open-loop bring-up:

```text
OFF
OPEN
SET OD 5
SET DMAX 30
ON
```

## Important parameters

Voltage scaling:
`TARGET`, `VREF`, `AMCREF`, `AMCVCLIP`, `RTOP`, `RBOT`, `VGAIN`, `VOFF`, `SENSORV`

PA10 EN actuator:
`FEN`, `FMIN`, `FMAX`, `MINEDGE`, `STATIC`, `DMIN`, `DMAX`, `OD`, `BIAS`, `PWRDUTY`

Autotune uses `FMIN` and `FMAX` as the EN-frequency search range. Set `FMIN` and `FMAX` to the same value if you want autotune to stay at one fixed EN frequency.

Control loop:
`CPER`, `STATUSMS`, `ADCV`, `ADCI`, `ADCDUMMY`, `VTAU`, `ITAU`, `KP`, `KI`, `DB`, `SLEW`, `IMIN`, `IMAX`

Current sense:
`CSRES`, `CSGAIN`, `CSOFF`, `ITRIP`, `ITRIPEN`, `ISOFT`, `IFOLDEN`, `IFOLD`, `IDROOP`

Fault/protection:
`OVPEN`, `OVP`, `MAXFAULTEN`, `MAXFAULTMS`, `MAXFAULTERR`

Comparator:
`COMPRUP`, `COMPRDN`, `COMPOFF`, `COMPHYST`

Autotune:
`AUTOMAX`, `AUTOSTEP`, `AUTOBIN`, `AUTOSETTLE`, `AUTOMEAS`, `AUTOTEST`, `LOAD1`, `LOAD2`, `LOAD3`

Load profile commands:
`LOAD 1..3`, `CALLOAD 1..3`, `AUTOFULL 1..3`, `CAL3`

## SET parameter min/max

Values outside these ranges are clamped or reset by firmware validation.

| Parameter | Min | Max | Units / notes |
|---|---:|---:|---|
| `TARGET` / `V` | 0.5 | 32 | V output target |
| `VREF` | 1.0 | 3.6 | V MCU ADC reference |
| `AMCREF` | 1.0 | 5.0 | V AMC reference |
| `AMCVCLIP` | 0.5 | 3.0 | V AMC input clip scale |
| `RTOP` | 1.0 | 10000 | kOhm divider top |
| `RBOT` | 0.1 | 1000 | kOhm divider bottom |
| `VGAIN` | 0.1 | 10.0 | voltage calibration gain |
| `VOFF` | -20.0 | 20.0 | V voltage calibration offset |
| `SENSORV` | 0.0 | 2.0 | V minimum valid PA1 sensor voltage |
| `FEN` / `E` | `FMIN` | `FMAX` | Hz PA10 EN frequency |
| `FMIN` | 1000 | 50000 | Hz lower EN frequency clamp |
| `FMAX` | 1000 | 50000 | Hz upper EN frequency clamp; forced >= `FMIN` |
| `MINEDGE` | 1 | 20 | us minimum PA10 high/low edge time |
| `STATIC` | 0 | 1 | 0 disables static 100% EN |
| `DMIN` | 0 | 100 | % minimum duty |
| `DMAX` | 0 | 100 | % maximum duty; forced at least about 1% above `DMIN` when possible |
| `OD` / `D` | 0 | 100 | % open-loop duty |
| `BIAS` / `B` | 0 | 100 | % closed-loop bias duty |
| `PWRDUTY` / `P` | 0 | 100 | % sensor power-up duty |
| `CPER` | 100 | 20000 | us requested control period |
| `STATUSMS` | 100 | 5000 | ms live status period |
| `ADCV` | 1 | 64 | voltage ADC samples |
| `ADCI` | 1 | 64 | current ADC samples |
| `ADCDUMMY` | 0 | 8 | dummy ADC reads |
| `VTAU` | 0.1 | 500 | ms voltage filter tau |
| `ITAU` | 0.1 | 500 | ms current filter tau |
| `KP` | 0.0 | 50.0 | %/V proportional gain |
| `KI` | 0.0 | 200.0 | %/(V*s) integral gain |
| `DB` | 0 | 2000 | mV deadband |
| `SLEW` | 0.1 | 2000 | %/s duty slew limit |
| `IMIN` | -100 | 100 | % integrator minimum |
| `IMAX` | -100 | 100 | % integrator maximum; forced >= `IMIN` |
| `CSRES` | 1.0 | 10000 | ohm current-sense load/pulldown |
| `CSGAIN` | 0.000001 | 0.1 | A/A current sensor gain term |
| `CSOFF` | -1.0 | 1.0 | V current offset |
| `ITRIP` | 0.1 | 100 | A current trip threshold |
| `ITRIPEN` | 0 | 1 | current trip enable |
| `ISOFT` | 0.0 | 100 | A foldback start threshold |
| `IFOLDEN` | 0 | 1 | current foldback enable |
| `IFOLD` | 0.0 | 100 | % duty removed per amp over `ISOFT` |
| `IDROOP` | 0.0 | 10.0 | V target droop per amp |
| `OVPEN` | 0 | 1 | output over-voltage enable |
| `OVP` | 0.5 | 80 | V output over-voltage threshold |
| `MAXFAULTEN` | 0 | 1 | max-duty fault enable |
| `MAXFAULTMS` | 50 | 10000 | ms at max duty before fault |
| `MAXFAULTERR` | 0 | 10000 | mV error required for max-duty fault |
| `COMPRUP` | 0.1 | 2000 | %/s comparator-mode duty ramp up |
| `COMPRDN` | 0.1 | 2000 | %/s comparator-mode duty ramp down |
| `COMPOFF` | -1000 | 1000 | mV comparator DAC threshold offset |
| `COMPHYST` | 0 | 3 | comparator hysteresis code |
| `AUTOMAX` | `DMIN + 5` | `DMAX` | % max duty autotune may try |
| `AUTOSTEP` | 0.5 | 20 | % coarse autotune duty step |
| `AUTOBIN` | 3 | 12 | binary trim passes |
| `AUTOSETTLE` | 20 | 3000 | ms settle before measuring |
| `AUTOMEAS` | 20 | 2000 | ms measurement window |
| `AUTOTEST` | 0.5 | 10 | % duty step for plant ID |
| `LOAD1` | 0 | 100000 | ohm calibration load slot 1; 0 disables load-current assumption |
| `LOAD2` | 0 | 100000 | ohm calibration load slot 2; 0 disables load-current assumption |
| `LOAD3` | 0 | 100000 | ohm calibration load slot 3; 0 disables load-current assumption |

## What autotune does

Run autotune with:

```text
CAL
```

or:

```text
AUTOTUNE
```

The tuner only changes the PA10 EN duty/frequency actuator. It does not stop or retune the PA8/PA9 1 MHz gate carrier.

Normal `CAL` is faster and assumes the duty response is mostly monotonic. `AUTOFULL` is slower and safer for weird/non-monotonic behavior: it keeps scanning the full duty range instead of stopping at the first target crossing.

Autotune sensor power-up:
Starts from `PWRDUTY` and slowly raises PA10 EN duty until the PA1 voltage sensor becomes valid. This is meant to avoid trying to tune while the isolated voltage sense is still too low or invalid. If voltage rises more than about 1 V above target during this stage, it aborts.

Autotune EN frequency + duty search:
Sweeps EN frequency across the `FMIN..FMAX` range. At each candidate frequency, it sweeps open-loop EN duty from `DMIN` up to `AUTOMAX`, stepping by `AUTOSTEP`. At each duty it waits `AUTOSETTLE` ms, measures for `AUTOMEAS` ms, then records average output voltage, ripple band, current, and ADC timing. It picks the frequency/duty pair with the best target error and ripple score.

Full autotune EN frequency + duty search:
`AUTOFULL` uses a denser frequency grid and scans the entire `DMIN..AUTOMAX` duty range at every frequency. It scores every point by target error, ripple, and a small duty penalty. If a load slot has a nonzero resistance and current sense is active, it also lightly checks whether measured current matches the expected `TARGET / LOADn`.

Autotune binary trim:
At each frequency candidate, if the duty sweep bracketed the target, it binary-searches between the last duty below target and the first duty above target. `AUTOBIN` controls how many binary trim attempts it makes.

Autotune plant gain/tau estimate:
Applies a small duty step of `AUTOTEST` percent from the best duty point, samples the output response for about 600 ms, and estimates plant gain in V/% duty plus output time constant tau. If the response is too weak, it uses a conservative fallback.

Autotune PI calculation:
Uses the measured gain and tau to calculate conservative `KP` and `KI` values for the closed-loop voltage controller. The code intentionally scales the gains down for LLC burst control.

Autotune enter closed loop:
Saves the selected EN frequency as `FEN`, saves the best duty as `BIAS`, stores the measured plant gain/tau, updates the comparator DAC threshold, switches to closed-loop mode, and saves everything to EEPROM.

Load-slot autotune:
`CALLOAD n` or `AUTOFULL n` stores the selected `FEN`, `BIAS`, `KP`, `KI`, gain/tau, measured voltage, and measured current into load slot `n`. Later, `LOAD n` applies that stored profile.

## Autotune knobs

`AUTOMAX`
: Maximum duty percent autotune is allowed to try. Default is `95`. Set this lower for first power tests, for example `SET AUTOMAX 25`.

`AUTOSTEP`
: Coarse duty step size in percent. Default is `5`. Smaller is gentler but slower. Example: `SET AUTOSTEP 2`.

`AUTOBIN`
: Number of binary trim passes after target is bracketed. Default is `7`. More passes are finer but take longer.

`AUTOSETTLE`
: Wait time in ms after each duty change before measuring. Default is `250`. Increase this if the output responds slowly.

`AUTOMEAS`
: Measurement window in ms after settling. Default is `120`. Increase this if the reading is noisy or burst ripple is large.

`AUTOTEST`
: Small plant-ID duty step in percent. Default is `3`. Lower is safer; higher gives a stronger gain/tau measurement.

`LOAD1`, `LOAD2`, `LOAD3`
: Calibration load resistances in ohms. Defaults are `10`, `5`, and `2.5` ohm.

Autotune EN frequency examples:

```text
SET FMIN 5000
SET FMAX 50000
CAL
```

Force autotune to one EN frequency:

```text
SET FMIN 10000
SET FMAX 10000
SET FEN 10000
CAL
```

Full scan with one load:

```text
OFF
SET TARGET 12
SET LOAD1 10
SET FMIN 5000
SET FMAX 50000
SET AUTOMAX 30
SET AUTOSTEP 2
AUTOFULL 1
```

Three-load calibration:

```text
OFF
SET LOAD1 10
SET LOAD2 5
SET LOAD3 2.5
SET FMIN 5000
SET FMAX 50000
SET AUTOMAX 30
SET AUTOSTEP 2
CAL3
```

## Bench notes

Default hardware scaling is `VREF=3.3 V`, `AMCREF=3.3 V`, secondary divider `390k/10k`, current sense load `820 ohm`.

The requested control-loop period range is `100..20000 us`. Start with `FAST` or `SET CPER 250`, then check `STATUS` for `last/max/overruns`. If overruns increase, raise `CPER`.

`STATIC` should normally stay `0`. `DMAX` should normally stay below `100` so PA10 EN cannot park at continuous high duty.

PA10 EN timing uses TIM3 fixed-period timing: the TIM3 update interrupt sets PA10 high at the start of each EN period, and the TIM3 compare interrupt sets PA10 low at the commanded high time. `STATUS` prints `period/high`, so at `FEN=10000` and `OD=30` you should see roughly `100/30 us`.

Quick PA10 duty scope test:

```text
OFF
OPEN
SET FMIN 10000
SET FMAX 10000
SET FEN 10000
SET DMAX 95
SET STATIC 0
SET OD 10
ON
STATUS
SET OD 30
STATUS
SET OD 60
STATUS
OFF
```

Expected PA10 high time at `FEN=10000`:
`OD=10` -> about `10 us`, `OD=30` -> about `30 us`, `OD=60` -> about `60 us`.
