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

