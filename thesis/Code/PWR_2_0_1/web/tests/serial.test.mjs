import test from 'node:test';
import assert from 'node:assert/strict';
import {DeviceLink} from '../serial.js';

const turn = () => new Promise(resolve => setImmediate(resolve));
async function until(predicate, label='condition') { for (let i=0; i<30; i++) { if (predicate()) return; await turn(); } assert.fail(`Timed out waiting for ${label}`); }

function fakeBoard({intercept}={}) {
  const board = {writes:[],opened:false,closed:false,canceled:false,enabled:false,requests:0,options:null};
  let controller; const decoder = new TextDecoder(); const encoder = new TextEncoder();
  board.sample = (changes={}) => ({type:'telemetry',protocol:1,ms:1000,enabled:board.enabled,mode:'VSBONLY',fault:'NONE',vpri:325,vsec:board.enabled?28:0,current:null,power:null,duty:board.enabled?50:0,adc:[2000,100,0],settings:{VSET:28,VON:28,VMAX:32,OVP:36,DMAX:100,OD:10,FEN:10000},lease_ms:5000,stream_ms:500,...changes});
  board.sendRaw = text => { if (!board.closed && !board.canceled) controller.enqueue(encoder.encode(text)); };
  board.send = frame => board.sendRaw(JSON.stringify(frame)+'\r\n');
  board.ack = (id, changes={}) => board.send({type:'ack',id:String(id),ok:true,code:'OK',...changes});
  board.emitSample = changes => board.send(board.sample(changes));
  const port = {
    readable:new ReadableStream({start(value) {controller=value;},cancel() {board.canceled=true;}}),
    writable:new WritableStream({write(bytes) {
      const line = decoder.decode(bytes).trim(); board.writes.push(line);
      if (line === 'WEB HELLO') { board.send({type:'hello',protocol:1,fw:'PWR-2.0.1',board:'Fake board',baud:115200}); return; }
      const match = /^WEB (\d+) (.+)$/.exec(line); assert.ok(match, `Unexpected wire command: ${line}`);
      const [,id,command] = match;
      if (intercept?.({id,command,line},board)) return;
      if (command === 'OFF') board.enabled=false;
      if (command === 'ON') board.enabled=true;
      if (command === 'SNAPSHOT') board.emitSample();
      board.ack(id);
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
