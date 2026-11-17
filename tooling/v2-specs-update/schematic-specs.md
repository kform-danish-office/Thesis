# New V2 schematic: sourced technical notes

Read-only inspection of the uploaded four-sheet Altium PDF. PDF JavaScript was not executed. This is a design drawing, not a bill of actually fitted parts or a completed electrical test.

## Identity and revision

- Source: `uploaded/Documentation/Schematic Print/_SCH DWG NO__SCH.PDF`, 4 pages, PDF metadata creation date October 27, 2026.
- SHA-256: `c2623551c7094d2caa60efbbd3dab674b49553c6a3e39d8407afe83cb36c8ad2`.
- Old export: `thesis/Pictures/Thesis/07_Hardware/Schematic_V2_F410_2026-10-18.pdf`, SHA-256 `7c2663d7d6780af657d53fcdf9cab8c8eb2d8ed29d1752392ff123f5de080270`.
- The new title blocks still contain placeholders (`*`, `<SCH DWG NO>`, etc.). A project-revision hash followed by `[Refreshing ...]` is visible on sheets 3–4, but this is not a human-readable assigned circuit revision. Refer to this as the October 27 V2 drawing/export, not a newly numbered circuit revision.
- Sheet 1 is a system overview joining MCU, LLC+PFC, and USB-PD blocks. The new export adds functional boxes/headings and groups the drawing more clearly.

## Confirmed design specifications

| Function | Drawing content | Source |
| --- | --- | --- |
| Controller | U8 STM32F410CBU6 | p.4 MCU & POWER |
| High gate | H_GATE to PA8 (package pin 29) | p.4 CONTROL & SENSE INTERFACE and U8 symbol |
| Low gate | L_GATE to PB13 (pin 26) | p.4 |
| Enable | GAN EN to PA11 (pin 32) | p.4 |
| UART | PA9 TX / PA10 RX (pins 30/31), through J3 pins 5/6 | p.4 STLINK and U8 |
| Debug/service | J3 STLINK_TC30+70; SWDIO PA13, SWCLK PA14; NRST; PB3 SWO; SCL/SDA service connections | p.4 STLINK |
| ADC nets | V_SENSE_P → PA0 (pin10), V_SENSE_S → PA1 (pin11), I_SENSE_P → PA2 (pin12) | p.4 CONTROL & SENSE INTERFACE |
| ADC front end | No TLV9064 buffer block in V2 drawing; those nets connect directly to PA0–PA2 | p.4 |
| Status | D14 RGB LED, Q2/Q3/Q4 switching channels from PA3/PB14/PB15 | p.4 RGB STATUS LED |
| GaN half bridge | U3 LMG2652RFBR, +12V AUX bias, H_GATE/L_GATE commands, GAN EN | p.3 GaN HALF BRIDGE |
| Local driver capacitors | C29 1µF at AUX/+12, C30 22nF bootstrap | p.3 GaN HALF BRIDGE |
| Input bridge | D4, D5, D9, D10 all labeled S4D02120T | p.3 MAINS RECTIFIER |
| Pump diodes | D6, D7, D8 all labeled S4D02120T | p.3 LLC RESONANT / TRANSFORMER |
| Input filtering | L2 explicitly 100µH / 7447480101; C21–C23 each10nF; F1 04653.15DR; R13 SL082R503; R14 ERZV07D471 | p.3 AC INPUT / EMI FILTER |
| Input connector | P3 691322110003 | p.3 |
| Discharge IC | U11 CAP300DG, R47/R48 each6.2MR, connected to the two line conductors | p.3 AC INPUT / EMI FILTER |
| Pump/link | C24 2nF; L3 value missing; D6–D8 as above; C25 10µF HVVCC-to-PGND link capacitor | p.3 LLC RESONANT / TRANSFORMER |
| Original external series inductor | L4 SER1512-103MED; pins1–2 used, pin3 NC | p.3 resonant branch |
| Resonant capacitor | C26 has reference but no printed value | p.3 resonant branch |
| Transformer | T1 symbol has no printed component definition/turns ratio/leakage value | p.3 resonant branch |
| Primary bias | U2 BAC1S12SC, AC(L)/AC(N) from line, output labeled+12; U10 TVS1400DRVR on this rail | p.3 PRIMARY AUXILIARY12V |
| Primary3.3V | U6 LMR54410DBVR, L6 74404054068, output MCU_3_3V | p.3 PRIMARY MCU3.3V |
| Secondary3.3V | U4 LMR54410DBVR, L5 74404054068, output SEC_3_3V | p.3 SECONDARY3.3V |
| Isolated sensing | U5 AMC0330RQDWVRQ1, V_SENSE_S output to PA1; primary-side supply/reference MCU_3_3V, secondary-side supply SEC_3_3V | p.3 ISOLATED SECONDARY VOLTAGE SENSE |
| Primary divider | R29,R30,R31,R32 each6.2MR; HVVCC through three series upper resistors, PA0 sense at top of R32, R32 toPGND | p.3 PRIMARY VOLTAGE SENSE |
| Secondary divider | R27/R28 each6.2MR; VCC throughR27 to AMC INP, R28 from sense node toGND | p.3 isolated sense |
| Current signal | U3 CS pin4 → I_SENSE_P → PA2; R50 820R toPGND | p.3/p.4 |
| USB power stage | U1A/U1B MPQ4242GVE-0000-AEC1-P, buck-boost stage, USB-C connector J1 629722000214 | p.2 USB PD CONTROLLER, POWER STAGE & USB-C |
| USB current shunt | R3 0.01R between USB_PD_OUT_GND andGND, ISENS inputs | p.2 |
| USB service | P2 TSW-103-07-G-S, PD_SCL/PD_SDA/GND | p.2 I2C SERVICE HEADER |
| USB protections | D3 TVS2200DRVR; D2/D11 824012823 onUSB data/CC paths | p.2 USB-C & PROTECTION |

Do not infer device voltage/current/temperature ratings merely from part-number digits. The above are drawing labels; actual fitted markings still need confirmation when interpreting bench tests.

## Connectivity distinctions that matter to thesis prose

- The rectified input bridge positive is BULK, its return PGND. The pump feeds HVVCC. C25 is on HVVCC after the pump, not directly across the line bridge.
- VSW → C26 → L4 pins1–2 → T1 primary; the other primary terminal returns toPGND. The separate pump branch uses L3. L3 is not the external series resonant L4.
- Secondary bridge CR1–CR4 rectifies T1 secondary into VCC/GND. W1/W2 connect VCC toward LLC_OUT, then USB stage PW_IN/V_PW_OUTPUT_BULK. The downstream regulated USB_PD_OUT is separate.
- PA1 is isolated-secondary-bulk feedback, not direct USB connector VBUS. PA2 is the LMG2652 primary half-bridge-current signal, not output current. R3 is the downstream USB output shunt and is a different current path.
- PrimaryPGND and secondaryGND remain distinct. C7 is a1nF PGND–GND capacitor, not the resonant C26.

## Actual differences from the October18 export

Visual and token-level comparison of the electrical sheets found no new printed tank values, no changed ADC divider values, and no changed controller pin assignment. The visible major component identifiers and power-network arrangement remain the same. The new export mostly adds descriptive block boxes/headings and tidies presentation/unused port labels. The input connector string is corrected/expanded from the earlier `322110003` visible text to `691322110003`. It is safe to update the circuit-document source and show the new grouped schematic, but do not describe a wholesale electrical redesign from this PDF alone.

The new PDF does **not** resolve these older drawing gaps:

1. C26 still has no value. Do not replace the reported bench1.66/1.667nF value with an inferred schematic value.
2. L3 and T1 definitions/measurements remain missing.
3. The visible R29–R32 values imply a literal4:1 divider, and R27/R28 imply2:1. These still disagree with the firmware's intended1.50MΩ/10kΩ and390kΩ/10kΩ conversion scales. Do not claim that the October27 schematic corrected the divider labels.
4. Drawing L4 is still present. The bench-reported external-inductor removal, leakage-only tank, and60ns software dead-time setting belong to the later tested configuration and must be described separately.
5. There is no switching-frequency/dead-time setting in the schematic. The1MHz/40ns archived PWR-2.0.1 description comes from firmware, not this PDF. The reported60ns trial is separate.
6. No100W continuous rating, measured efficiency, thermal equilibrium, verified ZVS, or USB-PD conformance is established by a design drawing.

## Safe thesis narrative

V1.0/G071 provides the matched measured baseline. V2 integrates the F410 controller, gate commands and UART service on the power PCB, retains the LMG2652 charge-pump/resonant conversion path and isolated secondary sensing, and feeds the separate MPQ4242 USB-C output stage. The October27 grouped schematic and PCB documentation describe that V2 design. Preliminary powered V2 testing then used the reported leakage-only resonant tank and60ns software dead time; the reported95W thermal image and unresolved bridge heating remain preliminary observations rather than a continuous-power rating.
