import test from 'node:test';
import assert from 'node:assert/strict';
import { PRESETS, SOURCES, TRANSFORMER_REFERENCES } from '../resonance-presets.js';
import { analyzeTank, equivalentCapacitance } from '../resonance.js';

test('tested thesis preset reproduces the nominal 25.9 uH / 1 nF tank', () => {
  const p = PRESETS.find(p => p.id === 'thesis-tested-nominal');
  const r = analyzeTank({ solveFor:'frequency', discreteInductanceH:p.discreteInductanceUh*1e-6, leakageInductanceH:p.leakageInductanceUh*1e-6, capacitanceF:equivalentCapacitance(p.capacitorsNf.map(c=>c*1e-9),p.capacitorConnection) });
  assert.ok(Math.abs(r.totalInductanceH-25.9e-6)<1e-16);
  assert.ok(Math.abs(r.resonantFrequencyHz-988940.697)<0.001);
  assert.equal(p.capacitorBasis,'documented-equivalent');
});

test('unvalued C26 and leakage remain unknown in drawing-only presets', () => {
  for(const id of ['f410-drawing-values','v11-drawing-values']) {
    const p = PRESETS.find(p=>p.id===id);
    assert.deepEqual(p.capacitorsNf,[]);
    assert.equal(p.leakageInductanceUh,null);
    assert.equal(p.capacitorBasis,'unprovided');
    assert.throws(()=>equivalentCapacitance(p.capacitorsNf,'parallel'));
  }
});

test('borrowed F410 circuit values are explicitly an assumed equivalent', () => {
  const p=PRESETS.find(p=>p.id==='f410-thesis-scenario');
  assert.equal(p.capacitorBasis,'assumed-equivalent');
  assert.match(p.sourceNote,/Neither C26 = 1 nF nor transformer leakage = 16.5/);
  assert.match(SOURCES.schematic12.detail,/C7 = 1 nF.*not C26/);
});

test('every preset has unique identity and valid source references', () => {
  assert.equal(new Set(PRESETS.map(p=>p.id)).size,PRESETS.length);
  for(const p of PRESETS) for(const id of p.sourceIds) assert.ok(SOURCES[id]?.detail,`${p.id}: ${id}`);
  for(const s of Object.values(SOURCES)) if(s.url) assert.equal(new URL(s.url).protocol,'https:');
});


test('transformer references retain measured pairs and source provenance without assigning fitted identity', () => {
  assert.deepEqual(TRANSFORMER_REFERENCES.map(r => [r.id, r.leakageInductanceUh, r.magnetizingInductanceUh, r.turnsRatio]), [
    ['supplied-a', 16.42, 150.78, 8.039],
    ['supplied-b', 16.50, 139.89, 8.000],
  ]);
  for (const reference of TRANSFORMER_REFERENCES) {
    assert.equal(reference.sourceId, 'thesisMagnetics');
    assert.match(SOURCES[reference.sourceId].detail, /Installed A\/B identity.*not recorded/);
    assert.match(SOURCES[reference.sourceId].detail, /8\.039.*8\.000/);
  }
  assert.equal(PRESETS.find(p => p.id === 'thesis-transformer-a').transformerReferenceId, 'supplied-a');
  assert.match(PRESETS.find(p => p.id === 'thesis-transformer-a').sourceNote, /does not identify.*installed/);
  assert.equal(PRESETS.find(p => p.id === 'thesis-tested-nominal').transformerReferenceId, undefined);
  for (const preset of PRESETS) {
    if (preset.transformerReferenceId) assert.ok(TRANSFORMER_REFERENCES.some(r => r.id === preset.transformerReferenceId));
    assert.equal(preset.magnetizingInductanceUh, undefined);
  }
});
