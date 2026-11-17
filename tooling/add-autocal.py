from pathlib import Path
p=Path('/workspace/working-source/thesi_power_control.ino');s=p.read_text()
s=s.replace('#define FW_VERSION_STRING "PWR-2.0.1"','#define FW_VERSION_STRING "PWR-2.0.2"')
s=s.replace('bool webFaultEventPending = false;', '''bool webFaultEventPending = false;
// Calibration is queued outside the parser; cooperative waits service OFF/lease.
bool webCalibrationRunning = false;
bool webCalibrationAbort = false;
bool webCalibrationSucceeded = false;
uint8_t webCalibrationState = 0; // idle, queued, running, complete, stopped, failed
uint8_t webCalibrationKind = 0; // precharge, no-load/load, current zero, line reference
int8_t webCalibrationSlot = -1;
uint32_t webCalibrationStartMs = 0;
uint16_t webCalibrationDuty = 0;
bool serviceWebCalibrationWait();
void runWebCalibration();
void handleSerial();
bool handleWebCalibrationCommand(String body, String id);
// Suppress legacy human output during web calibration so JSON chunks never mix.
struct QuietTuneSerial {
  template<typename... A> void print(A... a) { if (!webSessionActive) CmdSerial.print(a...); }
  template<typename... A> void println(A... a) { if (!webSessionActive) CmdSerial.println(a...); }
} TuneSerial;''')
# Do not persist while the legacy algorithm is running inside a web transaction.
s=s.replace('return !systemEnabled && !autoTuneRunning && !startupPrechargeActive();','return !systemEnabled && !autoTuneRunning && !webCalibrationRunning && !startupPrechargeActive();')
# Quiet output in the tune routines only, preserving ordinary terminal behavior.
for a,b in [('bool runStartupPrechargeBlocking()', 'void setSystemEnabled('),('void initMeasure(', '// UART\n')]:
 start=s.index(a);end=s.index(b,start)
 s=s[:start]+s[start:end].replace('CmdSerial.', 'TuneSerial.')+s[end:]
# Service all powered measurement waits and the startup path.
s=s.replace('while (systemEnabled && startupPrechargeActive() && !faultLatched) {','while (systemEnabled && startupPrechargeActive() && !faultLatched) {\n    if (!serviceWebCalibrationWait()) return false;')
s=s.replace('while (millis() - startMs < burstMs) {','while (millis() - startMs < burstMs) {\n    if (!serviceWebCalibrationWait()) return false;')
s=s.replace('while (millis() - settleStartMs < cfg.prechargeSettleMs) {','while (millis() - settleStartMs < cfg.prechargeSettleMs) {\n    if (!serviceWebCalibrationWait()) return false;')
s=s.replace('while (millis() - start < ms) {','while (millis() - start < ms) {\n    if (!serviceWebCalibrationWait()) return false;',1)
# Measurement failure must propagate rather than use a partial sample on cancel.
pos=s.index('MeasureResult measureWindow(');end=s.index('MeasureResult settleAndMeasure',pos)
part=s[pos:end].replace('while (millis() - start < ms) {','while (millis() - start < ms) {\n    if (!serviceWebCalibrationWait()) { m.fault = true; break; }');s=s[:pos]+part+s[end:]
s=s.replace('  lastTunePointHighVStop = m.highVStop', '  if (webCalibrationRunning && webCalibrationAbort) return false;\n  lastTunePointHighVStop = m.highVStop')
s=s.replace('  cfg.enFreqHz = bestFreq;\n  cfg.noLoadDutyX10', '  if (webCalibrationRunning) webCalibrationSucceeded = true;\n  cfg.enFreqHz = bestFreq;\n  cfg.noLoadDutyX10')
s=s.replace('void savePrechargeTuneResult(uint16_t dutyX10, uint8_t bursts, float vAfter) {','void savePrechargeTuneResult(uint16_t dutyX10, uint8_t bursts, float vAfter) {\n  if (webCalibrationRunning) webCalibrationSucceeded = true;')
s=s.replace('  setEnDutyX10(dutyX10);\n  filtersPrimed = false;\n  MeasureResult m', '  setEnDutyX10(dutyX10);\n  if (webCalibrationRunning) webCalibrationDuty = dutyX10;\n  filtersPrimed = false;\n  MeasureResult m')
s=s.replace('  setEnDutyX10BypassLimits(dutyX10);\n\n  uint32_t startMs', '  setEnDutyX10BypassLimits(dutyX10);\n  if (webCalibrationRunning) webCalibrationDuty = dutyX10;\n\n  uint32_t startMs')
# Current zero is finite but still interruptible; silence its ordinary printout.
s=s.replace('  for (int i = 0; i < 64; i++) {\n    rawPa2Adc', '  for (int i = 0; i < 64; i++) {\n    if (!serviceWebCalibrationWait()) return;\n    rawPa2Adc')
a=s.index('void zeroCurrentOffset() {');b=s.index('int8_t waitForLoadGo',a);s=s[:a]+s[a:b].replace('CmdSerial.', 'TuneSerial.')+s[b:]
# Capability and state are explicit, rather than guessing firmware versions.
s=s.replace('\\"lease_required\\":true}', '\\"lease_required\\":true,\\"capabilities\\":[\\"calibration_v1\\"]}')
s=s.replace('  webAppendText(frame, ",\\"control_dt_us\\":");', '''  webAppendText(frame, ",\\"calibration\\":{\\"state\\":"); webAppendUInt(frame, webCalibrationState);
  webAppendText(frame, ",\\"kind\\":"); webAppendUInt(frame, webCalibrationKind);
  webAppendText(frame, ",\\"slot\\":"); webAppendUInt(frame, webCalibrationSlot < 0 ? 0 : webCalibrationSlot + 1);
  webAppendText(frame, ",\\"duty\\":"); webAppendNumber(frame, dutyX10ToPercent(webCalibrationDuty));
  webAppendText(frame, ",\\"nlduty\\":"); webAppendNumber(frame, dutyX10ToPercent(cfg.noLoadDutyX10));
  webAppendText(frame, ",\\"preduty\\":"); webAppendNumber(frame, dutyX10ToPercent(cfg.prechargeDutyX10));
  webAppendText(frame, "}");
  webAppendText(frame, ",\\"control_dt_us\\":");''')
s=s.replace('    webLeaseExpiredEvent = true;', '    webLeaseExpiredEvent = true;\n    webCalibrationAbort = true;\n    if (webCalibrationState == 1) webCalibrationState = 4;')
# OFF always cancels any queued/running calibration before other mutations.
s=s.replace('  if (up == "OFF") {\n    setSystemEnabled', '  if (up == "OFF") {\n    webCalibrationAbort = true;\n    if (webCalibrationState == 1) webCalibrationState = 4;\n    setSystemEnabled')
s=s.replace('  if (up == "ON") {\n    if (webLeaseRemainingMs()', '''  if (handleWebCalibrationCommand(body, id)) return;
  if ((webCalibrationRunning || webCalibrationState == 1) && up != "OFF") { webAck(id, false, "calibration_busy_use_off"); return; }
  if (up == "ON") {
    if (webLeaseRemainingMs()''')
# Plain emergency OFF inside an active web session also stops a tune.
s=s.replace('    if (up == "OFF") {\n      setSystemEnabled', '    if (up == "OFF") {\n      webCalibrationAbort = true;\n      if (webCalibrationState == 1) webCalibrationState = 4;\n      setSystemEnabled')
# Runner is outside the production protocol extraction used by the older tests.
runner=r'''
// WEB_CALIBRATION_RUNNER_BEGIN
bool serviceWebCalibrationWait() {
  if (!webCalibrationRunning) return true;
  serviceWebLease();
  handleSerial();
  if (!adcDmaRunning || !gatePwmReady || faultLatched ||
      (webCalibrationKind <= 2 && !systemEnabled) ||
      millis() - webCalibrationStartMs >= 180000UL || webLeaseRemainingMs() == 0)
    webCalibrationAbort = true;
  if (webCalibrationAbort) {
    setSystemEnabled(false, false);
    setGateOutputsEnabled(false);
    return false;
  }
  serviceWebTelemetry();
  serviceWebTx();
  return true;
}

bool handleWebCalibrationCommand(String body, String id) {
  String command = body; command.trim(); command.toUpperCase();
  if (!command.startsWith("CAL ")) return false;
  if (webCalibrationRunning || webCalibrationState == 1) { webAck(id, false, "calibration_busy_use_off"); return true; }
  if (systemEnabled) { webAck(id, false, "turn_off_first"); return true; }
  if (configImportActive) { webAck(id, false, "end_config_first"); return true; }
  if (!webSessionActive || webLeaseRemainingMs() == 0) { webAck(id, false, "lease_required"); return true; }
  if (faultLatched || !adcDmaRunning || !gatePwmReady || !filtersPrimed) { webAck(id, false, "calibration_hardware_not_ready"); return true; }
#if defined(STM32F410Cx)
  if (!settingsStorageReady) { webAck(id, false, "storage_not_ready"); return true; }
#endif
  uint8_t kind = 0; int8_t slot = -1;
  if (command == "CAL PRECHARGE") kind = 1;
  else if (command == "CAL NOLOAD") kind = 2;
  else if (command.startsWith("CAL LOAD ")) {
    uint32_t n;
    if (!webParseUInt(command.substring(9), n) || n < 1 || n > CAL_LOAD_SLOT_COUNT) { webAck(id, false, "load_range_1_3"); return true; }
    kind = 2; slot = (int8_t)(n - 1);
  } else if (command == "CAL ZERO") kind = 3;
  else if (command == "CAL LINE") kind = 4;
  else { webAck(id, false, "unknown_calibration"); return true; }
  webCalibrationKind = kind; webCalibrationSlot = slot;
  webCalibrationAbort = false; webCalibrationSucceeded = false;
  webCalibrationState = 1; webCalibrationDuty = 0;
  webAck(id, true, "calibration_queued");
  return true;
}

void runWebCalibration() {
  if (webCalibrationState != 1 || webCalibrationRunning) return;
  if (webLeaseRemainingMs() == 0 || systemEnabled || faultLatched || webCalibrationAbort) { webCalibrationState = 4; return; }
  SettingsSlot original = cfg;
  bool dirtyBefore = settingsDirty;
  ControlMode modeBefore = controlMode;
  webCalibrationRunning = true; webCalibrationState = 2;
  webCalibrationStartMs = millis();
  configImportActive = true; // Algorithm saves remain RAM-only until explicit SAVE.
  if (webCalibrationKind == 1) autoTunePrecharge();
  else if (webCalibrationKind == 2) autoTunePower(true, webCalibrationSlot);
  else if (webCalibrationKind == 3) {
    zeroCurrentOffset();
    webCalibrationSucceeded = !webCalibrationAbort;
  } else if (webCalibrationKind == 4) {
    updateAnalogFilters(true);
    float v = latestVpriRaw > 1.0f ? latestVpriRaw : filteredVpri;
    if (isfinite(v) && v >= 1.0f) { cfg.lineFfRefV = clampFloat(v, 1.0f, 1000.0f); cfg.lineFfEnable = 1; webCalibrationSucceeded = true; }
  }
  serviceWebLease();
  bool success = webCalibrationSucceeded && !webCalibrationAbort && !faultLatched;
  setSystemEnabled(false, false);
  setGateOutputsEnabled(false);
  autoTuneRunning = false;
  configImportActive = false;
  if (!success) { cfg = original; settingsDirty = dirtyBefore; }
  else { cfg.systemEnabled = original.systemEnabled; cfg.controlMode = original.controlMode; markSettingsDirty(); }
  controlMode = modeBefore;
  setEnFrequencyHz(cfg.enFreqHz);
  webCalibrationState = success ? 3 : webCalibrationAbort ? 4 : 5;
  webCalibrationRunning = false;
}
// WEB_CALIBRATION_RUNNER_END

'''
needle='void processCommand(String cmd) {';s=s.replace(needle,runner+needle)
s=s.replace('void loop() {\n  serviceWebLease();\n  handleSerial();','void loop() {\n  serviceWebLease();\n  handleSerial();\n  runWebCalibration();')
p.write_text(s)
