# STM32F410CBU6 Port

Firmware: `PWR-2.0.1`, retaining the `PWR-2.0.0` F410 port based on the existing
`PWR-1.9.20` control behavior and the supplied
`Schematic PDF_[No Variations] (12).pdf`, MCU sheet 4 and power sheet 3.
See the [browser protocol](web-protocol.md) for the added JSON telemetry,
correlated commands, and explicit communication lease.

## Schematic Pin Map

| Function | F410 MCU pin | Hardware |
|---|---|---|
| H_GATE | PA8, package pin 29 | TIM1_CH1, AF1 |
| L_GATE | PB13, package pin 26 | TIM1_CH1N, AF1 |
| GAN EN | PA11, package pin 32 | GPIO, scheduled by TIM5 update/compare |
| V_SENSE_P | PA0, package pin 10 | ADC1 channel 0 |
| V_SENSE_S | PA1, package pin 11 | ADC1 channel 1 |
| I_SENSE_P | PA2, package pin 12 | ADC1 channel 2; half-bridge current |
| Command TX | PA9, package pin 30 | USART1 TX; J3 pin 5 |
| Command RX | PA10, package pin 31 | USART1 RX; J3 pin 6 |
| Open-mode LED | PA3, package pin 13 | Q2 gate, active high |
| Closed-mode LED | PB14, package pin 27 | Q3 gate, active high |
| System LED | PB15, package pin 28 | Q4 gate, active high |
| SWDIO / SWCLK | PA13 / PA14 | J3 pins 2 / 12 |
| NRST | package pin 7 | J3 pin 3 |

Connect adapter RX to board TX and adapter TX to board RX. The UART is on the
primary MCU domain: use a suitably rated isolated USB-to-3.3 V UART interface
and connect its isolated board-side reference to J3 ground according to the
bench isolation procedure. Do not connect computer ground directly to an
energized, nonisolated mains-referenced primary. Use 115200 baud, 8N1, no flow
control. PA9/PA10 belong to USART1 and are never configured as gate or EN
outputs on this board.

## Carrier, ADC, and Control

The installed STM32 core's F410CBU variant uses internal HSI and PLL for 100 MHz;
the schematic does not populate an external high-speed crystal.

TIM1 generates center-aligned complementary CH1/CH1N. At a 100 MHz timer clock,
ARR=50, CCR1=25, and DTG=4 produce a nominal 1 MHz carrier with 40 ns dead time
at both transitions. The repetition counter is 1, giving one update per full
up/down cycle. CH2 stays disabled so it cannot take PA9 away from USART1.

TIM5 replaces the unavailable TIM3. The existing bounded TIM1 update-polling
path aligns non-static EN edge requests; this retains software latency and is
not a hardware-triggered zero-jitter EN output. There is no continuous 1 MHz ISR.
Static 100% EN, minimum carrier-cycle bursts, pulse skipping, and 10 kHz default
EN frequency remain available.

ADC1 scans PA0, PA1, PA2 into circular DMA2 Stream0 Channel0, with no blocking
`analogRead()` and no per-conversion CPU interrupt. At PCLK2=100 MHz, ADC clock
is 25 MHz; 84-cycle acquisition plus 12-cycle conversion takes about 3.84 us
per channel, or 11.52 us per three-channel frame (~86.8 kframes/s). Runtime
ADC overrun or DMA transfer errors mark feedback unavailable and stop EN through
the sensor fault path.

PA1 still closes the voltage loop. PA2 selects light/loaded state and supports
optional current protection. PA2 is not secondary output current. Light-load
bang-bang, loaded averaged duty, voltage overrides, no-load soft OVP, LINEFF,
startup precharge, AUTOPRE, AUTOBANG, CALLOAD 1..3, CAL3, and EXPORT are retained.

Requested control rates remain 50 Hz to 50 kHz (`CPER` 20000..20 us); default
is 40 kHz (`CPER=25`). `MAXRATE` requests 50 kHz. These are scheduling requests,
not measured guarantees: check STATUS last/max periods and overruns on hardware.

## Sense-Divider Population

The PDF labels R29/R30/R31/R32 and R27/R28 as 6.2 Mohm. Taken literally,
the primary divider is 4:1 and the secondary divider is 2:1, which cannot be
used at the stated 450 V primary / 28 V secondary operating points. Verify or
correct the populated values before enabling the converter.

The firmware retains the earlier values as assumptions:

| Sensor | Assumed population | Firmware settings |
|---|---|---|
| Primary PA0 | R29+R30+R31 = 1.50 Mohm; R32 = 10 kohm | VPRITOP=1500, VPRIBOT=10 |
| Secondary AMC0330 input | R27 = 390 kohm; R28 = 10 kohm | VSECTOP=390, VSECBOT=10 |
| AMC reference / ADC reference | 3.3 V | AMCREF=3.3, VREF=3.3 |
| LMG2652 current sense load | R50 = 820 ohm to primary ground | CSRES=820 |

A practical primary ladder is three 499 kohm resistors plus a 10 kohm bottom
resistor: set `VPRITOP 1497` for that population. It gives about 2.99 V at 450 V.
Use appropriately voltage-rated series parts. With the secondary 390k/10k divider,
28 V produces 0.70 V at the AMC input, and 36 V produces 0.90 V.
Validate PA1 voltage scaling against a meter before reusing old calibrations.

## Build and Flash

From the repository root with STM32 Arduino core 2.8.1 installed:

```powershell
.\firmware\build.ps1 -Target F410
```

The script selects `GENERIC_F410CBUX`, Cortex-M4 hardware floating point,
hardware UART without a generic Serial instance, USB off, and size optimization
with LTO. It copies the current root `.ino` into an Arduino sketch directory and
uses [stm32f410.ld](../firmware/stm32f410.ld). A stock-linker build is unsupported;
the firmware requires the custom linker's storage-layout symbols.

Artifacts: `arduino-build-f410/thesi_power_control.ino.hex`, `.bin`, `.elf`, `.map`.

Fresh `PWR-2.0.1` builds completed successfully for both targets:

| Target | Program storage | Static RAM | RAM remaining after static allocation |
|---|---|---|---|
| F410 | 85,184 / 98,304 bytes | 6,820 / 32,768 bytes | 25,948 bytes |
| G071 | 127,340 / 131,072 bytes | 9,524 / 32,768 bytes | 23,244 bytes |

The G071 build has 3,732 bytes of program storage remaining. These are compiler
size reports, not measurements of runtime control timing or validation of stack
and heap use. The HEX verifier checks record checksums, initial stack/reset
vectors, and exclusion of the settings sector:

```powershell
python firmware/verify_f410_hex.py arduino-build-f410/thesi_power_control.ino.hex
```

```powershell
STM32_Programmer_CLI.exe -c port=SWD -w arduino-build-f410/thesi_power_control.ino.hex -v -rst
```

The HEX contains reset vectors and application addresses. It does not program
the settings sector. Avoid full-chip erase when retaining settings, and use HEX
rather than BIN: the BIN includes the address gap and can overwrite settings.
The G071 build remains available with `-Target G071`.

## Saved Settings

The F410 has no native EEPROM. The existing SAVE/EXPORT interface uses a flash
journal instead:

| Region | Address | Purpose |
|---|---|---|
| Sector 0 | 0x08000000..0x08003FFF | Reset vectors; unused remainder |
| Sector 1 | 0x08004000..0x08007FFF | 16 KB settings journal |
| Sectors 2-4 | 0x08008000..0x0801FFFF | Up to 96 KB of program code and constants |
| SRAM | 0x20000000..0x20007FFF | 32 KB RAM |

Packed settings are padded to a word-aligned flash record. Saves append complete
records and verify readback. This version uses 472-byte records, giving 34 slots.
Boot scans checksummed records and selects the newest
valid sequence, skipping a torn final write. Erase occurs only when the journal
wraps or no valid settings exist. Flash writes are deferred while EN is active.

This is a single-sector journal, not a redundant two-sector store: a power loss
during the wrap erase can lose the saved settings. Missing/invalid settings use
defaults with output OFF. `STATUS` reports the slot, sequence, pending state,
and flash-layout readiness. Flash errors leave the save pending in RAM.

## Initial Commands

First check UART and raw feedback with output OFF:

```text
VER
OFF
BOOTOFF
STATUS
```

After confirming the actual divider population and measured voltage scaling:

```text
BEGINCFG
SET VREF 3.3
SET AMCREF 3.3
SET VPRITOP 1500
SET VPRIBOT 10
SET VSECTOP 390
SET VSECBOT 10
SET CSRES 820
SET FEN 10000
SET VSET 28
SET VON 28
SET VMAX 32
SET OVP 36
ENDCFG
ZEROI
VSBONLY
MAXRATE
STATUS
```

The values above assume the populations listed earlier. Use `ON` only after the
readings are correct. Check PA8/PB13 dead time and PA11 EN with the scope at low
input first. `AUTOPRE` tunes the initial burst; `AUTOBANG` and `CALLOAD 1..3` keep
their existing meanings. An old board's EXPORT block can be imported, but sensor
offsets and tuning must be checked on the new board.

For an enabled cold-start test, send `OFF`, then `BOOTON`, then `SAVE`, and power
cycle. `ON`/`OFF` alone do not change the saved boot default. `BOOTOFF` restores
disabled-on-boot behavior.

Hardware references: [ST F410 datasheet](https://www.st.com/resource/en/datasheet/stm32f410rb.pdf)
and [RM0401 reference manual](https://www.st.com/resource/en/reference_manual/dm00180366.pdf).
