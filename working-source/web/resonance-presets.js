// Source-backed nominal values. Unknown schematic values deliberately stay null/empty.
export const SOURCES = {
  thesisTank: {
    title: 'Thesis Chapter 4: Resonant Network and Transformer Ratio',
    detail: '07_Resonant_Stage.tex: 9.4 µH external series inductance + approximately 16.5 µH primary-referred leakage, with 1 nF equivalent resonant capacitance; approximately 989 kHz. This is a nominal model of the tested V1.0 assembly.',
  },
  thesisMagnetics: {
    title: 'Thesis Chapter 6: Electrical Reference Values',
    detail: '02_Inherited_Specifications.tex: standalone transformer A leakage 16.42 µH, Lm 150.78 µH, primary/secondary turns ratio 8.039; B leakage 16.50 µH, Lm 139.89 µH, turns ratio 8.000. Installed A/B identity and post-assembly inductance were not recorded. Lm is a separate branch.',
  },
  thesisHardware: {
    title: 'Thesis Appendix B: Identity of the Tested Assembly',
    detail: 'The tested V1.0 assembly used two Würth 7443640470B 4.7 µH inductors in series. Later drawing values do not identify the fitted final hardware. Individual resonant-bank capacitor population values are not recorded by the 1 nF lumped model.',
  },
  schematic12: {
    title: 'Latest supplied F410 schematic (12), sheet 3: LLC+PFC',
    detail: 'Visually checked series path: VSW → C26 → L4 (SER1512-103MED, pins 1–2; pin 3 NC) → T1 primary. C26 has no value; T1 leakage and pump L3 are unspecified. C24 is the separate 2 nF pump capacitor. C7 = 1 nF bridges PGND and GND; it is not C26.',
  },
  coilcraftL4: {
    title: 'Coilcraft SER1512 datasheet',
    detail: 'SER1512-103ME_: nominal 10 µH ±20%, measured at 100 kHz, 0.1 Vrms and zero DC bias. This identifies the drawing part, not its installed 1 MHz inductance or loss.',
    url: 'https://www.coilcraft.com/getmedia/96260b65-ad47-4056-b696-1ca56c2663fc/ser1512.pdf',
  },
  schematicV11: {
    title: 'Schematic V1.1, sheet 3: LLC+PFC',
    detail: 'Visually checked C26 in series with L4 (74439346082) and T1. C26 is unvalued. C24 = 2 nF is in the separate pump path; L3 is unspecified. This drawing was not a separately tested V1.1 assembly.',
  },
  wurthL4: {
    title: 'Würth 74439346082 datasheet',
    detail: 'Nominal 8.2 µH ±20% at 100 kHz / 10 mA. Nominal inductance alone does not establish current, thermal, voltage or resonant-circuit suitability.',
    url: 'https://www.we-online.com/components/products/datasheet/74439346082.pdf',
  },
  pumpThesis: {
    title: 'Thesis Chapter 4: Pump-Inductor Selection',
    detail: '05_Pump_Inductor.tex: triangular, clamped-cycle estimate Lp = 1/(16 Cp fs²). Cp = 2 nF and fs = 1 MHz give 31.25 µH, with natural fp = 636.62 kHz. Supplied planar inductors measured 34.26 and 33.09 µH; the installed A/B identity is unknown.',
  },
  tiModel: {
    title: 'TI: Series resonant frequency and separate magnetizing branch',
    detail: 'Supports fr = 1/(2π√(Lr Cr)); a complete resonant converter also includes the magnetizing branch and load.',
    url: 'https://www.ti.com/document-viewer/lit/html/SSZTC48/GUID-448E1208-D9B0-4FF1-B7E8-481DA3288A83',
  },
  rlcModel: {
    title: 'Analog Devices: Resonance in RLC circuits',
    detail: 'Ideal series-RLC response with an explicitly entered series resistance. The response is not the measured transfer function of this converter.',
    url: 'https://wiki.analog.com/university/courses/electronics/rlc_resonance',
  },
  preferredValues: {
    title: 'Vishay: Preferred E-series values',
    detail: 'E12/E24 nominal series. Candidate values do not imply available components, tolerances or ratings.',
    url: 'https://www.vishay.com/docs/28372/e-series.pdf',
  },
};

// Supplied standalone measurements for explicit comparisons, not fitted-part identification.
export const TRANSFORMER_REFERENCES = Object.freeze([
  Object.freeze({ id: 'supplied-a', label: 'Transformer A', leakageInductanceUh: 16.42, magnetizingInductanceUh: 150.78, turnsRatio: 8.039, sourceId: 'thesisMagnetics' }),
  Object.freeze({ id: 'supplied-b', label: 'Transformer B', leakageInductanceUh: 16.50, magnetizingInductanceUh: 139.89, turnsRatio: 8.000, sourceId: 'thesisMagnetics' }),
]);

const toleranceNote = 'The default ±10% total-L and ±5% C ranges are editable starting assumptions, not measured uncertainty or guaranteed fitted-component tolerances. Edited ranges are user inputs.';
const baseline = {
  capacitorConnection: 'parallel', targetFrequencyKhz: 1000, operatingFrequencyKhz: 1000,
  seriesResistanceOhm: null, inductorTolerancePercent: 10, capacitorTolerancePercent: 5,
};
export const PRESETS = [
  {
    ...baseline, id: 'thesis-tested-nominal', label: 'Tested V1.0 · thesis nominal tank',
    description: 'Two external 4.7 µH inductors in series, nominal transformer leakage, and the thesis 1 nF lumped resonant capacitor.',
    sourceNote: 'Nominal analysis of the tested, modified V1.0 hardware. The 1 nF entry is an equivalent tank capacitance, not a documented individual capacitor population. Carrier = 1 MHz; nominal resonance ≈ 988.941 kHz.',
    sourceIds: ['thesisTank','thesisMagnetics','thesisHardware','tiModel','rlcModel','preferredValues'],
    discreteInductanceUh: 9.4, leakageInductanceUh: 16.5, capacitorsNf: [1],
    capacitorBasis: 'documented-equivalent',
    warnings: ['Transformer leakage is a supplied nominal standalone value; no installed extraction is available. Magnetizing inductance is excluded from series L.',toleranceNote],
  },
  {
    ...baseline, id: 'thesis-transformer-a', label: 'Thesis tank · supplied transformer A scenario',
    description: 'Same external 9.4 µH and 1 nF equivalent, with the supplied transformer A leakage measurement of 16.42 µH.',
    sourceNote: 'A comparison scenario using supplied transformer A data. It does not identify transformer A as the installed part.',
    sourceIds: ['thesisTank','thesisMagnetics','thesisHardware','tiModel'],
    discreteInductanceUh: 9.4, leakageInductanceUh: 16.42, capacitorsNf: [1],
    transformerReferenceId: 'supplied-a',
    capacitorBasis: 'documented-equivalent',
    warnings: ['The installed transformer A/B assignment is unknown; this is an explicit comparison scenario.',toleranceNote],
  },
  {
    ...baseline, id: 'f410-drawing-values', label: 'Latest F410 drawing (12) · enter missing C26',
    description: 'Drawing L4 = SER1512-103MED (nominal 10 µH). C26 and transformer leakage are not specified.',
    sourceNote: 'Sheet 3 contains a single C26 in the series tank, but gives no value. Enter its measured/fitted capacitance before solving frequency. C7 = 1 nF is between PGND and GND and must not be substituted for C26.',
    sourceIds: ['schematic12','coilcraftL4','tiModel'],
    discreteInductanceUh: 10, leakageInductanceUh: null, capacitorsNf: [],
    capacitorBasis: 'unprovided', inductorTolerancePercent: 20,
    warnings: ['C26 is unvalued in this drawing; the calculator deliberately leaves it blank.', 'Transformer leakage is not provided. A blank field uses zero only as an explicit calculation assumption; add the actual primary-referred value.', 'The 20% L setting is the discrete L4 nominal tolerance only; it is not a characterized tolerance of L4 plus transformer leakage. C tolerance remains a user assumption.'],
  },
  {
    ...baseline, id: 'f410-thesis-scenario', label: 'F410 L4 + inherited thesis assumptions · what-if',
    description: 'Nominal drawing L4 = 10 µH, with 16.5 µH leakage and 1 nF equivalent C borrowed explicitly from the older thesis model.',
    sourceNote: 'Design scenario only. Neither C26 = 1 nF nor transformer leakage = 16.5 µH is specified by schematic (12). These assumed values allow comparison, not confirmation of the new assembly.',
    sourceIds: ['schematic12','coilcraftL4','thesisTank','thesisMagnetics','tiModel'],
    discreteInductanceUh: 10, leakageInductanceUh: 16.5, capacitorsNf: [1],
    capacitorBasis: 'assumed-equivalent',
    warnings: ['Unmeasured scenario: the capacitance and leakage are borrowed from the thesis; verify the fitted F410 board.',toleranceNote],
  },
  {
    ...baseline, id: 'v11-drawing-values', label: 'V1.1 drawing · enter missing C26',
    description: 'Drawing L4 = 74439346082 (nominal 8.2 µH). Resonant C26 and transformer leakage are not specified.',
    sourceNote: 'Drawing-only preset, not the tested final V1.0 assembly. Enter the actual equivalent resonant capacitance and primary-referred leakage.',
    sourceIds: ['schematicV11','wurthL4','tiModel'],
    discreteInductanceUh: 8.2, leakageInductanceUh: null, capacitorsNf: [],
    capacitorBasis: 'unprovided', inductorTolerancePercent: 20,
    warnings: ['C26 is not valued in V1.1; no capacitor value is inferred from the separate 2 nF pump capacitor.', 'Discrete L4 is nominal 8.2 µH ±20%; installed total-L tolerance is uncharacterized. C tolerance is a user assumption.'],
  },
];
