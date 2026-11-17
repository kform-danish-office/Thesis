# PWR-2.0.4 main-text review

Read-only source comparison against `/workspace/working-source/thesi_power_control.ino` and its firmware release/protocol notes. No thesis files changed by this review.

## Findings

1. **Scope the coarse/fine search to no-load and reference-load calibration.** `Chapters/08_Control_Firmware/15_PWR_2_Port.tex:55` introduces precharge with the duty searches in one paragraph, which can suggest precharge uses the same coarse/fine routine. Only the no-load/reference-load path uses `autotunePowerFull`; precharge calls `autoTunePrecharge`. Suggested sentence: “For no-load and reference-load calibration, the existing coarse and fine duty search is used to select a burst duty from the measured secondary-bulk voltage.”

2. **Describe primary-reference capture as feed-forward setup, not sensor calibration.** `15_PWR_2_Port.tex:57` calls current-zero and primary-voltage-reference capture “sensor calibration.” The first adjusts current offset; the second assigns `cfg.lineFfRefV` and enables feed-forward without calibrating the primary-voltage conversion. Suggested wording: “Current-sensor zeroing and primary-voltage-reference capture for line feed-forward are also provided.” Source: `runWebCalibration`, lines 4878–4885.

## Cross-document consistency

- Current introductory architecture says “fixed-frequency half bridge” in `Chapters/01_Introduction/10_Controller_Basics.tex:5`. This remains physically correct within each powered interval because carrier changes are OFF-only. “Half bridge at the configured carrier frequency” would make the current capability clearer without implying frequency-modulated closed-loop control.
- The Chapter 8 opening describes the historical development with a fixed carrier and is followed immediately by current additions. No correction required.
- Original baseline architecture/timing, functional requirements explicitly scoped to the original prototype, V1 compliance records and fixed-FEN duty-search statements remain accurate. Do not blanket-replace these.
- `Chapters/12_Conclusion/03_Contributions.tex` lists only the initial V2 port/browser additions. Add a short current-stage sentence about browser calibration and OFF-only carrier/dead-time adjustment to complete the contributions summary; retain earlier bench attribution.
- `Chapters/12_Conclusion/02_Research_Questions.tex` describes fixed-carrier feedback within operation. It remains accurate. A short statement that the carrier can be configured while OFF is optional where discussing the later V2 controls.

## Verified

- Main timing section matches the actual default 1 MHz/40 ns, F410-only numerical ranges, even-period selection, upward dead-time rounding, 4Nd<Np constraint, 950 kHz/53 ns example, actual-count burst scheduling and OFF/idle application.
- Edge alignment is stated explicitly; no false claim of active carrier-frequency auto-tuning or PI identification.
- Learned profiles are cleared only when applied period/dead-time counts change; resistances, sensor calibration and applied duty settings remain.
- Browser RAM-only changes and terminal 1.5 s OFF-state auto-save are distinguished correctly.
- Settings record size and slot count are 488 bytes / 33. Legacy loading and erase-interruption limitation are described accurately.
- Old V1 measurements and preliminary V2 powered trials remain separate from software verification of adjustable firmware.
- All 65 files currently copied into `Code/PWR_2_0_4` are byte-identical to matching files in `/workspace/working-source`; none lacks a counterpart.
- Pin roles, first-use context, and prose follow the practical engineering voice. No MCU tutorial or random revision-number scatter was introduced.
