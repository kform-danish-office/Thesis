# Thesis firmware and software

The current V2 snapshot is `PWR_2_0_4`: firmware, linker/build tools, protocol and storage tests, browser runtime and tests, fonts, and supporting documentation. The F410 build identifies as PWR-2.0.4; the G071 build remains PWR-2.0.3 with fixed carrier timing. `source_manifest.json` lists the exact source hashes and `software_verification.json` records software checks.

`PWR_2_0_1` is retained as a historical snapshot, including its original manifest and software verification. The separate `thesi_power_control_PWR_1_9_20.ino` remains the measured V1.0 baseline. Earlier test results are not relabelled as current-firmware tests.

The new snapshot adds browser calibration, editable reference-load/setup settings and output-OFF carrier/dead-time adjustment. The physical test load is connected separately. Powered verification remains necessary; no board is flashed by the browser application.
