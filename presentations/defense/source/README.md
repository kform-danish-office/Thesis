# USB-C power supply defense

Editable PowerPoint in the supplied DTU Blue 16:9 template, with presenter notes and a PDF preview. The main talk has 16 slides with an estimated 25-minute speaking allocation; four supporting slides follow the conclusion.

The story begins with compact USB-C adapter demand, explains the frequency/loss tradeoff and the circuit choice, then follows the implemented control into measured switching and output performance. A V1 thermal image shows the 102.9 °C surface maximum before the V2 tank-change explanation. V2 secondary-load results illustrate the expected power-control response: more burst-enable PWM means more transferred power. Thermal results identify the remaining heating problem. The V2 thermal slide pairs the 70.75 W and 137.08 W secondary-load images with the regional temperature plot.

## Build

Install Python packages from `requirements.txt`. LibreOffice is needed to render the PDF. Arial is requested by the template; Liberation Sans is used as the metric-compatible font when rendering in this environment.

```sh
python build_defense.py
python render_defense.py
python validate_defense.py
python package_defense.py
```

The generated files are `Thesis_Defense_Supervisor_Flow.pptx` and `.pdf`. Slides and notes are defined in `proposals/`; their order and timing are in `manifest.json`. Text, tables and data charts remain editable. The three displayed equations use native Office Math with structured overbars, subscripts, fractions and radicals. The title includes a crop of the original V2 board photograph. The three main circuit views use the original digest schematic directly, with native PowerPoint crops for detail; its drawing and labels are preserved. The input-quality slide uses the original digest harmonic-current graph against IEC 61000-3-2:2018 Class A limits at approximately 80 W USB-C output. The comparison is for that measured point. Its original figure bytes and native crop are recorded in `assets/iec-harmonic-figure.json`. Scope screenshots and the thermal frame retain their original pixels; cropping is native to PowerPoint. The supplied template's masters, layouts and theme are preserved.

The complete V2 power schematic is available as a vector PDF in `assets/` for zooming during questions. Adapter photography is credited to Apple, with source URLs in `review/adapter-photo-downloads.json`. The three adapter images use an approximate common physical scale and a shared body baseline; calibration references and geometry are in `assets/adapter-scale.json`.

Timing is a speaking allocation, not a timed rehearsal. The complete deck was rendered and visually reviewed using LibreOffice. Native Microsoft PowerPoint inspection was not available.
