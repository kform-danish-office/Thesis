# Independent review of Chapters 7–8 wording changes

Compared current chapter source with thesis-natural-voice/before. Read-only review; no source edits made.

Actionable findings:

1. **Queue-drop condition became inaccurate.** In `Chapters/08_Control_Firmware/15_PWR_2_Port.tex`, "Periodic samples are dropped when the queue is full" conflicts with the archived firmware: `serviceWebTelemetry()` queues a periodic sample only if `webTxCount < 2`, reserving two of four frame slots for commands/events. Periodic samples therefore start dropping before the queue is full. Use "when the transmit queue is congested" or state the reservation threshold. Confirmed against `Code/PWR_2_0_1/thesi_power_control.ino` around lines 4242–4247.

2. **Unavailable thermal metadata became a claim that it was never recorded.** In `Chapters/07_Hardware/13_Thermal.tex`, "The full test duration and ambient conditions were not recorded with the high-power captures" goes beyond the baseline's statement that this information is missing from the captures. Use "The supplied high-power captures do not include the full test duration and ambient conditions."

3. **Unavailable V2 configuration metadata became a claim about historical recording.** In `Chapters/07_Hardware/16_V2_F410.tex`, "These details were not recorded together" goes beyond the baseline's "These matched details are missing." Use "The supplied records do not include these details together."

No other actionable technical-meaning, evidence-strength, or grammar regressions were found in this scope. The baseline/V2 distinction, programmed versus actual dead time, calibration limitations, no direct connector-current interpretation of PA2, pending ZVS measurements, and USB-PD qualification limits are preserved.
