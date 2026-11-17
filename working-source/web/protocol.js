export const carrierTimingLimits = Object.freeze({min_hz:500000,max_hz:2000000,min_dead_ns:20,max_dead_ns:200});

// carrier_timing_v1 reports both the request and the timer's quantized result.
// Reject incomplete or inconsistent readback before it can authorize an edit.
export function validCarrierTiming(t) {
  if (!t || typeof t !== 'object' || Array.isArray(t)) return false;
  for (const key of ['requested_hz','actual_hz','requested_dead_ns','actual_dead_ns','timer_hz','period_ticks','dead_ticks','revision',...Object.keys(carrierTimingLimits)])
    if (!Number.isSafeInteger(t[key])) return false;
  for (const [key,value] of Object.entries(carrierTimingLimits)) if (t[key] !== value) return false;
  if (t.requested_hz < t.min_hz || t.requested_hz > t.max_hz || t.requested_dead_ns < t.min_dead_ns || t.requested_dead_ns > t.max_dead_ns ||
      t.timer_hz <= 0 || t.timer_hz > 1000000000 || t.period_ticks < 2 || t.period_ticks > 65536 || t.period_ticks % 2 ||
      t.dead_ticks < 1 || t.dead_ticks > 127 || t.dead_ticks * 4 >= t.period_ticks || t.revision < 0 || t.revision > 0xffffffff ||
      typeof t.enabled !== 'boolean' || typeof t.busy !== 'boolean') return false;
  return t.period_ticks === 2 * Math.floor((t.timer_hz + t.requested_hz) / (2 * t.requested_hz)) &&
    t.dead_ticks === Math.ceil(t.requested_dead_ns * t.timer_hz / 1000000000) &&
    t.actual_hz === Math.floor((t.timer_hz + t.period_ticks / 2) / t.period_ticks) &&
    t.actual_dead_ns === Math.ceil(t.dead_ticks * 1000000000 / t.timer_hz);
}

// Newline framing tolerates UART prompts/echo without interpreting human output.
export class LineFramer {
  constructor(onLine, maxLength = 4096) { this.onLine = onLine; this.maxLength = maxLength; this.buffer = ''; this.dropping = false; }
  push(text) {
    for (const char of text) {
      if (char === '\r' || char === '\n') {
        if (!this.dropping && this.buffer) this.onLine(this.buffer);
        this.buffer = ''; this.dropping = false;
      } else if (!this.dropping) {
        this.buffer += char;
        if (this.buffer.length > this.maxLength) { this.buffer = ''; this.dropping = true; }
      }
    }
  }
}

export function parseFrame(line) {
  const start = line.indexOf('{');
  if (start < 0) return null;
  try {
    const frame = JSON.parse(line.slice(start));
    if (!frame || Array.isArray(frame) || typeof frame !== 'object') return null;
    if (!['hello','telemetry','timing','ack','event'].includes(frame.type)) return null;
    if (frame.type === 'hello' && (frame.protocol !== 1 || typeof frame.fw !== 'string')) return null;
    if (frame.type === 'ack' && (typeof frame.id !== 'string' || typeof frame.ok !== 'boolean')) return null;
    if (frame.type === 'timing' && (frame.protocol !== 1 || (frame.id !== undefined && typeof frame.id !== 'string') || !validCarrierTiming(frame.timing))) return null;
    if (frame.type === 'telemetry') {
      if (frame.protocol !== 1 || !Number.isFinite(frame.ms) || typeof frame.enabled !== 'boolean' || typeof frame.mode !== 'string' || !['string','number'].includes(typeof frame.fault)) return null;
      if (!Number.isInteger(frame.lease_ms) || frame.lease_ms < 0 || frame.lease_ms > 10000) return null;
      if (!Number.isInteger(frame.stream_ms) || frame.stream_ms < 0 || frame.stream_ms > 5000) return null;
      for (const key of ['vsec','vpri','current','power','duty']) if (frame[key] !== null && !Number.isFinite(frame[key])) return null;
      if (frame.calibration !== undefined) {
        const c = frame.calibration;
        if (!c || typeof c !== 'object' || Array.isArray(c) || !Number.isInteger(c.state) || c.state < 0 || c.state > 5 || !Number.isInteger(c.kind) || c.kind < 0 || c.kind > 4 || !Number.isInteger(c.slot) || c.slot < 0 || c.slot > 3) return null;
        for (const key of ['duty','nlduty','preduty']) if (!Number.isFinite(c[key]) || c[key] < 0 || c[key] > 100) return null;
        for (const key of ['offset','line_ref']) if (c[key] !== null && !Number.isFinite(c[key])) return null;
      }
      if (!frame.settings || typeof frame.settings !== 'object' || Array.isArray(frame.settings)) return null;
    }
    return frame;
  } catch { return null; }
}

export function validateCommand(text) {
  const command = String(text).trim().replace(/ +/g, ' ').toUpperCase();
  if (!command || command.length > 72 || !/^[A-Z0-9 .+?_-]+$/.test(command)) throw new Error('Enter a single UART command, up to 72 characters.');
  if (command.startsWith('WEB ')) throw new Error('Enter the command without the WEB prefix.');
  return command;
}

export function faultActive(fault) { return ![0,'0','NONE','none','OK',''].includes(fault); }
