V2 / **STM32F410CBU6 only**. This pre-release adds adjustable switching-carrier frequency and complementary-gate dead time. The older G071 timing remains fixed; no G071 binary is included.

Download **`pwr-2.0.4-v2-f410-release.zip`** for the HEX, instructions and protocol/storage notes, or download **`pwr-2.0.4-v2-stm32f410cbu6.hex`** directly. Verify downloads with `pwr-2.0.4-SHA256SUMS.txt`. Matching firmware source is attached as **`pwr-2.0.4-v2-source.zip`**.

### Timing controls

- Companion monitor: https://thesis-power-lab.vercel.app/#device-setup → **V2 switching/carrier timing**.
- Request **500,000–2,000,000 Hz** and **20–200 ns** as one atomic pair. Changes require output OFF and idle startup/autotune/calibration; they never enable output automatically.
- Actual timer values are reported separately from requests. At a nominal 100 MHz timer, 950,000 Hz / 53 ns realizes 943,396 Hz / 60 ns. Not every pair is valid: at 2 MHz, 120 ns is accepted and 130 ns rejected.
- This adjusts the drive carrier. LC resonance is set by the physical components, and `FEN` remains the separate burst frequency.
- Effective timing changes clear learned load-profile/tuned data. Recalibrate explicitly before reusing profiles. Browser Apply changes RAM; **Save to device** persists timing and calibration together. Native terminal retains its existing quiet-OFF deferred save.

### Hardware and settings

**Software validation has passed; powered bench validation is pending.** The ranges above are software limits, not a validated electrical operating range. Default steady timing remains 1 MHz / 40 ns, but the new balanced edge-aligned PWM changes startup phase. Check actual gate non-overlap, first pulses and EN alignment on the bench. No board was flashed or powered during cloud validation.

Use the sparse HEX and the existing SWD procedure, preserving settings sector `0x08004000–0x08007FFF`. Avoid full-chip erase or a flat BIN spanning the reserved gap when retaining settings. New 488-byte records pair timing and calibration; legacy settings load without a boot write/erase. Older firmware cannot read new wrappers and may load older settings/defaults after downgrade. Single-sector journal wrap retains its existing power-loss limitation.

### Validation

- F410 compile: **90,268 / 98,304 bytes** program; **6,868 / 32,768 bytes** RAM.
- HEX: **90,752 programmed bytes**; vectors valid; reserved settings sector excluded.
- Native protocol: **131 JSON frames**; timing math, scheduler, OFF/busy/lease, readback and profile checks passed.
- Production storage tests: legacy migration, corruption/torn records and all **122 interrupted append-word boundaries** passed with mocked flash.
- Companion monitor: **76 web tests** plus responsive/keyboard, timing readback and recording/export checks passed. Hardware and physical flash behavior are not established by these checks.

### Source provenance

The release tag references the existing repository baseline **`e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`**, which contains older firmware. **GitHub's automatic “Source code” archives contain that baseline. Use the attached `pwr-2.0.4-v2-source.zip` for the actual PWR-2.0.4 firmware source.** Its `SOURCE-SHA256SUMS.txt` identifies every packaged file; the sketch SHA-256 is `fa9d842ce7787d37501701379a66b97807969d3a9064f8d03fa372b3842b30ad`. `pwr-2.0.4-build.json` records the toolchain, source hashes and build checks. No branch was updated and no source commit was pushed for this release.
