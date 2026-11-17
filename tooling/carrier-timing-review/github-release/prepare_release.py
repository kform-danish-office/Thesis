from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile

source = Path('/workspace/working-source')
review = Path('/workspace/tooling/carrier-timing-review')
stage = review / 'github-release'
snapshot = stage / 'source'
assets = stage / 'assets'
snapshot.mkdir(exist_ok=True)
assets.mkdir(exist_ok=True)
baseline = 'e3c3f6ac36ab1458dcf8e20dbb71da87fd1cf51a'
tag = 'pwr-2.0.4'
hex_name = 'pwr-2.0.4-v2-stm32f410cbu6.hex'
hex_bytes = (review / 'firmware' / hex_name).read_bytes()
assert hashlib.sha256(hex_bytes).hexdigest() == 'fe3a6b02f06b025ba83e53dd482bbfdf9dd166f9f2afc0fe806062eab14ded47'
(assets / hex_name).write_bytes(hex_bytes)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

code_files = ['thesi_power_control.ino', 'firmware/build.ps1', 'firmware/stm32f410.ld', 'firmware/verify_f410_hex.py', 'firmware/test_web_protocol.py', 'firmware/test_carrier_storage.py']
for relative in code_files:
    target = snapshot / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / relative, target)
    assert target.read_bytes() == (source / relative).read_bytes()

for relative in ['docs/web-protocol.md', 'docs/stm32f410-port.md']:
    text = (source / relative).read_text()
    text = text.replace('The current F410 build is a private,\nsoftware-validated candidate', 'The F410 build is a software-validated pre-release')
    target = snapshot / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)

notes = (source / 'firmware/releases/pwr-2.0.4.md').read_text()
notes = notes.replace('Private, software-validated F410 candidate; powered bench validation pending.\nNo board was flashed or powered during cloud validation. No public firmware\nrelease was created.', 'Software-validated V2/F410 pre-release; powered bench validation pending.\nNo board was flashed or powered during cloud validation.')
notes = notes.replace('`python3 /workspace/tooling/test-working-protocol-linux.py`', '`python3 firmware/test_web_protocol.py`')
notes = notes.replace('Build from the source root with `firmware/build.ps1 -Target F410`, or this\nenvironment\'s `/workspace/tooling/build-working-firmware.sh F410`. Verify with', 'Build from the attached firmware-source root with `firmware/build.ps1 -Target F410`. Verify with')
notes = notes.replace('Private review artifacts and evidence are under\n`/workspace/tooling/carrier-timing-review`; firmware is excluded from web builds.', 'The attached source ZIP contains the exact firmware/build/test sources for this build, the custom linker, documentation and a source checksum manifest. Firmware is excluded from the static web build.')
(snapshot / 'firmware/releases').mkdir(parents=True, exist_ok=True)
(snapshot / 'firmware/releases/pwr-2.0.4.md').write_text(notes)

source_readme = f'''# PWR-2.0.4 V2 firmware source snapshot

This is the source snapshot for the attached V2 / STM32F410CBU6 HEX. It is a software-validated pre-release; physical bench validation is pending. The conditional G071 source remains in the canonical sketch, but no G071 firmware asset is released here.

The GitHub tag references the existing repository baseline `{baseline}`. That baseline contains older firmware. GitHub's automatic Source code archives contain the baseline; use this attached `pwr-2.0.4-v2-source.zip` for the actual PWR-2.0.4 firmware sources. No branch was updated and no source commit was pushed for this release.

The sketch, custom linker, build script, HEX verifier and native test scripts are byte-identical to the validated local sources. README/release documentation has been adapted for publication. `SOURCE-SHA256SUMS.txt` records every packaged source/document file. The sketch SHA-256 is `{digest(snapshot / 'thesi_power_control.ino')}`.

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
'''
(snapshot / 'README.md').write_text(source_readme)
relatives = code_files + ['docs/web-protocol.md', 'docs/stm32f410-port.md', 'firmware/releases/pwr-2.0.4.md', 'README.md']
(snapshot / 'SOURCE-SHA256SUMS.txt').write_text(''.join(digest(snapshot / relative) + '  ' + relative + '\n' for relative in sorted(relatives)))
source_zip = assets / 'pwr-2.0.4-v2-source.zip'
with zipfile.ZipFile(source_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
    for relative in sorted(relatives + ['SOURCE-SHA256SUMS.txt']):
        archive.write(snapshot / relative, 'pwr-2.0.4-v2-source/' + relative)
with zipfile.ZipFile(source_zip) as archive:
    assert archive.testzip() is None
    for relative in relatives:
        assert archive.read('pwr-2.0.4-v2-source/' + relative) == (snapshot / relative).read_bytes()

binary = stage / 'binary'
binary.mkdir(exist_ok=True)
shutil.copyfile(assets / hex_name, binary / hex_name)
binary_readme = f'''# PWR-2.0.4 — V2 / STM32F410CBU6 only

Software-validated pre-release; no physical flashing or powered bench verification was performed. Confirm the actual fitted MCU and use the existing isolated-bench/SWD bring-up procedure.

Use `{hex_name}`. This sparse Intel HEX excludes settings sector 0x08004000..0x08007FFF. Use a programming method that preserves untouched sectors and verify programming. Do not use full-chip erase or a flat BIN spanning the reserved gap when retaining settings. No automatic flasher is included.

Controls: https://thesis-power-lab.vercel.app/#device-setup → V2 switching/carrier timing. With output OFF and no calibration/startup running, Apply both requested values and inspect actual readback. Browser changes require Save to device. Native terminal retains its existing 1.5-second quiet-OFF deferred save.

Requests: carrier 500000–2000000 Hz and dead time 20–200 ns, with invalid coupled pairs rejected. At the nominal 100 MHz timer, 950000 Hz / 53 ns realizes 943396 Hz / 60 ns. These are software limits, not a validated electrical operating range. Physical LC resonance and EN burst frequency are separate. Effective timing changes clear learned load profiles; recalibrate before relying on them.

Default steady timing is 1 MHz / 40 ns. The V2 timer now uses balanced edge-aligned complementary PWM; first-pulse/EN phase and actual driver non-overlap need scope checks. New saves pair timing/calibration in 488-byte records. Legacy records load without boot erasure; older firmware cannot read new wrappers and may fall back to old data/defaults after downgrade. Single-sector wrap retains its existing erase/power-loss limitation.

The release also supplies `pwr-2.0.4-v2-source.zip` with matching firmware/build/test sources and source checksums. The GitHub tag targets baseline {baseline}, whose automatic Source code archives are older. Use the attached source ZIP for PWR-2.0.4.

Validated: F410 90268/98304 program bytes; 6868/32768 RAM; 90752 programmed HEX bytes. Native protocol 131 JSON frames; storage migration and all 122 interrupted append-word boundaries; companion monitor 76 web tests and responsive/functional browser checks. Hardware actions are mocked in native/browser checks.
'''
(binary / 'README.md').write_text(binary_readme)
(binary / 'release-notes.md').write_text(notes.replace('../../docs/', 'docs/'))
(binary / 'docs').mkdir(exist_ok=True)
for name in ['web-protocol.md', 'stm32f410-port.md']:
    shutil.copyfile(snapshot / 'docs' / name, binary / 'docs' / name)
binary_files = [hex_name, 'README.md', 'release-notes.md', 'docs/web-protocol.md', 'docs/stm32f410-port.md']
(binary / 'SHA256SUMS').write_text(''.join(digest(binary / relative) + '  ' + relative + '\n' for relative in sorted(binary_files)))
binary_zip = assets / 'pwr-2.0.4-v2-f410-release.zip'
with zipfile.ZipFile(binary_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
    for relative in sorted(binary_files + ['SHA256SUMS']):
        archive.write(binary / relative, relative)
with zipfile.ZipFile(binary_zip) as archive:
    assert archive.testzip() is None
    for relative in binary_files:
        assert archive.read(relative) == (binary / relative).read_bytes()

build = {
    'firmware': 'PWR-2.0.4', 'target': 'V2 / STM32F410CBU6', 'status': 'software-validated pre-release; powered bench verification pending',
    'tag': tag, 'repository_baseline': baseline, 'tag_contains_current_firmware_source': False,
    'canonical_source_asset': source_zip.name, 'source_asset_sha256': digest(source_zip),
    'source_sketch_sha256': digest(snapshot / 'thesi_power_control.ino'),
    'source_file_hashes': {relative: digest(snapshot / relative) for relative in sorted(relatives)},
    'hex_asset': hex_name, 'hex_sha256': digest(assets / hex_name),
    'toolchain': {'arduino_cli': '1.5.0', 'stm32_core': '2.8.1', 'arm_gcc': '13.2.1-1.1', 'native_gcc': '14.2.0'},
    'fqbn': 'STMicroelectronics:stm32:GenF4:pnum=GENERIC_F410CBUX,usb=none,xserial=none,opt=oslto',
    'linker': 'firmware/stm32f410.ld', 'flash_bytes': 90268, 'flash_limit_bytes': 98304, 'static_ram_bytes': 6868,
    'hex_programmed_bytes': 90752, 'initial_sp': '0x20008000', 'reset_vector': '0x08016939',
    'reserved_settings_sector': ['0x08004000', '0x08007FFF'], 'hex_excludes_settings_sector': True,
    'tests': {'web_passed': 76, 'native_protocol_frames': 131, 'interrupted_append_word_boundaries': 122, 'physical_hardware_tested': False},
    'binary_package': {'name': binary_zip.name, 'sha256': digest(binary_zip)},
}
(assets / 'pwr-2.0.4-build.json').write_text(json.dumps(build, indent=2) + '\n')
asset_paths = sorted(path for path in assets.iterdir() if path.is_file() and path.name != 'pwr-2.0.4-SHA256SUMS.txt')
assert len(asset_paths) == 4
(assets / 'pwr-2.0.4-SHA256SUMS.txt').write_text(''.join(digest(path) + '  ' + path.name + '\n' for path in asset_paths))
manifest = [{'name': path.name, 'bytes': path.stat().st_size, 'sha256': digest(path)} for path in sorted(assets.iterdir()) if path.is_file()]
(stage / 'asset-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

body = f'''V2 / **STM32F410CBU6 only**. This pre-release adds adjustable switching-carrier frequency and complementary-gate dead time. The older G071 timing remains fixed; no G071 binary is included.

Download **`{binary_zip.name}`** for the HEX, instructions and protocol/storage notes, or download **`{hex_name}`** directly. Verify downloads with `pwr-2.0.4-SHA256SUMS.txt`. Matching firmware source is attached as **`{source_zip.name}`**.

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

The release tag references the existing repository baseline **`{baseline}`**, which contains older firmware. **GitHub's automatic “Source code” archives contain that baseline. Use the attached `{source_zip.name}` for the actual PWR-2.0.4 firmware source.** Its `SOURCE-SHA256SUMS.txt` identifies every packaged file; the sketch SHA-256 is `{digest(snapshot / 'thesi_power_control.ino')}`. `pwr-2.0.4-build.json` records the toolchain, source hashes and build checks. No branch was updated and no source commit was pushed for this release.
'''
(stage / 'release-body.md').write_text(body)
print(json.dumps(manifest, indent=2))
