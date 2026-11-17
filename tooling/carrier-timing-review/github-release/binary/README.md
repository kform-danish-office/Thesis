# PWR-2.0.4 — V2 / STM32F410CBU6 only

Software-validated pre-release; no physical flashing or powered bench verification was performed. Confirm the actual fitted MCU and use the existing isolated-bench/SWD bring-up procedure.

Use `pwr-2.0.4-v2-stm32f410cbu6.hex`. This sparse Intel HEX excludes settings sector 0x08004000..0x08007FFF. Use a programming method that preserves untouched sectors and verify programming. Do not use full-chip erase or a flat BIN spanning the reserved gap when retaining settings. No automatic flasher is included.

Controls: https://thesis-power-lab.vercel.app/#device-setup → V2 switching/carrier timing. With output OFF and no calibration/startup running, Apply both requested values and inspect actual readback. Browser changes require Save to device. Native terminal retains its existing 1.5-second quiet-OFF deferred save.

Requests: carrier 500000–2000000 Hz and dead time 20–200 ns, with invalid coupled pairs rejected. At the nominal 100 MHz timer, 950000 Hz / 53 ns realizes 943396 Hz / 60 ns. These are software limits, not a validated electrical operating range. Physical LC resonance and EN burst frequency are separate. Effective timing changes clear learned load profiles; recalibrate before relying on them.

Default steady timing is 1 MHz / 40 ns. The V2 timer now uses balanced edge-aligned complementary PWM; first-pulse/EN phase and actual driver non-overlap need scope checks. New saves pair timing/calibration in 488-byte records. Legacy records load without boot erasure; older firmware cannot read new wrappers and may fall back to old data/defaults after downgrade. Single-sector wrap retains its existing erase/power-loss limitation.

The release also supplies `pwr-2.0.4-v2-source.zip` with matching firmware/build/test sources and source checksums. The GitHub tag targets baseline e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a, whose automatic Source code archives are older. Use the attached source ZIP for PWR-2.0.4.

Validated: F410 90268/98304 program bytes; 6868/32768 RAM; 90752 programmed HEX bytes. Native protocol 131 JSON frames; storage migration and all 122 interrupted append-word boundaries; companion monitor 76 web tests and responsive/functional browser checks. Hardware actions are mocked in native/browser checks.
