from pathlib import Path
p=Path('/workspace/working-source/firmware/test_web_protocol.py');s=p.read_text()
s=s.replace('protocol = "char *webNewFrame()" + protocol','''protocol = "char *webNewFrame()" + protocol.split("// WEB_CALIBRATION_RUNNER_BEGIN", 1)[0]
runner = source.split("// WEB_CALIBRATION_RUNNER_BEGIN",1)[1].split("// WEB_CALIBRATION_RUNNER_END",1)[0]''')
s=s.replace('  int availableForWrite() {', '  template<typename... A> void print(A...) {}\n  template<typename... A> void println(A...) {}\n  int availableForWrite() {')
s=s.replace('  uint32_t enFreqHz=10000;','''  uint32_t enFreqHz=10000;
  uint16_t noLoadDutyX10=250,prechargeDutyX10=100;
  bool systemEnabled=false;
  uint8_t controlMode=0;
  float lineFfRefV=100;
''')
s=s.replace('} cfg;','};\nusing SettingsSlot = Settings;\nSettings cfg;')
s=s.replace('cpp.write_text(prefix + globals_code + protocol + tests, encoding="utf-8")','''cpp.write_text(prefix + globals_code + protocol + calibration_mocks + runner + tests, encoding="utf-8")''')
# Support the actual runner/dispatcher with mock legacy algorithms, not a mock dispatcher.
pos=s.index("out_dir = ROOT")
s=s[:pos]+'''calibration_mocks = r\'\'\'
int mockAction = 0;
bool mockFail = false;
bool mockWriteGuard = false;
float latestVpriRaw=155;
void handleSerial() {
  if (mockAction == 1) { mockAction=0; processWebCommand(String("WEB calstop OFF")); }
}
void setEnFrequencyHz(uint32_t) {}
float clampFloat(float v,float lo,float hi) { return std::max(lo,std::min(hi,v)); }
void updateAnalogFilters(bool) {}
void mockLegacyTune() {
  systemEnabled=true; gateOn=true;
  nowMs+=5;
  if(!serviceWebCalibrationWait()) return;
  mockWriteGuard=webCalibrationRunning && configImportActive;
  cfg.noLoadDutyX10=321;
  settingsDirty=true;
  if(!mockFail) webCalibrationSucceeded=true;
}
void autoTunePrecharge() { mockLegacyTune(); }
void autoTunePower(bool,int8_t) { mockLegacyTune(); }
void zeroCurrentOffset() { mockWriteGuard=webCalibrationRunning && configImportActive; }
\'\'\'

'''+s[pos:]
anchor='  expect(CmdSerial.maxWrite<=16,"unbounded TX");'
new=anchor+'''
  // The production calibration dispatcher and runner, with only the legacy
  // physical sweep mocked, must preserve cancellation and RAM-only semantics.
  run("WEB callease LEASE 5000");
  run("WEB calqueued CAL NOLOAD");
  expect(webCalibrationState==1 && !systemEnabled,"calibration must queue without energizing in parser");
  has(run("WEB calbusy SET VSET 29"),"calibration_busy_use_off");
  run("WEB calqueueoff OFF");
  runWebCalibration();
  expect(webCalibrationState==4 && !systemEnabled,"queued calibration survived OFF");
  cfg.noLoadDutyX10=250; settingsDirty=false;
  run("WEB calstart CAL LOAD 2");
  expect(webCalibrationSlot==1,"load slot mismatch");
  runWebCalibration(); drain();
  expect(webCalibrationState==3 && !systemEnabled && !gateOn,"calibration completion must leave output OFF");
  expect(cfg.noLoadDutyX10==321 && settingsDirty && mockWriteGuard && !configImportActive,"calibration result must remain pending in RAM");
  cfg.noLoadDutyX10=250; settingsDirty=false; mockAction=1;
  run("WEB calabort CAL NOLOAD"); runWebCalibration(); drain();
  expect(webCalibrationState==4 && cfg.noLoadDutyX10==250 && !settingsDirty && !systemEnabled && !gateOn,"OFF did not cancel/rollback calibration");
  mockFail=true;
  run("WEB calfail CAL PRECHARGE");runWebCalibration();drain();
  expect(webCalibrationState==5 && cfg.noLoadDutyX10==250,"failed tune did not rollback");
  mockFail=false;
  run("WEB calexpired CAL NOLOAD");nowMs+=5000;runWebCalibration();
  expect(webCalibrationState==4 && !systemEnabled,"expired lease started calibration");
  run("WEB renew LEASE 5000");gatePwmReady=false;
  has(run("WEB calhw CAL NOLOAD"),"calibration_hardware_not_ready");gatePwmReady=true;
  has(run("WEB calslot CAL LOAD 4"),"load_range_1_3");
'''
assert anchor in s;s=s.replace(anchor,new)
p.write_text(s)
