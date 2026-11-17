from pathlib import Path
p=Path('/workspace/working-source/web/app.js');s=p.read_text()
s=s.replace("const keys = ['VSET', 'VON', 'VMAX', 'OVP', 'DMAX', 'OD', 'FEN'];", "const keys = [...document.querySelectorAll('#settings-form input[name]')].map((input) => input.name);\nconst benchKeys = new Set(['LOAD1','LOAD2','LOAD3','NLDUTY','AUTOMAX','AUTOSTEP','AUTOFINE','AUTOSETTLE','AUTOMEAS','PREMS','PRESETTLE','PREMAX']);")
s=s.replace('let modeDirty = false;', 'let modeDirty = false;\nlet loadProfileDirty = false;')
s=s.replace('  latest = null;','  loadProfileDirty = false;\n  latest = null;',1)
s=s.replace("  $('save-device-settings').disabled", "  $('workspace-output-summary').textContent = calibrationActive() ? 'Calibration running · output may be ON' : !latest || !isFresh() ? 'Output unconfirmed' : latest.enabled ? 'Output ON' : 'Output OFF';\n  document.body.classList.toggle('has-device', isLive());\n  updateBenchControls();\n  $('save-device-settings').disabled",1)
s=s.replace("$('setting-' + key).disabled = !ready || busy || latest?.settings?.[key] === undefined;", "$('setting-' + key).disabled = !ready || busy || !Number.isFinite(latest?.settings?.[key]) || (benchKeys.has(key) && (!link.supportsBenchSettings || !!latest?.enabled));")
s=s.replace("$('apply-settings').disabled = !ready || busy || dirty.size === 0;", "$('apply-settings').disabled = !ready || busy || dirty.size === 0 || (!!latest?.enabled && [...dirty].some((key) => benchKeys.has(key)));")
s=s.replace("if (!dirty.has(key) && latest.settings[key] !== undefined) $('setting-' + key).value = latest.settings[key];", "if (!dirty.has(key)) $('setting-' + key).value = Number.isFinite(latest.settings[key]) ? latest.settings[key] : '';")
s=s.replace('active || dirty.size > 0 || modeDirty ||', 'active || dirty.size > 0 || modeDirty || loadProfileDirty ||')
s=s.replace('(dirty.size || modeDirty)) status', '(dirty.size || modeDirty || loadProfileDirty)) status')
s=s.replace("  $('calibration-instructions').textContent = calibrationInstructions[kind];", """  $('calibration-instructions').textContent = calibrationInstructions[kind];
  const resistance = latest?.settings?.[`LOAD${$('calibration-slot').value}`];
  for (const option of $('calibration-slot').options) {
    const r = latest?.settings?.[`LOAD${option.value}`];
    option.textContent = `Load slot ${option.value}${Number.isFinite(r) ? r > 0 ? ` · ${r} Ω reference` : ' · unconfigured' : ''}`;
  }
  if (kind === 'LOAD' && Number.isFinite(resistance) && resistance > 0) $('calibration-instructions').textContent = `Connect the physical ${resistance} Ω reference load for slot ${$('calibration-slot').value}. The routine energizes the converter. Switch loads only with output OFF.`;""")
s=s.replace("  if (supported && !active && latest?.enabled) status", "  if (supported && kind === 'LOAD' && link.supportsBenchSettings && !(resistance > 0) && !active) { $('calibration-start').disabled = true; status = 'Set a positive reference resistance in Setup before calibrating this slot.'; }\n  if (supported && !active && latest?.enabled) status")
anchor='function updateControls() {'
bench='''function updateBenchControls() {
  const supported = link.supportsBenchSettings;
  const activeSlot = latest?.settings?.ACTLOAD;
  const readback = Number.isInteger(activeSlot) && activeSlot >= 1 && activeSlot <= 3;
  const available = isReady() && supported && readback;
  const locked = !!latest?.enabled || calibrationActive() || commandCount > 0;
  $('load-profile').disabled = !available || locked;
  if (!loadProfileDirty && readback) $('load-profile').value = String(activeSlot);
  for (const option of $('load-profile').options) {
    const r = latest?.settings?.[`LOAD${option.value}`];
    option.textContent = `Slot ${option.value}${Number.isFinite(r) ? r > 0 ? ` · ${r} Ω` : ' · unconfigured' : ''}`;
  }
  $('apply-load-profile').disabled = !available || locked || !loadProfileDirty || dirty.size > 0 || modeDirty;
  const r = latest?.settings?.[`LOAD${activeSlot}`];
  $('active-load-summary').textContent = readback ? `Device reference slot: ${activeSlot}${Number.isFinite(r) ? r > 0 ? ` · ${r} Ω configured` : ' · resistance unconfigured' : ''}.` : 'Waiting for load-reference readback.';
  $('bench-settings-status').textContent = !isLive() ? 'Connect compatible firmware or start Demo to explore these settings.' : !supported ? 'Load/tuning readback requires firmware PWR-2.0.3 with bench_settings_v1. Existing voltage controls remain available.' : calibrationActive() ? 'Calibration is running. Load and tuning edits are locked.' : latest?.enabled ? 'Turn output OFF to edit load references and tuning settings.' : link.state === 'demo' ? 'Synthetic demo settings only. No physical load is changed.' : 'Extended settings are reported by the device. Apply changes in RAM, then save explicitly.';
}
$('load-profile').addEventListener('change', () => { loadProfileDirty = Number($('load-profile').value) !== latest?.settings?.ACTLOAD; updateControls(); });
$('apply-load-profile').addEventListener('click', async () => {
  if ($('apply-load-profile').disabled) return;
  try { await runCommand(`LOAD ${$('load-profile').value}`, 'Select reference slot'); loadProfileDirty = false; renderLive(); } catch {}
});
$('workspace-record-stop').addEventListener('click', async () => { if (recording) await stopRecording(); });

'''+anchor
assert anchor in s;s=s.replace(anchor,bench)
s=s.replace("  $('recording-duration').textContent =", "  $('workspace-recording').hidden = !recording;\n  $('workspace-recording-label').textContent = recording ? `Recording ${recording.name} · ${duration(Date.now() - new Date(recording.startedAt).getTime())}` : '';\n  $('recording-duration').textContent =",1)
# Field feedback is local, and a hidden advanced field opens before validation focus.
s=s.replace("keys.forEach((key) => $('setting-' + key).addEventListener('input', () => {", """keys.forEach((key) => {
  const input = $('setting-' + key);
  const error = document.createElement('span'); error.id = `error-setting-${key}`; error.className = 'setting-error'; error.hidden = true;
  input.closest('label').after(error); input.setAttribute('aria-describedby', error.id);
});
keys.forEach((key) => $('setting-' + key).addEventListener('input', () => {
  $('setting-' + key).removeAttribute('aria-invalid');
  $(`error-setting-${key}`).hidden = true;""")
s=s.replace("  if (!isReady() || commandCount || !dirty.size) return;", "  if ($('apply-settings').disabled || !isReady() || commandCount || !dirty.size) return;")
s=s.replace("  if (edits.some(([, value]) => value === '' || !Number.isFinite(Number(value)))) { notify('Enter a finite number for each edited setting.'); return; }", """  for (const [key, value] of edits) {
    const input = $('setting-' + key);
    if (value === '' || !Number.isFinite(Number(value)) || !input.checkValidity()) {
      const details = input.closest('details'); if (details) details.open = true;
      input.setAttribute('aria-invalid','true');
      const error = $(`error-setting-${key}`); error.textContent = value === '' ? 'Enter a value before applying.' : input.validationMessage || 'Enter a finite value in the supported range.'; error.hidden = false;
      input.focus(); notify(`Check ${key}: ${error.textContent}`); return;
    }
  }""")
s=s.replace("keys.forEach((key) => { $('setting-' + key).closest('label').classList.remove('dirty'); });", "keys.forEach((key) => { $('setting-' + key).closest('label').classList.remove('dirty'); $('setting-' + key).removeAttribute('aria-invalid'); $(`error-setting-${key}`).hidden = true; });")
# Replace scroll-driven active-section guessing with explicit workspaces.
a=s.index('function setActiveSection(href) {');b=s.index("if ('ResizeObserver'",a)
s=s[:a]+'''const workspaceViews = { dashboard:'dashboard', 'device-setup':'device-setup', calibration:'calibration', experiments:'sessions-view' };
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
  $('workspace-heading').textContent = title; $('workspace-description').textContent = description;
  document.title = `${title} · Power Lab`;
  if (anchor === 'connection-guide') $('connection-details').open = true;
  if (anchor === 'terminal-details') $('terminal-details').open = true;
  window.scrollTo(0,0); queueChart();
  if (focus) requestAnimationFrame(() => { const target = ['capture-heading','output-heading'].includes(anchor) ? $(anchor) : $('workspace-heading'); target.focus({preventScroll:true}); });
}
window.addEventListener('hashchange', () => showWorkspaceFromHash(true));
showWorkspaceFromHash();
''' +s[b:]
p.write_text(s)
