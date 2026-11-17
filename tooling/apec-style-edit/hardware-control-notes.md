# Hardware and control prose revision

The latest user request was to use a more technical APEC-digest style and remove the overly elementary explanations. No separate APEC digest manuscript was available locally; the revision uses concise power-electronics conference prose while retaining the user's direct, factual, mostly impersonal voice. This request supersedes the older beginner-reader preference for this pass.

Scope: Chapters 07–08 only. No source code, data, figures, tables, equation blocks, manifests, build artifacts, or GitHub files were changed.

## Word counts

Counts include LaTeX source, tabular content, captions, and commands, using whitespace separation consistently before and after.

| Scope | Before | After | Change |
|---|---:|---:|---:|
| Chapter 07 | 5,840 | 5,064 | −776 (13.3%) |
| Chapter 08 | 5,031 | 3,976 | −1,055 (21.0%) |
| Total | 10,871 | 9,040 | −1,831 (16.8%) |

## Editorial changes

- Replaced chapter-opening MCU/pin tutorials with architecture, operating requirements, and implementation scope.
- Condensed timer, ADC, DMA, UART, and register explanations to their implementation role. Signal functions remain tied to their board-specific pin assignments.
- Kept software identifiers in the contextual identity table and used descriptive control stages elsewhere.
- Tightened V2 integration, sensing, and V3 layout discussions without changing operating values or elevating reported observations to validated ratings.
- Condensed control development and voltage-control prose while retaining its implementation constraints and validation gaps.

## Examples

Before: “A peripheral is a hardware block inside the MCU, such as a timer, converter, or serial interface. Timer TIM1 was configured to generate the paired carrier commands on outputs PA8/PA9 in center-aligned mode, where the counter runs up and down.”

After: “The Arduino STM32 framework was used with direct peripheral configuration. Center-aligned TIM1 generates the carrier commands at PA8/PA9: [unchanged carrier and dead-time values].”

Before: “ADC1 is the internal analog-to-digital converter that turns each input voltage into a numerical reading. It scans the scaled primary-voltage input PA0, secondary-bulk-voltage input PA1, and half-bridge-current input PA2 continuously.”

After: “ADC1 continuously scans primary voltage at PA0, secondary-bulk voltage at PA1, and half-bridge current at PA2 through DMA2 Stream0 Channel0, independently of carrier phase.”

Before: “At light or no load, duty follows a hysteretic high/low state: different voltage thresholds are used to increase and reduce transfer, so a small change near one threshold does not repeatedly reverse the decision.”

After: “Light/no-load operation uses hysteretic high/low duty, while loaded operation trims a stored duty command from bulk-voltage error.”

## Preserved technical qualifications

- The baseline G071 SENSOR path checks the acquisition-running flag; it does not establish detection of every ADC/DMA conversion or transfer error. The V2-specific ADC overrun/DMA error polling remains distinct.
- Burst-edge polling attempts synchronization within a bounded wait; successful synchronization is not guaranteed.
- The archived V2 source remains nominally 40 ns. The later bench report remains a 60 ns software setting with unrecorded firmware identity.
- PA2 remains primary half-bridge current, not connector output current. PA1 remains the secondary bulk upstream of the USB-PD stage.
- V2 measured/reported power, pending calibration, and missing assembly dimensions retain their limits. The V3 8% estimate remains a reduced-function layout estimate.

## Checks

Compared edited chapter sources with `/workspace/tooling/apec-style-edit/before` using multiset comparisons. SI expressions, citation commands, label definitions, and complete equation, table, figure, and code-listing environments are unchanged. No thesis build was run by this agent, as requested; the parent agent owns full compilation and final review.

## Edited files

| File under `Chapters/` | Before | After |
|---|---:|---:|
| `07_Hardware/04_GaN_Half_Bridge.tex` | 429 | 357 |
| `07_Hardware/05_Gate_Drive.tex` | 185 | 107 |
| `07_Hardware/08_Sensing.tex` | 321 | 249 |
| `07_Hardware/09_Protection.tex` | 179 | 156 |
| `07_Hardware/10_Auxiliary_Power.tex` | 165 | 140 |
| `07_Hardware/14_BOM_Manufacturing.tex` | 322 | 299 |
| `07_Hardware/16_V2_F410.tex` | 1447 | 1137 |
| `07_Hardware/17_V3_Edge_Card_Plan.tex` | 755 | 654 |
| `07_Hardware/chapter.tex` | 206 | 134 |
| `08_Control_Firmware/01_Control_Objectives.tex` | 187 | 88 |
| `08_Control_Firmware/02_Architecture_Timing.tex` | 630 | 462 |
| `08_Control_Firmware/03_Feedback_Calibration.tex` | 328 | 252 |
| `08_Control_Firmware/04_V0_Open_Loop.tex` | 86 | 39 |
| `08_Control_Firmware/05_V1_Blocking_Closed_Loop.tex` | 64 | 34 |
| `08_Control_Firmware/06_Blocking_Limitations.tex` | 64 | 34 |
| `08_Control_Firmware/07_V2_DMA.tex` | 162 | 134 |
| `08_Control_Firmware/08_Control_Law.tex` | 513 | 431 |
| `08_Control_Firmware/10_Open_Circuit_Safety.tex` | 227 | 209 |
| `08_Control_Firmware/11_State_Machine.tex` | 504 | 489 |
| `08_Control_Firmware/12_Fault_Handling.tex` | 309 | 293 |
| `08_Control_Firmware/13_Timing_Resources.tex` | 147 | 135 |
| `08_Control_Firmware/14_Version_Comparison.tex` | 164 | 134 |
| `08_Control_Firmware/15_PWR_2_Port.tex` | 968 | 752 |
| `08_Control_Firmware/chapter.tex` | 481 | 293 |
