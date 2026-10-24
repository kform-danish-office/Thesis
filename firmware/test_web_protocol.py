"""Execute the production browser dispatcher with mocked UART/control on Windows.

Requires the Visual Studio C++ Build Tools. Does not open hardware or flash a board.
The generated harness lives in the ignored arduino-build-web-host-tests directory.
"""
from pathlib import Path
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "thesi_power_control.ino").read_text(encoding="utf-8")
globals_code = source.split("#define WEB_FRAME_BYTES", 1)[1].split("uint16_t rawPa0Adc", 1)[0]
globals_code = "#define WEB_FRAME_BYTES" + globals_code
protocol = source.split("char *webNewFrame()", 1)[1].split("void processCommand(String cmd)", 1)[0]
protocol = "char *webNewFrame()" + protocol

prefix = r'''
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <string>
#include <algorithm>
#include <iostream>
using std::isfinite;
#define STM32F410Cx 1
#define FW_VERSION_STRING "PWR-2.0.1"
#define MCU_NAME "STM32F410CBU6"
#define CAL_LOAD_SLOT_COUNT 3
class String {
  std::string text;
public:
  String() = default;
  String(const char *s): text(s) {}
  String(std::string s): text(std::move(s)) {}
  unsigned int length() const { return (unsigned int)text.size(); }
  const char *c_str() const { return text.c_str(); }
  char charAt(unsigned int i) const { return i < text.size() ? text[i] : 0; }
  void trim() {
    auto first = text.find_first_not_of(" \r\n\t");
    if (first == std::string::npos) { text.clear(); return; }
    auto last = text.find_last_not_of(" \r\n\t");
    text = text.substr(first, last-first+1);
  }
  void toUpperCase() { for (char &c: text) if(c >= 'a' && c <= 'z') c -= 32; }
  bool startsWith(const char *s) const { return text.rfind(s, 0) == 0; }
  bool endsWith(const char *s) const {
    size_t n = strlen(s); return text.size() >= n && text.compare(text.size()-n, n, s) == 0;
  }
  int indexOf(char c) const { auto n=text.find(c); return n == std::string::npos ? -1 : (int)n; }
  String substring(unsigned int i) const { return String(i < text.size() ? text.substr(i) : ""); }
  String substring(unsigned int i,unsigned int j) const { return String(text.substr(i,j-i)); }
  bool operator==(const char *s) const { return text == s; }
};
uint32_t nowMs = 0;
uint32_t millis() { return nowMs; }
struct SerialMock {
  int capacity = 64;
  size_t maxWrite = 0;
  std::string out;
  int availableForWrite() { return capacity; }
  size_t write(const uint8_t *data, size_t count) {
    if (count > (size_t)capacity || count > 16) { std::cerr << "TX exceeded capacity"; exit(2); }
    maxWrite = std::max(maxWrite,count);
    out.append((const char *)data,count);
    return count;
  }
} CmdSerial;
enum ControlMode { MODE_OPEN_LOOP, MODE_POWER_LOOP };
enum FaultCode { FAULT_NONE, FAULT_SENSOR };
struct Settings {
  float voltageSetV=28,loadedTurnOnV=28,secMinV=10,secMaxV=32,secOvpV=36;
  uint8_t secOvpEnable=1,allowStatic100=1,lineFfEnable=0;
  uint16_t dutyMaxX10=1000,openLoopDutyX10=0,bangHighDutyX10=1000;
  uint32_t enFreqHz=10000;
} cfg;
bool systemEnabled=false, faultLatched=false, adcDmaRunning=true, filtersPrimed=true;
bool gatePwmReady=true,settingsStorageReady=true,settingsDirty=false,configImportActive=false;
bool gateOn=false, saveSucceeds=true;
FaultCode faultCode=FAULT_NONE;
ControlMode controlMode=MODE_OPEN_LOOP;
float filteredVpri=155,filteredVsec=28,filteredCurrent=0.15f,filteredPower=4.2f;
uint16_t rawPa0Adc=1274,rawPa1Adc=1160,rawPa2Adc=180;
uint32_t lastControlDtUs=25,maxControlDtUs=140,controlOverrunCount=3;
const char *modeName() { return controlMode == MODE_OPEN_LOOP ? "OPEN" : cfg.lineFfEnable ? "VSB+VIN" : "VSB"; }
const char *faultName() { return faultCode == FAULT_NONE ? "NONE" : "SENSOR"; }
float dutyX10ToPercent(uint16_t value) { return value*0.1f; }
float getEffDutyPercent() { return systemEnabled && !faultLatched ? 10.0f : 0.0f; }
void setSystemEnabled(bool enabled,bool save) { if(save) exit(3); systemEnabled=enabled; gateOn=enabled; }
void setGateOutputsEnabled(bool enabled) { gateOn=enabled; }
void updateModeLEDs() {}
void setMode(ControlMode mode,bool save) { if(save) exit(3); controlMode=mode; }
void markSettingsDirty() { settingsDirty=true; }
void applyLoadProfile(uint8_t slot,bool save) { if(slot>2 || save) exit(3); }
bool requestSettingsSave(const char *) { settingsDirty=!saveSucceeds; return saveSucceeds; }
bool parseSetParam(String name,float value) {
  if(!configImportActive) { std::cerr << "SET could write flash"; exit(4); }
  if(name == "VSET") { cfg.voltageSetV=std::max(0.0f,std::min(80.0f,value)); settingsDirty=true; return true; }
  return false;
}
'''

tests = r'''
void expect(bool condition,const char *message) { if(!condition) { std::cerr << message << '\n'; exit(1); } }
std::string drain() {
  for(unsigned int n=0; webTxCount && n<10000; ++n) serviceWebTx();
  expect(webTxCount==0,"queue failed to drain");
  std::string out=CmdSerial.out;
  CmdSerial.out.clear();
  std::cout << out;
  return out;
}
std::string run(const char *command) { processWebCommand(String(command)); return drain(); }
void has(const std::string &text,const char *needle) { expect(text.find(needle)!=std::string::npos,needle); }
int main() {
  has(run("WEB pre SNAPSHOT"),"hello_required");
  systemEnabled=true;
  has(run("WEB HELLO"),"\"type\":\"hello\"");
  expect(systemEnabled && webLeaseDurationMs==0,"hello changed existing enable or armed lease");
  systemEnabled=false;
  has(run("WEB a1 ON"),"lease_required");
  expect(!systemEnabled,"ON without lease");
  has(run("WEB a2 SET VSET nope"),"invalid_number");
  has(run("WEB a3 SET VSET NaN"),"invalid_number");
  has(run("WEB a4 SET VSET 1e30"),"invalid_number");
  has(run("WEB a5 SET VSET 28 garbage"),"invalid_number");
  has(run("WEB a6 SET FEN -1"),"negative_value_not_allowed");
  has(run("WEB a7 SET UNKNOWN 42"),"unknown_parameter");
  has(run("WEB a8 SET VSET 30"),"applied_pending");
  expect(cfg.voltageSetV==30 && settingsDirty && !configImportActive,"SET did not remain pending");
  has(run("WEB a9 SET BOOTON 1"),"boot_setting_terminal_only");
  saveSucceeds=false;
  has(run("WEB a10 SAVE"),"save_failed");
  expect(settingsDirty,"failed save cleared pending flag");
  saveSucceeds=true;
  has(run("WEB a11 SAVE"),"saved");
  has(run("WEB a12 LEASE 999"),"lease_range_");
  has(run("WEB a13 STREAM 249"),"stream_range_");
  has(run("WEB a14 LEASE 5000"),"lease_armed");
  has(run("WEB a15 STREAM 500"),"stream_enabled");
  has(run("WEB a16 ON"),"enabled");
  expect(systemEnabled,"valid ON not applied");
  has(run("WEB a17 LEASE 0"),"output_active");
  expect(webLeaseDurationMs==5000,"active lease disarmed");
  has(run("WEB a18 SAVE"),"turn_off_first");
  has(run("WEB a19 CLR"),"turn_off_first");
  nowMs=1000;
  has(run("WEB a20 PING"),"pong");
  nowMs=5999;
  serviceWebLease();
  expect(systemEnabled,"lease expired early");
  nowMs=6000;
  serviceWebLease();
  expect(!systemEnabled && !gateOn && webStreamMs==0 && webLeaseDurationMs==0 && webSessionActive,"lease did not stop output/stream quietly");
  serviceWebTelemetry();
  has(drain(),"lease_expired");
  has(run("WEB a21 PING"),"lease_not_armed");
  has(run("WEB a22 ON"),"lease_required");
  has(run("WEB a23 CAL3"),"unsupported_web_command");
  has(run("WEB a24 LEASE 5000"),"lease_armed");
  faultLatched=true; faultCode=FAULT_SENSOR;
  has(run("WEB a25 ON"),"fault_latched");
  has(run("WEB a26 CLR"),"fault_cleared");
  has(run("WEB a27 SNAPSHOT"),"\"vsec\":28.000");
  adcDmaRunning=false;
  has(run("WEB a28 ON"),"hardware_not_ready");
  has(run("WEB a29 SNAPSHOT"),"\"vsec\":null");
  adcDmaRunning=true;
  run("WEB a30 BEGINCFG");
  has(run("WEB a31 SAVE"),"end_config_first");
  has(run("WEB a32 ENDCFG"),"saved");
  CmdSerial.capacity=0;
  processWebCommand(String("WEB a33 SNAPSHOT"));
  auto previous=webTxOffset;
  serviceWebTx();
  expect(webTxOffset==previous,"TX wrote while full");
  CmdSerial.capacity=1;
  serviceWebTx();
  expect(webTxOffset==1,"TX ignored available capacity");
  CmdSerial.capacity=64;
  drain();
  run("WEB a34 OFF");
  processWebCommand(String("WEB a35 PING"));
  processWebCommand(String("WEB a36 PING"));
  processWebCommand(String("WEB a37 PING"));
  expect(webTxCount==3,"ack queue fixture");
  processWebCommand(String("WEB a38 ON"));
  expect(!systemEnabled && webTxCount==3,"mutation executed without reply capacity");
  drain();
  nowMs=0xfffffff0U;
  run("WEB a39 LEASE 1000");
  run("WEB a40 ON");
  nowMs=0x000003e0U;
  serviceWebLease();
  expect(!systemEnabled,"lease failed over millis wrap");
  serviceWebTelemetry(); drain();
  expect(CmdSerial.maxWrite<=16,"unbounded TX");
  return 0;
}
'''

out_dir = ROOT / "arduino-build-web-host-tests"
out_dir.mkdir(exist_ok=True)
cpp = out_dir / "protocol_harness.cpp"
cpp.write_text(prefix + globals_code + protocol + tests, encoding="utf-8")
vswhere = Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Microsoft Visual Studio/Installer/vswhere.exe"
installation = subprocess.check_output([
    str(vswhere), "-latest", "-products", "*", "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64", "-property", "installationPath"
], text=True).strip()
if not installation:
    raise SystemExit("Visual Studio C++ Build Tools were not found; install them to run this host harness.")
devcmd = Path(installation) / "Common7/Tools/VsDevCmd.bat"
command = f'call "{devcmd}" -arch=x64 >nul && cl /nologo /EHsc /std:c++17 /W3 /Fe:protocol_harness.exe /Fo:protocol_harness.obj protocol_harness.cpp'
compiled = subprocess.run('cmd.exe /d /s /c "' + command + '"', cwd=out_dir, capture_output=True, text=True)
if compiled.returncode:
    raise SystemExit(compiled.stdout + compiled.stderr)
result = subprocess.run([str(out_dir / "protocol_harness.exe")], cwd=out_dir, capture_output=True, text=True)
if result.returncode:
    raise SystemExit(result.stdout + result.stderr)
frames = [json.loads(line) for line in result.stdout.splitlines() if line]
assert all(frame["protocol"] == 1 for frame in frames)
assert all(len(json.dumps(frame)) < 1024 for frame in frames)
acks = {frame["id"]: frame for frame in frames if frame["type"] == "ack"}
assert acks["a7"]["ok"] is False and acks["a8"]["ok"] is True
assert acks["a10"]["ok"] is False and acks["a11"]["ok"] is True
assert "a38" not in acks
samples = [frame for frame in frames if frame["type"] == "telemetry"]
assert samples[0]["settings"]["VSET"] == 30 and samples[0]["vsec"] == 28
assert samples[1]["vsec"] is None and samples[1]["adc"] == [None, None, None]
assert sum(frame.get("event") == "lease_expired" for frame in frames) == 2
print(f"PASS: production firmware protocol; {len(frames)} JSON frames; malformed input, honest acknowledgements, save failure, enable interlocks, lease expiry/wrap, congestion, null telemetry, and bounded UART writes.")
