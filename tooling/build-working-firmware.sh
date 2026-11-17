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

