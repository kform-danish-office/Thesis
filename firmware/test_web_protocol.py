"""Execute the production browser dispatcher with mocked UART/control.

Uses GCC/Clang on Linux or Visual Studio C++ Build Tools on Windows.
Does not open hardware or flash a board.
The generated harness lives in the ignored arduino-build-web-host-tests directory.
"""
from pathlib import Path
import json
import os
import subprocess
import shutil

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "thesi_power_control.ino").read_text(encoding="utf-8")
globals_code = source.split("#define WEB_FRAME_BYTES", 1)[1].split("uint16_t rawPa0Adc", 1)[0]
globals_code = "#define WEB_FRAME_BYTES" + globals_code
protocol = source.split("char *webNewFrame()", 1)[1].split("void processCommand(String cmd)", 1)[0]
protocol = "char *webNewFrame()" + protocol.split("// WEB_CALIBRATION_RUNNER_BEGIN", 1)[0]
runner = source.split("// WEB_CALIBRATION_RUNNER_BEGIN",1)[1].split("// WEB_CALIBRATION_RUNNER_END",1)[0]

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
  bool operator!=(const char *s) const { return text != s; }
};
uint32_t nowMs = 0;
uint32_t millis() { return nowMs; }
struct SerialMock {
  int capacity = 64;
  size_t maxWrite = 0;
  std::string out;
  template<typename... A> void print(A...) {}
  template<typename... A> void println(A...) {}
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
// PRODUCTION_SETTINGS_TYPE
SettingsSlot cfg = {};
bool autoTuneRunning=false;
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
void applyLoadProfile(uint8_t slot,bool save);
bool requestSettingsSave(const char *) { settingsDirty=!saveSucceeds; return saveSucceeds; }
bool parseSetParam(String name,float value) {
  if(!configImportActive) { std::cerr << "SET could write flash"; exit(4); }
  if(name == "VSET") { cfg.voltageSetV=std::max(0.0f,std::min(80.0f,value)); settingsDirty=true; return true; }
  if(name == "LOAD1" || name == "LOAD2" || name == "LOAD3") {
    unsigned int slot=(unsigned int)(name.charAt(4)-'1');
    cfg.calLoadOhms[slot]=std::max(0.0f,std::min(100000.0f,value));settingsDirty=true;return true;
  }
  return false;
}
'''

# Keep HELLO metadata aligned with the production build rather than a stale test version.
prefix = prefix.replace('#define FW_VERSION_STRING "PWR-2.0.1"', '#define FW_VERSION_STRING "' + source.split('#define FW_VERSION_STRING "', 1)[1].split('"', 1)[0] + '"')
settings_type = "#pragma pack(push, 1)\nstruct SettingsSlot {" + source.split("struct __attribute__((packed)) SettingsSlot {",1)[1].split("\n};",1)[0] + "\n};\n#pragma pack(pop)\n"
prefix = prefix.replace("// PRODUCTION_SETTINGS_TYPE", settings_type, 1)

def production_region(name):
    return source.split("// " + name + "_BEGIN",1)[1].split("// " + name + "_END",1)[0]

timing_constants = "\n".join(line for line in source.splitlines() if line.startswith(("#define CARRIER_MIN_", "#define CARRIER_MAX_", "#define CARRIER_DEAD_")))
timing_math = timing_constants + production_region("CARRIER_TIMING_MATH")
timing_hardware = r'''
#define EN_FREQ_MIN_HARD_HZ 1000UL
#define EN_FREQ_MAX_HARD_HZ 50000UL
#define EN_MIN_EDGE_HARD_US 1UL
#define EN_MAX_EDGE_HARD_US 20UL
#define EN_MIN_GATE_CYCLES_MIN 1UL
#define EN_MIN_GATE_CYCLES_MAX 40UL
#define EN_GATE_LEAD_CYCLES_MIN 0UL
#define EN_GATE_LEAD_CYCLES_MAX 40UL
#define EN_GATE_TAIL_CYCLES 1UL
#define TIM_BDTR_MOE (1UL<<15)
#define TIM_CR1_CEN 1UL
#define TIM_CR1_ARPE (1UL<<7)
CarrierTiming carrierTiming = {100000000,100,50,4};
uint32_t carrierRequestedHz=1000000,carrierRequestedDeadNs=40,carrierTimingRevision=0;
struct RegisterMock {
  uint32_t value;
  bool ignoreWrites=false;
  operator uint32_t() const { return value; }
  RegisterMock &operator=(uint32_t next) { if(!ignoreWrites) value=next; return *this; }
};
struct TimerMock {
  RegisterMock ARR={99};
  uint32_t BDTR=(1UL<<15)|4,CR1=1,DIER=0,PSC=0,CNT=0,RCR=0,CCR1=50,CCR2=0,EGR=0,SR=0;
} timerMock;
TimerMock *TIM1=&timerMock;
uint32_t irqMask=0,timerApplyCount=0;
bool startupActive=false,injectBusyOnIrqDisable=false;
uint32_t __get_PRIMASK() { return irqMask; }
void __disable_irq() { irqMask=1;if(injectBusyOnIrqDisable) startupActive=true; }
void __enable_irq() { irqMask=0; }
uint32_t carrierTimerClockHz() { return 100000000; }
bool startupPrechargeActive() { return startupActive; }
uint16_t enDutyCmdX10=0,enDutyEffX10=0,enHighGateCycles=8,enPulseSkipN=1,enPulseSkipCountdown=0;
bool enDutyLimitBypass=false;
uint32_t enFreqRuntimeHz=10000,enPeriodUs=100,enHighUs=0;
void forceEnSyncLowNow() { gateOn=false; }
void setEnLow() { gateOn=false; }
void setGateCarrierDrive(bool) { TIM1->BDTR|=TIM_BDTR_MOE; }
void applyEnableTimerNoInterruptLock(bool) { ++timerApplyCount; }
uint32_t clampU32(uint32_t value,uint32_t minimum,uint32_t maximum) { return std::max(minimum,std::min(value,maximum)); }
'''
timing_hardware += "bool carrierTimingBusy() {" + source.split("bool carrierTimingBusy() {",1)[1].split("\n}",1)[0] + "\n}\n"
timing_hardware += "uint32_t gateCyclesToUsCeil(" + source.split("uint32_t gateCyclesToUsCeil(",1)[1].split("void setTim1CarrierSyncIrq(",1)[0]
timing_hardware += "uint32_t clampEnFreq(" + source.split("uint32_t clampEnFreq(",1)[1].split("uint32_t enCompareUsForTimer(",1)[0]
timing_apply = production_region("CARRIER_TIMING_APPLY")
load_profile_code = "void setEnFrequencyHz(uint32_t);\nvoid saveSettings() { std::cerr << \"Unexpected direct profile save\"; exit(4); }\n"
load_profile_code += "bool validLoadSlot(" + source.split("bool validLoadSlot(",1)[1].split("float calLoadOhms(",1)[0]
load_profile_code += "bool loadProfileValid(" + source.split("bool loadProfileValid(",1)[1].split("void ledWrite(",1)[0]
load_profile_code += "void applyLoadProfile(" + source.split("void applyLoadProfile(",1)[1].split("void autoTunePower(",1)[0]


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
  cfg.voltageSetV=cfg.loadedTurnOnV=28;cfg.secMinV=10;cfg.secMaxV=32;cfg.secOvpV=36;cfg.secOvpEnable=1;
  cfg.allowStatic100=1;cfg.dutyMaxX10=cfg.bangHighDutyX10=1000;cfg.enFreqHz=10000;
  cfg.enFreqMinHz=1000;cfg.enFreqMaxHz=50000;cfg.enMinGateCycles=8;cfg.enMinEdgeUs=1;
  cfg.calLoadOhms[0]=50;cfg.calLoadOhms[1]=100;cfg.calLoadOhms[2]=200;
  cfg.autotuneMaxDutyX10=1000;cfg.autotuneCoarseStepX10=50;cfg.autotuneFineStepX10=10;
  cfg.autotuneSettleMs=cfg.autotuneMeasureMs=200;cfg.prechargeBurstMs=10;cfg.prechargeSettleMs=100;
  cfg.prechargeMaxBursts=3;cfg.noLoadDutyX10=250;cfg.prechargeDutyX10=100;
  cfg.lineFfRefV=100;cfg.currentOffsetV=0.1f;
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
  systemEnabled=true;gateOn=true;
  processWebCommand(String("WEB full1 PING"));
  processWebCommand(String("WEB full2 PING"));
  processWebCommand(String("WEB full3 PING"));
  processWebCommand(String("WEB stopfull OFF"));
  expect(!systemEnabled && !gateOn,"OFF must stop even during TX congestion");drain();
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
  mockAction=2;
  run("WEB calleaseabort CAL NOLOAD"); runWebCalibration(); drain();
  expect(webCalibrationState==4 && cfg.noLoadDutyX10==250 && !systemEnabled && !gateOn,"active lease expiry did not rollback/stop");
  run("WEB calrenew LEASE 5000");
  mockAction=3;
  run("WEB calfault CAL NOLOAD");runWebCalibration();drain();
  expect(faultLatched && webCalibrationState==4 && !systemEnabled && !gateOn && cfg.noLoadDutyX10==250,"fault cancellation did not stop/rollback");
  run("WEB calclear CLR");
  mockAction=4;
  run("WEB caltimeout CAL NOLOAD");runWebCalibration();drain();
  expect(webCalibrationState==4 && !systemEnabled && cfg.noLoadDutyX10==250,"maximum calibration duration not enforced");
  mockFail=true;
  run("WEB calfail CAL PRECHARGE");runWebCalibration();drain();
  expect(webCalibrationState==5 && cfg.noLoadDutyX10==250,"failed tune did not rollback");
  mockFail=false;
  run("WEB calexpired CAL NOLOAD");nowMs+=5000;runWebCalibration();
  expect(webCalibrationState==4 && !systemEnabled,"expired lease started calibration");
  run("WEB renew LEASE 5000");gatePwmReady=false;
  has(run("WEB calhw CAL NOLOAD"),"calibration_hardware_not_ready");gatePwmReady=true;
  has(run("WEB calslot CAL LOAD 4"),"load_range_1_3");
  has(run("WEB benchset SET LOAD2 120"),"applied_pending");
  expect(cfg.calLoadOhms[1]==120 && settingsDirty,"OFF load resistance change/readback pending");
  has(run("WEB benchslot LOAD 2"),"applied_pending");
  expect(cfg.activeCalLoadSlot==1,"profile selection/readback mismatch");
  std::string bench=run("WEB benchsnapshot SNAPSHOT");
  has(bench,"\"LOAD2\":120.000");has(bench,"\"ACTLOAD\":2");
  has(bench,"\"AUTOSTEP\":5.000");has(bench,"\"AUTOSETTLE\":200");
  run("WEB benchon ON");
  for (const char *name : {"LOAD1","LOAD2","LOAD3","ACTIVELOAD","LOADSLOT","NLDUTY","AUTOMAX","AUTOSTEP","AUTOFINE","AUTOSETTLE","AUTOMEAS","PREMS","PRESETTLE","PREMAX","PREAUTOMAX","L1FEN"}) {
    std::string command="WEB benchbusy SET ";command+=name;command+=" 12";
    has(run(command.c_str()),"turn_off_first");
  }
  has(run("WEB benchbusyload LOAD 1"),"turn_off_first");
  expect(cfg.calLoadOhms[1]==120 && cfg.activeCalLoadSlot==1,"ON load mutation applied");
  // Live voltage changes retain their prior semantics.
  has(run("WEB benchlive SET VSET 29"),"applied_pending");
  run("WEB benchoff OFF");
  has(run("WEB benchnegative SET LOAD1 -1"),"negative_value_not_allowed");
  has(run("WEB benchbadslot LOAD 4"),"load_range_1_3");
  // The production pair math, scheduler and atomic register-apply function
  // run behind only the timer/IRQ primitives mocked above.
  CarrierTiming math;
  expect(calculateCarrierTiming(100000000,500000,40,math) && math.periodTicks==200 && math.ccr==100 && math.deadTicks==4,"500k timing");
  expect(calculateCarrierTiming(100000000,1000000,40,math) && math.periodTicks==100 && math.ccr==50,"default timing");
  expect(calculateCarrierTiming(100000000,2000000,120,math) && math.periodTicks==50 && math.deadTicks==12,"highest valid pair");
  expect(!calculateCarrierTiming(100000000,2000000,130,math),"overlapping pair accepted");
  expect(calculateCarrierTiming(100000000,500000,200,math) && math.deadTicks==20,"long deadtime at low carrier");
  expect(calculateCarrierTiming(100000000,1000000,21,math) && math.deadTicks==3,"deadtime must round up");
  expect(!calculateCarrierTiming(100000000,499999,40,math) && !calculateCarrierTiming(100000000,2000001,40,math),"frequency bounds");
  expect(!calculateCarrierTiming(100000000,1000000,19,math) && !calculateCarrierTiming(100000000,1000000,201,math),"deadtime bounds");
  expect(calculateCarrierTiming(100000000,980392,40,math) && math.periodTicks==102,"nearest even period");
  expect(carrierCyclesToUsCeil(8,math)==9 && carrierCyclesFromUsCeil(2,math)==2,"exact rational cycle conversion");
  for(uint32_t hz=500000;hz<=2000000;hz+=7919) {
    for(uint32_t ns=20;ns<=200;++ns) {
      if(!calculateCarrierTiming(100000000,hz,ns,math)) continue;
      expect(math.periodTicks%2==0 && math.ccr*2==math.periodTicks && math.deadTicks*4<math.periodTicks,"balanced positive gate pulses");
      expect(uint64_t(math.deadTicks)*1000000000ULL>=uint64_t(ns)*math.timerHz,"deadtime rounded below request");
      expect(math.deadTicks==1 || uint64_t(math.deadTicks-1)*1000000000ULL<uint64_t(ns)*math.timerHz,"deadtime not minimal ceil");
    }
  }
  has(run("WEB timingbad TIMING 1000000 NaN"),"use_timing_hz_ns_integers");
  has(run("WEB timingfraction TIMING 1000000 20.1"),"use_timing_hz_ns_integers");
  has(run("WEB timingnegative TIMING -1 40"),"use_timing_hz_ns_integers");
  has(run("WEB timingoverflow TIMING 4294967296 40"),"use_timing_hz_ns_integers");
  has(run("WEB timingextra TIMING 1000000 40 50"),"use_timing_hz_ns_integers");
  has(run("WEB timingrange TIMING 3000000 40"),"timing_pair_not_representable");
  has(run("WEB timingpair TIMING 2000000 130"),"timing_pair_not_representable");
  expect(carrierRequestedHz==1000000 && TIM1->ARR==99,"rejected pair changed registers");
  systemEnabled=true;gateOn=true;
  has(run("WEB timingon TIMING 500000 40"),"turn_off_first");
  expect(systemEnabled && gateOn && TIM1->ARR==99,"active timing mutation touched output");
  systemEnabled=false;gateOn=false;startupActive=true;
  has(run("WEB timingstartup TIMING 500000 40"),"turn_off_first");startupActive=false;
  autoTuneRunning=true;has(run("WEB timingautotune TIMING 500000 40"),"turn_off_first");autoTuneRunning=false;
  webCalibrationState=1;has(run("WEB timingcal TIMING 500000 40"),"calibration_busy_use_off");webCalibrationState=0;
  settingsStorageReady=false;has(run("WEB timingstorage TIMING 500000 40"),"hardware_not_ready");settingsStorageReady=true;
  cfg.calLoadTargetW[0]=10;cfg.calLoadDutyX10[0]=250;cfg.calLoadGainWPerPct[0]=1;cfg.tunedTargetW=10;
  cfg.bangHighDutyX10=500;cfg.noLoadDutyX10=250;webCalibrationState=3;webCalibrationDuty=250;
  std::string timing=run("WEB timingapply TIMING 500000 21");
  has(timing,"timing_applied_pending");has(timing,"\"type\":\"timing\"");has(timing,"\"actual_dead_ns\":30");
  expect(!systemEnabled && !gateOn && TIM1->ARR==199 && TIM1->CCR1==100 && TIM1->CCR2==0 && TIM1->RCR==0,"atomic V2 timer install");
  expect((TIM1->CR1 & TIM_CR1_CEN) && (TIM1->BDTR & TIM_BDTR_MOE) && TIM1->PSC==0 && TIM1->SR==0,"carrier did not resume with EN low");
  expect(irqMask==0 && settingsDirty && carrierTimingRevision==1 && timerApplyCount==1,"timing scheduler/IRQ/pending transaction");
  expect(webCalibrationState==0 && webCalibrationDuty==0,"old calibration completion survived timing change");
  expect(cfg.calLoadTargetW[0]==0 && cfg.calLoadDutyX10[0]==0 && cfg.tunedTargetW==0 && cfg.calLoadOhms[0]==50,"stale learned calibration survived actual timing change");
  expect(cfg.bangHighDutyX10==500 && cfg.noLoadDutyX10==250,"timing silently changed applied duty settings");
  expect(!loadProfileValid(0),"production validity check accepted cleared calibration");
  has(run("WEB timingload LOAD 1"),"applied_pending");
  expect(cfg.bangHighDutyX10==500 && cfg.tunedTargetW==0,"LOAD reapplied a profile from previous carrier timing");
  cfg.calLoadTargetW[0]=10;cfg.calLoadDutyX10[0]=250;cfg.tunedTargetW=10;
  has(run("WEB timingsame TIMING 500001 29"),"timing_applied_pending");
  expect(cfg.calLoadTargetW[0]==10 && cfg.calLoadDutyX10[0]==250 && cfg.tunedTargetW==10,"same quantized pair invalidated profiles");
  irqMask=1;expect(applyCarrierTiming(500001,29)==nullptr && irqMask==1,"atomic application changed caller interrupt mask");irqMask=0;
  enDutyCmdX10=10;cfg.enGateLeadCycles=0;
  has(run("WEB timingschedule TIMING 2000000 40"),"timing_applied_pending");
  expect(enHighUs==4 && enHighGateCycles==8 && enPulseSkipN==4,"2MHz minimum burst/pulse skip did not use actual timing");
  has(run("WEB timingschedule2 TIMING 980392 40"),"timing_applied_pending");
  expect(enHighUs==9 && enHighGateCycles==9 && enPulseSkipN==9,"noninteger carrier burst/pulse skip did not use exact period");
  run("WEB timingfreshlease LEASE 5000");webLeaseExpiredEvent=false;webFaultEventPending=false;
  CmdSerial.capacity=0;webStreamMs=250;nowMs+=250;
  processWebCommand(String("WEB timingqueue PING"));serviceWebTelemetry();
  expect(webTxCount==1,"periodic timing pair consumed reserved reply slots");CmdSerial.capacity=64;drain();
  nowMs+=250;serviceWebTelemetry();expect(webTxCount==2,"periodic telemetry/timing pair missing");drain();
  processWebCommand(String("WEB tfull1 PING"));processWebCommand(String("WEB tfull2 PING"));processWebCommand(String("WEB tfull3 PING"));
  auto previousTiming=carrierRequestedHz;processWebCommand(String("WEB timingfull TIMING 500000 40"));
  expect(carrierRequestedHz==previousTiming && webTxCount==3,"timing mutation ran without paired response space");drain();
  run("WEB timingreset TIMING 1000000 40");enDutyCmdX10=0;webStreamMs=0;
  injectBusyOnIrqDisable=true;
  expect(std::string(applyCarrierTiming(500000,40))=="turn_off_first" && irqMask==0 && TIM1->ARR==99,"OFF condition was not rechecked under interrupt lock");
  injectBusyOnIrqDisable=false;startupActive=false;
  TIM1->ARR.ignoreWrites=true;auto oldRequested=carrierRequestedHz;
  expect(std::string(applyCarrierTiming(500000,40))=="timing_readback_failed","hardware readback failure accepted");
  expect(!systemEnabled && !gateOn && !gatePwmReady && faultLatched && !(TIM1->BDTR & TIM_BDTR_MOE) && !(TIM1->CR1 & TIM_CR1_CEN),"failed timing install did not leave EN/MOE/CEN off");
  expect(carrierRequestedHz==oldRequested && irqMask==0,"failed hardware transaction published new request or left IRQ disabled");
  TIM1->ARR.ignoreWrites=false;gatePwmReady=true;faultLatched=false;faultCode=FAULT_NONE;
  expect(applyCarrierTiming(1000000,40)==nullptr,"reinitialized hardware fixture failed");

  // Exercise the real serializer with maximum supported bench settings,
  // long numeric measurements and saturated diagnostic counters.
  expect(applyCarrierTiming(500000,200)==nullptr,"maximum serializer timing fixture");
  cfg.calLoadOhms[0]=cfg.calLoadOhms[1]=cfg.calLoadOhms[2]=100000;
  cfg.activeCalLoadSlot=2;cfg.noLoadDutyX10=1000;cfg.autotuneMaxDutyX10=1000;
  cfg.autotuneCoarseStepX10=250;cfg.autotuneFineStepX10=100;
  cfg.autotuneSettleMs=3000;cfg.autotuneMeasureMs=2000;
  cfg.prechargeBurstMs=500;cfg.prechargeSettleMs=2000;cfg.prechargeMaxBursts=20;
  filteredVpri=999.999f;filteredVsec=79.999f;filteredCurrent=199.999f;filteredPower=1999999;
  lastControlDtUs=maxControlDtUs=controlOverrunCount=0xffffffffU;
  cfg.voltageSetV=cfg.loadedTurnOnV=cfg.secMaxV=cfg.secOvpV=80;cfg.secMinV=79.5f;
  cfg.openLoopDutyX10=cfg.bangHighDutyX10=cfg.prechargeDutyX10=1000;
  cfg.enFreqHz=50000;cfg.currentOffsetV=-1;cfg.lineFfRefV=1000;
  rawPa0Adc=rawPa1Adc=rawPa2Adc=4095;
  filteredVpri=filteredVsec=filteredCurrent=filteredPower=-1999999;
  controlMode=MODE_POWER_LOOP;cfg.lineFfEnable=1;faultCode=FAULT_SENSOR;
  webCalibrationState=5;webCalibrationKind=4;webCalibrationSlot=2;webCalibrationDuty=1000;
  carrierTimingRevision=0xffffffffU;
  nowMs=0xffffffffU;webLeaseDurationMs=10000;webLastPingMs=nowMs;webStreamMs=5000;

  std::string maximum=run("WEB abcdefghijklmnopqrstuvwx SNAPSHOT");has(maximum,"\"PREMAX\":20");
  has(maximum,"\"LOAD3\":100000.000");has(maximum,"\"control_overruns\":4294967295");


  return 0;
}
'''

calibration_mocks = r'''
int mockAction = 0;
bool mockFail = false;
bool mockWriteGuard = false;
float latestVpriRaw=155;
void handleSerial() {
  if (mockAction == 3) { mockAction=0; faultLatched=true; }
  if (mockAction == 4) { mockAction=0; nowMs+=180001;webLastPingMs=nowMs; }
  if (mockAction == 2) { mockAction=0; nowMs+=5000; }
  if (mockAction == 1) { mockAction=0; processWebCommand(String("WEB calstop OFF")); }
}
void setEnFrequencyHz(uint32_t) {}
float clampFloat(float v,float lo,float hi) { return std::max(lo,std::min(hi,v)); }
void updateAnalogFilters(bool) {}
bool checkFaults() { return faultLatched; }
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
'''

out_dir = ROOT / "arduino-build-web-host-tests"
out_dir.mkdir(exist_ok=True)
cpp = out_dir / "protocol_harness.cpp"
cpp.write_text(prefix + timing_math + globals_code + timing_hardware + timing_apply + load_profile_code + protocol + calibration_mocks + runner + tests, encoding="utf-8")
if os.name == "nt":
    vswhere = Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "Microsoft Visual Studio/Installer/vswhere.exe"
    installation = subprocess.check_output([
        str(vswhere), "-latest", "-products", "*", "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64", "-property", "installationPath"
    ], text=True).strip()
    if not installation:
        raise SystemExit("Visual Studio C++ Build Tools were not found.")
    devcmd = Path(installation) / "Common7/Tools/VsDevCmd.bat"
    command = f'call "{devcmd}" -arch=x64 >nul && cl /nologo /EHsc /std:c++17 /W3 /Fe:protocol_harness.exe /Fo:protocol_harness.obj protocol_harness.cpp'
    compiled = subprocess.run('cmd.exe /d /s /c "' + command + '"', cwd=out_dir, capture_output=True, text=True)
    executable = out_dir / "protocol_harness.exe"
else:
    compiler = shutil.which("g++") or shutil.which("clang++")
    if not compiler:
        raise SystemExit("Install g++ or clang++ to run the native protocol harness.")
    executable = out_dir / "protocol_harness"
    compiled = subprocess.run([compiler,"-std=c++17","-Wall","-Wextra","-O2",str(cpp),"-o",str(executable)],cwd=out_dir,capture_output=True,text=True)
if compiled.returncode:
    raise SystemExit(compiled.stdout + compiled.stderr)
result = subprocess.run([str(executable)], cwd=out_dir, capture_output=True, text=True)
if result.returncode:
    raise SystemExit(result.stdout + result.stderr)
frames = [json.loads(line) for line in result.stdout.splitlines() if line]
assert all(frame["protocol"] == 1 for frame in frames)
assert all(len(line.encode("utf-8")) < 1024 for line in result.stdout.splitlines() if line)
assert all(len(json.dumps(frame)) < 1024 for frame in frames)
assert "carrier_timing_v1" in next(frame for frame in frames if frame["type"] == "hello")["capabilities"]
assert any(frame["type"] == "timing" and frame.get("id") == "timingapply" and frame["timing"]["period_ticks"] == 200 for frame in frames)
assert "bench_settings_v1" in next(frame for frame in frames if frame["type"] == "hello")["capabilities"]
assert next(frame for frame in frames if frame["type"] == "telemetry" and frame["settings"].get("PREMAX") == 20)["settings"]["LOAD3"] == 100000
acks = {frame["id"]: frame for frame in frames if frame["type"] == "ack"}
assert acks["a7"]["ok"] is False and acks["a8"]["ok"] is True
assert acks["a10"]["ok"] is False and acks["a11"]["ok"] is True
assert "a38" not in acks
samples = [frame for frame in frames if frame["type"] == "telemetry"]
assert samples[0]["settings"]["VSET"] == 30 and samples[0]["vsec"] == 28
assert samples[1]["vsec"] is None and samples[1]["adc"] == [None, None, None]
assert sum(frame.get("event") == "lease_expired" for frame in frames) == 3
print(f"PASS: production firmware protocol; {len(frames)} JSON frames; malformed input, honest acknowledgements, save failure, enable interlocks, lease expiry/wrap, congestion, null telemetry, bounded UART writes, cooperative calibration queue/OFF/lease/rollback/RAM-only behavior; V2 timing math, coupled bounds, exact cycle scheduling, OFF/busy interlocks, atomic apply, profile invalidation, and fresh readback.")
