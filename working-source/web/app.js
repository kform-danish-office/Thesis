import { DeviceLink } from './serial.js';
import { validCarrierTiming } from './protocol.js';
import { openStore, saveSession, listSessions, getSession, deleteSession, toCSV, download } from './storage.js';

const $ = (id) => document.getElementById(id);
const link = new DeviceLink();
const keys = [...document.querySelectorAll('#settings-form input[name]')].map((input) => input.name);
const benchKeys = new Set(['LOAD1','LOAD2','LOAD3','NLDUTY','AUTOMAX','AUTOSTEP','AUTOFINE','AUTOSETTLE','AUTOMEAS','PREMS','PRESETTLE','PREMAX']);
const dirty = new Set();
const history = [];
const terminalLines = [];
const unsaved = new Map();
let latest = null;
let lastReceived = 0;
let previousReceived = 0;
let intervalEstimate = 0;
let hello = null;
let chartKind = 'voltage';
let modeDirty = false;
let loadProfileDirty = false;
let timingDirty = false;
let latestTiming = null;
let timingPendingSave = false;
let timingAwaitOff = false;
let recordedTimingKey = null;
let commandCount = 0;
let applyGeneration = 0;
let recording = null;
let lastRecording = null;
let sessions = [];
let chartQueued = false;
let source = null;
let lastStale = false;
let terminalDirty = false;
let checkpointPromise = null;
let checkpointFailed = false;
const canvas = $('live-chart');
const ctx = canvas.getContext('2d');

const isLive = () => link.state === 'connected' || link.state === 'demo';
const isFresh = () => !!latest && performance.now() - lastReceived < 3000;
const isReady = () => isLive() && !!link.isReady && isFresh();
const faultActive = (fault) => ![null, undefined, false, 0, '', '0', 'NONE', 'none', 'OK', 'ok', 'CLEAR', 'clear'].includes(fault);
const fmt = (value, places = 1) => value !== null && value !== undefined && Number.isFinite(Number(value)) ? Number(value).toFixed(places) : '—';
const duration = (ms) => {
  const total = Math.max(0, Math.floor(ms / 1000));
  return [Math.floor(total / 3600), Math.floor(total / 60) % 60, total % 60].map(value => String(value).padStart(2, '0')).join(':');
};
const actualMode = (value) => String(value || '').toUpperCase();
const modeCommand = (value) => ({ VSB: 'VSBONLY', 'VSB+VIN': 'LINEFF', VINFF: 'LINEFF' }[actualMode(value)] || actualMode(value));
const clone = (value) => JSON.parse(JSON.stringify(value));
const otherDrafts = () => dirty.size > 0 || modeDirty || loadProfileDirty;
const anyDrafts = () => otherDrafts() || timingDirty;
const settingsPending = () => !!latest?.settings_pending || timingPendingSave;
const timingFresh = () => {
  const age = Date.now() - Date.parse(latestTiming?.receivedAt);
  return isLive() && link.supportsCarrierTiming && validCarrierTiming(latestTiming) && age >= 0 && age < 2500;
};
const timingSnapshot = () => timingFresh() ? clone(latestTiming) : null;
const integer = (value) => Number.isFinite(value) ? new Intl.NumberFormat().format(value) : '—';

function notify(message, success = false) {
  $('alert-text').textContent = String(message);
  $('app-alert').classList.toggle('success', success);
  $('app-alert').hidden = false;
}

function feedback(message, type = '') {
  $('command-feedback').textContent = /^(Waiting for verified telemetry|Opening connection)/.test(message) ? '' : message;
  $('command-feedback').className = `command-feedback ${type}`;
}

function announce(message) {
  if ($('workspace-status').textContent !== message) $('workspace-status').textContent = message;
}

function clearLiveData() {
  $('calibration-confirm').checked = false;
  loadProfileDirty = false;
  timingDirty = false;
  latestTiming = null;
  timingPendingSave = false;
  timingAwaitOff = false;
  recordedTimingKey = null;
  $('timing-frequency').value = '';
  $('timing-deadtime').value = '';
  latest = null;
  lastReceived = 0;
  previousReceived = 0;
  intervalEstimate = 0;
  hello = null;
  $('firmware-label').textContent = 'Awaiting firmware identification';
  history.length = 0;
  dirty.clear();
  modeDirty = false;
  keys.forEach((key) => { $('setting-' + key).value = ''; $('setting-' + key).closest('label').classList.remove('dirty'); });
  $('mode-select').value = '';
  renderLive();
  queueChart();
}

function renderState(message = '') {
  const state = link.state;
  const live = isLive();
  const demo = state === 'demo';
  $('demo-banner').hidden = !demo;
  canvas.setAttribute('aria-label', `${chartKind === 'duty' ? 'Applied duty' : 'Primary and secondary voltage'} over the last sixty seconds${demo ? ', synthetic demo data' : ''}`);
  $('connection-dot').className = `status-dot ${demo ? 'demo' : state === 'connected' ? 'live' : ''}`;
  $('side-dot').className = $('connection-dot').className;
  $('side-state').replaceChildren(document.createTextNode(demo ? 'SIMULATOR' : state === 'connected' ? 'USB CONNECTED' : state === 'connecting' ? 'CONNECTING' : state === 'disconnecting' ? 'DISCONNECTING' : 'DISCONNECTED'));
  const sideSmall = document.createElement('small');
  sideSmall.textContent = demo ? 'Synthetic data' : '115200 · 8N1';
  $('side-state').append(sideSmall);
  $('connection-label').textContent = demo ? 'Demo · synthetic data' : state === 'connected' ? 'USB connected' : state === 'connecting' ? 'Opening serial port…' : state === 'disconnecting' ? 'Disabling output and closing port…' : 'No USB connection';
  $('connection-detail').textContent = message || (demo ? 'Controls affect the simulator only.' : state === 'connected' ? 'Waiting for verified firmware telemetry.' : state === 'connecting' ? 'Choose your adapter in the browser connection dialog.' : 'Connect your USB-UART adapter to begin.');
  $('connect-button').replaceChildren();
  const connectText = document.createElement('span');
  connectText.textContent = state === 'connected' ? 'Disconnect' : state === 'connecting' ? 'Connecting…' : state === 'disconnecting' ? 'Disconnecting…' : 'Connect USB';
  $('connect-button').append(connectText);
  $('connect-button').disabled = state === 'connecting' || state === 'disconnecting';
  $('demo-button').textContent = demo ? 'Exit demo' : 'Start demo';
  $('demo-button').disabled = state === 'connecting' || state === 'disconnecting';
  if (!live) feedback(state === 'connecting' ? 'Opening connection. Output is not enabled automatically.' : 'Waiting for verified telemetry.');
  announce($('connection-label').textContent);
  renderLive();
}

function setHello(detail) {
  hello = clone(detail);
  const firmware = hello.firmware || hello.version || hello.fw || 'Verified firmware';
  $('firmware-label').textContent = `${firmware}${hello.board ? ` · ${hello.board}` : ''}`;
}

const calibrationActive = () => isLive() && [1,2].includes(latest?.calibration?.state);
const calibrationInstructions = {
  NOLOAD: 'Prepare the no-load condition for your bench. Tunes the no-load soft-switch cap at the existing EN frequency; the converter is energized during this routine.',
  PRECHARGE: 'Prepare the startup condition for your bench. Tests precharge bursts using the configured limits; the converter is energized during this routine.',
  LOAD: 'Connect the physical reference load for the selected slot. Tunes one slot at a time and energizes the converter. After it stops, change loads only with output OFF.',
  ZERO: 'Remove current from the sensed path before zeroing. Output must be OFF; this records the PA2 current-sensor offset, not a gain calibration.',
  LINE: 'Provide the intended primary-voltage reference with output OFF. Captures the present PA0 voltage as LFFREF and enables line feed-forward.',
};
function updateCalibrationControls() {
  const supported = link.state === 'connected' && link.supportsCalibration;
  const c = latest?.calibration;
  const active = calibrationActive();
  const kind = $('calibration-kind').value;
  $('calibration-slot-row').hidden = kind !== 'LOAD';
  $('calibration-instructions').textContent = calibrationInstructions[kind];
  const resistance = latest?.settings?.[`LOAD${$('calibration-slot').value}`];
  for (const option of $('calibration-slot').options) {
    const r = latest?.settings?.[`LOAD${option.value}`];
    const label = `Load slot ${option.value}${Number.isFinite(r) ? r > 0 ? ` · ${r} Ω reference` : ' · unconfigured' : ''}`;
    if (option.textContent !== label) option.textContent = label;
  }
  if (kind === 'LOAD' && Number.isFinite(resistance) && resistance > 0) $('calibration-instructions').textContent = `Connect the physical ${resistance} Ω reference load for slot ${$('calibration-slot').value}. The routine energizes the converter. Switch loads only with output OFF.`;
  $('calibration-confirm-label').textContent = ['ZERO','LINE'].includes(kind)
    ? 'I have prepared the correct zero-current or primary-voltage reference, with output OFF.'
    : 'I have prepared the correct load and reference; this routine may energize the converter.';
  $('calibration-capability').textContent = supported ? 'FIRMWARE SUPPORTED' : isLive() ? 'UPGRADE / BOARD REQUIRED' : 'BOARD REQUIRED';
  $('calibration-start').disabled = !supported || !c || !isReady() || commandCount > 0 || active || anyDrafts() || !!latest?.enabled || faultActive(latest?.fault) || !$('calibration-confirm').checked;
  $('calibration-stop').disabled = !isLive();
  $('calibration-kind').disabled = active || commandCount > 0;
  $('calibration-slot').disabled = active || commandCount > 0;
  $('calibration-confirm').disabled = active;
  $('calibration-save').disabled = !supported || !isReady() || active || commandCount > 0 || anyDrafts() || !!latest?.enabled || !settingsPending();
  const states = ['Ready. Prepare the reference and confirm before starting.', 'Calibration queued. Waiting for the device to start.', 'Calibration running. Stop / output OFF remains available.', 'Calibration complete. Output OFF; results are in RAM until saved.', 'Calibration stopped. Output OFF; the interrupted result was discarded.', 'Calibration failed. Output OFF; previous settings restored. Check the bench conditions and reported faults.'];
  let status = !supported ? link.state === 'demo' ? 'Demo cannot calibrate physical hardware. Connect a compatible board.' : isLive() ? 'Firmware upgrade required for calibration: compatible PWR-2.0.2 or newer.' : 'Connect a compatible board to calibrate hardware.' : !isFresh() ? 'Telemetry is stale; calibration state is unconfirmed. Use Stop / output OFF.' : states[c?.state ?? 0];
  if (supported && isFresh() && !c) status = 'Waiting for verified calibration-state telemetry.';
  if (supported && c?.state === 3 && !settingsPending()) status = 'Calibration complete. Output OFF; device settings saved.';
  if (supported && !active && anyDrafts()) status = 'Apply or reset your settings, timing, mode, and slot edits before starting calibration.';
  if (supported && kind === 'LOAD' && link.supportsBenchSettings && !(resistance > 0) && !active) { $('calibration-start').disabled = true; status = 'Set a positive reference resistance in Setup before calibrating this slot.'; }
  if (supported && !active && latest?.enabled) status = 'Turn output OFF before starting calibration.';
  if ($('calibration-status').textContent !== status) $('calibration-status').textContent = status;
  if (active) { $('calibration-confirm').checked = false; $('calibration-progress').removeAttribute('value'); }
  else $('calibration-progress').value = c?.state === 3 ? 1 : 0;
  $('calibration-limits').textContent = latest?.settings ? `Uses device settings: VSET ${fmt(latest.settings.VSET)} V; ceiling ${fmt(latest.settings.VMAX)} V; OVP ${fmt(latest.settings.OVP)} V; EN frequency ${fmt(latest.settings.FEN,0)} Hz.` : 'Calibration uses the device settings, not unsubmitted form edits.';
  $('calibration-duty').textContent = supported && c ? `${fmt(c.duty)} %` : '—';
  $('calibration-result-label').textContent = c?.kind === 3 ? 'Current-sensor zero offset' : c?.kind === 4 ? 'Primary line reference' : 'No-load cap / precharge duty';
  $('calibration-result').textContent = supported && c ? c.kind === 3 ? `${fmt(c.offset,3)} V` : c.kind === 4 ? `${fmt(c.line_ref)} V` : `${fmt(c.nlduty)} % / ${fmt(c.preduty)} %` : '—';
}
$('calibration-kind').addEventListener('change', () => { $('calibration-confirm').checked = false; updateControls(); });
$('calibration-slot').addEventListener('change', () => { $('calibration-confirm').checked = false; updateControls(); });
$('calibration-confirm').addEventListener('change', updateControls);
$('calibration-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  if ($('calibration-start').disabled) return;
  const kind = $('calibration-kind').value;
  const command = `CAL ${kind === 'LOAD' ? `LOAD ${$('calibration-slot').value}` : kind}`;
  $('calibration-confirm').checked = false;
  try { await runCommand(command, 'Calibration start'); } catch { /* Board rejection already reported. */ }
});
$('calibration-stop').addEventListener('click', async () => { applyGeneration += 1; try { await runCommand('OFF', 'Stop calibration'); } catch {} });
$('calibration-save').addEventListener('click', async () => { try { await runCommand('SAVE', 'Save device settings'); } catch {} });

function updateBenchControls() {
  const supported = link.supportsBenchSettings;
  const activeSlot = latest?.settings?.ACTLOAD;
  const readback = Number.isInteger(activeSlot) && activeSlot >= 1 && activeSlot <= 3;
  const available = isReady() && supported && readback;
  const locked = !!latest?.enabled || calibrationActive() || commandCount > 0;
  $('load-profile').disabled = !available || locked;
  if (!loadProfileDirty && readback && $('load-profile').value !== String(activeSlot)) $('load-profile').value = String(activeSlot);
  for (const option of $('load-profile').options) {
    const r = latest?.settings?.[`LOAD${option.value}`];
    const label = `Slot ${option.value}${Number.isFinite(r) ? r > 0 ? ` · ${r} Ω` : ' · unconfigured' : ''}`;
    if (option.textContent !== label) option.textContent = label;
  }
  $('apply-load-profile').disabled = !available || locked || !loadProfileDirty || dirty.size > 0 || modeDirty || timingDirty;
  const r = latest?.settings?.[`LOAD${activeSlot}`];
  $('active-load-summary').textContent = readback ? `Device reference slot: ${activeSlot}${Number.isFinite(r) ? r > 0 ? ` · ${r} Ω configured` : ' · resistance unconfigured' : ''}.` : 'Waiting for load-reference readback.';
  $('bench-settings-status').textContent = !isLive() ? 'Connect compatible firmware or start Demo to explore these settings.' : !supported ? 'This firmware does not report load/tuning settings. Install compatible PWR-2.0.3 firmware. Existing voltage controls remain available.' : calibrationActive() ? 'Calibration is running. Load and tuning edits are locked.' : latest?.enabled ? 'Turn output OFF to edit load references and tuning settings.' : link.state === 'demo' ? 'Synthetic demo settings only. No physical load is changed.' : 'Extended settings are reported by the device. Apply changes in RAM, then save explicitly.';
}
$('load-profile').addEventListener('change', () => { loadProfileDirty = Number($('load-profile').value) !== latest?.settings?.ACTLOAD; updateControls(); });
$('apply-load-profile').addEventListener('click', async () => {
  if ($('apply-load-profile').disabled) return;
  try { await runCommand(`LOAD ${$('load-profile').value}`, 'Select reference slot'); loadProfileDirty = false; renderLive(); } catch {}
});
$('workspace-record-stop').addEventListener('click', async () => { if (recording) await stopRecording(); });

function timingDraft() {
  const hz = Number($('timing-frequency').value);
  const ns = Number($('timing-deadtime').value);
  if (!$('timing-frequency').value || !Number.isSafeInteger(hz) || hz < 500000 || hz > 2000000)
    return {error:'Enter a whole-number carrier frequency from 500,000 to 2,000,000 Hz.', field:'timing-frequency'};
  if (!$('timing-deadtime').value || !Number.isSafeInteger(ns) || ns < 20 || ns > 200)
    return {error:'Enter a whole-number deadtime from 20 to 200 ns.', field:'timing-deadtime'};
  if (!validCarrierTiming(latestTiming)) return {error:'Wait for verified timer readback before applying timing.'};
  const period = 2 * Math.floor((latestTiming.timer_hz + hz) / (2 * hz));
  const dead = Math.ceil(ns * latestTiming.timer_hz / 1e9);
  if (dead * 4 >= period) return {error:'This pair leaves too little switching time. Reduce the carrier frequency or deadtime.', field:'timing-deadtime'};
  return {hz, ns, period, dead, actualHz:Math.floor((latestTiming.timer_hz + period / 2) / period), actualNs:Math.ceil(dead * 1e9 / latestTiming.timer_hz)};
}

function updateTimingControls() {
  const supported = isLive() && link.supportsCarrierTiming;
  const verified = supported && validCarrierTiming(latestTiming);
  const fresh = timingFresh();
  const busy = commandCount > 0 || calibrationActive() || latestTiming?.busy;
  const off = latest?.enabled === false && latestTiming?.enabled === false;
  const editable = supported && fresh && isReady() && off && !timingAwaitOff && !busy && !faultActive(latest?.fault);
  if (verified && !timingDirty) {
    $('timing-frequency').value = latestTiming.requested_hz;
    $('timing-deadtime').value = latestTiming.requested_dead_ns;
  }
  for (const id of ['timing-frequency','timing-deadtime']) {
    $(id).disabled = !editable;
    $(id).closest('label').classList.toggle('dirty', timingDirty);
  }
  const draft = timingDirty ? timingDraft() : null;
  $('apply-timing').disabled = !editable || !timingDirty || otherDrafts() || !!draft?.error;
  $('reset-timing').disabled = commandCount > 0 || !timingDirty;
  $('timing-summary-status').textContent = !supported ? 'V2 / F410 only' : !verified ? 'Waiting for readback' : !fresh ? 'Readback stale' : timingDirty ? 'Edits not applied' : link.state === 'demo' ? 'Synthetic' : 'Verified readback';
  let status = !isLive() ? 'Connect V2 / STM32F410 with compatible PWR-2.0.4 or newer firmware.'
    : !supported ? 'Unavailable on this board or firmware. V2 / STM32F410 requires compatible PWR-2.0.4 or newer firmware; G071 timing remains fixed.'
    : !verified ? 'Waiting for verified carrier timing readback. Controls remain locked.'
    : !fresh ? 'Carrier timing readback is stale. Wait for a fresh timing frame before editing or applying.'
    : !isReady() ? 'Wait for fresh telemetry and a confirmed device link before changing timing.'
    : commandCount > 0 ? 'A command is in progress. Wait for its acknowledgment and verified timing readback.'
    : busy ? 'Calibration or startup is active. Use Stop / output OFF and wait for idle timing readback.'
    : !off ? 'Turn output OFF and wait for verified OFF timing readback before editing.'
    : timingAwaitOff ? 'Wait for a new verified OFF timing readback after the output ON request.'
    : faultActive(latest?.fault) ? 'Clear the reported fault with output OFF before changing timing.'
    : otherDrafts() ? 'Apply or reset other settings, mode, and slot edits before editing timing. Reset timing edits first if both forms have edits.'
    : draft?.error || (timingDirty ? 'Timing edits are not applied. Apply both values together with output OFF.'
      : link.state === 'demo' ? 'Synthetic V2 timing only. Demo cannot calibrate physical hardware.' : 'Timing is verified. Changes apply in RAM with output OFF; save explicitly to retain them.');
  if ($('timing-status').textContent !== status) $('timing-status').textContent = status;
  $('timing-preview').hidden = !timingDirty || !!draft?.error;
  if (timingDirty && !draft.error) $('timing-preview').textContent = `Draft timer result: ${integer(draft.actualHz)} Hz · ${integer(draft.actualNs)} ns · ${draft.period} period ticks / ${draft.dead} deadtime ticks. This is a preview; actual values below require device readback.`;
  $('timing-actual-frequency').textContent = verified ? `${integer(latestTiming.actual_hz)} Hz` : '—';
  $('timing-actual-deadtime').textContent = verified ? `${integer(latestTiming.actual_dead_ns)} ns` : '—';
  $('timing-ticks').textContent = verified ? `${latestTiming.period_ticks} period / ${latestTiming.dead_ticks} deadtime` : '—';
  $('timing-timer').textContent = verified ? `${integer(latestTiming.timer_hz)} Hz · ${fmt(1e9 / latestTiming.timer_hz, 1)} ns per tick` : '—';
  $('timing-readback-state').textContent = !verified ? 'No verified timer readback.' : `${fresh ? 'Fresh' : 'Last reported; stale'} ${link.state === 'demo' ? 'synthetic' : 'device'} readback · revision ${latestTiming.revision} · requested ${integer(latestTiming.requested_hz)} Hz / ${integer(latestTiming.requested_dead_ns)} ns.`;
  $('timing-readback').classList.toggle('readings-stale', verified && !fresh);
}

for (const id of ['timing-frequency','timing-deadtime']) $(id).addEventListener('input', () => {
  timingDirty = !latestTiming || Number($('timing-frequency').value) !== latestTiming.requested_hz || Number($('timing-deadtime').value) !== latestTiming.requested_dead_ns;
  updateControls();
});
$('reset-timing').addEventListener('click', () => { timingDirty = false; updateControls(); });
$('timing-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  if ($('apply-timing').disabled) return;
  const draft = timingDraft();
  if (draft.error) { notify(draft.error); if (draft.field) $(draft.field).focus(); return; }
  try {
    await runCommand(`TIMING ${draft.hz} ${draft.ns}`, 'Apply carrier timing');
    timingDirty = false;
    updateControls();
  } catch { /* Keep the draft available until verified or reset. */ }
});

function updateControls() {
  const ready = isReady();
  const busy = commandCount > 0 || calibrationActive();
  $('output-on').disabled = !ready || busy || timingDirty || !!latest?.enabled || faultActive(latest?.fault);
  $('output-off').disabled = !isLive();
  $('mode-select').disabled = !ready || busy;
  $('apply-mode').disabled = !ready || busy || timingDirty || !modeDirty || !$('mode-select').value;
  $('clear-fault').disabled = !ready || busy;
  $('terminal-command').disabled = !isLive() || busy;
  $('send-command').disabled = !isLive() || busy;
  keys.forEach((key) => {
    $('setting-' + key).disabled = !ready || busy || !Number.isFinite(latest?.settings?.[key]) || (benchKeys.has(key) && (!link.supportsBenchSettings || !!latest?.enabled));
  });
  $('apply-settings').disabled = !ready || busy || timingDirty || dirty.size === 0 || (!!latest?.enabled && [...dirty].some((key) => benchKeys.has(key)));
  $('reset-settings').disabled = busy || !anyDrafts();
  $('workspace-output-summary').textContent = calibrationActive() ? 'Calibration running · output may be ON' : !latest || !isFresh() ? 'Output unconfirmed' : latest.enabled ? 'Output ON' : 'Output OFF';
  document.body.classList.toggle('has-device', isLive());
  document.documentElement.classList.toggle('bench-connected', isLive());
  updateBenchControls();
  updateTimingControls();
  $('save-device-settings').disabled = !ready || busy || anyDrafts() || !!latest?.enabled || !settingsPending();
  $('record-button').disabled = !recording && !ready;
  $('experiment-name').disabled = !!recording;
  $('settings-status').textContent = timingDirty ? 'Timing edits not applied · reset timing to apply other edits' : dirty.size ? `${dirty.size} edited ${dirty.size === 1 ? 'value' : 'values'} · not applied` : latest?.settings ? 'Actual values reported by device' : 'Device values load after connection';
  updateCalibrationControls();
  $('device-save-status').textContent = anyDrafts() ? 'Unapplied edits are not saved. Apply or reset edits before saving the running device configuration.' : settingsPending() ? `Running settings, carrier timing, and calibration results are not saved to flash.${latest?.enabled ? ' Turn output OFF before saving.' : ' Save to device to retain them together after power cycling.'}` : 'Apply changes to the running configuration; Save to device retains settings, supported carrier timing, and calibration results together with output OFF.';
}

function renderLive() {
  const stale = !!latest && !isFresh();
  const previousOutputState = $('output-state').textContent;
  $('telemetry-metrics').classList.toggle('readings-stale', stale);
  $('telemetry-metrics').setAttribute('aria-label', stale ? 'Last reported telemetry; stream paused' : 'Live telemetry');
  $('telemetry-status').hidden = !stale;
  $('metric-vsec').textContent = fmt(latest?.vsec);
  $('metric-vpri').textContent = fmt(latest?.vpri);
  $('metric-current').textContent = fmt(latest?.current, 3);
  $('metric-duty').textContent = fmt(latest?.duty, 1);
  $('metric-duty-detail').textContent = latest ? `${actualMode(latest.mode) || 'Unknown mode'} · ${stale ? 'last reported value' : 'reported duty'}` : 'Waiting for reported duty';
  const fault = faultActive(latest?.fault);
  $('metric-fault').textContent = !latest ? 'No data' : stale ? 'Data stale' : fault ? 'Fault active' : 'No faults';
  $('metric-fault').className = `health-value ${latest && fault ? 'fault' : latest && !stale ? 'ok' : ''}`;
  $('metric-fault-detail').textContent = !latest ? 'Fault state unconfirmed' : fault ? `Reported: ${String(latest.fault)}` : stale ? 'Connection controls are restricted' : 'Device-reported fault state';
  $('output-badge').textContent = !latest ? 'UNCONFIRMED' : stale ? 'LAST REPORTED' : fault ? 'FAULT · INHIBITED' : latest.enabled ? 'OUTPUT ON' : 'OUTPUT OFF';
  $('output-badge').className = `badge ${fault ? 'error' : !latest || stale ? 'neutral' : latest.enabled ? 'live' : 'neutral'}`;
  $('output-symbol').classList.toggle('live', !!latest?.enabled && !stale && !fault);
  $('output-state').textContent = !latest ? 'Not connected' : fault ? 'Fault latched · output inhibited' : latest.enabled ? 'Output enabled' : 'Output disabled';
  $('output-description').textContent = !latest ? 'Awaiting device state' : stale ? 'Last reported state; check hardware locally' : link.state === 'demo' ? 'Simulator only' : 'Software enable state reported by firmware';
  if (latest && previousOutputState !== $('output-state').textContent) announce($('output-state').textContent);
  $('reported-mode').textContent = `REPORTED: ${actualMode(latest?.mode) || '—'}`;
  if (!modeDirty) $('mode-select').value = modeCommand(latest?.mode);
  $('mode-note').textContent = latest?.enabled ? 'Output is ON. Applying a mode immediately changes control behavior.' : 'Mode changes take effect when acknowledged by the device.';
  if (latest?.settings) keys.forEach((key) => {
    if (!dirty.has(key)) $('setting-' + key).value = Number.isFinite(latest.settings[key]) ? latest.settings[key] : '';
  });
  if (latest) {
    const elapsed = Math.max(0, (performance.now() - lastReceived) / 1000);
    $('last-update').textContent = stale ? `${Math.floor(elapsed)}s SINCE DATA` : link.state === 'demo' ? 'SYNTHETIC · LIVE' : 'USB · LIVE';
    $('sample-rate').textContent = `${link.state === 'demo' ? 'Synthetic samples' : 'Device samples'}${intervalEstimate ? ` · ~${(1000 / intervalEstimate).toFixed(1)} Hz` : ''}${stale ? ' · stream paused' : ''}`;
    $('adc-values').textContent = `ADC ${Array.isArray(latest.adc) ? latest.adc.join(' / ') : '— / — / —'}`;
  } else {
    $('last-update').textContent = 'NO DATA';
    $('sample-rate').textContent = 'No samples received';
    $('adc-values').textContent = 'ADC — / — / —';
  }
  if (stale && !lastStale && isLive()) {
    $('connection-label').textContent = 'Telemetry paused';
    $('connection-detail').textContent = 'No fresh sample for 3 seconds. Enabling and tuning are restricted.';
    $('connection-dot').className = 'status-dot error';
    announce('Telemetry paused. Readings show the last received values.');
    if (recording) void stopRecording('Telemetry became stale.');
  } else if (!stale && lastStale && isLive()) {
    $('connection-label').textContent = link.state === 'demo' ? 'Demo · synthetic data' : 'USB connected';
    $('connection-detail').textContent = link.state === 'demo' ? 'Controls affect the simulator only.' : 'Verified telemetry is streaming from firmware.';
    $('connection-dot').className = `status-dot ${link.state === 'demo' ? 'demo' : 'live'}`;
    announce('Telemetry resumed.');
  }
  lastStale = stale;
  $('chart-empty').hidden = history.length > 0;
  updateControls();
}

async function runCommand(command, label = command) {
  recordEvent({type:'command',command,label});
  commandCount += 1;
  feedback(`${label} · waiting for acknowledgment…`, 'pending');
  updateControls();
  try {
    const normalized = String(command).trim().replace(/ +/g, ' ').toUpperCase();
    const changesTiming = /^TIMING(?: |$)/.test(normalized);
    if (changesTiming && otherDrafts()) throw new Error('Apply or reset other settings, mode, and slot edits before changing carrier timing.');
    if (otherDrafts() && /^(?:SAVE|CAL)(?: |$)/.test(normalized)) throw new Error('Apply or reset settings, mode, and slot edits before calibration or saving.');
    if (timingDirty && !changesTiming && /^(?:ON|SAVE|SET|LOAD|OPEN|VSBONLY|LINEFF|CAL)(?: |$)/.test(normalized))
      throw new Error('Apply or reset timing edits before changing settings, selecting a mode or slot, starting calibration, enabling output, or saving.');
    if (changesTiming && timingDirty && normalized !== `TIMING ${Number($('timing-frequency').value)} ${Number($('timing-deadtime').value)}`)
      throw new Error('Apply or reset the timing form edits before sending a different TIMING command.');
    if (normalized === 'ON') timingAwaitOff = true;
    const previousTiming = latestTiming;
    const ack = await link.command(command);
    recordEvent({type:'ack',command,ack});
    if (changesTiming) {
      const changed = !previousTiming || previousTiming.requested_hz !== latestTiming?.requested_hz || previousTiming.requested_dead_ns !== latestTiming?.requested_dead_ns;
      timingPendingSave = timingPendingSave || changed;
      timingDirty = false;
      feedback(`${label} acknowledged and timer readback verified. Output remains OFF. Save to device to retain the running configuration.`);
    } else {
      if (normalized === 'SAVE') timingPendingSave = false;
      feedback(`${label} acknowledged. Actual values follow in telemetry.`);
    }
    return ack;
  } catch (error) {
    const message = `${label}: ${error?.message || error}`;
    recordEvent({type:'command_error',command,message});
    feedback(message, 'error');
    notify(message);
    throw error;
  } finally {
    commandCount = Math.max(0, commandCount - 1);
    updateControls();
  }
}

function recordEvent(event) {
  if (!recording) return;
  if (recording.events.length < 2000) recording.events.push({...clone(event),at:new Date().toISOString()});
  else recording.eventsTruncated = true;
}

function recordTiming(timing, initial = false) {
  if (!recording || !timing) return;
  // Poll timestamps and busy/output flags must not fill the operator event log.
  const key = [timing.source,timing.revision,timing.requested_hz,timing.requested_dead_ns,timing.actual_hz,timing.actual_dead_ns,timing.timer_hz,timing.period_ticks,timing.dead_ticks].join(':');
  if (initial || key !== recordedTimingKey) recordEvent({type:'timing',initial,timing});
  recordedTimingKey = key;
}

link.addEventListener('state', (event) => {
  const nextSource = event.detail.state === 'demo' ? 'demo' : event.detail.state === 'connected' ? 'usb' : null;
  if (recording && (nextSource !== recording.source || !nextSource)) void stopRecording('Connection changed; recording stopped.');
  if (source !== nextSource || !nextSource) clearLiveData();
  source = nextSource;
  if (nextSource && link.hello) setHello(link.hello);
  renderState(event.detail.message || '');
});
link.addEventListener('hello', (event) => {
  setHello(event.detail);
});
link.addEventListener('timing', (event) => {
  latestTiming = clone(event.detail);
  if (!latestTiming.enabled && !latestTiming.busy && latest?.enabled === false && commandCount === 0) timingAwaitOff = false;
  recordTiming(timingSnapshot());
  updateControls();
});
link.addEventListener('sample', (event) => {
  latest = clone(event.detail);
  const now = performance.now();
  if (previousReceived) {
    const dt = now - previousReceived;
    intervalEstimate = intervalEstimate ? intervalEstimate * 0.8 + dt * 0.2 : dt;
  }
  previousReceived = now;
  lastReceived = now;
  history.push({ ...latest, received: now });
  while (history.length && (history[0].received < now - 60000 || history.length > 1200)) history.shift();
  if (recording) {
    recording.samples.push({ ...clone(latest), timing:timingSnapshot(), receivedAt: new Date().toISOString() });
    if (recording.samples.length >= 20000) void stopRecording('20,000-sample limit reached. Run saved automatically.');
  }
  renderLive();
  updateRecording();
  queueChart();
});
link.addEventListener('line', (event) => {
  const line = event.detail;
  const at = line.at ? new Date(line.at) : new Date();
  const timestamp = Number.isNaN(at.getTime()) ? new Date().toLocaleTimeString() : at.toLocaleTimeString();
  terminalLines.push(`${timestamp}  ${String(line.direction || 'info').toUpperCase().padEnd(5)} ${String(line.text)}`);
  if (terminalLines.length > 400) terminalLines.shift();
  terminalDirty = true;
  // Keep operator actions and faults in the notebook; the high-volume wire
  // stream remains in samples/terminal and must not crowd out later commands.
  if (line.direction === 'info' || line.direction === 'error') recordEvent(line);
});
link.addEventListener('error', (event) => {
  notify(event.detail?.message || 'The device connection reported an error.');
  feedback(event.detail?.message || 'Connection error', 'error');
});

$('dismiss-alert').addEventListener('click', () => { $('app-alert').hidden = true; });
$('connect-button').addEventListener('click', async () => {
  try {
    if (link.state === 'connected') {
      if (recording) await stopRecording('USB disconnected by user.');
      await link.disconnect();
    } else {
      if (recording) await stopRecording('Switched from demo to USB.');
      if (link.state === 'demo') await link.stopDemo();
      await link.connect();
    }
  } catch (error) { notify(error?.message || String(error)); }
});
async function toggleDemo() {
  try {
    if (recording) await stopRecording('Demo source changed.');
    if (link.state === 'demo') await link.stopDemo();
    else {
      if (link.state === 'connected') await link.disconnect();
      await link.startDemo();
    }
  } catch (error) { notify(error?.message || String(error)); }
}
$('demo-button').addEventListener('click', toggleDemo);
$('exit-demo').addEventListener('click', toggleDemo);
$('output-on').addEventListener('click', () => { if (isReady() && !faultActive(latest?.fault)) void runCommand('ON', 'Enable output').catch(() => {}); });
$('output-off').addEventListener('click', () => { applyGeneration += 1; void runCommand('OFF', 'Output OFF').catch(() => {}); });
$('clear-fault').addEventListener('click', () => { void runCommand('CLR', 'Clear fault').catch(() => {}); });
$('save-device-settings').addEventListener('click', () => {
  if (!$('save-device-settings').disabled) void runCommand('SAVE', 'Save settings to device flash').catch(() => {});
});
$('mode-select').addEventListener('change', () => { modeDirty = $('mode-select').value !== modeCommand(latest?.mode); updateControls(); });
$('apply-mode').addEventListener('click', async () => {
  const mode = $('mode-select').value;
  if ($('apply-mode').disabled || !isReady() || !['OPEN', 'VSBONLY', 'LINEFF'].includes(mode)) return;
  try { await runCommand(mode, `Set ${mode} mode`); modeDirty = false; } catch { /* The device error is already visible. */ }
  updateControls();
});
keys.forEach((key) => {
  const input = $('setting-' + key);
  const error = document.createElement('span'); error.id = `error-setting-${key}`; error.className = 'setting-error'; error.hidden = true;
  input.closest('label').after(error); input.setAttribute('aria-describedby', error.id);
});
keys.forEach((key) => $('setting-' + key).addEventListener('input', () => {
  $('setting-' + key).removeAttribute('aria-invalid');
  $(`error-setting-${key}`).hidden = true;
  const field = $('setting-' + key);
  if (field.value !== '' && Number(field.value) === Number(latest?.settings?.[key])) dirty.delete(key);
  else dirty.add(key);
  field.closest('label').classList.toggle('dirty', dirty.has(key));
  updateControls();
}));
$('reset-settings').addEventListener('click', () => {
  dirty.clear();
  timingDirty = false;
  loadProfileDirty = false; modeDirty = false; $('mode-select').value = modeCommand(latest?.mode);
  keys.forEach((key) => { $('setting-' + key).closest('label').classList.remove('dirty'); $('setting-' + key).removeAttribute('aria-invalid'); $(`error-setting-${key}`).hidden = true; });
  renderLive();
});
$('settings-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  if ($('apply-settings').disabled || !isReady() || commandCount || !dirty.size) return;
  const edits = keys.filter((key) => dirty.has(key)).map((key) => [key, $('setting-' + key).value]);
  for (const [key, value] of edits) {
    const input = $('setting-' + key);
    if (value === '' || !Number.isFinite(Number(value)) || !input.checkValidity()) {
      const details = input.closest('details'); if (details) details.open = true;
      input.setAttribute('aria-invalid','true');
      const error = $(`error-setting-${key}`); error.textContent = value === '' ? 'Enter a value before applying.' : input.validationMessage || 'Enter a finite value in the supported range.'; error.hidden = false;
      input.focus(); notify(`Check ${key}: ${error.textContent}`); return;
    }
  }
  const generation = ++applyGeneration;
  // Holding the busy state across the sequence prevents accidental interleaving.
  commandCount += 1;
  updateControls();
  try {
    for (const [key, value] of edits) {
      if (generation !== applyGeneration || !isReady()) throw new Error('Remaining setting changes canceled.');
      await runCommand(`SET ${key} ${Number(value)}`, `Apply ${key}`);
      dirty.delete(key);
      $('setting-' + key).closest('label').classList.remove('dirty');
    }
    feedback(`${edits.length} ${edits.length === 1 ? 'setting' : 'settings'} acknowledged. Telemetry shows applied values.`);
  } catch (error) {
    if (generation !== applyGeneration) feedback('Output OFF requested. Remaining setting changes canceled.');
    else notify(error?.message || String(error));
  } finally { commandCount = Math.max(0, commandCount - 1); updateControls(); }
});

$('terminal-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const input = $('terminal-command');
  const command = input.value.trim();
  if (!command || commandCount || !isLive()) return;
  if (/^ON(?:\s|$)/i.test(command) && (!isReady() || faultActive(latest?.fault))) { notify('Enabling output requires fresh, verified telemetry and no active fault.'); return; }
  try { await runCommand(command, command); input.value = ''; } catch { /* Keep the command available for correction. */ }
});
$('clear-terminal').addEventListener('click', () => { terminalLines.length = 0; terminalDirty = true; });

function updateRecording() {
  const run = recording || lastRecording;
  $('workspace-recording').hidden = !recording;
  $('workspace-recording-label').textContent = recording ? `Recording ${recording.name} · ${duration(Date.now() - new Date(recording.startedAt).getTime())}` : '';
  $('recording-duration').textContent = run ? duration((recording ? Date.now() : new Date(run.endedAt).getTime()) - new Date(run.startedAt).getTime()) : '00:00:00';
  $('recording-samples').textContent = run ? run.samples.length.toLocaleString() : '0';
  $('recording-source').textContent = run ? run.source === 'demo' ? 'DEMO' : 'USB' : '—';
  $('recording-state').textContent = recording ? 'RECORDING' : lastRecording ? 'STOPPED' : 'IDLE';
  $('recording-state').className = `badge ${recording ? recording.source === 'demo' ? 'demo' : 'live' : 'neutral'}`;
  $('record-button').classList.toggle('recording', !!recording);
  $('record-button').replaceChildren();
  const dot = document.createElement('span');
  dot.className = 'record-dot';
  $('record-button').append(dot, document.createTextNode(recording ? 'Stop & save recording' : 'Start recording'));
  updateControls();
}

$('record-button').addEventListener('click', async () => {
  if (recording) { await stopRecording(); return; }
  if (!isReady()) { notify('Connect a verified device or start demo before recording.'); return; }
  const now = new Date();
  recording = {
    id: crypto.randomUUID(),
    name: $('experiment-name').value.trim() || `Experiment · ${now.toLocaleString()}`,
    notes: $('experiment-notes').value.trim(),
    source: link.state === 'demo' ? 'demo' : 'usb',
    startedAt: now.toISOString(),
    endedAt: null,
    firmware: hello ? clone(hello) : null,
    timing: timingSnapshot(),
    samples: [],
    events: []
  };
  recordedTimingKey = null;
  recordTiming(recording.timing, true);
  checkpointFailed = false;
  $('recording-note').textContent = recording.source === 'demo' ? 'Recording synthetic demo data. This run will be labeled DEMO in exports.' : 'Recording device telemetry. Notes can be edited while the run is active.';
  announce(recording.source === 'demo' ? 'Recording started with synthetic demo data.' : 'Recording started with USB telemetry.');
  updateRecording();
});

async function stopRecording(reason = '') {
  if (!recording) return;
  const completed = recording;
  recording = null;
  completed.endedAt = new Date().toISOString();
  completed.notes = $('experiment-notes').value.trim();
  if (reason) completed.events.push({ direction: 'info', text: reason, at: completed.endedAt });
  lastRecording = completed;
  updateRecording();
  $('recording-note').textContent = 'Saving your recording…';
  try {
    if (checkpointPromise) await checkpointPromise;
    await saveSession(completed);
    $('recording-note').textContent = reason || 'Run saved in this browser. Export a copy from the experiment list.';
    announce('Recording stopped and saved in this browser.');
    await refreshSessions();
  } catch (error) {
    unsaved.set(completed.id, completed);
    $('recording-note').textContent = 'Browser storage failed. Your run is kept in memory; export it below before closing this tab.';
    announce('Recording stopped. Browser storage failed; export the run before closing this tab.');
    notify(`Recording is not saved in browser storage: ${error?.message || error}. Export CSV or JSON below.`);
    renderSessions();
  }
}

function checkpointRecording() {
  if (!recording || checkpointPromise || checkpointFailed) return;
  const snapshot = clone(recording);
  snapshot.notes = $('experiment-notes').value.trim();
  snapshot.checkpointedAt = new Date().toISOString();
  checkpointPromise = saveSession(snapshot).then(() => refreshSessions()).catch((error) => {
    checkpointFailed = true;
    notify(`Automatic checkpoint failed: ${error?.message || error}. Recording continues in memory; stop and export this run before closing the tab.`);
  }).finally(() => { checkpointPromise = null; });
}

async function refreshSessions() {
  try { sessions = await listSessions(); renderSessions(); }
  catch (error) { notify(`Could not read experiment storage: ${error?.message || error}`); renderSessions(); }
}

const element = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
};
function renderSessions() {
  const all = [...unsaved.values(), ...sessions.filter((session) => !unsaved.has(session.id))].sort((a, b) => String(b.startedAt).localeCompare(String(a.startedAt)));
  $('session-count').textContent = `${sessions.length} SAVED${unsaved.size ? ` · ${unsaved.size} UNSAVED` : ''}`;
  $('nav-session-count').textContent = String(all.length);
  const list = $('session-list');
  list.replaceChildren();
  if (!all.length) {
    const row = element('tr'); const empty = element('td', 'archive-empty'); empty.colSpan = 6;
    empty.textContent = 'No recorded sessions. Start a recording to save measurements here.';
    row.append(empty); list.append(row);
    return;
  }
  all.forEach((session) => {
    const row = element('tr', 'session-item');
    const name = element('th', 'session-name'); name.scope = 'row';
    const isDemo = session.source === 'demo';
    const incomplete = !session.endedAt;
    const active = recording?.id === session.id;
    const status = unsaved.has(session.id) ? 'UNSAVED' : active ? 'RECORDING' : incomplete ? 'INTERRUPTED' : null;
    name.append(element('strong', '', session.name || 'Untitled experiment'));
    if (session.notes) name.append(element('small', 'session-notes', session.notes.length > 160 ? session.notes.slice(0,160) + '…' : session.notes));
    const sourceCell = element('td', 'session-source');
    sourceCell.append(element('span', `badge ${isDemo ? 'demo' : 'neutral'}`, isDemo ? 'DEMO' : 'USB'));
    if (status) sourceCell.append(element('small', unsaved.has(session.id) ? 'error-label' : '',status));
    const count = session.samples?.length ?? session.sampleCount ?? 0;
    const date = new Date(session.startedAt);
    const elapsed = new Date(session.endedAt || session.checkpointedAt || session.startedAt).getTime() - date.getTime();
    row.append(name,sourceCell,element('td','session-date',date.toLocaleString('en-GB',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'})),element('td','session-duration',duration(elapsed)),element('td','session-samples',count.toLocaleString()));
    const actions = element('td', 'session-actions');
    const csv = element('button', '', 'CSV');
    const json = element('button', '', 'JSON');
    const remove = element('button', 'delete-session', 'Delete');
    remove.disabled = active;
    [csv, json, remove].forEach((button) => { button.type = 'button'; });
    csv.setAttribute('aria-label',`Export CSV for ${session.name || 'Untitled experiment'}`);
    json.setAttribute('aria-label',`Export JSON for ${session.name || 'Untitled experiment'}`);
    remove.setAttribute('aria-label',`Delete ${session.name || 'Untitled experiment'}`);
    csv.addEventListener('click', () => void exportSession(session.id, 'csv'));
    json.addEventListener('click', () => void exportSession(session.id, 'json'));
    let confirming = false;
    remove.addEventListener('click', async () => {
      if (!confirming) {
        confirming = true;
        remove.textContent = 'Confirm delete';
        remove.classList.add('confirm');
        setTimeout(() => { confirming = false; remove.textContent = 'Delete'; remove.classList.remove('confirm'); }, 5000);
        return;
      }
      try {
        if (unsaved.has(session.id)) unsaved.delete(session.id);
        else await deleteSession(session.id);
        await refreshSessions();
      } catch (error) { notify(`Could not delete this run: ${error?.message || error}`); }
    });
    actions.append(csv, json, remove);
    row.append(actions);
    list.append(row);
  });
}

async function exportSession(id, kind) {
  try {
    const session = unsaved.get(id) || await getSession(id);
    if (!session) throw new Error('This recording is no longer available.');
    const name = (session.name || 'experiment').replace(/[^\p{L}\p{N}_-]+/gu, '-').slice(0, 80);
    const prefix = session.source === 'demo' ? 'DEMO-' : 'USB-';
    if (kind === 'csv') download(`${prefix}${name}.csv`, toCSV(session), 'text/csv;charset=utf-8');
    else download(`${prefix}${name}.json`, JSON.stringify(session, null, 2), 'application/json');
  } catch (error) { notify(`Export failed: ${error?.message || error}`); }
}

function queueChart() {
  if (chartQueued) return;
  chartQueued = true;
  requestAnimationFrame(() => { chartQueued = false; drawChart(); });
}

function drawChart() {
  if (!ctx) return;
  const rect = canvas.getBoundingClientRect();
  if (!rect.width || !rect.height) return;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(rect.width * dpr);
  canvas.height = Math.round(rect.height * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const width = rect.width;
  const height = rect.height;
  const pad = { left: 44, right: chartKind === 'voltage' ? 48 : 15, top: 20, bottom: 29 };
  const plotW = width - pad.left - pad.right;
  const plotH = height - pad.top - pad.bottom;
  const fields = chartKind === 'duty' ? [['duty', '#8fc886']] : [['vsec', '#f0d365'], ['vpri', '#67cbd1']];
  const scales = Object.fromEntries(fields.map(([key]) => {
    const values = history.filter(sample => sample[key] != null && Number.isFinite(sample[key])).map(sample => sample[key]);
    const observedMax = values.length ? Math.max(...values) : key === 'vpri' ? 400 : key === 'duty' ? 100 : 40;
    const observedMin = values.length ? Math.min(...values) : 0;
    const step = key === 'vpri' ? 50 : 5;
    const max = key === 'duty' ? 100 : Math.max(step * 2, Math.ceil(observedMax * 1.12 / step) * step);
    const min = observedMin < 0 ? Math.floor(observedMin / step) * step : 0;
    return [key,{min,max}];
  }));
  const y = (value,key) => { const {min,max} = scales[key]; return pad.top + plotH * (1 - (value-min)/(max-min || 1)); };
  const now = performance.now();
  const x = (time) => pad.left + plotW * (1 - (now - time) / 60000);
  ctx.fillStyle = '#12191f'; ctx.fillRect(0,0,width,height);
  ctx.font = '10px Consolas, monospace';
  ctx.fillStyle = '#899aa6';
  ctx.strokeStyle = '#29343e';
  ctx.lineWidth = 1;
  for (let n = 0; n <= 4; n += 1) {
    const yy = pad.top + plotH * n / 4;
    ctx.beginPath(); ctx.moveTo(pad.left, yy); ctx.lineTo(width - pad.right, yy); ctx.stroke();
    fields.forEach(([key,color],index) => {
      const {min,max} = scales[key]; const value = max - (max-min)*n/4;
      ctx.textAlign = index ? 'left' : 'right'; ctx.fillStyle = color;
      ctx.fillText(value.toFixed(value % 1 ? 1 : 0),index ? width-pad.right+8 : pad.left-8,yy+3);
    });
  }
  ctx.textAlign='left'; ctx.fillStyle=fields[0][1]; ctx.fillText(chartKind==='duty' ? '%' : 'V',pad.left-20,11);
  if (fields.length > 1) {ctx.textAlign='right';ctx.fillStyle=fields[1][1];ctx.fillText('V',width-pad.right+20,11);}
  ctx.fillStyle='#899aa6';
  ctx.textAlign = 'center';
  for (let n = 0; n <= 4; n += 1) {
    const xx = pad.left + plotW * n / 4;
    ctx.beginPath();ctx.moveTo(xx,pad.top);ctx.lineTo(xx,height-pad.bottom);ctx.stroke();
    ctx.fillText(n === 4 ? '0 s' : `−${60 - n * 15} s`, xx, height - 9);
  }
  ctx.save();
  ctx.beginPath(); ctx.rect(pad.left, pad.top - 2, plotW, plotH + 4); ctx.clip();
  fields.forEach(([key, color], index) => {
    const valid = history.filter((sample) => sample[key] !== null && sample[key] !== undefined && Number.isFinite(Number(sample[key])));
    if (!valid.length) return;
    ctx.beginPath();
    let previous = null;
    valid.forEach((sample) => {
      const xx = x(sample.received), yy = y(Number(sample[key]),key);
      if (!previous || sample.received - previous > 3000) ctx.moveTo(xx, yy);
      else ctx.lineTo(xx, yy);
      previous = sample.received;
    });
    ctx.strokeStyle = color; ctx.lineWidth = index ? 1.4 : 1.8; ctx.lineJoin = 'round'; ctx.stroke();
    const last = valid[valid.length - 1];
    ctx.beginPath(); ctx.arc(x(last.received), y(Number(last[key]),key), 2, 0, Math.PI * 2); ctx.fillStyle = color; ctx.fill();
  });
  ctx.restore();
}

document.querySelectorAll('[data-chart]').forEach((button) => button.addEventListener('click', () => {
  chartKind = button.dataset.chart;
  document.querySelectorAll('[data-chart]').forEach((other) => { const selected = other === button; other.classList.toggle('selected', selected); other.setAttribute('aria-pressed', String(selected)); });
  const legend = $('chart-legend');
  legend.replaceChildren();
  const entries = chartKind === 'duty' ? [['duty', 'EN duty · %']] : [['green', 'CH1 Vsec · left axis'], ['orange', 'CH2 Vpri · right axis']];
  entries.forEach(([color, label]) => { const span = element('span'); span.append(element('i', color), document.createTextNode(label)); legend.append(span); });
  legend.append(element('span', 'chart-window', '60 s window'));
  canvas.setAttribute('aria-label', `${chartKind === 'duty' ? 'Applied duty' : 'Primary and secondary voltage'} over the last sixty seconds${link.state === 'demo' ? ', synthetic demo data' : ''}`);
  queueChart();
}));

const workspaceViews = { dashboard:'dashboard', 'device-setup':'device-setup', calibration:'calibration', experiments:'sessions-view' };
const workspaceCopy = {
  dashboard:['Converter monitor','Live signals and quick output controls.'],
  'device-setup':['Device setup','Configure load references, limits, and timing from device readback.'],
  calibration:['Auto-calibration','Prepare the physical reference, run one routine, then review the result.'],
  experiments:['Sessions','Record a bench run and keep its measurements and commands.'],
};
let currentView = 'dashboard';
function showWorkspaceFromHash(focus=false) {
  const anchor = location.hash.slice(1);
  const routes = { 'capture-heading':'experiments', 'output-heading':'dashboard', 'connection-guide':'device-setup', 'terminal-details':'device-setup', 'settings-heading':'device-setup', 'load-references':'device-setup' };
  if (anchor && !workspaceViews[anchor] && !routes[anchor]) return;
  currentView = routes[anchor] || (workspaceViews[anchor] ? anchor : 'dashboard');
  for (const [name,id] of Object.entries(workspaceViews)) $(id).hidden = name !== currentView;
  document.querySelectorAll('.workspace-nav .nav-link').forEach(nav => {
    const active = nav.getAttribute('href') === `#${currentView}`;
    nav.classList.toggle('active',active);
    if (active) nav.setAttribute('aria-current','page'); else nav.removeAttribute('aria-current');
  });
  const [title,description] = workspaceCopy[currentView];
  document.querySelector('.firmware-link').hidden = currentView !== 'device-setup';
  $('workspace-heading').textContent = title; $('workspace-description').textContent = description;
  document.title = `${title} · Power Lab`;
  if (anchor === 'connection-guide') $('connection-details').open = true;
  if (anchor === 'terminal-details') $('terminal-details').open = true;
  window.scrollTo(0,0); queueChart();
  if (focus) requestAnimationFrame(() => {
    let target = ['capture-heading','output-heading'].includes(anchor) ? $(anchor) : $('workspace-heading');
    if (anchor === 'connection-guide') target = $('connection-heading');
    if (anchor === 'terminal-details') target = $('terminal-details').querySelector('summary');
    if (['connection-guide','terminal-details','capture-heading','output-heading'].includes(anchor)) target.scrollIntoView({block:'start'});
    target.focus({preventScroll:true});
  });
}
window.addEventListener('hashchange', () => showWorkspaceFromHash(true));
showWorkspaceFromHash();
if ('ResizeObserver' in window) new ResizeObserver(queueChart).observe(canvas.parentElement);
else window.addEventListener('resize', queueChart);
window.addEventListener('beforeunload', (event) => {
  if (recording || unsaved.size) { event.preventDefault(); event.returnValue = ''; }
});
window.addEventListener('pagehide', () => {
  if (recording) {
    const snapshot = clone(recording);
    snapshot.notes = $('experiment-notes').value.trim();
    snapshot.checkpointedAt = new Date().toISOString();
    void saveSession(snapshot).catch(() => {});
  }
  link.abandon?.();
});

$('browser-support').textContent = 'serial' in navigator && window.isSecureContext ? 'Web Serial available. Select Connect USB, then choose the adapter port. Firmware PWR-2.0.1 or later is required.' : 'USB requires desktop Chrome or Edge with HTTPS or localhost. Demo and saved sessions are available here.';
renderState();
updateRecording();
queueChart();
setInterval(() => {
  renderLive();
  if (recording) updateRecording();
  if (history.length) queueChart();
  if (terminalDirty && $('terminal-details').open) {
    const output = $('terminal-output');
    const nearBottom = output.scrollHeight - output.scrollTop - output.clientHeight < 60;
    output.textContent = terminalLines.join('\n');
    if (nearBottom) output.scrollTop = output.scrollHeight;
    $('terminal-count').textContent = `${terminalLines.length} lines · latest 400 retained`;
    terminalDirty = false;
  }
}, 500);
setInterval(checkpointRecording, 5000);
void (async () => {
  try { await openStore(); await refreshSessions(); }
  catch (error) { notify(`Local experiment storage is unavailable: ${error?.message || error}. Recordings can still be exported from memory.`); }
})();
