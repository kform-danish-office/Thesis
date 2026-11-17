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
    if (!['hello','telemetry','ack','event'].includes(frame.type)) return null;
    if (frame.type === 'hello' && (frame.protocol !== 1 || typeof frame.fw !== 'string')) return null;
    if (frame.type === 'ack' && (typeof frame.id !== 'string' || typeof frame.ok !== 'boolean')) return null;
    if (frame.type === 'telemetry') {
      if (frame.protocol !== 1 || !Number.isFinite(frame.ms) || typeof frame.enabled !== 'boolean' || typeof frame.mode !== 'string' || !['string','number'].includes(typeof frame.fault)) return null;
      if (!Number.isInteger(frame.lease_ms) || frame.lease_ms < 0 || frame.lease_ms > 10000) return null;
      if (!Number.isInteger(frame.stream_ms) || frame.stream_ms < 0 || frame.stream_ms > 5000) return null;
      for (const key of ['vsec','vpri','current','power','duty']) if (frame[key] !== null && !Number.isFinite(frame[key])) return null;
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
