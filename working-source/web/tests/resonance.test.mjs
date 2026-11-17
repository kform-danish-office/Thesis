import test from 'node:test';
import assert from 'node:assert/strict';
import { analyzeTank, analyzePump, analyzeMagnetizingBranch, equivalentCapacitance, equivalentSeriesInductance, resonanceFrequency, toSI, fromSI, preferredCandidates, generateFrequencyResponse } from '../resonance.js';

function close(actual, expected, relative = 1e-12) {
  assert.ok(Math.abs(actual - expected) <= relative * Math.max(Math.abs(expected), Number.MIN_VALUE), `${actual} != ${expected}`);
}
const base = { discreteInductanceH: 9.4e-6, leakageInductanceH: 0, capacitanceF: 2.7e-9 };

test('thesis pump sizing solves the documented 2 nF / 1 MHz example independently of tank resonance', () => {
  const pump = analyzePump({ solveFor: 'inductance', capacitanceF: 2e-9, switchingFrequencyHz: 1e6 });
  close(pump.inductanceH, 31.25e-6);
  close(pump.pumpResonantFrequencyHz, 2e6 / Math.PI);
  close(pump.frequencyRatio, Math.PI / 2);
  assert.ok(pump.switchingFrequencyHz > pump.pumpResonantFrequencyHz);
  const seriesLC = analyzeTank({ solveFor: 'inductance', capacitanceF: 2e-9, targetFrequencyHz: 1e6 });
  assert.ok(Math.abs(pump.inductanceH - seriesLC.totalInductanceH) > 10e-6);
});

test('all three triangular/clamped pump solves roundtrip', () => {
  const pumpL = analyzePump({ solveFor: 'inductance', capacitanceF: 2e-9, switchingFrequencyHz: 1e6 });
  const pumpC = analyzePump({ solveFor: 'capacitance', inductanceH: pumpL.inductanceH, switchingFrequencyHz: 1e6 });
  const pumpF = analyzePump({ solveFor: 'frequency', inductanceH: pumpL.inductanceH, capacitanceF: pumpC.capacitanceF });
  close(pumpC.capacitanceF, 2e-9);
  close(pumpF.switchingFrequencyHz, 1e6);
  close(pumpF.pumpResonantFrequencyHz, pumpL.pumpResonantFrequencyHz);
  const alternate = analyzePump({ solveFor: 'capacitance', inductanceH: 33.09e-6, switchingFrequencyHz: 900e3 });
  close(alternate.capacitanceF, 1 / (16 * 33.09e-6 * (900e3) ** 2));
});

test('pump model rejects invalid inputs and out-of-range results', () => {
  const args = { solveFor: 'inductance', capacitanceF: 2e-9, switchingFrequencyHz: 1e6 };
  for (const changes of [{ capacitanceF: 0 }, { capacitanceF: -1 }, { capacitanceF: NaN }, { capacitanceF: '2e-9' }, { switchingFrequencyHz: 0 }, { switchingFrequencyHz: Infinity }, { solveFor: 'power' }, { switchingFrequencyHz: 1e308 }]) assert.throws(() => analyzePump({ ...args, ...changes }));
  assert.throws(() => analyzePump({ solveFor: 'capacitance', inductanceH: 0, switchingFrequencyHz: 1e6 }));
  assert.throws(() => analyzePump({ solveFor: 'frequency', inductanceH: Number.MIN_VALUE, capacitanceF: Number.MIN_VALUE }));
});

test('documented nominal Lr includes 9.4 uH discrete plus 16.5 uH leakage', () => {
  const result = analyzeTank({ discreteInductanceH: 9.4e-6, leakageInductanceH: 16.5e-6, capacitanceF: 1e-9, inductorTolerance: 0.1 });
  close(result.totalInductanceH, 25.9e-6);
  close(result.resonantFrequencyHz, 1 / (2 * Math.PI * Math.sqrt(25.9e-6 * 1e-9)));
  assert.ok(result.resonantFrequencyHz > 988e3 && result.resonantFrequencyHz < 990e3);
  close(result.tolerance.frequencyMinHz, result.resonantFrequencyHz / Math.sqrt(1.1));
});

test('explicit units preserve SI dimensions and reject missing, unknown, or nonfinite values', () => {
  close(toSI(9.4, 'uH'), 9.4e-6);
  close(toSI(9.4, '\u00b5H'), 9.4e-6);
  close(toSI(9.4, '\u03bcH'), 9.4e-6);
  close(toSI(1000, 'kHz'), 1e6);
  close(fromSI(toSI(2.7, 'nF'), 'pF'), 2700);
  close(fromSI(toSI(1.2, 'mH'), 'uH'), 1200);
  assert.equal(toSI(0, 'ohm'), 0);
  for (const value of [NaN, Infinity, -Infinity, '', null, '9.4']) assert.throws(() => toSI(value, 'uH'));
  assert.throws(() => toSI(1, 'mh'));
  assert.throws(() => toSI(1, '__proto__'));
  assert.throws(() => toSI(1e308, 'MHz'));
  assert.throws(() => toSI(Number.MIN_VALUE, 'pF'));
});

test('capacitor banks use their actual series or parallel topology', () => {
  close(equivalentCapacitance([1e-9, 2e-9, 3e-9], 'parallel'), 6e-9);
  close(equivalentCapacitance([1e-9, 2e-9, 3e-9], 'series'), 6e-9 / 11);
  close(equivalentCapacitance([4.7e-9, 4.7e-9], 'series'), 2.35e-9);
  close(equivalentCapacitance([2.7e-9]), 2.7e-9);
  close(equivalentSeriesInductance([4.7e-6, 4.7e-6]), 9.4e-6);
  for (const values of [[], [0], [-1], [NaN], [Infinity], ['2.7'], null]) assert.throws(() => equivalentCapacitance(values));
  assert.throws(() => equivalentCapacitance([1e-9], 'unknown'));
  assert.throws(() => equivalentCapacitance([1e308, 1e308], 'parallel'));
});

test('frequency, capacitance, and inductance solves roundtrip independently', () => {
  const targetFrequencyHz = 1e6;
  const resultC = analyzeTank({ ...base, solveFor: 'capacitance', targetFrequencyHz });
  close(resultC.capacitanceF, 1 / ((2 * Math.PI * targetFrequencyHz) ** 2 * base.discreteInductanceH));
  close(resultC.capacitanceF, 2.694712330913e-9, 1e-12);
  close(resultC.resonantFrequencyHz, targetFrequencyHz);
  const resultL = analyzeTank({ solveFor: 'inductance', targetFrequencyHz, capacitanceF: resultC.capacitanceF });
  close(resultL.totalInductanceH, base.discreteInductanceH);
  close(resultL.discreteInductanceH, base.discreteInductanceH);
  const resultF = analyzeTank(base);
  close(resultF.resonantFrequencyHz, 1 / (2 * Math.PI * Math.sqrt(base.discreteInductanceH * base.capacitanceF)));
});

test('leakage belongs in total series inductance and is subtracted from the discrete solution', () => {
  const result = analyzeTank({ ...base, leakageInductanceH: 0.8e-6 });
  close(result.totalInductanceH, 10.2e-6);
  const solved = analyzeTank({ solveFor: 'inductance', targetFrequencyHz: result.resonantFrequencyHz, capacitanceF: base.capacitanceF, leakageInductanceH: 0.8e-6 });
  close(solved.discreteInductanceH, base.discreteInductanceH);
  assert.ok(solved.warnings.some(warning => warning.includes('included once')));
  assert.throws(() => analyzeTank({ solveFor: 'inductance', targetFrequencyHz: 1e6, capacitanceF: 2.7e-9, leakageInductanceH: 20e-6 }), /exceeds/);
});

test('a leakage-only series path is valid while adding an Lm property cannot change Lr', () => {
  const noDiscrete = analyzeTank({ discreteInductanceH: 0, leakageInductanceH: 9.4e-6, capacitanceF: 2.7e-9 });
  close(noDiscrete.resonantFrequencyHz, analyzeTank(base).resonantFrequencyHz);
  const recovered = analyzeTank({ solveFor: 'inductance', leakageInductanceH: 9.4e-6, capacitanceF: 2.7e-9, targetFrequencyHz: noDiscrete.resonantFrequencyHz });
  assert.ok(recovered.discreteInductanceH >= 0 && recovered.discreteInductanceH < 1e-18);
  const extraLm = analyzeTank({ ...base, magnetizingInductanceH: 1e-3 });
  close(extraLm.totalInductanceH, base.discreteInductanceH);
});

test('worst-case tolerance endpoints are exact and encompass every corner', () => {
  const result = analyzeTank({ ...base, inductorTolerance: 0.1, capacitorTolerance: 0.05 });
  close(result.tolerance.frequencyMinHz, result.resonantFrequencyHz / Math.sqrt(1.1 * 1.05));
  close(result.tolerance.frequencyMaxHz, result.resonantFrequencyHz / Math.sqrt(0.9 * 0.95));
  for (const factorL of [0.9, 1.1]) for (const factorC of [0.95, 1.05]) {
    const corner = resonanceFrequency(base.discreteInductanceH * factorL, base.capacitanceF * factorC);
    assert.ok(corner >= result.tolerance.frequencyMinHz * (1 - 1e-12));
    assert.ok(corner <= result.tolerance.frequencyMaxHz * (1 + 1e-12));
  }
  assert.throws(() => analyzeTank({ ...base, inductorTolerance: 1 }));
  assert.throws(() => analyzeTank({ ...base, capacitorTolerance: 5 }));
  assert.throws(() => analyzeTank({ ...base, capacitorTolerance: -0.05 }));
});

test('operating-frequency reactance changes sign around resonance', () => {
  const nominal = analyzeTank(base);
  assert.equal(nominal.region, 'resonant');
  close(nominal.frequencyRatio, 1);
  close(nominal.inductiveReactanceOhm, nominal.capacitiveReactanceOhm);
  for (const ratio of [0.5, 2]) {
    const result = analyzeTank({ ...base, operatingFrequencyHz: nominal.resonantFrequencyHz * ratio });
    close(result.frequencyRatio, ratio);
    close(result.inductiveReactanceOhm, nominal.characteristicImpedanceOhm * ratio);
    close(result.capacitiveReactanceOhm, nominal.characteristicImpedanceOhm / ratio);
    assert.equal(result.region, ratio < 1 ? 'capacitive' : 'inductive');
    assert.equal(Math.sign(result.netReactanceOhm), ratio < 1 ? -1 : 1);
  }
});

test('series-loss Q and half-power bandwidth are consistent', () => {
  const result = analyzeTank({ ...base, seriesResistanceOhm: 2 });
  close(result.q, Math.sqrt(base.discreteInductanceH / base.capacitanceF) / 2);
  close(result.bandwidthHz, 2 / (2 * Math.PI * base.discreteInductanceH));
  close(result.resonantFrequencyHz / result.q, result.bandwidthHz);
  const noR = analyzeTank(base);
  assert.equal(noR.q, null);
  assert.equal(noR.bandwidthHz, null);
  assert.equal(analyzeTank({ ...base, seriesResistanceOhm: 0 }).q, null);
  assert.throws(() => analyzeTank({ ...base, seriesResistanceOhm: -1 }));
});

test('current response peaks at one at fr and is reciprocal symmetric in frequency ratio', () => {
  const args = { totalInductanceH: 9.4e-6, capacitanceF: 2.7e-9, seriesResistanceOhm: 2, points: 101 };
  const response = generateFrequencyResponse(args);
  const peak = response.find(point => Math.abs(point.frequencyRatio - 1) < 1e-12);
  assert.ok(peak);
  close(peak.normalizedCurrent, 1);
  assert.ok(response.every(point => point.normalizedCurrent >= 0 && point.normalizedCurrent <= 1));
  for (let index = 1; index < response.length; index++) assert.ok(response[index].frequencyHz > response[index - 1].frequencyHz);
  close(response[0].normalizedCurrent, response.at(-1).normalizedCurrent);
  close(response[0].frequencyRatio, 0.25);
  close(response.at(-1).frequencyRatio, 4);
});

test('analytical half-power endpoints reproduce exact R/(2 pi L) bandwidth', () => {
  const r = 12;
  const tank = analyzeTank({ ...base, seriesResistanceOhm: r });
  const d = 1 / tank.q;
  const low = (Math.sqrt(d * d + 4) - d) / 2;
  const high = (Math.sqrt(d * d + 4) + d) / 2;
  const response = generateFrequencyResponse({ totalInductanceH: tank.totalInductanceH, capacitanceF: tank.capacitanceF, seriesResistanceOhm: r, minRatio: low, maxRatio: high, points: 2 });
  close(response[0].normalizedCurrent, 1 / Math.sqrt(2));
  close(response.at(-1).normalizedCurrent, 1 / Math.sqrt(2));
  close(response.at(-1).frequencyHz - response[0].frequencyHz, tank.bandwidthHz);
});

test('lossless or malformed response requests cannot masquerade as finite current curves', () => {
  const args = { totalInductanceH: 9.4e-6, capacitanceF: 2.7e-9, seriesResistanceOhm: 2 };
  for (const changes of [{ seriesResistanceOhm: 0 }, { seriesResistanceOhm: -1 }, { minRatio: 0 }, { minRatio: 2, maxRatio: 1 }, { points: 1 }, { points: 2.5 }, { points: 3000 }]) assert.throws(() => generateFrequencyResponse({ ...args, ...changes }));
});

test('E12 and E24 use tabulated values, bracket decade transitions, and expose real error', () => {
  const exact = preferredCandidates(2.7e-9, 'E12');
  close(exact[0].valueSI, 2.7e-9);
  assert.ok(Math.abs(exact[0].deviationPercent) < 1e-12);
  const transition = preferredCandidates(9.8e-9, 'E24', 3);
  close(transition[0].valueSI, 10e-9);
  close(transition[0].deviationPercent, 100 * (10 / 9.8 - 1));
  assert.ok(transition.some(candidate => candidate.valueSI < 9.8e-9));
  assert.ok(preferredCandidates(4.3e-6, 'E24').some(candidate => Math.abs(candidate.valueSI - 4.3e-6) < 1e-18));
  assert.throws(() => preferredCandidates(0));
  assert.throws(() => preferredCandidates(1e-9, 'E96'));
  assert.throws(() => preferredCandidates(1e-9, 'E24', 100));
});

test('invalid component values and numeric overflow fail instead of displaying NaN or Infinity', () => {
  for (const changes of [{ discreteInductanceH: -1 }, { discreteInductanceH: 0 }, { leakageInductanceH: -1 }, { capacitanceF: 0 }, { capacitanceF: NaN }, { capacitanceF: Infinity }, { capacitanceF: '2.7e-9' }, { operatingFrequencyHz: 0 }, { solveFor: 'power' }, { operatingFrequencyHz: 1e308 }]) assert.throws(() => analyzeTank({ ...base, ...changes }));
  assert.throws(() => analyzeTank({ ...base, solveFor: 'inductance', targetFrequencyHz: 0 }));
  assert.throws(() => analyzeTank({ ...base, solveFor: 'capacitance', targetFrequencyHz: Infinity }));
  assert.throws(() => resonanceFrequency(Number.MIN_VALUE, Number.MIN_VALUE));
  assert.throws(() => analyzeTank({ ...base, discreteInductanceH: 1e308, leakageInductanceH: 1e308 }));
});


test('separate magnetizing branch reproduces supplied A and B comparison values', () => {
  for (const [leakage, lm, expectedFrequency, expectedReactance, expectedRatio] of [
    [16.42e-6, 150.78e-6, 378725.70440436486, 947.378680616538, 5.839659178931061],
    [16.50e-6, 139.89e-6, 390877.76453581935, 878.9547926213521, 5.401158301158301],
  ]) {
    const totalInductanceH = 9.4e-6 + leakage;
    const result = analyzeMagnetizingBranch({ totalInductanceH, capacitanceF: 1e-9, magnetizingInductanceH: lm, operatingFrequencyHz: 1e6 });
    close(result.magnetizingInductanceH, lm);
    close(result.openSecondaryFrequencyHz, expectedFrequency);
    close(result.magnetizingReactanceOhm, expectedReactance);
    close(result.inductanceRatio, expectedRatio);
    assert.ok(result.openSecondaryFrequencyHz < resonanceFrequency(totalInductanceH, 1e-9));
  }
});

test('magnetizing comparison scales physically without changing the series solve', () => {
  const args = { totalInductanceH: 25.9e-6, capacitanceF: 1e-9, magnetizingInductanceH: 139.89e-6, operatingFrequencyHz: 1e6 };
  const reference = analyzeMagnetizingBranch(args);
  const largerLm = analyzeMagnetizingBranch({ ...args, magnetizingInductanceH: args.magnetizingInductanceH * 2 });
  assert.ok(largerLm.openSecondaryFrequencyHz < reference.openSecondaryFrequencyHz);
  close(largerLm.inductanceRatio, reference.inductanceRatio * 2);
  close(largerLm.magnetizingReactanceOhm, reference.magnetizingReactanceOhm * 2);
  const faster = analyzeMagnetizingBranch({ ...args, operatingFrequencyHz: 2e6 });
  close(faster.openSecondaryFrequencyHz, reference.openSecondaryFrequencyHz);
  close(faster.magnetizingReactanceOhm, reference.magnetizingReactanceOhm * 2);
  const scaled = analyzeMagnetizingBranch({ ...args, totalInductanceH: args.totalInductanceH * 4, magnetizingInductanceH: args.magnetizingInductanceH * 4 });
  close(scaled.openSecondaryFrequencyHz, reference.openSecondaryFrequencyHz / 2);
  close(scaled.inductanceRatio, reference.inductanceRatio);
  const tank = analyzeTank({ discreteInductanceH: 9.4e-6, leakageInductanceH: 16.5e-6, capacitanceF: 1e-9, magnetizingInductanceH: args.magnetizingInductanceH });
  close(tank.totalInductanceH, 25.9e-6);
  close(tank.resonantFrequencyHz, 988940.6974694531);
});

test('missing operating frequency leaves magnetizing reactance unknown', () => {
  const args = { totalInductanceH: 25.9e-6, capacitanceF: 1e-9, magnetizingInductanceH: 139.89e-6 };
  for (const operatingFrequencyHz of [undefined, null]) {
    const result = analyzeMagnetizingBranch({ ...args, operatingFrequencyHz });
    assert.equal(result.magnetizingReactanceOhm, null);
    close(result.openSecondaryFrequencyHz, 390877.76453581935);
  }
});

test('magnetizing comparison rejects invalid quantities and unsupported numeric results', () => {
  const args = { totalInductanceH: 25.9e-6, capacitanceF: 1e-9, magnetizingInductanceH: 139.89e-6, operatingFrequencyHz: 1e6 };
  for (const key of ['totalInductanceH', 'capacitanceF', 'magnetizingInductanceH']) {
    for (const value of [0, -1, NaN, Infinity, '1e-6', null, undefined]) {
      assert.throws(() => analyzeMagnetizingBranch({ ...args, [key]: value }), /must/);
    }
  }
  for (const value of [0, -1, NaN, Infinity, '1000000']) assert.throws(() => analyzeMagnetizingBranch({ ...args, operatingFrequencyHz: value }));
  assert.throws(() => analyzeMagnetizingBranch({ ...args, totalInductanceH: 1e308, magnetizingInductanceH: 1e308 }), /numeric range/);
  assert.throws(() => analyzeMagnetizingBranch({ ...args, totalInductanceH: 1e308, magnetizingInductanceH: Number.MIN_VALUE }), /numeric range/);
  assert.throws(() => analyzeMagnetizingBranch({ ...args, magnetizingInductanceH: 1, operatingFrequencyHz: 1e308 }), /numeric range/);
  assert.throws(() => analyzeMagnetizingBranch({ ...args, totalInductanceH: Number.MIN_VALUE, magnetizingInductanceH: Number.MIN_VALUE, capacitanceF: Number.MIN_VALUE }), /numeric range/);
});
