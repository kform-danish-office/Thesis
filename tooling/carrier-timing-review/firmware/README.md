# PWR-2.0.4 — V2 / STM32F410CBU6 only

This is a compiled software-validation candidate. It has not been flashed or electrically verified on a physical board. No board/programmer is exposed to the cloud environment. Verify the actual fitted MCU and use the project's existing isolated-bench/SWD bring-up procedure.

The sparse Intel HEX contains vectors and application sections while excluding settings sector 0x08004000..0x08007FFF. Use the HEX with a programming method that preserves untouched sectors, then verify programming. Do not substitute a flat BIN spanning the reserved gap or use full-chip erase if stored settings must be retained. This package does not contain an automatic flasher.

After installing on the matching V2 target, open https://thesis-power-lab.vercel.app/#device-setup and expand V2 switching/carrier timing. With output OFF, enter both requested values, Apply timing, inspect actual timer readback, and use Save to device to persist settings. The new firmware alone cannot establish an electrically usable timing range.

Commands: TIMING reads timing in the native terminal; TIMING 950000 53 atomically requests 950000 Hz and 53 ns. At the nominal 100 MHz timer this realizes 943396 Hz and 60 ns (106/6 ticks). Browser wrapping is WEB <id> TIMING <Hz> <ns>. Requests are bounded to 500000..2000000 Hz and 20..200 ns, plus a coupled dead-tick/period constraint. At 2 MHz, 120 ns is accepted and 130 ns rejected. This adjusts the drive carrier; the physical LC resonance and EN burst frequency are separate.

Default steady timing remains 1 MHz / 40 ns. V2 uses balanced edge-aligned complementary PWM for finer frequency steps, so startup edge phase differs from older firmware and needs scope verification. Effective timing changes clear learned load-profile/tuned data in RAM; recalibrate before reusing load profiles. Reference resistances and applied duty settings remain operator configuration. Browser changes require explicit Save; native terminal retains the existing 1.5-second quiet-OFF deferred-save behavior.

The new 488-byte journal records pair timing and calibration. Older 471-byte payloads at 472-byte flash strides load without a boot write/erase; new records are saved only through allowed save operations. Older firmware cannot read new records and may fall back to older data or defaults. Journal wrap remains a single-sector erase; preserve settings exports and the prior firmware when planning a downgrade.

Validation: 76 web tests, 131 native protocol frames, production storage migration/corruption and all 122 interrupted-append boundaries, browser functional/responsive checks, and F410 compile/HEX verification passed. Flash 90268/98304 bytes; RAM 6868/32768; 90752 programmed HEX bytes. Real gate timing, driver non-overlap, powered converter operation and on-board persistence remain bench checks.

The current editable source and complete protocol/port documentation are retained in /workspace/working-source; validation and backups are in /workspace/tooling/carrier-timing-review. SHA256SUMS covers this package. No public GitHub release, Git push or physical flashing occurred.
