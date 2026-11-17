let dbPromise;
export function openStore() {
  if (!dbPromise) dbPromise = new Promise((resolve, reject) => {
    if (!globalThis.indexedDB) { reject(new Error('This browser cannot store sessions. Export your session before closing.')); return; }
    const request = indexedDB.open('thesis-power-lab', 1);
    request.onupgradeneeded = () => request.result.createObjectStore('sessions', {keyPath:'id'});
    request.onerror = () => reject(request.error);
    request.onblocked = () => reject(new Error('Session storage is blocked by another app tab.'));
    request.onsuccess = () => { request.result.onversionchange = () => { request.result.close(); dbPromise = undefined; }; resolve(request.result); };
  }).catch(error => { dbPromise = undefined; throw error; });
  return dbPromise;
}
async function transaction(mode, operation) {
  const db = await openStore();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('sessions', mode);
    let value;
    const request = operation(tx.objectStore('sessions'));
    request.onsuccess = () => { value = request.result; };
    tx.oncomplete = () => resolve(value);
    tx.onerror = () => reject(tx.error || request.error);
    tx.onabort = () => reject(tx.error || new Error('Session storage was interrupted.'));
  });
}
export const saveSession = session => transaction('readwrite', store => store.put(session));
export const listSessions = async () => (await transaction('readonly', store => store.getAll())).sort((a,b) => b.startedAt.localeCompare(a.startedAt));
export const getSession = id => transaction('readonly', store => store.get(id));
export const deleteSession = id => transaction('readwrite', store => store.delete(id));
function csvCell(value) {
  let text = value == null ? '' : String(value);
  if (/^[\s]*[=+@-]/.test(text) && !Number.isFinite(Number(text))) text = "'" + text;
  return '"' + text.replaceAll('"', '""') + '"';
}
export function toCSV(session) {
  const columns = ['session_id','session_name','notes','source','firmware','received_at','device_ms','enabled','mode','fault','vpri_V','vsec_V','current_diagnostic_A','power_diagnostic_W','duty_percent','adc_pa0','adc_pa1','adc_pa2','VSET','VON','VMAX','OVP','DMAX','OD','FEN','lease_ms'];
  const rows = (session.samples || []).map(s => [session.id,session.name,session.notes,session.source,typeof session.firmware === 'object' ? session.firmware?.fw : session.firmware,s.receivedAt,s.ms,s.enabled,s.mode,s.fault,s.vpri,s.vsec,s.current,s.power,s.duty,s.adc?.[0],s.adc?.[1],s.adc?.[2],...['VSET','VON','VMAX','OVP','DMAX','OD','FEN'].map(k => s.settings?.[k]),s.lease_ms]);
  return '\uFEFF' + [columns,...rows].map(row => row.map(csvCell).join(',')).join('\r\n');
}
export function download(name, text, mime = 'application/json') {
  const url = URL.createObjectURL(new Blob([text],{type:mime}));
  const a = document.createElement('a'); a.href = url; a.download = name.replace(/[<>:"/\\|?*]/g, '_'); a.click();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}
