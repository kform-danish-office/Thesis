import test from 'node:test';
import assert from 'node:assert/strict';
import {DeviceLink} from '../serial.js';

const turn = () => new Promise(resolve => setImmediate(resolve));
async function until(predicate, label='condition') { for (let i=0; i<30; i++) { if (predicate()) return; await turn(); } assert.fail(`Timed out waiting for ${label}`); }

function timingSample(changes={}) {
  const requested_hz = changes.requested_hz ?? 1000000, requested_dead_ns = changes.requested_dead_ns ?? 40;
  const timer_hz = 100000000, period_ticks = 2 * Math.floor((timer_hz + requested_hz) / (2 * requested_hz));
  const dead_ticks = Math.ceil(requested_dead_ns / 10);
  return {requested_hz,actual_hz:Math.floor((timer_hz + period_ticks / 2) / period_ticks),requested_dead_ns,actual_dead_ns:dead_ticks*10,
    timer_hz,period_ticks,dead_ticks,min_hz:500000,max_hz:2000000,min_dead_ns:20,max_dead_ns:200,revision:0,enabled:false,busy:false,...changes};
}

function fakeBoard({intercept,capabilities,boardName='Fake board'}={}) {
  const board = {writes:[],opened:false,closed:false,canceled:false,enabled:false,requests:0,options:null,timing:timingSample()};
  let controller; const decoder = new TextDecoder(); const encoder = new TextEncoder();
  board.sample = (changes={}) => ({type:'telemetry',protocol:1,ms:1000,enabled:board.enabled,mode:'VSBONLY',fault:'NONE',vpri:325,vsec:board.enabled?28:0,current:null,power:null,duty:board.enabled?50:0,adc:[2000,100,0],settings:{VSET:28,VON:28,VMAX:32,OVP:36,DMAX:100,OD:10,FEN:10000,...(capabilities?.includes('bench_settings_v1') ? benchSample() : {})},lease_ms:5000,stream_ms:500,...(capabilities?.includes('calibration_v1') ? {calibration:calibrationSample(0)} : {}),...changes});
  board.sendRaw = text => { if (!board.closed && !board.canceled) controller.enqueue(encoder.encode(text)); };
  board.send = frame => board.sendRaw(JSON.stringify(frame)+'\r\n');
  board.ack = (id, changes={}) => board.send({type:'ack',id:String(id),ok:true,code:'OK',...changes});
  board.emitSample = changes => board.send(board.sample(changes));
  board.emitTiming = (changes={},id='') => board.send({type:'timing',protocol:1,id,timing:{...board.timing,enabled:board.enabled,busy:board.enabled,...changes}});
  const port = {
    readable:new ReadableStream({start(value) {controller=value;},cancel() {board.canceled=true;}}),
    writable:new WritableStream({write(bytes) {
      const line = decoder.decode(bytes).trim(); board.writes.push(line);
      if (line === 'WEB HELLO') { board.send({type:'hello',protocol:1,fw:'PWR-2.0.1',board:boardName,baud:115200,capabilities}); return; }
      const match = /^WEB (\d+) (.+)$/.exec(line); assert.ok(match, `Unexpected wire command: ${line}`);
      const [,id,command] = match;
      if (intercept?.({id,command,line},board)) return;
      if (command === 'OFF') board.enabled=false;
      if (command === 'ON') board.enabled=true;
      if (command === 'SNAPSHOT') { board.emitSample(); if (capabilities?.includes('carrier_timing_v1')) board.emitTiming({},id); }
      if (command.startsWith('TIMING ')) {
        const [,hz,deadNs] = command.split(' ');
        board.timing = timingSample({requested_hz:Number(hz),requested_dead_ns:Number(deadNs),revision:board.timing.revision+1});
      }
      board.ack(id);
      if (command.startsWith('TIMING ')) board.emitTiming({},id);
    }}),
    async open(options) {board.opened=true;board.options=options;},
    async close() {board.closed=true;},
  };
  board.unplug = () => {board.closed=true;controller.close();};
  board.serial = {async requestPort() {board.requests++;return port;}};
  board.link = new DeviceLink({serial:board.serial});
  return board;
}

test('USB handshake, lease, streaming and snapshots negotiate at 115200 without a physical port', async t => {
  const board = fakeBoard(); t.after(() => board.link.disconnect());
  const samples=[]; board.link.addEventListener('sample',event => samples.push(event.detail));
  await board.link.connect();
  assert.equal(board.requests,1); assert.equal(board.options.baudRate,115200);
  assert.deepEqual(board.writes.slice(0,4), ['WEB HELLO','WEB 1 LEASE 5000','WEB 2 STREAM 500','WEB 3 SNAPSHOT']);
  assert.equal(board.link.state,'connected'); assert.equal(board.link.isReady,true);
  assert.equal(samples.length,1); assert.equal(samples[0].receivedAt.endsWith('Z'),true);
  assert.equal(samples[0].current,null);
});

test('unknown acknowledgments and human UART output do not settle or corrupt a command', async t => {
  let held; const board=fakeBoard({intercept:(request) => {if (request.command==='SET VSET 30') {held=request;return true;}}});
  t.after(() => board.link.disconnect()); await board.link.connect();
  let settled=false; const pending=board.link.command('SET VSET 30').finally(() => {settled=true;});
  await until(() => held,'held command'); board.ack('999'); board.sendRaw('PWR> enabled=0\r\n'); await turn();
  assert.equal(settled,false); board.ack(held.id); await pending;
  assert.equal(board.link.state,'connected');
});

test('board rejections become actionable command errors and the queue recovers', async t => {
  const board=fakeBoard({intercept:(request,b) => {if (request.command==='SET VSET 999') {b.ack(request.id,{ok:false,code:'RANGE'});return true;}}});
  t.after(() => board.link.disconnect()); await board.link.connect();
  await assert.rejects(board.link.command('SET VSET 999'), /SET VSET 999: RANGE/);
  assert.equal((await board.link.command('SNAPSHOT')).ok,true);
});

test('invalid commands are rejected before any bytes are sent', async t => {
  const board=fakeBoard(); t.after(() => board.link.disconnect()); await board.link.connect();
  const count=board.writes.length;
  for (const command of ['ON\nOFF','WEB 44 ON',';ON','']) await assert.rejects(board.link.command(command));
  assert.equal(board.writes.length,count);
});

test('ON is refused after stale telemetry, a fault, or loss of the reported lease', async t => {
  let now=1_000_000; t.mock.method(Date,'now',() => now);
  const board=fakeBoard(); t.after(() => board.link.disconnect()); await board.link.connect();
  now+=2600; const baseline=board.writes.length;
  await assert.rejects(board.link.command('ON'),/fresh telemetry/); assert.equal(board.writes.length,baseline);
  board.emitSample({fault:'OVP'}); await turn();
  // A fresh sample cannot make an expired host-confirmed lease ready; reconnect is required.
  await assert.rejects(board.link.command('ON'),/fresh telemetry/);
  await board.link.disconnect();
  const faultBoard=fakeBoard(); t.after(() => faultBoard.link.disconnect()); await faultBoard.link.connect();
  faultBoard.emitSample({fault:'OVP'}); await turn(); const count=faultBoard.writes.length;
  await assert.rejects(faultBoard.link.command('ON'),/fault/); assert.equal(faultBoard.writes.length,count);
  faultBoard.emitSample({fault:'NONE',lease_ms:0}); await turn();
  await assert.rejects(faultBoard.link.command('ON'),/lease/);
});

test('OFF bypasses a pending command and cancels queued ON and parameter changes', async t => {
  let held; const board=fakeBoard({intercept:(request) => {if (request.command==='SET VSET 30') {held=request;return true;}}});
  t.after(() => board.link.disconnect()); await board.link.connect();
  const first=board.link.command('SET VSET 30'); await until(() => held);
  const queuedOn=assert.rejects(board.link.command('ON'),/canceled/);
  const queuedSet=assert.rejects(board.link.command('SET OD 40'),/canceled/);
  await board.link.command('OFF');
  assert.ok(board.writes.some(line => line.endsWith(' OFF')));
  board.ack(held.id); await first; await Promise.all([queuedOn,queuedSet]);
  assert.equal(board.writes.some(line => line.endsWith(' ON') || line.endsWith(' SET OD 40')),false);
});

test('disconnect sends OFF then stops streaming and closes the fake port', async () => {
  const board=fakeBoard(); await board.link.connect(); await board.link.command('ON'); await turn();
  const start=board.writes.length; await board.link.disconnect();
  const commands=board.writes.slice(start).map(line => line.replace(/^WEB \d+ /,''));
  assert.ok(commands.includes('OFF')); assert.ok(commands.includes('STREAM 0'));
  assert.ok(commands.indexOf('OFF') < commands.indexOf('STREAM 0'));
  assert.equal(board.enabled,false); assert.equal(board.closed,true); assert.equal(board.canceled,true);
  assert.equal(board.link.state,'disconnected'); assert.equal(board.link.lastSample,null);
});

test('disconnect immediately blocks a concurrent ON from passing its OFF command', async t => {
  let held; const board=fakeBoard({intercept:(request) => {if (request.command==='OFF') {held=request;return true;}}});
  await board.link.connect(); const disconnect=board.link.disconnect(); await until(() => held,'disconnect OFF');
  const concurrent=assert.rejects(board.link.command('ON'),/disconnect|closing|connect|canceled/i);
  board.ack(held.id); await disconnect; await concurrent;
  assert.equal(board.writes.some(line => line.endsWith(' ON')),false);
  t.after(() => board.link.disconnect());
});

test('unplug clears readiness and rejects pending control requests', async t => {
  let held; const board=fakeBoard({intercept:(request) => {if (request.command==='SET VSET 30') {held=request;return true;}}});
  t.after(() => board.link.disconnect()); await board.link.connect();
  const pending=assert.rejects(board.link.command('SET VSET 30'),/lost|disconnected/i); await until(() => held);
  board.unplug(); await pending; await until(() => board.link.state==='disconnected');
  assert.equal(board.link.isReady,false); await assert.rejects(board.link.command('ON'),/Connect/);
});

test('demo remains visibly synthetic and never requests or writes to USB', async t => {
  const board=fakeBoard(); t.after(() => board.link.stopDemo()); board.link.startDemo();
  assert.equal(board.link.state,'demo'); assert.equal(board.link.lastSample.source,'demo'); assert.equal(board.link.hello.fw,'SIMULATED');
  await board.link.command('ON'); await board.link.command('SET VSET 30'); assert.equal(board.link.lastSample.enabled,true);
  await board.link.command('OFF'); assert.equal(board.link.lastSample.enabled,false);
  await assert.rejects(board.link.command('SET VSET 900'),/invalid/);
  assert.equal(board.requests,0); assert.deepEqual(board.writes,[]); await board.link.disconnect();
  assert.equal(board.link.state,'disconnected');
});

test('disconnect cancels a pending port chooser before the chosen port can open', async () => {
  let choose; let opens=0;
  const selected = {async open() {opens++;},async close() {}};
  const link = new DeviceLink({serial:{requestPort() {return new Promise(resolve => {choose=resolve;});}}});
  const pending = assert.rejects(link.connect(),/canceled/i);
  await link.disconnect(); choose(selected); await pending;
  assert.equal(opens,0); assert.equal(link.state,'disconnected'); assert.equal(link.isReady,false);
});

test('a command acknowledgment timeout is an error and never retries the mutation', async t => {
  const board=fakeBoard({intercept: request => request.command === 'SET VSET 31'});
  t.after(() => board.link.disconnect()); await board.link.connect();
  await assert.rejects(board.link.command('SET VSET 31'),/No acknowledgment/);
  assert.equal(board.writes.filter(line => line.endsWith('SET VSET 31')).length,1);
  assert.equal((await board.link.command('OFF')).ok,true);
});

test('demo settings persistence is explicit and requires output OFF', async t => {
  const board=fakeBoard(); t.after(() => board.link.stopDemo()); board.link.startDemo();
  await board.link.command('SET OD 20'); assert.equal(board.link.lastSample.settings_pending,true);
  await board.link.command('ON'); await assert.rejects(board.link.command('SAVE'),/turn_off_first/);
  await board.link.command('OFF'); await board.link.command('SAVE');
  assert.equal(board.link.lastSample.settings_pending,false); assert.equal(board.requests,0);
});

const calibrationSample = (state=2) => ({state,kind:2,slot:1,duty:10,nlduty:25,preduty:10,offset:0.1,line_ref:325});
test('calibration is capability-gated and never sent to legacy firmware or demo', async t => {
  const board=fakeBoard();t.after(()=>board.link.disconnect());await board.link.connect();
  let count=board.writes.length;
  await assert.rejects(board.link.command('CAL NOLOAD'),/firmware PWR-2.0.2/);
  assert.equal(board.writes.length,count);
  await board.link.disconnect();board.link.startDemo();
  await assert.rejects(board.link.command('CAL ZERO'),/Demo cannot calibrate hardware/);
  board.link.stopDemo();
});
test('capable calibration commands require output OFF and reject conflicting commands while running',async t=>{
  const board=fakeBoard({capabilities:['calibration_v1']});t.after(()=>board.link.disconnect());await board.link.connect();
  assert.equal(board.link.supportsCalibration,true);
  await board.link.command('CAL LOAD 2');assert(board.writes.some(s=>s.endsWith('CAL LOAD 2')));
  await assert.rejects(board.link.command('CAL LOAD 4'),/supported calibration/);
  board.emitSample({enabled:true});await until(()=>board.link.lastSample.enabled);
  await assert.rejects(board.link.command('CAL ZERO'),/Turn output OFF/);
  board.emitSample({enabled:true,calibration:calibrationSample()});await until(()=>board.link.lastSample.calibration);
  const count=board.writes.length;
  await assert.rejects(board.link.command('SET VSET 29'),/Calibration is active/);assert.equal(board.writes.length,count);
  await board.link.command('OFF');assert(board.writes.some(s=>s.endsWith(' OFF')));
});

const benchSample = () => ({LOAD1:50,LOAD2:5,LOAD3:2.5,ACTLOAD:1,NLDUTY:25,AUTOMAX:100,AUTOSTEP:2,AUTOFINE:0.5,AUTOSETTLE:160,AUTOMEAS:100,PREMS:3,PRESETTLE:80,PREMAX:4});

test('demo bench settings expose synthetic readback and require explicit save without USB writes', async t => {
  const board=fakeBoard();t.after(()=>board.link.stopDemo());board.link.startDemo();
  assert.equal(board.link.supportsBenchSettings,true);assert.equal(board.link.supportsCalibration,false);
  assert.equal(board.link.lastSample.settings.LOAD1,50);assert.equal(board.link.lastSample.settings.ACTLOAD,1);
  await board.link.command('SET LOAD1 47.5');await board.link.command('SET LOAD2 0');await board.link.command('LOAD 3');
  await board.link.command('SET NLDUTY 27.4');await board.link.command('SET AUTOSETTLE 250');await board.link.command('SET PREMAX 5');
  assert.equal(board.link.lastSample.settings.LOAD1,47.5);assert.equal(board.link.lastSample.settings.LOAD2,0);
  assert.equal(board.link.lastSample.settings.ACTLOAD,3);assert.equal(board.link.lastSample.settings.NLDUTY,27.4);
  assert.equal(board.link.lastSample.settings.AUTOSETTLE,250);assert.equal(board.link.lastSample.settings.PREMAX,5);
  assert.equal(board.link.lastSample.settings_pending,true);await board.link.command('SAVE');assert.equal(board.link.lastSample.settings_pending,false);
  assert.equal(board.requests,0);assert.deepEqual(board.writes,[]);
});

test('demo tuning maximum follows the device DMAX cap without changing the requested DMAX',async t=>{
  const board=fakeBoard();t.after(()=>board.link.stopDemo());board.link.startDemo();
  await board.link.command('SET DMAX 60');await board.link.command('SET AUTOMAX 80');
  assert.equal(board.link.lastSample.settings.DMAX,60);assert.equal(board.link.lastSample.settings.AUTOMAX,60);
  await board.link.command('SET DMAX 40');assert.equal(board.link.lastSample.settings.AUTOMAX,40);
});

test('legacy boards cannot receive unreported bench settings or load/profile aliases',async t=>{
  const board=fakeBoard();t.after(()=>board.link.disconnect());await board.link.connect();const count=board.writes.length;
  for(const command of ['SET LOAD1 50','SET NLDUTY 25','SET AUTOMAX 50','LOAD 2','SET ACTIVELOAD 2','SET LOADSLOT 3'])
    await assert.rejects(board.link.command(command),/bench_settings_v1/);
  await assert.rejects(board.link.command('SET ACTLOAD 2'),/read-only/);assert.equal(board.writes.length,count);
  // Existing generic terminal commands retain firmware-side validation.
  await board.link.command('SET VPRIGAIN 1.01');assert(board.writes.some(s=>s.endsWith('SET VPRIGAIN 1.01')));
});

test('capability alone cannot authorize settings without verified numeric readback',async t=>{
  const board=fakeBoard({capabilities:['bench_settings_v1']});t.after(()=>board.link.disconnect());await board.link.connect();
  assert.equal(board.link.supportsBenchSettings,true);board.emitSample({settings:{VSET:28,VON:28,VMAX:32,OVP:36,DMAX:100,OD:10,FEN:10000}});await until(()=>board.link.lastSample.settings.ACTLOAD===undefined);let count=board.writes.length;
  await assert.rejects(board.link.command('SET LOAD1 50'),/verified LOAD1 readback/);
  await assert.rejects(board.link.command('LOAD 1'),/verified load-reference readback/);
  assert.equal(board.writes.length,count);
  board.emitSample({settings:{...board.sample().settings,...benchSample(),LOAD2:'5'}});await until(()=>board.link.lastSample.settings.ACTLOAD===1);
  count=board.writes.length;await assert.rejects(board.link.command('SET LOAD2 6'),/verified LOAD2 readback/);
  await assert.rejects(board.link.command('LOAD 2'),/verified load-reference readback/);assert.equal(board.writes.length,count);
});

test('bench edits validate exact ranges, numeric values and tokens before any wire write',async t=>{
  const board=fakeBoard({capabilities:['bench_settings_v1']});t.after(()=>board.link.disconnect());await board.link.connect();
  board.emitSample({settings:{...board.sample().settings,...benchSample()}});await until(()=>board.link.lastSample.settings.ACTLOAD===1);
  const count=board.writes.length;
  for(const command of ['SET LOAD1 -1','SET LOAD1 100000.01','SET LOAD1 0X10','SET LOAD1 NAN','SET LOAD1 1E309','SET LOAD1 .','SET LOAD1 50 60','SET LOAD1','SET AUTOMAX 100.1','SET NLDUTY 25.05','SET AUTOSTEP 0.4','SET AUTOSTEP 25.1','SET AUTOFINE 0','SET AUTOFINE 10.1','SET AUTOSETTLE 19','SET AUTOSETTLE 3001','SET AUTOSETTLE 20.5','SET AUTOMEAS 2001','SET PREMS 0','SET PREMS 501','SET PRESETTLE 2001','SET PREMAX 1.5','SET PREMAX 21','LOAD 0','LOAD 4','LOAD 1.0','LOAD +1','LOAD 2 extra'])
    await assert.rejects(board.link.command(command),undefined,command);
  assert.equal(board.writes.length,count);
  for(const command of ['SET LOAD1 0','SET LOAD2 100000','SET NLDUTY 0.1','SET AUTOSTEP 0.5','SET AUTOFINE 0.1','SET AUTOSETTLE 20','SET AUTOMEAS 2000','SET PREMS 500','SET PRESETTLE 2000','SET PREMAX 20','LOAD 2','SET ACTIVELOAD 3'])await board.link.command(command);
  assert(board.writes.some(s=>s.endsWith('SET LOAD1 0')));assert(board.writes.some(s=>s.endsWith('LOAD 2')));
});

test('load and tuning changes are refused while output ON, while base live edits and OFF remain usable',async t=>{
  const board=fakeBoard({capabilities:['bench_settings_v1']});t.after(()=>board.link.disconnect());await board.link.connect();
  board.emitSample({enabled:true,settings:{...board.sample().settings,...benchSample()}});await until(()=>board.link.lastSample.enabled);
  const count=board.writes.length;
  for(const command of ['SET LOAD3 3','SET NLDUTY 20','SET PREMS 5','LOAD 2','SET LOADSLOT 2'])await assert.rejects(board.link.command(command),/Turn output OFF/);
  assert.equal(board.writes.length,count);
  await board.link.command('SET VSET 29');await board.link.command('OFF');assert(board.writes.some(s=>s.endsWith('SET VSET 29')));assert(board.writes.some(s=>s.endsWith(' OFF')));
});

test('carrier timing is capability-gated for legacy and G071 boards without changing generic terminal SET',async t=>{
  for (const boardName of ['Legacy F410','STM32G071']) {
    const board=fakeBoard({boardName});t.after(()=>board.link.disconnect());await board.link.connect();
    assert.equal(board.link.supportsCarrierTiming,false);board.emitTiming();await turn();assert.equal(board.link.lastTiming,null);
    const count=board.writes.length;await assert.rejects(board.link.command('TIMING 1000000 40'),/carrier_timing_v1/);assert.equal(board.writes.length,count);
    await board.link.command('SET VPRIGAIN 1.01');assert(board.writes.some(line=>line.endsWith(' SET VPRIGAIN 1.01')));
    await board.link.disconnect();
  }
});

test('capable timing edits send one atomic pair and expose verified quantized device readback',async t=>{
  const board=fakeBoard({capabilities:['carrier_timing_v1']});t.after(()=>board.link.disconnect());
  const events=[];board.link.addEventListener('timing',event=>events.push(event.detail));await board.link.connect();
  assert.equal(board.link.supportsCarrierTiming,true);assert.equal(board.link.lastTiming.requested_hz,1000000);
  assert.equal(board.link.lastTiming.source,'device');assert(board.link.lastTiming.receivedAt.endsWith('Z'));
  const ack=await board.link.command('TIMING 1400000 41');
  assert.equal(ack.ok,true);assert.equal(ack.timing.requested_hz,1400000);assert.equal(ack.timing.requested_dead_ns,41);
  assert.equal(board.link.lastTiming.period_ticks,72);assert.equal(board.link.lastTiming.actual_hz,1388889);
  assert.equal(board.link.lastTiming.dead_ticks,5);assert.equal(board.link.lastTiming.actual_dead_ns,50);
  assert.equal(board.writes.filter(line=>line.endsWith(' TIMING 1400000 41')).length,1);assert(events.length>=2);
  await board.link.disconnect();assert.equal(board.link.lastTiming,null);
});

test('TIMING waits for both its ACK and matching id readback, in either order',async t=>{
  let held;const board=fakeBoard({capabilities:['carrier_timing_v1'],intercept:request=>{if(request.command.startsWith('TIMING ')){held=request;return true;}}});
  t.after(()=>board.link.disconnect());await board.link.connect();
  let settled=false;const first=board.link.command('TIMING 1400000 41').finally(()=>{settled=true;});await until(()=>held);
  board.ack(held.id);await turn();assert.equal(settled,false);
  const readback=timingSample({requested_hz:1400000,requested_dead_ns:41,revision:1});
  board.emitTiming(readback,'unrelated');await turn();assert.equal(settled,false);board.emitTiming(readback,held.id);await first;
  held=null;settled=false;const second=board.link.command('TIMING 1000000 40').finally(()=>{settled=true;});await until(()=>held);
  board.emitTiming(timingSample({revision:2}),held.id);await turn();assert.equal(settled,false);board.ack(held.id);await second;
});

test('an ACK cannot confirm missing or mismatched timing readback and mutations are never retried',async t=>{
  const board=fakeBoard({capabilities:['carrier_timing_v1'],intercept:(request,b)=>{
    if(request.command==='TIMING 1400000 40'){b.ack(request.id);return true;}
    if(request.command==='TIMING 1200000 40'){b.ack(request.id);b.emitTiming({},request.id);return true;}
  }});t.after(()=>board.link.disconnect());await board.link.connect();
  await assert.rejects(board.link.command('TIMING 1200000 40'),/does not confirm.*unconfirmed/);
  await assert.rejects(board.link.command('TIMING 1400000 40'),/No verified timing readback.*unconfirmed/);
  assert.equal(board.writes.filter(line=>line.endsWith(' TIMING 1400000 40')).length,1);
  await board.link.command('OFF');
});

test('carrier timing validates exact integer tokens, independent bounds and the coupled switching-time bound before writing',async t=>{
  const board=fakeBoard({capabilities:['carrier_timing_v1']});t.after(()=>board.link.disconnect());await board.link.connect();
  const count=board.writes.length;
  for(const command of ['TIMING','TIMING 1000000','TIMING 1000000 40 extra','TIMING 499999 40','TIMING 2000001 40','TIMING 1000000 19','TIMING 1000000 201',
    'TIMING 1000000.0 40','TIMING +1000000 40','TIMING 1E6 40','TIMING 0X100000 40','TIMING NAN 40','TIMING 1000000 40.0','TIMING 1000000 +40','TIMING 1000000 -40','TIMING 9007199254740992 40',
    'TIMING 2000000 121','TIMING 2000000 200']) await assert.rejects(board.link.command(command),undefined,command);
  assert.equal(board.writes.length,count);
  for(const command of ['TIMING 500000 200','TIMING 2000000 120','TIMING 1000000 20']) await board.link.command(command);
  assert.equal(board.link.lastTiming.requested_dead_ns,20);
});

test('timing edits require fresh numeric readback, output OFF, and no calibration or device operation',async t=>{
  const board=fakeBoard({capabilities:['carrier_timing_v1','calibration_v1']});t.after(()=>board.link.disconnect());await board.link.connect();
  const count=board.writes.length;
  board.link.lastTiming=null;await assert.rejects(board.link.command('TIMING 1000000 40'),/verified carrier timing readback/);
  board.emitTiming();await until(()=>board.link.lastTiming);
  board.emitSample({enabled:true});await until(()=>board.link.lastSample.enabled);await assert.rejects(board.link.command('TIMING 1000000 40'),/Turn output OFF/);
  board.emitSample({enabled:false,calibration:calibrationSample(2)});await until(()=>!board.link.lastSample.enabled);await assert.rejects(board.link.command('TIMING 1000000 40'),/Calibration.*active/);
  board.emitSample({calibration:calibrationSample(0)});board.emitTiming({busy:true});await until(()=>board.link.lastTiming.busy);await assert.rejects(board.link.command('TIMING 1000000 40'),/device operation.*active/);
  assert.equal(board.writes.length,count);board.emitTiming();await until(()=>!board.link.lastTiming.busy);await board.link.command('TIMING 1000000 40');
});

test('timing readback expires independently of fresh telemetry and a renewed lease',async t=>{
  let now=1000000;t.mock.method(Date,'now',()=>now);t.mock.timers.enable({apis:['setInterval']});
  const board=fakeBoard({capabilities:['carrier_timing_v1']});t.after(()=>board.link.disconnect());await board.link.connect();
  now+=2000;t.mock.timers.tick(1000);await turn();
  now+=600;board.emitSample();await turn();assert.equal(board.link.isReady,true);
  const count=board.writes.length;await assert.rejects(board.link.command('TIMING 1000000 40'),/fresh, verified carrier timing/);assert.equal(board.writes.length,count);
  board.emitTiming();await turn();await board.link.command('TIMING 1000000 40');
});

test('queued timing edits recheck capability, output state, readback, busy state and freshness at execution',async t=>{
  for(const condition of ['capability','output','readback','busy','stale']) {
    let held,holdSnapshots=false;let now=1000000;t.mock.method(Date,'now',()=>now);
    const board=fakeBoard({capabilities:['carrier_timing_v1'],intercept:(request,b)=>{
      if(request.command==='SET VSET 30'){held=request;return true;}
      if(holdSnapshots&&request.command==='SNAPSHOT'){b.ack(request.id);return true;}
    }});t.after(()=>board.link.disconnect());await board.link.connect();holdSnapshots=true;
    const first=board.link.command('SET VSET 30');await until(()=>held);
    const timing=assert.rejects(board.link.command('TIMING 1000000 40'));
    if(condition==='capability') board.link.hello.capabilities=[];
    if(condition==='output') {board.emitSample({enabled:true});await turn();}
    if(condition==='readback') board.link.lastTiming=null;
    if(condition==='busy') {board.emitTiming({busy:true});await turn();}
    if(condition==='stale') now+=2600;
    board.ack(held.id);await first;await timing;
    assert.equal(board.writes.some(line=>line.includes(' TIMING ')),false,condition);await board.link.disconnect();t.mock.restoreAll();
  }
});

test('OFF retains priority and cancels a queued timing pair',async t=>{
  let held;const board=fakeBoard({capabilities:['carrier_timing_v1'],intercept:request=>{if(request.command==='SET VSET 30'){held=request;return true;}}});
  t.after(()=>board.link.disconnect());await board.link.connect();const first=board.link.command('SET VSET 30');await until(()=>held);
  const timing=assert.rejects(board.link.command('TIMING 1400000 40'),/canceled/);await board.link.command('OFF');board.ack(held.id);await first;await timing;
  assert(board.writes.some(line=>line.endsWith(' OFF')));assert.equal(board.writes.some(line=>line.includes(' TIMING ')),false);
});

test('ON intent blocks timing until a later confirmed OFF timing frame, including during queued ON',async t=>{
  let held,holdSnapshots=false;const board=fakeBoard({capabilities:['carrier_timing_v1'],intercept:(request,b)=>{
    if(request.command==='ON'){held=request;return true;}
    if(holdSnapshots&&request.command==='SNAPSHOT'){b.ack(request.id);return true;}
  }});t.after(()=>board.link.disconnect());await board.link.connect();holdSnapshots=true;
  const on=board.link.command('ON');await until(()=>held);board.emitTiming();await turn();
  await assert.rejects(board.link.command('TIMING 1000000 40'),/new output OFF timing readback/);
  board.enabled=true;board.ack(held.id);await on;
  await assert.rejects(board.link.command('TIMING 1000000 40'),/new output OFF timing readback/);
  await board.link.command('OFF');await assert.rejects(board.link.command('TIMING 1000000 40'),/new output OFF timing readback/);
  board.emitTiming();await turn();await board.link.command('TIMING 1000000 40');
});

test('demo V2 timing quantization is synthetic, OFF-only, paired and saved explicitly without USB access',async t=>{
  const board=fakeBoard();t.after(()=>board.link.stopDemo());board.link.startDemo();
  assert.equal(board.link.supportsCarrierTiming,true);assert.equal(board.link.supportsCalibration,false);assert.equal(board.link.lastTiming.source,'demo');
  assert.equal(board.link.lastTiming.timer_hz,100000000);assert.equal(board.link.lastTiming.period_ticks,100);assert.equal(board.link.lastTiming.dead_ticks,4);
  await board.link.command('TIMING 1234567 41');
  assert.equal(board.link.lastTiming.requested_hz,1234567);assert.equal(board.link.lastTiming.actual_hz,1219512);assert.equal(board.link.lastTiming.period_ticks,82);
  assert.equal(board.link.lastTiming.actual_dead_ns,50);assert.equal(board.link.lastTiming.dead_ticks,5);assert.equal(board.link.lastTiming.revision,1);
  assert.equal(board.link.lastSample.settings_pending,true);await board.link.command('SAVE');assert.equal(board.link.lastSample.settings_pending,false);
  await assert.rejects(board.link.command('TIMING 2000000 121'),/too little switching time/);assert.equal(board.link.lastTiming.revision,1);
  await board.link.command('ON');await assert.rejects(board.link.command('TIMING 1000000 40'),/Turn output OFF/);await board.link.command('OFF');await board.link.command('TIMING 1000000 40');
  assert.equal(board.requests,0);assert.deepEqual(board.writes,[]);board.link.stopDemo();assert.equal(board.link.lastTiming,null);
});
