# Run the project locally

Clone or download this repository. The editable thesis is in `thesis/`; the current firmware and browser app are in `working-source/`. Imported skills are in `skills/`, and project build/review records are in `tooling/`.

## Ready-to-open files

- [Full thesis PDF](thesis/Thesis_V1_V2_V3.pdf)
- [Editable defense PowerPoint](presentations/defense/Defense_Supervisor_Flow.pptx)
- [Defense PDF](presentations/defense/Defense_Supervisor_Flow.pdf)
- [Defense build source](presentations/defense/source/)
- [Complete earlier local handoff](https://github.com/kform-danish-office/Thesis/releases/download/thesis-v1-v2-v3-review/Thesis_Local_Handoff.zip)

## Browser app

Use Node.js 20 or newer. The app has no npm dependencies to install.

```sh
cd working-source/web
npm test
npm run build
npm run dev
```

The server prints its local address. Physical USB serial access requires a supported desktop browser. Hardware auto-calibration, load-reference settings and V2 timing controls are available when the connected firmware reports the corresponding capabilities.

## Firmware

Read `working-source/README.md`, `working-source/docs/stm32f410-port.md` and `working-source/firmware/releases/pwr-2.0.4.md`. The V2/F410 source is PWR-2.0.4; the G071 path remains PWR-2.0.3. Build instructions and the custom F410 linker are included. Run the source tests without hardware:

```sh
cd working-source
python firmware/test_web_protocol.py
python firmware/test_carrier_storage.py
```

Board compilation uses Arduino CLI with STM32 core 2.8.1, or the supplied PowerShell build helper. Retain the custom F410 flash layout and use the board-specific HEX. The cloud shell helpers contain `/workspace` paths and need path adaptation for a different local folder.

## Thesis

Install XeLaTeX, latexmk and PDF tools. The bibliography is manual; Biber is not needed. The build uses fonts and LaTeX packages listed in `tooling/setup-report.md`.

From `thesis/`, run:

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

For a separate output folder, create mirrored auxiliary directories as shown in `tooling/build-thesis.sh`. The existing PDF has 490 pages and contains the V1/V2/V3 discussion, colour V2 schematics, PCB sheets and the secondary-load/thermal tests. The thermal load points did not reach equilibrium; secondary-load power is distinct from USB-C connector delivery.

## Presentation

Use the editable PowerPoint directly, or build it from `presentations/defense/source/` after installing its Python requirements and LibreOffice. The supplied DTU template and original figure assets are included. The presentation has 16 main slides allocated approximately 25 minutes, followed by four supporting slides.

The GitHub source-code download now includes the editable project. See `SYNC_REPORT.md` for the export scope and checks.
