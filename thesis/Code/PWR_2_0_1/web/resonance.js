// SI-only, pure helpers for the ideal series LC / series-loss RLC model.
// Transformer magnetizing inductance is a separate branch, not part of Lr.
export const CALCULATION_REFERENCES = Object.freeze([
  Object.freeze({ title: 'Texas Instruments: LLC resonant-frequency model', url: 'https://www.ti.com/document-viewer/lit/html/SSZTC48/GUID-448E1208-D9B0-4FF1-B7E8-481DA3288A83' }),
  Object.freeze({ title: 'Analog Devices: Resonance in RLC circuits', url: 'https://wiki.analog.com/university/courses/electronics/rlc_resonance' }),
  Object.freeze({ title: 'Vishay: Preferred E-series values', url: 'https://www.vishay.com/docs/28372/e-series.pdf' }),
]);

const TAU = 2 * Math.PI;
const UNIT_SCALE = Object.freeze({
  Hz: 1, kHz: 1e3, MHz: 1e6,
  H: 1, mH: 1e-3, uH: 1e-6, '\u00b5H': 1e-6, '\u03bcH': 1e-6, nH: 1e-9,
  F: 1, mF: 1e-3, uF: 1e-6, '\u00b5F': 1e-6, '\u03bcF': 1e-6, nF: 1e-9, pF: 1e-12,
  ohm: 1, Ohm: 1, '\u03a9': 1, kohm: 1e3, 'k\u03a9': 1e3,
});
const PREFERRED = Object.freeze({
  E12: Object.freeze([1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]),
  E24: Object.freeze([1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]),
});

function finite(value, label) {
  if (typeof value !== 'number' || !Number.isFinite(value)) throw new RangeError(`${label} must be a finite number.`);
  return value;
}
function positive(value, label) {
  finite(value, label);
  if (value <= 0) throw new RangeError(`${label} must be greater than zero.`);
  return value;
}
function nonnegative(value, label) {
  finite(value, label);
  if (value < 0) throw new RangeError(`${label} cannot be negative.`);
  return value;
}
function fraction(value, label) {
  nonnegative(value, label);
  if (value >= 1) throw new RangeError(`${label} must be a fraction from 0 up to, but excluding, 1.`);
  return value;
}
function computed(value, label) {
  if (!Number.isFinite(value) || value <= 0) throw new RangeError(`${label} is outside the supported numeric range. Check the values and units.`);
  return value;
}
function scaleFor(unit) {
  if (!Object.hasOwn(UNIT_SCALE, unit)) throw new RangeError(`Unknown unit: ${unit}.`);
  return UNIT_SCALE[unit];
}

/** Convert a finite numeric value to SI. Units are explicit and case sensitive. */
export function toSI(value, unit) {
  finite(value, 'Value');
  const converted = value * scaleFor(unit);
  if (!Number.isFinite(converted) || (converted === 0 && value !== 0)) throw new RangeError('Unit conversion is outside the supported numeric range.');
  return converted;
}

export function fromSI(value, unit) {
  finite(value, 'Value');
  const converted = value / scaleFor(unit);
  if (!Number.isFinite(converted) || (converted === 0 && value !== 0)) throw new RangeError('Unit conversion is outside the supported numeric range.');
  return converted;
}

function componentValues(values, label) {
  if (!Array.isArray(values) || values.length === 0 || values.length > 1000) throw new RangeError(`${label} requires between 1 and 1000 component values.`);
  values.forEach((value, index) => positive(value, `${label} ${index + 1}`));
  return values;
}

/** Positive capacitor values in farads. Empty/zero placeholders are rejected. */
export function equivalentCapacitance(values, connection = 'parallel') {
  componentValues(values, 'Capacitance');
  if (connection === 'parallel') return computed(values.reduce((sum, value) => sum + value, 0), 'Equivalent capacitance');
  if (connection === 'series') {
    const smallest = Math.min(...values);
    return computed(smallest / values.reduce((sum, value) => sum + smallest / value, 0), 'Equivalent capacitance');
  }
  throw new RangeError('Capacitor connection must be series or parallel.');
}

/** Uncoupled discrete series inductors only; do not add transformer Lm here. */
export function equivalentSeriesInductance(values) {
  componentValues(values, 'Inductance');
  return computed(values.reduce((sum, value) => sum + value, 0), 'Series inductance');
}

export function resonanceFrequency(inductanceH, capacitanceF) {
  positive(inductanceH, 'Total series inductance');
  positive(capacitanceF, 'Equivalent resonant capacitance');
  // The logarithmic form avoids overflowing/underflowing the intermediate LC product.
  return computed(Math.exp(-Math.log(TAU) - 0.5 * (Math.log(inductanceH) + Math.log(capacitanceF))), 'Resonant frequency');
}

/**
 * Solve one unknown. All component values and frequencies are SI numbers.
 * leakageInductanceH must already be referred to the resonant/primary side.
 * inductorTolerance applies to the TOTAL Lr; tolerances are fractions, not percent.
 * R is optional equivalent SERIES resistance, not DC load resistance.
 */
export function analyzeTank({
  solveFor = 'frequency', targetFrequencyHz,
  discreteInductanceH = 0, leakageInductanceH = 0, capacitanceF,
  operatingFrequencyHz, seriesResistanceOhm,
  inductorTolerance = 0, capacitorTolerance = 0,
} = {}) {
  if (!['frequency', 'inductance', 'capacitance'].includes(solveFor)) throw new RangeError('Choose frequency, inductance, or capacitance to solve.');
  nonnegative(leakageInductanceH, 'Primary-referred leakage inductance');
  fraction(inductorTolerance, 'Total inductance tolerance');
  fraction(capacitorTolerance, 'Capacitance tolerance');
  let totalInductanceH;
  if (solveFor === 'inductance') {
    positive(targetFrequencyHz, 'Target resonant frequency');
    positive(capacitanceF, 'Equivalent resonant capacitance');
    totalInductanceH = computed(Math.exp(-2 * Math.log(TAU * targetFrequencyHz) - Math.log(capacitanceF)), 'Required total inductance');
    discreteInductanceH = totalInductanceH - leakageInductanceH;
    // Log/exp roundtrips can differ by a few ulps at the leakage-only boundary.
    if (discreteInductanceH < -64 * Number.EPSILON * Math.max(totalInductanceH, leakageInductanceH)) throw new RangeError('The leakage inductance exceeds the required total inductance. A nonnegative discrete inductor cannot meet this target.');
    if (discreteInductanceH < 0) discreteInductanceH = 0;
  } else {
    nonnegative(discreteInductanceH, 'Discrete series inductance');
    totalInductanceH = computed(discreteInductanceH + leakageInductanceH, 'Total series inductance');
    if (solveFor === 'capacitance') {
      positive(targetFrequencyHz, 'Target resonant frequency');
      capacitanceF = computed(Math.exp(-2 * Math.log(TAU * targetFrequencyHz) - Math.log(totalInductanceH)), 'Required capacitance');
    } else positive(capacitanceF, 'Equivalent resonant capacitance');
  }

  const resonantFrequencyHz = resonanceFrequency(totalInductanceH, capacitanceF);
  operatingFrequencyHz = operatingFrequencyHz ?? resonantFrequencyHz;
  positive(operatingFrequencyHz, 'Operating frequency');
  const characteristicImpedanceOhm = computed(Math.exp(0.5 * (Math.log(totalInductanceH) - Math.log(capacitanceF))), 'Characteristic impedance');
  const frequencyRatio = computed(operatingFrequencyHz / resonantFrequencyHz, 'Normalized frequency');
  const inductiveReactanceOhm = computed(TAU * operatingFrequencyHz * totalInductanceH, 'Inductive reactance');
  const capacitiveReactanceOhm = computed(1 / (TAU * operatingFrequencyHz * capacitanceF), 'Capacitive reactance');
  const netReactanceOhm = finite(inductiveReactanceOhm - capacitiveReactanceOhm, 'Net reactance');
  const region = Math.abs(frequencyRatio - 1) <= 1e-10 ? 'resonant' : frequencyRatio > 1 ? 'inductive' : 'capacitive';
  let q = null;
  let bandwidthHz = null;
  if (seriesResistanceOhm != null) {
    nonnegative(seriesResistanceOhm, 'Equivalent series resistance');
    if (seriesResistanceOhm > 0) {
      q = computed(characteristicImpedanceOhm / seriesResistanceOhm, 'Series-loss quality factor');
      bandwidthHz = computed(seriesResistanceOhm / (TAU * totalInductanceH), 'Series-loss bandwidth');
    }
  }
  const tolerance = {
    frequencyMinHz: resonanceFrequency(computed(totalInductanceH * (1 + inductorTolerance), 'Maximum total inductance'), computed(capacitanceF * (1 + capacitorTolerance), 'Maximum capacitance')),
    frequencyMaxHz: resonanceFrequency(computed(totalInductanceH * (1 - inductorTolerance), 'Minimum total inductance'), computed(capacitanceF * (1 - capacitorTolerance), 'Minimum capacitance')),
  };
  const warnings = [
    'Ideal series LC estimate: converter gain, ZVS, power, efficiency, parasitics, and component ratings require a separate model and measurement.',
  ];
  if (leakageInductanceH > 0) warnings.push('Leakage is included once, referred to the resonant side. Do not add it again if the measured Lr already includes it.');
  if (seriesResistanceOhm === 0) warnings.push('Zero series resistance gives an ideal undamped model; finite Q, bandwidth, and normalized current response are undefined.');
  return {
    solveFor, resonantFrequencyHz, totalInductanceH, discreteInductanceH, leakageInductanceH, capacitanceF,
    operatingFrequencyHz, characteristicImpedanceOhm, inductiveReactanceOhm, capacitiveReactanceOhm,
    netReactanceOhm, frequencyRatio, region, q, bandwidthHz, tolerance, warnings,
  };
}

/**
 * Nearest single equivalent-component values, not a proposed PCB bank layout.
 * E-series membership does not establish tolerance, voltage/current ratings, or stock.
 */
export function preferredCandidates(targetSI, series = 'E24', count = 5) {
  positive(targetSI, 'Target component value');
  if (!Object.hasOwn(PREFERRED, series)) throw new RangeError('Preferred series must be E12 or E24.');
  if (!Number.isInteger(count) || count < 1 || count > 12) throw new RangeError('Candidate count must be an integer from 1 to 12.');
  const decade = Math.floor(Math.log10(targetSI));
  const candidates = [];
  for (let exponent = decade - 1; exponent <= decade + 1; exponent++) {
    for (const base of PREFERRED[series]) {
      const valueSI = base * 10 ** exponent;
      if (valueSI > 0 && Number.isFinite(valueSI)) candidates.push({ valueSI, deviationPercent: 100 * (valueSI / targetSI - 1) });
    }
  }
  return candidates.sort((a, b) => Math.abs(a.deviationPercent) - Math.abs(b.deviationPercent) || a.valueSI - b.valueSI).slice(0, count);
}

/**
 * Normalized sinusoidal SERIES RLC current |I(f)| / |I(fr)| = R / |Z(f)|.
 * This is not a converter output-voltage gain. Strictly positive loss is required.
 * points controls log-grid size; exact fr is added when within the range.
 */
export function generateFrequencyResponse({
  totalInductanceH, capacitanceF, seriesResistanceOhm,
  minRatio = 0.25, maxRatio = 4, points = 181,
} = {}) {
  const resonantFrequencyHz = resonanceFrequency(totalInductanceH, capacitanceF);
  positive(seriesResistanceOhm, 'Equivalent series resistance for current response');
  positive(minRatio, 'Minimum frequency ratio');
  positive(maxRatio, 'Maximum frequency ratio');
  if (maxRatio <= minRatio) throw new RangeError('Maximum frequency ratio must exceed minimum frequency ratio.');
  if (!Number.isInteger(points) || points < 2 || points > 2001) throw new RangeError('Response point count must be an integer from 2 to 2001.');
  const q = computed(Math.exp(0.5 * (Math.log(totalInductanceH) - Math.log(capacitanceF))) / seriesResistanceOhm, 'Series-loss quality factor');
  const ratios = Array.from({ length: points }, (_, index) => Math.exp(Math.log(minRatio) + index / (points - 1) * (Math.log(maxRatio) - Math.log(minRatio))));
  if (minRatio <= 1 && maxRatio >= 1 && !ratios.some(value => Math.abs(value - 1) < 1e-12)) ratios.push(1);
  return ratios.sort((a, b) => a - b).map(frequencyRatio => ({
    frequencyHz: computed(resonantFrequencyHz * frequencyRatio, 'Response frequency'),
    frequencyRatio,
    normalizedCurrent: 1 / Math.hypot(1, q * (frequencyRatio - 1 / frequencyRatio)),
  }));
}
