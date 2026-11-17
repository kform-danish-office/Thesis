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
const timing = {requested_hz:1100000,actual_hz:1111111,requested_dead_ns:41,actual_dead_ns:50,timer_hz:100000000,period_ticks:90,dead_ticks:5,revision:7,receivedAt:'2026-10-19T11:59:59.950Z',source:'device'};
const originalColumns = ['session_id','session_name','notes','source','firmware','received_at','device_ms','enabled','mode','fault','vpri_V','vsec_V','current_diagnostic_A','power_diagnostic_W','duty_percent','adc_pa0','adc_pa1','adc_pa2','VSET','VON','VMAX','OVP','DMAX','OD','FEN','lease_ms'];
const timingColumns = ['requestedcarrier_Hz','actualcarrier_Hz','requesteddeadtime_ns','actualdeadtime_ns','timer_clock_Hz','period_ticks','dead_ticks','timing_revision','timing_received_at','timing_source'];

test('CSV preserves quoted names, commas, newlines, missing diagnostics, units and column order', () => {
  const csv = toCSV(session({name:'Run, "A"',notes:'first\nsecond'}));
  assert.ok(csv.startsWith('\uFEFF')); const [columns,row] = parseCSV(csv);
  assert.deepEqual(columns, [...originalColumns,...timingColumns]); assert.equal(row.length, columns.length);
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

test('CSV records each sample timing readback, request, units and independent receive time', () => {
  const changedTiming = {...timing,requested_hz:1300000,actual_hz:1315789,requested_dead_ns:55,actual_dead_ns:60,period_ticks:76,dead_ticks:6,revision:8,receivedAt:'2026-10-19T12:00:00.750Z',source:'device'};
  const [columns,...rows] = parseCSV(toCSV(session({timing:changedTiming,samples:[{...sample,timing},{...sample,receivedAt:'2026-10-19T12:00:01.000Z',ms:1500,timing:changedTiming}]})));
  const values = rows.map(row => Object.fromEntries(columns.map((key,index) => [key,row[index]])));
  for (const [index,readback] of [timing,changedTiming].entries()) {
    assert.deepEqual(timingColumns.map(key => values[index][key]), [
      readback.requested_hz,readback.actual_hz,readback.requested_dead_ns,readback.actual_dead_ns,
      readback.timer_hz,readback.period_ticks,readback.dead_ticks,readback.revision,readback.receivedAt,readback.source,
    ].map(String));
  }
  assert.equal(values[0].received_at, sample.receivedAt);
  assert.equal(values[1].received_at, '2026-10-19T12:00:01.000Z');
  assert.equal(values[0].device_ms, '500');
  assert.equal(values[1].device_ms, '1500');
  assert.notEqual(values[0].timing_received_at, values[0].received_at);
});

test('CSV leaves legacy, stale and unreported sample timing blank without session fallback', () => {
  const [columns,...rows] = parseCSV(toCSV(session({timing,samples:[sample,{...sample,timing:null},{...sample,timing:{}}]})));
  for (const row of rows) {
    assert.deepEqual(timingColumns.map(key => row[columns.indexOf(key)]), timingColumns.map(() => ''));
    assert.equal(row[columns.indexOf('FEN')], '10000');
  }
});

test('CSV protects timing provenance from spreadsheet formulas and preserves reported zero revision', () => {
  const formula = '=HYPERLINK("https://example.invalid")';
  const [columns,row] = parseCSV(toCSV(session({samples:[{...sample,timing:{...timing,revision:0,source:formula}}]})));
  assert.equal(row[columns.indexOf('timing_source')], "'"+formula);
  assert.equal(row[columns.indexOf('timing_revision')], '0');
});
