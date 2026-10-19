# G071 Baseline Firmware Flow

This diagram describes the G071 baseline, version `PWR-1.9.20`, from which the
current [`thesi_power_control.ino`](../thesi_power_control.ino) was ported.
It documents the implemented behavior; it is not a proposed control scheme.

For the `PWR-2.0.0` F410 pin assignments and hardware changes, see
[STM32F410 port notes](stm32f410-port.md).

PNG export: [firmware-flow.png](firmware-flow.png)

## Boot And Main Loop

```mermaid
flowchart TD
    RESET([Reset or power applied]) --> UART["Start hardware UART<br/>PC5 RX, PC4 TX, 115200 baud"]
    UART --> IO["Configure LEDs and PA0, PA1, PA2 as analog inputs"]
    IO --> LOAD["Load newest valid settings slot from EEPROM<br/>or apply compiled defaults"]
    LOAD --> DMA{"Start ADC1 circular DMA<br/>PA0, PA1, PA2"}
    DMA -- Failed --> SENSOR["Latch SENSOR fault<br/>keep PA10 EN low"]
    DMA -- Running --> TIM1["Start TIM1 center-aligned 1 MHz carrier<br/>PA8 and PA9 with dead gap at both transitions"]
    TIM1 --> TIM3["Start TIM3 PA10 EN scheduler<br/>default 10 kHz"]
    TIM3 --> BOOT{"Saved boot default ON?"}
    BOOT -- No --> OFF["Output remains OFF<br/>PA10 low"]
    BOOT -- Yes --> PRE{"Startup precharge enabled?"}
    PRE -- No --> POST["Apply selected OPEN or VSB mode"]
    PRE -- Yes --> BURST["Apply tiny PA10 burst<br/>default 0.1 percent average"]
    BURST --> SETTLE["PA10 low during settle time<br/>sample PA1 and check current"]
    SETTLE --> READY{"PA1 at PREV<br/>or PREMAX reached?"}
    READY -- No --> BURST
    READY -- Yes --> POST
    OFF --> LOOP
    POST --> LOOP

    LOOP["Arduino loop"] --> RX["Service a bounded number of UART bytes"]
    RX --> ACTIVE{"System ON and not autotuning?"}
    ACTIVE -- Yes --> STARTING{"Precharge still active?"}
    STARTING -- Yes --> PRESTEP["Advance BURST or SETTLE state"]
    STARTING -- No --> CONTROL["Run voltage-control service when CPER elapsed<br/>default 25 us requested"]
    ACTIVE -- No --> BG["Background sensing and fault check every 2 ms<br/>when OFF or in OPEN mode"]
    PRESTEP --> RATE["Update transition counters"]
    CONTROL --> RATE
    BG --> RATE
    RATE --> RX2["Service UART again"]
    RX2 --> STATUS["Print periodic status only while UART input is idle"]
    STATUS --> SAVE{"Pending EEPROM save and output OFF?"}
    SAVE -- Yes --> EEPROM["Write next wear-levelled EEPROM slot"]
    SAVE -- No --> LOOP
    EEPROM --> LOOP
```

## Voltage Control And EN Generation

```mermaid
flowchart TD
    ADC["ADC1 circular DMA<br/>PA0 primary V, PA1 secondary V, PA2 bridge current"] --> SCALE["Scale latest DMA samples and update low-pass filters"]
    SCALE --> CLASSIFY["Use PA2 only for load classification and optional current trip<br/>PA1 remains the control feedback"]
    CLASSIFY --> SOFT{"Light-load soft OVP active<br/>or PA1 at NLSOVP?"}
    SOFT -- Yes --> HOLD["Command BLOW and hold PA10 low<br/>resume after PA1 falls to NLSOVPR"]
    SOFT -- No --> FAULT{"DMA stopped, enabled current trip,<br/>or hard secondary OVP?"}
    FAULT -- Yes --> LATCH["Latch fault and force PA10 low<br/>TIM1 carrier remains running<br/>wait for CLR"]
    FAULT -- No --> MODE{"Control mode"}

    MODE -- OPEN --> OPEN["Use fixed OPEN duty"]
    MODE -- VSB bang-bang --> LOADED{"Loaded steady eligible?<br/>LDET current or low apparent resistance,<br/>with no-load guard inactive"}

    LOADED -- Yes --> STEADY["LSTEADY: retain an averaged duty state<br/>bounded by LDUTY and DMAX"]
    STEADY --> SHIGH{"PA1 at or above VMAX?"}
    SHIGH -- Yes --> SCUT["Immediately output BLOW<br/>and reduce remembered duty"]
    SHIGH -- No --> TRIM{"Filtered PA1 relative to VSET and VON"}
    TRIM -- "Above VSET + 0.4 V" --> DOWN["Slowly trim duty down"]
    TRIM -- "Below VON" --> UP["Boost duty upward<br/>report LBOOST"]
    TRIM -- "Inside loaded band with current" --> KEEP["Hold learned duty constant"]

    LOADED -- No --> NLG{"No-load guard active?"}
    NLG -- Yes --> NLBANG["Bang-bang window<br/>ON below VSET - NLDROP<br/>OFF at VSET"]
    NLBANG --> SAG{"Below low threshold for NLFULL cycles?"}
    SAG -- Yes --> FULL["Bypass no-load cap<br/>request DMAX until VMAX"]
    SAG -- No --> NLCAP["Cap high state with NLDUTY<br/>or calibrated load interpolation"]
    NLG -- No --> BANG["Normal bang-bang window<br/>ON at or below VON<br/>OFF at or above VMAX"]
    BANG --> UV{"PA1 at or below VMIN?"}
    UV -- Yes --> FULL
    UV -- No --> BH["Select BLOW or BHIGH"]

    OPEN --> DUTY
    SCUT --> DUTY
    DOWN --> DUTY
    UP --> DUTY
    KEEP --> DUTY
    FULL --> DUTY
    NLCAP --> DUTY
    BH --> DUTY

    DUTY["Optional PA0 LINEFF duty cap<br/>then clamp to DMIN and DMAX"] --> TIMING["Convert duty to PA10 period and high time<br/>enforce complete GATECYC burst width"]
    TIMING --> STATIC0{"Effective duty"}
    STATIC0 -- "0 percent" --> LOW["Drive PA10 low"]
    STATIC0 -- "100 percent and STATIC enabled" --> HIGH["Drive PA10 continuously high"]
    STATIC0 -- "Between 0 and 100 percent" --> CHOP["TIM3 period and compare events request PA10 edges<br/>pulse-skip if minimum pulse exceeds requested average"]
    CHOP --> SYNC["Wait for a TIM1 carrier update boundary<br/>then switch PA10 with GPIO BSRR"]

    CARRIER["TIM1 runs continuously in center-aligned mode<br/>CH1 PWM1 on PA8, CH2 PWM2 on PA9<br/>CCR1 to CCR2 is the dead gap on both crossings"] --> SYNC
    CARRIER --> GATES["PA8 and PA9 carrier signals"]
    LOW --> ENOUT["PA10 external enable or throttle"]
    HIGH --> ENOUT
    SYNC --> ENOUT
    GATES --> DRIVER["External gate driver and half bridge"]
    ENOUT --> DRIVER
```

## Important Boundaries

- PA1 secondary voltage is the closed-loop control signal.
- PA2 measures half-bridge current. It classifies light versus loaded operation and
  can trip protection when explicitly enabled; it is not secondary output-current
  feedback.
- PA0 affects duty only when optional `LINEFF` is enabled.
- The active controller is voltage bang-bang plus loaded steady-duty trim. Legacy
  power-loop fields remain in the settings structure for compatibility, but they do
  not form an active power-control loop.
- ADC reads in live control come only from the circular DMA buffer.
- UART work is byte-budgeted, and EEPROM writes are deferred until the output is
  off, preventing command handling or flash writes from blocking active switching.
