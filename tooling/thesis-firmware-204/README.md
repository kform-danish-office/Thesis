# Thesis firmware and scope update

Updated the current V2 firmware description and full source listings to PWR-2.0.4 (F410). The same source builds G071 as PWR-2.0.3 with a fixed carrier. Added direct explanations of browser calibration, connected reference-load settings, OFF-only atomic carrier/dead-time adjustment, timer resolution, learned-profile clearing, readback and persistence. Historical code and earlier measurement attribution remain intact.

The 240 W USB-PD EPR point is mentioned once as a higher-load question raised in APEC digest feedback. It is no longer a project objective. The actual 100 W target and 65 W minimum remain.

Current frozen software: `/workspace/thesis/Code/PWR_2_0_4` (48 files). Historical snapshot: `/workspace/thesis/Code/PWR_2_0_1`. Editable firmware/web: `/workspace/working-source`, unchanged apart from normal generated build products. No board was flashed or accessed. `/workspace/Thesis` remains clean at the original reference commit.

Validation:

- `python3 firmware/test_web_protocol.py` from the current thesis snapshot: 131 JSON frames passed.
- `python3 firmware/test_carrier_storage.py`: legacy migration, corruption, torn records and all 122 interrupted-append boundaries passed.
- `npm test` and `npm run build` from snapshot/web: 76 tests passed and 15 runtime/font files built. Generated test/build outputs were moved out of the source tree into this review directory.
- `bash /workspace/tooling/build-working-firmware.sh F410`: 90,268/98,304 program bytes; 6,868/32,768 static RAM bytes. HEX 90,752 programmed bytes; settings sector excluded.
- `bash /workspace/tooling/build-working-firmware.sh G071`: 130,424/131,072 program bytes; 9,544/32,768 static RAM bytes.
- `bash /workspace/tooling/build-thesis.sh`: 492-page complete thesis. No missing glyphs/references/citations, no overfull horizontal/vertical boxes or physical-page text overflow. All 12 chapters, references, A–J appendices, four current V2 schematic sheets and 31 PCB pages retained. 82 nonfatal underfull horizontal messages and existing math-font substitutions remain.
- `python3 /workspace/tooling/thesis-firmware-204/audit.py`: 23 existing files edited, 50 added, 468 prior files unchanged, 541 total. Numerical measurements, images and historical firmware unchanged; all 48 current snapshot files byte-match working-source.
- `python3 /workspace/tooling/verify-sources.py`: original archives, approved current sources and clean selected checkout pass.
- `check-pdf.py` and `package.py` in this review: PDF completeness and 541-member ZIP CRC/member hashes pass. Main calibration/timing pages visually inspected.

Tools: Arduino CLI 1.5.0; STM32 Arduino core 2.8.1; Node v24.19.0; Python 3.12.14; latexmk 4.86; XeTeX 0.999996 (TeX Live 2025/dev/Debian).

The long HTML source line is printed directly from the untouched file. A listings bookkeeping-width cap avoids TeX dimension overflow, Unicode parallel-symbol handling restores the missing glyph, and a scoped broken-line penalty allows that physical line to continue across pages. Body margins remain 30 mm.

Powered timing, calibration accuracy, physical UART/stop response, on-board flash and converter performance remain to be checked on hardware. Software timing limits are not an established electrical operating range.

Technical and prose reviews: `main-technical-review.md`, `final-review.md`, `epr-scope-review.md`. Final review has no actionable findings. Exact edits and byte/hash checks are recorded alongside this report.

Existing review prerelease refreshed under prior download-publication authorization. All three remote asset sizes/digests match local artifacts; fresh downloads byte-match. Downloaded source ZIP CRC and 541 entries pass. Evidence: `github-release/published-state.json` and `download-verification.json`.
