import test from 'node:test';
import assert from 'node:assert/strict';
import {toCSV} from '../storage.js';

function parseCSV(text) {
  const rows = []; let row = [], field = '', quoted = false;
  text = text.replace(/^\uFEFF/, '');
  for (let i=0; i<text.length; i++) {
    const char = text[i];
    if (char === '"') { if (quoted && text[i+1] === '"') { field += '"'; i++; } else quoted = !quoted; }
    else if (!quoted && char === ',') { row.push(field); field = ''; }
    else if (!quoted && char === '\r' && text[i+1] === '\n') { row.push(field); rows.push(row); row = []; field = ''; i++; }
    else field += char;
  }
  row.push(field); rows.push(row);
  return rows;
}
const sample = {receivedAt:'2026-10-19T12:00:00.000Z', ms:500, enabled:false, mode:'VSBONLY', fault:'NONE', vpri:325, vsec:0, current:null, power:null, duty:0, adc:[1,2,3], settings:{VSET:28,VON:26,VMAX:32,OVP:36,DMAX:75,OD:10,FEN:10000}, lease_ms:5000};
const session = (changes={}) => ({id:'session-1',name:'Bench run',notes:'',source:'usb',firmware:{fw:'PWR-2.0.1'},samples:[sample],...changes});

test('CSV preserves quoted names, commas, newlines, missing diagnostics, units and column order', () => {
  const csv = toCSV(session({name:'Run, "A"',notes:'first\nsecond'}));
  assert.ok(csv.startsWith('\uFEFF')); const [columns,row] = parseCSV(csv);
  assert.equal(columns.length, 26); assert.equal(row.length, columns.length);
  const values = Object.fromEntries(columns.map((key,index) => [key,row[index]]));
  assert.equal(values.session_name, 'Run, "A"'); assert.equal(values.notes, 'first\nsecond');
  assert.equal(values.current_diagnostic_A, ''); assert.equal(values.power_diagnostic_W, '');
  assert.equal(values.vpri_V, '325'); assert.equal(values.FEN, '10000'); assert.equal(values.adc_pa2, '3');
});

test('CSV prevents spreadsheet formulas while preserving negative numeric readings', () => {
  for (const formula of ['=HYPERLINK("https://example.invalid")','+SUM(1,2)','-SUM(1,2)','@SUM(A1:A2)','\t =1+1']) {
    const [,row] = parseCSV(toCSV(session({name:formula,notes:formula})));
    assert.equal(row[1], "'"+formula); assert.equal(row[2], "'"+formula);
  }
  const [columns,row] = parseCSV(toCSV(session({samples:[{...sample,current:-0.02,vsec:-1.5}]})));
  assert.equal(row[columns.indexOf('current_diagnostic_A')], '-0.02');
  assert.equal(row[columns.indexOf('vsec_V')], '-1.5');
});

test('every CSV sample retains session provenance and firmware, including synthetic sessions', () => {
  const [columns,...rows] = parseCSV(toCSV(session({source:'demo',firmware:{fw:'SIMULATED'},samples:[sample,{...sample,ms:1000}]})));
  for (const row of rows) { assert.equal(row[columns.indexOf('source')], 'demo'); assert.equal(row[columns.indexOf('firmware')], 'SIMULATED'); }
});

test('empty sessions produce only a header', () => { assert.equal(parseCSV(toCSV(session({samples:[]}))).length, 1); });

test('CSV handles absent firmware metadata from an imported session', () => {
  assert.doesNotThrow(() => toCSV(session({firmware:null})));
  assert.doesNotThrow(() => toCSV(session({firmware:undefined})));
});
