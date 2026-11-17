# Read-only cross review of Chapters 7–8

The function-first wording is substantially clearer. Sensing inputs are distinguished from power terminals, low-voltage gate commands are distinguished from load current, F410 pin reuse is explicitly explained, and timer-register / ADC-channel / DMA-route labels are separated. Actual pin assignments and timing values were not changed. The programmed-versus-measured dead-time caveats are retained.

Actionable findings:

1. **Narrow the G071 SENSOR fault description.** `08_Control_Firmware/12_Fault_Handling.tex` now says a failure in ADC conversion or DMA transfer to memory latches SENSOR. The archived PWR-1.9.20 implementation only checks `!adcDmaRunning` in `checkFaults()` (`Code/thesi_power_control_PWR_1_9_20.ino:1878`); the flag is set by acquisition setup. This does not establish detection of arbitrary runtime conversion or transfer failures. Suggested wording: “If ADC/DMA acquisition has not started, SENSOR is latched.” A version of “The software acquisition state is checked; if it is not running, SENSOR is latched” also preserves the narrower behavior.

2. **Make the carrier alignment an attempt.** `08_Control_Firmware/02_Architecture_Timing.tex` describes bounded polling “used to align burst transitions.” The code's `waitForCarrierBoundaryPolled()` may return false and `setPA10HighCarrierSynced()` still changes the pin after incrementing the abort counter (`...ino:1129–1151`). Suggested wording: “This bounded polling attempts to align burst transitions; the output can still change after a polling timeout.” It must not read as guaranteed hardware synchronization.

3. **Avoid attributing 1 MHz to the counter clock.** In the same opening paragraph, “using center-aligned counting at 1 MHz” can be read by a new reader as the internal count-clock rate. The value describes the generated carrier. Prefer “TIM1 was configured in center-aligned mode to generate the paired 1 MHz carrier commands on PA8/PA9.” The following nominal dead-time quantity can remain as written.

No other actionable technical regressions were found in the new Chapter 7–8 explanations. The review made no source edits, builds, manifest changes or GitHub actions.
