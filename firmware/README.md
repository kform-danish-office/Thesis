# Firmware Files

The active firmware is kept at the repository root:

- [../thesi_power_control.ino](../thesi_power_control.ino)

Supporting firmware folders:

| Path | Purpose |
|---|---|
| [archive/snapshots](archive/snapshots) | Historical `.ino` source snapshots by firmware version |
| [archive/legacy-autofull](archive/legacy-autofull) | Early voltage/autofull experiment kept for traceability |
| [compile-sketches](compile-sketches) | Older Arduino wrapper sketches kept for reference |
| [build.ps1](build.ps1) | Builds the current source for F410CBU6 or G071 |
| [stm32f410.ld](stm32f410.ld) | F410 memory layout: reset vectors, reserved settings sector, application |

Current development should happen in [../thesi_power_control.ino](../thesi_power_control.ino).

For the new board, run `./firmware/build.ps1 -Target F410` from the repository root.
Read [the F410 port notes](../docs/stm32f410-port.md) for the schematic pin map,
sense-divider discrepancy, flash layout, and first-start commands.
