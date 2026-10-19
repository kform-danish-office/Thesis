"""Check the F410 boot vectors and that a HEX image leaves sector 1 untouched."""

import argparse
from pathlib import Path
import struct


def load_hex(path):
    memory = {}
    base = 0
    ended = False
    for number, line in enumerate(Path(path).read_text(encoding="ascii").splitlines(), 1):
        if not line.strip():
            continue
        if ended or not line.startswith(":"):
            raise ValueError(f"Unexpected HEX data at line {number}")
        record = bytes.fromhex(line[1:])
        if len(record) < 5 or len(record) != record[0] + 5 or sum(record) & 255:
            raise ValueError(f"Invalid length/checksum at line {number}")
        count, high, low, kind = record[:4]
        address = (high << 8) | low
        data = record[4:4 + count]
        if kind == 0:
            for offset, value in enumerate(data):
                absolute = base + address + offset
                if absolute in memory and memory[absolute] != value:
                    raise ValueError(f"Conflicting bytes at 0x{absolute:08X}")
                memory[absolute] = value
        elif kind == 1 and count == 0:
            ended = True
        elif kind == 2 and count == 2:
            base = int.from_bytes(data, "big") << 4
        elif kind == 4 and count == 2:
            base = int.from_bytes(data, "big") << 16
        elif kind in (3, 5) and count == 4:
            pass
        else:
            raise ValueError(f"Unsupported HEX record at line {number}")
    if not ended or not memory:
        raise ValueError("Missing EOF or empty firmware")
    return memory


def verify(memory):
    if any(not 0x08000000 <= address < 0x08020000 for address in memory):
        raise ValueError("Image contains data outside the 128 KB F410 flash")
    if any(0x08004000 <= address < 0x08008000 for address in memory):
        raise ValueError("Image programs the settings sector")
    if 0x08008000 not in memory:
        raise ValueError("Application does not start in sector 2")
    try:
        vectors = bytes(memory[0x08000000 + offset] for offset in range(8))
    except KeyError as exc:
        raise ValueError("Missing initial boot vectors") from exc
    stack, reset = struct.unpack("<II", vectors)
    if not 0x20000000 < stack <= 0x20008000 or stack % 8:
        raise ValueError(f"Invalid initial stack pointer 0x{stack:08X}")
    if not reset & 1 or not 0x08008000 <= (reset & ~1) < 0x08020000:
        raise ValueError(f"Invalid Thumb reset handler 0x{reset:08X}")
    if (reset & ~1) not in memory:
        raise ValueError("Reset handler points outside emitted application code")
    return stack, reset


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hex", type=Path)
    args = parser.parse_args()
    memory = load_hex(args.hex)
    stack, reset = verify(memory)
    print(f"PASS: {len(memory)} programmed bytes; SP=0x{stack:08X}; reset=0x{reset:08X}")
    print("Settings sector 0x08004000..0x08007FFF is excluded from the HEX image.")


if __name__ == "__main__":
    main()
