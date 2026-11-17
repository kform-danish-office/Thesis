#!/bin/bash
set -euo pipefail
mkdir -p /workspace/tooling/bin /workspace/tooling/downloads /workspace/tooling/arduino-data /workspace/tooling/arduino-user
cd /workspace/tooling/downloads
curl -fsSL https://github.com/arduino/arduino-cli/releases/download/v1.5.0/arduino-cli_1.5.0_Linux_64bit.tar.gz -o arduino-cli_1.5.0_Linux_64bit.tar.gz
curl -fsSL https://github.com/arduino/arduino-cli/releases/download/v1.5.0/1.5.0-checksums.txt -o checksums.txt
rg '  arduino-cli_1.5.0_Linux_64bit.tar.gz$' checksums.txt | sha256sum -c -
tar -xzf arduino-cli_1.5.0_Linux_64bit.tar.gz -C /workspace/tooling/bin arduino-cli
cat > /workspace/tooling/arduino-cli.yaml <<'YAML'
board_manager:
  additional_urls:
    - https://github.com/stm32duino/BoardManagerFiles/raw/main/package_stmicroelectronics_index.json
directories:
  data: /workspace/tooling/arduino-data
  downloads: /workspace/tooling/arduino-downloads
  user: /workspace/tooling/arduino-user
YAML
cat > /workspace/tooling/test-working-protocol-linux.py <<'PYTHON'
#!/usr/bin/env python3
"""Compatibility entrypoint for the now-portable production protocol runner."""
import runpy
runpy.run_path('/workspace/working-source/firmware/test_web_protocol.py', run_name='__main__')
PYTHON
cat > /workspace/tooling/build-working-firmware.sh <<'SHELL'
#!/bin/bash
set -euo pipefail
cd /workspace/working-source
target=${1:-F410}
cli=/workspace/tooling/bin/arduino-cli
config=/workspace/tooling/arduino-cli.yaml
case "$target" in
 F410) fqbn='STMicroelectronics:stm32:GenF4:pnum=GENERIC_F410CBUX,usb=none,xserial=none,opt=oslto'; name=f410; extra=(--build-property upload.maximum_size=98304 --build-property 'compiler.c.elf.extra_flags="-Wl,--script=/workspace/working-source/firmware/stm32f410.ld"');;
 G071) fqbn='STMicroelectronics:stm32:Nucleo_64:pnum=NUCLEO_G071RB'; name=g071; extra=();;
 *) echo 'Expected F410 or G071' >&2; exit 2;;
esac
sketch="build-sketch/$target/thesi_power_control"
mkdir -p "$sketch"
cp thesi_power_control.ino "$sketch/"
ARDUINO_NETWORK_PROXY="${HTTPS_PROXY:-}" "$cli" compile --config-file "$config" --jobs 4 --warnings all --fqbn "$fqbn" --build-path "$PWD/arduino-build-$name" "${extra[@]}" "$sketch"
if [[ $target == F410 ]]; then python3 firmware/verify_f410_hex.py arduino-build-f410/thesi_power_control.ino.hex; fi

SHELL
python3 /workspace/tooling/test-working-protocol-linux.py
python3 /workspace/working-source/firmware/test_carrier_storage.py
export ARDUINO_NETWORK_PROXY="${HTTPS_PROXY:-}"
/workspace/tooling/bin/arduino-cli core update-index --config-file /workspace/tooling/arduino-cli.yaml
/workspace/tooling/bin/arduino-cli core install STMicroelectronics:stm32@2.8.1 --config-file /workspace/tooling/arduino-cli.yaml
bash /workspace/tooling/build-working-firmware.sh F410
bash /workspace/tooling/build-working-firmware.sh G071

cd /workspace/working-source/web
npm test
npm run build
command -v xelatex latexmk pdfinfo pdftotext pdftoppm

# Source archives and unpacked current sources are retained by the environment snapshot.
# Do not overwrite /workspace/working-source or /workspace/thesis from GitHub.
cd /workspace/tooling/tex-packages
echo '452596eb7ab5ee08ff1664a8586e243e561ff675abb88d2f764b38113c688adc  texlive-science_2024.20250309-2_all.deb' | sha256sum -c -
dpkg-deb -x texlive-science_2024.20250309-2_all.deb /workspace/tooling/tex-packages/root
cat > /workspace/tooling/build-thesis.sh <<'THESIS_BUILD'
#!/bin/bash
set -euo pipefail
cd /workspace/thesis
export TEXINPUTS="/workspace/tooling/tex-packages/root/usr/share/texlive/texmf-dist/tex//:${TEXINPUTS:-}"
mkdir -p /workspace/thesis-build
# Mirror source directories for \include auxiliary files outside the source tree.
python3 - <<'PYTHON'
from pathlib import Path
root=Path('/workspace/thesis')
for p in root.rglob('*'):
    if p.is_dir(): (Path('/workspace/thesis-build')/p.relative_to(root)).mkdir(parents=True,exist_ok=True)
PYTHON
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=/workspace/thesis-build main.tex
pdfinfo /workspace/thesis-build/main.pdf
pdftotext /workspace/thesis-build/main.pdf /workspace/thesis-build/main.txt

THESIS_BUILD
bash /workspace/tooling/build-thesis.sh


# Verify retained archives, current authorized local-source revision, and imported user skills.
python3 /workspace/tooling/verify-sources.py
