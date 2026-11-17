import test from 'node:test';
import assert from 'node:assert/strict';
import {LineFramer, parseFrame, validateCommand, faultActive} from '../protocol.js';

const sample = (changes = {}) => ({type:'telemetry', protocol:1, ms:123, enabled:false, mode:'VSBONLY', fault:'NONE', vpri:325, vsec:0, current:null, power:null, duty:0, adc:[2000,0,0], settings:{VSET:28}, lease_ms:5000, stream_ms:500, ...changes});

test('line framer preserves arbitrary chunks and CRLF without empty frames', () => {
  const lines = []; const framer = new LineFramer(line => lines.push(line));
  for (const chunk of ['PWR> {"type":','"ack","id":"1","ok":true}\r','\nstatus\r','\n\nlast',' line\n']) framer.push(chunk);
  assert.deepEqual(lines, ['PWR> {"type":"ack","id":"1","ok":true}', 'status', 'last line']);
});

test('line framer drops a whole oversized frame and recovers at newline', () => {
  const lines = []; const framer = new LineFramer(line => lines.push(line), 5);
  framer.push('12345\n123456'); framer.push('TRAILING\r\nvalid\n');
  assert.deepEqual(lines, ['12345', 'valid']);
});

test('frame parser handles a UART prompt and ignores text, echo, malformed and unknown frames', () => {
  assert.equal(parseFrame('PWR> '+JSON.stringify(sample()))?.type, 'telemetry');
  for (const line of ['PWR>', 'WEB 3 ON', 'status enabled=1', '{', '[]', 'null', '{"type":"mystery"}', '{"type":"hello","protocol":2,"fw":"future"}', '{"type":"ack","id":1,"ok":true}', '{"type":"ack","id":"1","ok":"true"}']) assert.equal(parseFrame(line), null, line);
  assert.deepEqual(parseFrame('{"type":"ack","id":"42","ok":false,"code":"FAULT"}'), {type:'ack',id:'42',ok:false,code:'FAULT'});
});

test('telemetry rejects missing, mistyped and nonfinite measurement fields while preserving null diagnostics', () => {
  assert.equal(parseFrame(JSON.stringify(sample()))?.current, null);
  for (const changes of [{protocol:2},{ms:'123'},{enabled:1},{mode:null},{fault:null},{vsec:'28'},{vpri:undefined},{current:undefined},{duty:{}},{settings:null},{settings:[]}]) assert.equal(parseFrame(JSON.stringify(sample(changes))), null, JSON.stringify(changes));
});

test('telemetry lease must be a finite nonnegative number before it can authorize control', () => {
  for (const lease_ms of ['5000', -1, null, undefined]) assert.equal(parseFrame(JSON.stringify(sample({lease_ms}))), null, String(lease_ms));
  assert.equal(parseFrame(JSON.stringify(sample({lease_ms:0})))?.lease_ms, 0);
});

test('command validation normalizes whitespace and rejects command injection and protocol prefixes', () => {
  assert.equal(validateCommand(' set   vset  +28.5 '), 'SET VSET +28.5');
  for (const command of ['', 'ON\nOFF', 'ON\rOFF', 'ON;OFF', 'ON\u0000OFF', 'WEB 1 ON', 'A'.repeat(73)]) {
    assert.throws(() => validateCommand(command), Error, JSON.stringify(command));
  }
});

test('fault gating permits only known clear states', () => {
  for (const value of [0,'0','NONE','none','OK','']) assert.equal(faultActive(value), false);
  for (const value of [1,'OVP','ADC_STALE',null,undefined,'unknown']) assert.equal(faultActive(value), true);
});
