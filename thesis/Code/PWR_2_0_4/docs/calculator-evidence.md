# Resonance calculator: source register and model boundary

Checked October 19, 2026. The calculator is a browser-only design aid in the
existing test-bench app. It does not change controller settings or select parts
with verified current, voltage, temperature, isolation, or ripple ratings.

## Circuit identity and preset values

| Preset | Discrete series L | Primary-referred leakage | Resonant C | Evidence |
| --- | --- | --- | --- | --- |
| Tested V1.0 thesis nominal | 2 × 4.7 µH = 9.4 µH | about 16.5 µH | 1 nF equivalent | Thesis Chapter 4 resonance analysis, Chapter 6 standalone measurements, Appendix B tested assembly |
| Supplied transformer A scenario | 9.4 µH | 16.42 µH | 1 nF equivalent | Chapter 6 transformer A; installed A/B identity unknown |
| Latest F410 schematic (12) | nominal 10 µH, L4 SER1512-103MED | unspecified | C26 unvalued | Latest drawing sheet 3 + Coilcraft datasheet |
| F410 + inherited thesis assumptions | nominal 10 µH | assumed 16.5 µH | assumed 1 nF equivalent | Explicit what-if; borrowed values are not specified in schematic (12) |
| V1.1 drawing | nominal 8.2 µH, L4 74439346082 | unspecified | C26 unvalued | V1.1 sheet 3 + Würth datasheet |

The default result is 988,940.697 Hz from Ltotal = 25.9 µH and C = 1 nF.
At exactly 1 MHz and 16.5 µH leakage, the required discrete L is approximately
8.8303 µH with 1 nF, or the required C is approximately 978.004 pF with 9.4 µH
discrete L. These are ideal nominal component requirements, not measured results.

The default ±10% total-L and ±5% C ranges are editable design assumptions.
Drawing-only L4 presets use the manufacturer's ±20% discrete-part tolerance;
that is not a characterized tolerance of the complete installed tank. No
capacitance uncertainty or loss resistance is inferred from a schematic label.

## Sources inspected

- `Overleaf/DTU_Thesis_USB_C_Filled_Template/Chapters/04_Topology_Analysis/07_Resonant_Stage.tex`:
  nominal series tank and model limitations.
- `.../Chapters/06_Magnetics_Integration/02_Inherited_Specifications.tex`:
  transformer A leakage 16.42 µH / Lm 150.78 µH; transformer B leakage 16.50 µH /
  Lm 139.89 µH; pump inductors 34.26 and 33.09 µH. The installed A/B identity is
  not retained and no installed inductance was extracted.
- `.../Backmatter/Appendices/B_Hardware_Documentation.tex`: manufactured V1.0
  with bring-up modifications and two external Würth 7443640470B 4.7 µH parts
  in series; later V1.1 was not separately manufactured/tested.
- `Files i made/Schematic V1.pdf`, sheet 3: visually inspected. The original
  drawing shows C26/C27/C65 sharing both endpoints, a parallel resonant bank,
  ahead of L4. Individual capacitor values are not displayed.
- `Files i made/Schematic V1.1.pdf`, sheet 3: visually inspected. A single
  unvalued C26 is in series with L4 74439346082 and T1.
- `C:/Users/multi/Downloads/Schematic PDF_[No Variations] (12).pdf`, sheet 3:
  visually inspected and checked against extracted component/net labels. The
  series path is VSW -> C26 -> L4 pins 1-2 -> T1 primary; L4 pin 3 is NC.
  C26 is unvalued. T1 and pump L3 are unspecified. C24 is the separate 2 nF pump
  capacitor. C7 = 1 nF is connected between PGND and GND; it is not the series
  resonant capacitor. No C26 value is copied from C7.
- [Coilcraft SER1512 datasheet](https://www.coilcraft.com/getmedia/96260b65-ad47-4056-b696-1ca56c2663fc/ser1512.pdf):
  SER1512-103ME_ is nominal 10 µH ±20%, measured at 100 kHz, 0.1 Vrms, zero DC
  bias. This does not establish its effective installed 1 MHz inductance.
- [Würth 74439346082 datasheet](https://www.we-online.com/components/products/datasheet/74439346082.pdf):
  nominal 8.2 µH ±20% at 100 kHz / 10 mA.

PDF inspection images/text are in `tmp/pdfs/calculator_schematic12` and
`tmp/pdfs/calculator_sources`. They are verification intermediates, not public
website assets. The public app contains brief source descriptions and verified
manufacturer links; it does not upload the user's source PDFs.

## Equations

For the isolated series-path check:

```
Ltotal = Ldiscrete + Lleak (same referred side)
fr = 1 / (2 pi sqrt(Ltotal Ceq))
Ldiscrete_required = 1 / ((2 pi fr)^2 Ceq) - Lleak
Ceq_required = 1 / ((2 pi fr)^2 Ltotal)
```

Ldiscrete is the sum of uncoupled external series inductors. Magnetizing
inductance Lm is a separate shunt branch and is never added to Ltotal.
Parallel capacitor values add; series capacitance is 1 / sum(1/Ci). A single
1 nF entry in the thesis preset represents the documented lumped equivalent,
not a claimed stuffed C26/C27/C65 population.

At an operating frequency fs, XL = 2 pi fs Ltotal and XC = 1/(2 pi fs Ceq).
Z0 = sqrt(Ltotal/Ceq). For an explicitly entered positive series resistance R,
Q = Z0/R, bandwidth = R/(2 pi Ltotal), and normalized current for a fixed
sinusoidal voltage is R/sqrt(R^2 + (XL-XC)^2). It is a series-RLC illustration,
not converter gain or a measured response. The app otherwise plots reactance.

Tolerance bounds use the high-L/high-C and low-L/low-C corners. Preferred
E12/E24 suggestions are nominal comparisons; each suggested L includes the
unchanged leakage when its resulting resonance is computed.

Primary equation references: [TI resonant-frequency model](https://www.ti.com/document-viewer/lit/html/SSZTC48/GUID-448E1208-D9B0-4FF1-B7E8-481DA3288A83),
[Analog Devices RLC lab](https://wiki.analog.com/university/courses/electronics/rlc_resonance),
[Vishay preferred values](https://www.vishay.com/docs/28372/e-series.pdf).

## Separate charge-pump calculation

Thesis `Chapters/04_Topology_Analysis/05_Pump_Inductor.tex` uses the reference
triangular-current, clamped-cycle sizing approximation:

```
Lp = 1 / (16 Cp fs^2)
Cp = 1 / (16 Lp fs^2)
fs = 1 / (4 sqrt(Lp Cp))
fp_natural = 1 / (2 pi sqrt(Lp Cp))
```

For Cp = 2 nF and fs = 1 MHz, Lp = 31.25 µH and natural fp = 636.620 kHz.
The 33 µH input is a nominal supplied pump-inductor design target. Under this
approximation, fp = 2 fs / pi; matching fp to fs is not the pump-sizing rule.
The thesis attributes this method to Ammar et al., “A 1-MHz Resonant LED Driver
with Charge-Pump-Based Power Factor Correction,” DOI
10.1109/JESTPE.2021.3083404. This check does not establish clamp completion,
power, current stress, or component ratings.

The complete hardware includes the pump, transformer magnetizing branch,
rectifier, load, nonlinear capacitances and burst control. Being above the ideal
series resonance alone is not proof of zero-voltage switching.

## Magnetizing branch and supplied A/B comparisons (October 25, 2026)

The user-supplied measurement table matches Chapter 6: transformer A has
16.42 µH leakage, 150.78 µH magnetizing inductance and Np/Ns = 8.039;
transformer B has 16.50 µH leakage, 139.89 µH magnetizing inductance and
Np/Ns = 8.000. The installed A/B identity remains unknown. The selector applies
leakage and Lm together as a comparison, preserving the entered external L and C.
Only the explicit transformer-A preset preselects a measured reference; other
presets leave Lm blank. Blank means unknown, not zero. Manual changes to either
leakage or Lm detach the selected measurement identity.

The primary-referred equivalent is Cr in series with Lr, feeding Lm in parallel
with the reflected AC load. Lr = Lexternal + Lleak. The series-resonance reference
therefore remains independent of Lm. Adding Lm into that sum for the loaded
series calculation would confuse the series path with the shunt branch.

An optional separate ideal branch calculation adds:

```
Xm(fs) = 2 pi fs Lm
inductance_ratio = Lm / Lr
f_open = 1 / (2 pi sqrt((Lr + Lm) Cr))
```

The last relation is the zero-input-reactance LC frequency only in the ideal
open-secondary limit, when the rectifier is nonconducting, Lm is linear and
primary-referred, and switching/pump/clamps/parasitics are omitted. It is not a
prediction of the loaded converter's gain, operating frequency or ZVS. The
series-RLC plot still excludes Lm. No magnetizing current is inferred without
the branch voltage/waveform. Missing fs leaves Xm unknown.

For external L = 9.4 µH, Cr = 1 nF and fs = 1 MHz:

| Supplied reference | Series fr | Ideal open-secondary f_open | Xm | Lm / Lr |
| --- | --- | --- | --- | --- |
| A | 990.472 kHz | 378.726 kHz | 947.379 Ω | 5.83966 |
| B | 988.941 kHz | 390.878 kHz | 878.955 Ω | 5.40116 |

The 34.26 / 33.09 µH measurements belong to the separate pump inductors,
not the external 9.4 µH resonant path. Their measured Rac values 2.05 / 2.17 Ω
are not treated as equivalent series-tank loss at 1 MHz without measurement
frequency and fixture evidence. Np/Ns affects load reflection and gain, which
are outside the isolated LC estimates; it is retained as source metadata.

JSON exports add optional magnetizingBranch and transformerReference fields,
plus Lm in the SI inputs and model assumptions. CSV/table exports include the
branch values and their basis. The existing v1 fields and series solution are
preserved. Invalid Lm gets local feedback and clears stale/exportable results;
clearing Lm restores the base series calculation. Supporting records and source
details use keyboard-accessible disclosures to keep the main workflow compact.
