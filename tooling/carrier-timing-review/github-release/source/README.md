# PWR-2.0.4 V2 firmware source snapshot

This is the source snapshot for the attached V2 / STM32F410CBU6 HEX. It is a software-validated pre-release; physical bench validation is pending. The conditional G071 source remains in the canonical sketch, but no G071 firmware asset is released here.

The GitHub tag references the existing repository baseline `e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a`. That baseline contains older firmware. GitHub's automatic Source code archives contain the baseline; use this attached `pwr-2.0.4-v2-source.zip` for the actual PWR-2.0.4 firmware sources. No branch was updated and no source commit was pushed for this release.

The sketch, custom linker, build script, HEX verifier and native test scripts are byte-identical to the validated local sources. README/release documentation has been adapted for publication. `SOURCE-SHA256SUMS.txt` records every packaged source/document file. The sketch SHA-256 is `fa9d842ce7787d37501701379a66b97807969d3a9064f8d03fa372b3842b30ad`.

## Build and check

Toolchain: Arduino CLI 1.5.0, STM32 Arduino core 2.8.1, ARM GCC 13.2.1-1.1. F410 FQBN: `STMicroelectronics:stm32:GenF4:pnum=GENERIC_F410CBUX,usb=none,xserial=none,opt=oslto`.

From this directory, with Arduino CLI/core installed, run `firmware/build.ps1 -Target F410` in PowerShell. Pass `-ArduinoCli` if needed. The script supplies the custom linker and 98304-byte application limit; use the generated sparse HEX, not a flat BIN spanning the settings sector. Exact core/toolchain versions and the linker are necessary to reproduce this build configuration.

Portable host checks (Python and GCC/Clang; the protocol runner also retains its Windows/MSVC branch):

```sh
python3 firmware/test_web_protocol.py
python3 firmware/test_carrier_storage.py
python3 firmware/verify_f410_hex.py arduino-build-f410/thesi_power_control.ino.hex
```

The host tests use mocked hardware/flash and do not establish electrical behavior. Windows/MSVC execution was not tested in the cloud validation.

See [release notes](firmware/releases/pwr-2.0.4.md), [UART/web protocol](docs/web-protocol.md) and [F410 port/storage notes](docs/stm32f410-port.md). The live companion monitor is https://thesis-power-lab.vercel.app/#device-setup . Select Setup → V2 switching/carrier timing after installing compatible firmware and connecting the appropriate isolated UART link.
