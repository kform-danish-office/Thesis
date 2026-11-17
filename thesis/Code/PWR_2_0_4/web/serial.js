import {LineFramer, parseFrame, validateCommand, faultActive, carrierTimingLimits, validCarrierTiming} from './protocol.js';

// Optional bench settings have explicit readback/capability contracts. Generic
// terminal SET commands retain the original firmware-side validation behavior.
const benchSettings = Object.freeze({
  LOAD1:{min:0,max:100000}, LOAD2:{min:0,max:100000}, LOAD3:{min:0,max:100000},
  NLDUTY:{min:0,max:100,step:0.1}, AUTOMAX:{min:0,max:100,step:0.1},
  AUTOSTEP:{min:0.5,max:25,step:0.1}, AUTOFINE:{min:0.1,max:10,step:0.1},
  AUTOSETTLE:{min:20,max:3000,step:1}, AUTOMEAS:{min:20,max:2000,step:1},
  PREMS:{min:1,max:500,step:1}, PRESETTLE:{min:1,max:2000,step:1}, PREMAX:{min:1,max:20,step:1},
});
const decimalNumber = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:E[+-]?\d+)?$/;
function benchNumber(raw, name, limits) {
  const value = Number(raw);
  if (!decimalNumber.test(raw ?? '') || !Number.isFinite(value) || value < limits.min || value > limits.max ||
      (limits.step && Math.abs(value / limits.step - Math.round(value / limits.step)) > 1e-7))
    throw new Error(`${name} must be ${limits.min}–${limits.max}${limits.step === 1 ? ' in whole numbers' : limits.step ? ` in ${limits.step} steps` : ''}.`);
  return value;
}

function quantizedCarrierTiming(hz, deadNs, timerHz=100000000) {
  const periodTicks = 2 * Math.floor((timerHz + hz) / (2 * hz));
  const deadTicks = Math.ceil(deadNs * timerHz / 1000000000);
  return {requested_hz:hz,actual_hz:Math.floor((timerHz + periodTicks / 2) / periodTicks),requested_dead_ns:deadNs,
    actual_dead_ns:Math.ceil(deadTicks * 1000000000 / timerHz),timer_hz:timerHz,period_ticks:periodTicks,dead_ticks:deadTicks,...carrierTimingLimits};
}

export class DeviceLink extends EventTarget {
  state = 'disconnected'; lastSample = null; lastTiming = null; hello = null;
  #port; #reader; #readTask; #pending = new Map(); #counter = 0; #tail = Promise.resolve(); #writeTail = Promise.resolve(); #heartbeat; #demoTimer; #lastReceived = 0; #lastLease = 0; #closing = false; #epoch = 0; #connection = 0; #queued = 0; #helloWait; #demo;
  #lastTimingReceived = 0; #timingNeedsOffReadback = true; #pendingOn = 0;
  constructor({serial = globalThis.navigator?.serial} = {}) { super(); this.serial = serial; }
  #emit(type, detail) { this.dispatchEvent(new CustomEvent(type,{detail})); }
  #line(direction,text) { this.#emit('line',{direction,text,at:new Date().toISOString()}); }
  #state(state,message='') { this.state = state; this.#emit('state',{state,message}); }
  get isReady() { return this.state === 'demo' || (this.state === 'connected' && this.hello?.protocol === 1 && Date.now()-this.#lastReceived < 2500 && Date.now()-this.#lastLease < 2500 && this.lastSample?.lease_ms > 0 && this.lastSample?.feedback_valid !== false); }
  async connect() {
    if (this.state !== 'disconnected') throw new Error('Disconnect the current session first.');
    if (!this.serial) throw new Error('USB control requires desktop Chrome or Edge on HTTPS or localhost.');
    const connectionEpoch = ++this.#connection; this.#epoch++; let port;
    const checkSession = () => { if (connectionEpoch !== this.#connection) throw new Error('Connection canceled.'); };
    this.#closing = false; this.#state('connecting','Choose your USB-to-UART adapter.');
    try {
      // requestPort must stay in the initiating click's user activation.
      port = await this.serial.requestPort(); checkSession(); this.#port = port;
      await port.open({baudRate:115200,dataBits:8,stopBits:1,parity:'none',flowControl:'none',bufferSize:16384}); checkSession();
      const hello = new Promise((resolve,reject) => {
        const timer = setTimeout(() => { this.#helloWait = null; reject(new Error('No web-protocol handshake. Flash PWR-2.0.1 and check UART wiring.')); },5000);
        this.#helloWait = {resolve: value => { clearTimeout(timer); this.#helloWait = null; resolve(value); },reject: error => { clearTimeout(timer); this.#helloWait = null; reject(error); }};
      });
      // A write may fail before the handshake is awaited; cleanup still rejects it.
      void hello.catch(() => {});
      this.#reader = port.readable.getReader(); this.#readTask = this.#readLoop(this.#reader,connectionEpoch);
      await this.#write('WEB HELLO'); await hello; checkSession();
      await this.#request('LEASE 5000'); checkSession(); this.#lastLease = Date.now();
      await this.#request('STREAM 500'); checkSession(); await this.#request('SNAPSHOT'); checkSession();
      this.#state('connected','USB UART · 115200 baud · 5 s link timeout');
      this.#heartbeat = setInterval(() => {
        if (Date.now()-this.#lastReceived > 2500) {
          clearInterval(this.#heartbeat);
          this.#emit('error',{message:'Telemetry is stale. Heartbeat stopped; the board lease will turn output OFF.'});
          void this.command('OFF').catch(() => {}); return;
        }
        if (![...this.#pending.values()].some(p => p.command === 'PING')) void this.#request('PING').then(() => { this.#lastLease = Date.now(); }).catch(error => this.#emit('error',{message:error.message}));
      },1000);
    } catch (error) {
      if (connectionEpoch === this.#connection) { await this.#close(); this.#state('disconnected',error.message); }
      else if (port) { try { await port.close(); } catch {} }
      throw error;
    }
  }
  async #write(text) {
    const port = this.#port; const connection = this.#connection;
    const run = this.#writeTail.catch(() => {}).then(async () => {
      if (port !== this.#port || connection !== this.#connection || !port?.writable) throw new Error('USB serial port is closed or command canceled.');
      const writer = port.writable.getWriter();
      try { await writer.write(new TextEncoder().encode(text+'\n')); this.#line('tx',text); }
      finally { writer.releaseLock(); }
    });
    this.#writeTail = run; return run;
  }
  #request(command) {
    const id = String(++this.#counter);
    return new Promise((resolve,reject) => {
      const timer = setTimeout(() => { const pending = this.#pending.get(id); this.#pending.delete(id); reject(new Error(`${pending?.ack ? 'No verified timing readback' : 'No acknowledgment'} for ${command}. Board state is unconfirmed.`)); },2200);
      this.#pending.set(id,{command,resolve,reject,timer,timingRequired:command.startsWith('TIMING ')});
      void this.#write(`WEB ${id} ${command}`).catch(error => { const p = this.#pending.get(id); if (p) { clearTimeout(timer); this.#pending.delete(id); reject(error); } });
    });
  }
  #settlePending(id, pending) {
    if (!pending.ack || (pending.timingRequired && !pending.timing)) return;
    clearTimeout(pending.timer); this.#pending.delete(id);
    pending.resolve(pending.timingRequired ? {...pending.ack,timing:pending.timing} : pending.ack);
  }
  async #readLoop(reader,epoch) {
    const decoder = new TextDecoder(); const framer = new LineFramer(line => this.#receive(line));
    try {
      while (true) { const {value,done} = await reader.read(); if (done) break; if (epoch === this.#connection) framer.push(decoder.decode(value,{stream:true})); }
    } catch (error) { if (!this.#closing) this.#emit('error',{message:`USB disconnected: ${error.message}`}); }
    finally {
      reader.releaseLock(); if (this.#reader === reader) this.#reader = null;
      if (!this.#closing && epoch === this.#connection) {
        clearInterval(this.#heartbeat); this.#rejectAll(new Error('USB connection lost.'));
        this.#state('disconnecting','USB lost; closing port.');
        void this.#close().then(() => this.#state('disconnected','USB lost; firmware lease expires within 5 s.'));
      }
    }
  }
  #receive(line) {
    this.#line('rx',line); const frame = parseFrame(line); if (!frame) return;
    if (frame.type === 'hello') { this.hello = frame; this.#helloWait?.resolve(frame); this.#emit('hello',frame); }
    if (frame.type === 'telemetry') {
      // Only a successfully negotiated device may publish measurements.
      if (!this.hello) return;
      this.#lastReceived = Date.now(); this.lastSample = {...frame,receivedAt:new Date().toISOString()}; this.#emit('sample',this.lastSample);
    }
    if (frame.type === 'timing') {
      if (!this.supportsCarrierTiming) return;
      this.#publishTiming(frame.timing);
      const pending = this.#pending.get(frame.id);
      if (pending?.timingRequired) {
        const [,hz,deadNs] = pending.command.split(' ');
        if (frame.timing.requested_hz !== Number(hz) || frame.timing.requested_dead_ns !== Number(deadNs) || frame.timing.enabled || frame.timing.busy) {
          clearTimeout(pending.timer); this.#pending.delete(frame.id);
          pending.reject(new Error(`${pending.command}: timing readback does not confirm the requested OFF-state pair. Board state is unconfirmed.`));
        } else { pending.timing = this.lastTiming; this.#settlePending(frame.id,pending); }
      }
    }
    if (frame.type === 'ack') {
      const pending = this.#pending.get(frame.id); if (!pending) return;
      if (frame.ok) { pending.ack = frame; this.#settlePending(frame.id,pending); }
      else { clearTimeout(pending.timer); this.#pending.delete(frame.id); pending.reject(new Error(`${pending.command}: ${frame.code || frame.error || 'rejected by board'}`)); }
    }
    if (frame.type === 'event') this.#line('info',frame.code || frame.message || JSON.stringify(frame));
  }
  get supportsBenchSettings() { return Array.isArray(this.hello?.capabilities) && this.hello.capabilities.includes('bench_settings_v1'); }
  get supportsCalibration() { return Array.isArray(this.hello?.capabilities) && this.hello.capabilities.includes('calibration_v1'); }
  get supportsCarrierTiming() { return Array.isArray(this.hello?.capabilities) && this.hello.capabilities.includes('carrier_timing_v1'); }
  #publishTiming(timing, source='device') {
    this.#lastTimingReceived = Date.now(); this.lastTiming = {...timing,receivedAt:new Date().toISOString(),source};
    if (!timing.enabled && !timing.busy && this.#pendingOn === 0) this.#timingNeedsOffReadback = false;
    this.#emit('timing',this.lastTiming);
  }
  #validateTiming(command) {
    if (!this.supportsCarrierTiming) throw new Error('Carrier timing requires V2 firmware with carrier_timing_v1 support.');
    if (!this.isReady) throw new Error('Wait for fresh telemetry and a confirmed link lease before changing carrier timing.');
    if (!validCarrierTiming(this.lastTiming) || Date.now()-this.#lastTimingReceived >= 2500) throw new Error('Wait for fresh, verified carrier timing readback.');
    if (this.lastSample?.enabled !== false || this.lastTiming.enabled) throw new Error('Turn output OFF before changing carrier timing.');
    if ([1,2].includes(this.lastSample?.calibration?.state) || this.lastTiming.busy) throw new Error('Calibration or a device operation is active. Use Stop / Output OFF before changing carrier timing.');
    if (this.#timingNeedsOffReadback || this.#pendingOn) throw new Error('Wait for a new output OFF timing readback after the ON request.');
    const parts = command.split(' ');
    if (parts.length !== 3 || !parts.slice(1).every(raw => /^\d+$/.test(raw) && Number.isSafeInteger(Number(raw)))) throw new Error('Use TIMING followed by whole-number frequency in Hz and deadtime in ns.');
    const hz = Number(parts[1]), deadNs = Number(parts[2]);
    if (hz < carrierTimingLimits.min_hz || hz > carrierTimingLimits.max_hz || deadNs < carrierTimingLimits.min_dead_ns || deadNs > carrierTimingLimits.max_dead_ns)
      throw new Error('Carrier frequency must be 500000–2000000 Hz and deadtime 20–200 ns, in whole numbers.');
    const target = quantizedCarrierTiming(hz,deadNs,this.lastTiming.timer_hz);
    if (target.dead_ticks < 1 || target.dead_ticks > 127 || target.dead_ticks * 4 >= target.period_ticks) throw new Error('This frequency and deadtime pair leaves too little switching time. Reduce frequency or deadtime.');
  }
  command(text) {
    let command; try { command = validateCommand(text); } catch(error) { return Promise.reject(error); }
    if (!['connected','demo'].includes(this.state)) return Promise.reject(new Error('Connect a board or start Demo first.'));
    const changingTiming = /^TIMING(?: |$)/.test(command);
    if (changingTiming) { try { this.#validateTiming(command); } catch(error) { return Promise.reject(error); } }
    if (command === 'ON') this.#timingNeedsOffReadback = true;
    const epoch = command === 'OFF' ? ++this.#epoch : this.#epoch;
    const run = async () => {
      if (epoch !== this.#epoch) throw new Error('Command canceled by output OFF or disconnect.');
      if (command !== 'OFF' && !this.isReady) throw new Error('Wait for fresh telemetry and a confirmed link lease. Reconnect if the link timed out.');
      if (changingTiming) this.#validateTiming(command);
      const calibrating = [1,2].includes(this.lastSample?.calibration?.state);
      if (calibrating && !['OFF','PING','SNAPSHOT'].includes(command)) throw new Error('Calibration is active. Use Stop / Output OFF before other commands.');
      if (command.startsWith('CAL ')) {
        if (!this.supportsCalibration || this.state === 'demo') throw new Error('Hardware auto-calibration requires firmware PWR-2.0.2 with calibration_v1 support. Demo cannot calibrate hardware.');
        if (!this.lastSample?.calibration) throw new Error('Wait for verified calibration-state telemetry.');
        if (!/^CAL (PRECHARGE|NOLOAD|ZERO|LINE|LOAD [1-3])$/.test(command)) throw new Error('Choose a supported calibration and load slot 1–3.');
        if (this.lastSample?.enabled || faultActive(this.lastSample?.fault)) throw new Error('Turn output OFF and resolve the reported fault before calibration.');
      }
      const parts = command.split(' ');
      const key = parts[0] === 'SET' ? parts[1] : null;
      if (key === 'ACTLOAD') throw new Error('ACTLOAD is read-only. Use LOAD 1, LOAD 2 or LOAD 3 to select a reference.');
      const slotAlias = key === 'ACTIVELOAD' || key === 'LOADSLOT';
      const selectingLoad = /^LOAD(?: |$)/.test(command);
      if (selectingLoad || slotAlias || Object.hasOwn(benchSettings, key ?? '')) {
        if (!this.supportsBenchSettings) throw new Error('Load and tuning settings require firmware with bench_settings_v1 support.');
        if (this.lastSample?.enabled) throw new Error('Turn output OFF before changing load or tuning settings.');
        if (selectingLoad || slotAlias) {
          const raw = selectingLoad ? parts[1] : parts[2];
          if (parts.length !== (selectingLoad ? 2 : 3)) throw new Error('Choose LOAD 1, LOAD 2 or LOAD 3.');
          if (selectingLoad && !/^[1-3]$/.test(raw ?? '')) throw new Error('Choose LOAD 1, LOAD 2 or LOAD 3.');
          const slot = benchNumber(raw, 'Load slot', {min:1,max:3,step:1});
          if (!Number.isInteger(this.lastSample?.settings?.ACTLOAD) || this.lastSample.settings.ACTLOAD < 1 || this.lastSample.settings.ACTLOAD > 3 ||
              !Number.isFinite(this.lastSample.settings[`LOAD${slot}`])) throw new Error('Wait for verified load-reference readback before selecting a slot.');
        } else {
          if (parts.length !== 3) throw new Error(`Use SET ${key} followed by one numeric value.`);
          benchNumber(parts[2], key, benchSettings[key]);
          if (!Number.isFinite(this.lastSample?.settings?.[key])) throw new Error(`Wait for verified ${key} readback before editing this setting.`);
        }
      }
      if (command === 'ON' && faultActive(this.lastSample?.fault)) throw new Error('Clear the reported fault while output is OFF before enabling.');
      if (this.state === 'demo') return this.#demoCommand(command);
      if (this.state !== 'connected') throw new Error('Device is disconnected.');
      const ack = await this.#request(command);
      if (command !== 'SNAPSHOT' && command !== 'PING') void this.#request('SNAPSHOT').catch(() => {});
      return ack;
    };
    if (command === 'OFF') return run();
    if (this.#queued >= 16) return Promise.reject(new Error('Too many pending commands. Wait for the board.'));
    if (command === 'ON') this.#pendingOn++;
    this.#queued++; const result = this.#tail.catch(() => {}).then(run).finally(() => { this.#queued--; if (command === 'ON') this.#pendingOn--; }); this.#tail = result; return result;
  }
  #rejectAll(error) { this.#helloWait?.reject(error); for (const p of this.#pending.values()) { clearTimeout(p.timer); p.reject(error); } this.#pending.clear(); }
  async #close() {
    this.#closing = true; clearInterval(this.#heartbeat); this.#epoch++; this.#connection++; this.#rejectAll(new Error('Device disconnected.'));
    if (this.#reader) { try { await this.#reader.cancel(); } catch {} }
    if (this.#port) { try { await this.#port.close(); } catch {} }
    this.#port = null; this.hello = null; this.lastSample = null; this.lastTiming = null; this.#lastReceived = 0; this.#lastTimingReceived = 0; this.#timingNeedsOffReadback = true;
  }
  async disconnect() {
    if (this.state === 'demo') { this.stopDemo(); return; }
    const wasConnected = this.state === 'connected';
    // Invalidate queued work before any await so ON cannot race the final OFF.
    this.#closing = true; this.#epoch++; clearInterval(this.#heartbeat);
    this.#state('disconnecting','Stopping output and closing USB.');
    if (wasConnected) { try { await this.#request('OFF'); await this.#request('STREAM 0'); } catch(error) { this.#line('error',error.message); } }
    await this.#close(); this.#state('disconnected','Disconnected.');
  }
  abandon() { clearInterval(this.#heartbeat); clearInterval(this.#demoTimer); if (this.state === 'connected') void this.#write('WEB 0 OFF').catch(() => {}); }
  startDemo() {
    if (this.state !== 'disconnected') throw new Error('Disconnect USB before starting Demo.');
    this.#epoch++; this.#demo = {start:Date.now(),enabled:false,mode:'VSBONLY',vsec:0,pending:false,timing:{...quantizedCarrierTiming(1000000,40),revision:0},settings:{VSET:28,VON:28,VMAX:32,OVP:36,DMAX:100,OD:10,FEN:10000,LOAD1:50,LOAD2:5,LOAD3:2.5,ACTLOAD:1,NLDUTY:25,AUTOMAX:100,AUTOSTEP:2,AUTOFINE:0.5,AUTOSETTLE:160,AUTOMEAS:100,PREMS:3,PRESETTLE:80,PREMAX:4}};
    this.hello = {type:'hello',protocol:1,fw:'SIMULATED',board:'Demo V2 · no hardware',baud:115200,capabilities:['bench_settings_v1','carrier_timing_v1']}; this.#emit('hello',this.hello);
    this.#state('demo','Synthetic data · no hardware commands'); this.#tickDemo(); this.#demoTimer = setInterval(() => this.#tickDemo(),500);
  }
  stopDemo() { clearInterval(this.#demoTimer); this.#epoch++; this.#demo = null; this.hello = null; this.lastSample = null; this.lastTiming = null; this.#lastTimingReceived = 0; this.#timingNeedsOffReadback = true; this.#state('disconnected','Demo stopped.'); }
  #tickDemo() {
    const d = this.#demo; if (!d) return; const ms = Date.now()-d.start;
    const demand = d.enabled ? (d.mode === 'OPEN' ? d.settings.VSET*d.settings.OD/100 : d.settings.VSET) : 0;
    d.vsec += (demand-d.vsec)*0.45;
    const vsec = Math.max(0,d.vsec+(d.enabled ? Math.sin(ms/850)*0.16 : 0)); const current = d.enabled ? 0.32+0.025*Math.sin(ms/1700) : 0;
    this.lastSample = {type:'telemetry',protocol:1,ms,enabled:d.enabled,mode:d.mode,fault:'NONE',vpri:325+2*Math.sin(ms/2200),vsec,current,power:vsec*current,duty:d.enabled ? Math.min(d.settings.DMAX,d.mode === 'OPEN' ? d.settings.OD : 52+3*Math.sin(ms/2100)) : 0,adc:[2670,Math.round(vsec/40*4095),Math.round(current*1000)],settings:{...d.settings},settings_pending:d.pending,lease_ms:5000,stream_ms:500,receivedAt:new Date().toISOString(),source:'demo'};
    this.#emit('sample',this.lastSample);
    this.#publishTiming({...d.timing,enabled:d.enabled,busy:d.enabled},'demo');
  }
  #demoCommand(command) {
    const d = this.#demo; this.#line('tx',`[DEMO] ${command}`);
    if (command === 'ON') d.enabled = true;
    else if (command === 'OFF') d.enabled = false;
    else if (['OPEN','VSBONLY','LINEFF','VSB'].includes(command)) { d.mode = command; d.pending = true; }
    else if (command === 'SAVE' || command === 'ENDCFG') { if (d.enabled) throw new Error('SAVE: turn_off_first'); d.pending = false; }
    else if (/^LOAD [1-3]$/.test(command)) { d.settings.ACTLOAD = Number(command.split(' ')[1]); d.pending = true; }
    else if (command.startsWith('TIMING ')) { const [,hz,deadNs] = command.split(' '); d.timing = {...quantizedCarrierTiming(Number(hz),Number(deadNs)),revision:(d.timing.revision + 1) >>> 0}; d.pending = true; }
    else if (command.startsWith('SET ')) {
      const [,key,raw,...extra] = command.split(' '); const value = Number(raw);
      const limits = {VSET:[0,80],VON:[0,80],VMAX:[0,80],OVP:[0,80],DMAX:[0,100],OD:[0,100],FEN:[1000,50000]};
      if (Object.hasOwn(benchSettings,key)) {
        // Validated in command() against the same device-facing range/step contract.
        d.settings[key] = key === 'AUTOMAX' ? Math.min(value,d.settings.DMAX) : value;
      } else if (['ACTIVELOAD','LOADSLOT'].includes(key)) d.settings.ACTLOAD=value;
      else {
        if (!limits[key] || raw === undefined || extra.length || !Number.isFinite(value) || value<limits[key][0] || value>limits[key][1]) throw new Error('Demo: invalid setting or value.');
        d.settings[key] = value;
        if (key === 'DMAX') d.settings.AUTOMAX = Math.min(d.settings.AUTOMAX,value);
      }
      d.pending = true;
    } else if (!['CLR','SAVE','SNAPSHOT','PING','BEGINCFG','ENDCFG'].includes(command)) throw new Error('Unsupported web command. Use the firmware terminal for legacy calibration commands.');
    this.#tickDemo(); return {type:'ack',id:String(++this.#counter),ok:true,code:'DEMO'};
  }
}
