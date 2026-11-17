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

test('calibration telemetry is validated before presenting running/completed state',()=>{
 const good={state:2,kind:2,slot:1,duty:20,nlduty:25,preduty:10,offset:0.1,line_ref:325};
 assert.equal(parseFrame(JSON.stringify(sample({calibration:good}))).calibration.state,2);
 for(const bad of [null,[],{...good,state:6},{...good,kind:-1},{...good,slot:4},{...good,duty:101},{...good,nlduty:null},{...good,offset:'0.1'}])
  assert.equal(parseFrame(JSON.stringify(sample({calibration:bad}))),null);
});

const timing = (changes={}) => ({requested_hz:1000000,actual_hz:1000000,requested_dead_ns:40,actual_dead_ns:40,timer_hz:100000000,
 period_ticks:100,dead_ticks:4,min_hz:500000,max_hz:2000000,min_dead_ns:20,max_dead_ns:200,revision:0,enabled:false,busy:false,...changes});
const timingFrame = (changes={}) => ({type:'timing',protocol:1,id:'42',timing:timing(),...changes});

test('dedicated timing frames preserve the request, exact timer ratio and safe quantized readback',()=>{
 const frame=parseFrame(JSON.stringify(timingFrame()));assert.equal(frame.timing.actual_hz,1000000);assert.equal(frame.id,'42');
 const quantized=timing({requested_hz:1400000,actual_hz:1388889,period_ticks:72,requested_dead_ns:41,actual_dead_ns:50,dead_ticks:5});
 assert.deepEqual(parseFrame(JSON.stringify(timingFrame({timing:quantized}))).timing,quantized);
 assert(parseFrame(JSON.stringify(timingFrame({id:undefined}))));assert(parseFrame(JSON.stringify(timingFrame({id:''}))));
 assert(parseFrame(JSON.stringify(timingFrame({timing:timing({requested_hz:2000000,actual_hz:2000000,period_ticks:50,requested_dead_ns:120,actual_dead_ns:120,dead_ticks:12})}))));
});

test('malformed, nonnumeric and inconsistent timing frames cannot authorize timing edits',()=>{
 for(const changes of [{protocol:2},{id:42},{timing:null},{timing:[]},{timing:{}}]) assert.equal(parseFrame(JSON.stringify(timingFrame(changes))),null,JSON.stringify(changes));
 for(const key of Object.keys(timing())) {
   for(const value of [undefined,null,typeof timing()[key]==='boolean' ? 0 : String(timing()[key])])
     assert.equal(parseFrame(JSON.stringify(timingFrame({timing:timing({[key]:value})}))),null,`${key}: ${value}`);
 }
 for(const changes of [{requested_hz:499999},{requested_hz:2000001},{requested_dead_ns:19},{requested_dead_ns:201},{actual_hz:999999},{actual_dead_ns:41},
  {timer_hz:0},{period_ticks:99},{period_ticks:102},{dead_ticks:5,actual_dead_ns:50},{min_hz:1},{max_hz:3000000},{min_dead_ns:0},{max_dead_ns:201},
  {revision:-1},{revision:4294967296},{requested_hz:2000000,actual_hz:2000000,period_ticks:50,requested_dead_ns:121,actual_dead_ns:130,dead_ticks:13}])
   assert.equal(parseFrame(JSON.stringify(timingFrame({timing:timing(changes)}))),null,JSON.stringify(changes));
});
