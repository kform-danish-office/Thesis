#!/usr/bin/env python3
"""Run the repository's unchanged C++ harness and JSON assertions using GCC."""
from pathlib import Path
import subprocess
root = Path('/workspace/Thesis')
path = root / 'firmware/test_web_protocol.py'
source = path.read_text()
setup, rest = source.split('vswhere = ', 1)
checks = rest[rest.index('frames = '):]
namespace = {'__file__': str(path)}
exec(compile(setup, str(path), 'exec'), namespace)
out = namespace['out_dir']
subprocess.run(['g++', '-std=c++17', '-Wall', '-Wextra', '-O2', str(namespace['cpp']), '-o', str(out / 'protocol_harness')], check=True)
namespace['result'] = subprocess.run([str(out / 'protocol_harness')], capture_output=True, text=True, check=True)
exec(compile(checks, str(path), 'exec'), namespace)
