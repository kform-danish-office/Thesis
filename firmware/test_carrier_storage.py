"""Run the production V2 journal loader, writer and integrity checks without hardware.

Uses a native C++ compiler; only STM32 HAL flash calls, unrelated settings
validation/defaults and serial/time are mocked. No board is opened or flashed.
"""
from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "thesi_power_control.ino").read_text(encoding="utf-8")


def region(name):
    return SOURCE.split(f"// {name}_BEGIN", 1)[1].split(f"// {name}_END", 1)[0]


def function(name):
    match = re.search(r"^[^\n;{}]*\b" + re.escape(name) + r"\([^;{}]*\)\s*\{", SOURCE, re.M)
    if not match:
        raise RuntimeError(f"Production function missing: {name}")
    end = match.end()
    depth = 1
    while depth:
        if SOURCE[end] == "{":
            depth += 1
        elif SOURCE[end] == "}":
            depth -= 1
        end += 1
    return SOURCE[match.start():end] + "\n"


settings_type = SOURCE.split("struct __attribute__((packed)) SettingsSlot {", 1)[1].split("\n};", 1)[0]
settings_type = "struct __attribute__((packed)) SettingsSlot {" + settings_type + "\n};\n"
constants = "\n".join(re.findall(r"^#define (?:CARRIER_(?:MIN_HZ|MAX_HZ|DEAD_MIN_NS|DEAD_MAX_NS)|GATE_FREQ_HZ|GATE_DEADTIME_NS|EEPROM_MAGIC|EEPROM_BASE_ADDR|SETTINGS_FLASH_BYTES)\s+[^\n]+", SOURCE, re.M))
# Keep the on-flash stride independent from the packed legacy payload length.
legacy_stride = "#define LEGACY_SETTINGS_RECORD_BYTES ((sizeof(SettingsSlot) + 3UL) & ~3UL)\n"
for line in SOURCE.splitlines():
    if line.startswith("#define LEGACY_") and ("RECORD_BYTES" in line or "SLOT_BYTES" in line):
        legacy_stride += line + "\n"

prefix = r'''
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>
#define STM32F410Cx 1
#define CAL_LOAD_SLOT_COUNT 3
#define HAL_OK 0
#define HAL_ERROR 1
#define FLASH_FLAG_EOP 0
#define FLASH_FLAG_OPERR 0
#define FLASH_FLAG_WRPERR 0
#define FLASH_FLAG_PGAERR 0
#define FLASH_FLAG_PGPERR 0
#define FLASH_FLAG_PGSERR 0
#define FLASH_TYPEERASE_SECTORS 1
#define FLASH_SECTOR_1 1
#define FLASH_VOLTAGE_RANGE_3 3
#define FLASH_TYPEPROGRAM_WORD 1
#define FLASH_ACR_DCEN 1
#define __HAL_FLASH_CLEAR_FLAG(...) ((void)0)
#define __HAL_FLASH_DATA_CACHE_DISABLE() ((void)0)
#define __HAL_FLASH_DATA_CACHE_RESET() ((void)0)
#define __HAL_FLASH_DATA_CACHE_ENABLE() ((void)0)
void expect(bool condition, const char *message) {
  if (!condition) { std::cerr << message << '\n'; std::exit(1); }
}
'''
state = r'''
#define SETTINGS_RECORD_BYTES ((sizeof(CarrierSettingsRecord) + 3UL) & ~3UL)
#define EEPROM_SLOT_COUNT ((int)(SETTINGS_FLASH_BYTES / SETTINGS_RECORD_BYTES))
alignas(4) std::array<uint8_t, SETTINGS_FLASH_BYTES> flashBytes;
#define SETTINGS_FLASH_BASE (reinterpret_cast<uintptr_t>(flashBytes.data()))
struct { uint32_t ACR = FLASH_ACR_DCEN; } flashRegs;
#define FLASH (&flashRegs)
struct FLASH_EraseInitTypeDef {
 uint32_t TypeErase=0, Sector=0, NbSectors=0, VoltageRange=0;
};
unsigned int unlocks=0, locks=0, erases=0, programs=0;
int failProgramAfter=-1;
bool settingsStorageReady=true;
bool systemEnabled=false, autoTuneRunning=false, webCalibrationRunning=false;
bool startupActive=false, webSessionActive=true, settingsDirty=false, configImportActive=false;
uint32_t settingsSequence=0, settingsDirtyMs=0;
int activeSlotIndex=-1;
uint32_t carrierRequestedHz=GATE_FREQ_HZ, carrierRequestedDeadNs=GATE_DEADTIME_NS;
SettingsSlot cfg = {};
enum ControlMode { MODE_OPEN_LOOP=0, MODE_POWER_LOOP=1 };
ControlMode controlMode=MODE_OPEN_LOOP;
struct { void println(const char *) {} } CmdSerial;
uint32_t millis() { return 12345; }
uint32_t carrierTimerClockHz() { return 100000000; }
bool startupPrechargeActive() { return startupActive; }
int HAL_FLASH_Unlock() { ++unlocks; return HAL_OK; }
int HAL_FLASH_Lock() { ++locks; return HAL_OK; }
int HAL_FLASHEx_Erase(FLASH_EraseInitTypeDef *request, uint32_t *) {
 expect(request->Sector==FLASH_SECTOR_1 && request->NbSectors==1, "Wrong flash sector erased");
 ++erases; flashBytes.fill(0xFF); return HAL_OK;
}
int HAL_FLASH_Program(uint32_t type, uintptr_t address, uint64_t word) {
 expect(type==FLASH_TYPEPROGRAM_WORD, "Wrong programming unit");
 expect(address>=SETTINGS_FLASH_BASE && address+4<=SETTINGS_FLASH_BASE+flashBytes.size(), "Out-of-bounds flash program");
 if(failProgramAfter==0) return HAL_ERROR;
 if(failProgramAfter>0) --failProgramAfter;
 auto *destination = reinterpret_cast<uint8_t *>(address);
 for(unsigned int i=0;i<4;++i) {
   uint8_t byte=(uint8_t)(word>>(8*i));
   expect((destination[i] & byte)==byte, "Flash attempted zero-to-one without erase");
   destination[i] &= byte;
 }
 ++programs; return HAL_OK;
}
void setDefaults() {
 std::memset(&cfg,0,sizeof(cfg)); cfg.magic=EEPROM_MAGIC;
 cfg.voltageSetV=28; cfg.enFreqHz=10000; cfg.calLoadOhms[0]=50;
}
void validateSettings() {
 // Out-of-scope physical settings validation is mocked; preserve all calibration
 // bytes so migration comparisons expose even a one-byte payload shift.
 controlMode=(ControlMode)cfg.controlMode;
}
bool safeToWriteEepromNow();
'''
tests = r'''
SettingsSlot legacyFixture(uint32_t sequence, float marker) {
 SettingsSlot value={}; value.magic=EEPROM_MAGIC; value.sequence=sequence;
 value.voltageSetV=marker; value.calLoadOhms[0]=120;
 value.calLoadFreqHz[0]=10000; value.calLoadDutyX10[0]=321;
 value.calLoadKp_x1000[0]=456; value.calLoadKi_x1000[0]=789;
 value.calLoadGainWPerPct[0]=1.25f; value.calLoadTauS[0]=0.125f;
 value.calLoadTargetW[0]=20; value.calLoadMeasuredW[0]=19.5f;
 value.calLoadMeasuredVsec[0]=28; value.calLoadMeasuredI[0]=0.7f;
 value.tunedPlantGainWPerPct=1.25f; value.tunedPlantTauS=.125f;
 value.tunedDutyX10=321; value.tunedTargetW=20;
 value.checksum=checksumSettings(value); return value;
}
CarrierSettingsRecord wrapperFixture(uint32_t sequence,float marker,uint32_t hz=1500000,uint32_t ns=70) {
 CarrierSettingsRecord record={}; record.magic=CARRIER_RECORD_MAGIC;
 record.settings=legacyFixture(sequence,marker); record.reserved=0xFF; record.carrierHz=hz; record.deadNs=ns;
 record.checksum=checksumCarrierRecord(record); return record;
}
void reset() {
 flashBytes.fill(0xFF); cfg={}; settingsSequence=0; activeSlotIndex=-1;
 settingsDirty=false; systemEnabled=false; startupActive=false;
 autoTuneRunning=webCalibrationRunning=false; controlMode=MODE_OPEN_LOOP;
 carrierRequestedHz=GATE_FREQ_HZ; carrierRequestedDeadNs=GATE_DEADTIME_NS;
 settingsStorageReady=true; failProgramAfter=-1;
 unlocks=locks=erases=programs=0;
}
void putLegacy(unsigned int slot,const SettingsSlot &value) {
 std::memcpy(flashBytes.data()+slot*LEGACY_SETTINGS_RECORD_BYTES,&value,sizeof(value));
}
void putWrapper(unsigned int slot,const CarrierSettingsRecord &value) {
 std::memcpy(flashBytes.data()+slotAddress(slot),&value,sizeof(value));
}
void reboot() {
 cfg={}; settingsSequence=0; activeSlotIndex=-1;
 carrierRequestedHz=765432; carrierRequestedDeadNs=199;
 settingsDirty=false; systemEnabled=false; loadSettings();
}
void loadDoesNotWrite() {
 auto previous=flashBytes; auto writeCount=programs,eraseCount=erases,unlockCount=unlocks;
 reboot(); expect(flashBytes==previous && programs==writeCount && erases==eraseCount && unlocks==unlockCount,
  "Boot/load touched flash");
}
int main() {
 expect(sizeof(SettingsSlot)==471,"Legacy packed payload size changed");
 expect(LEGACY_SETTINGS_RECORD_BYTES==472,"Legacy flash stride changed");
 expect(sizeof(CarrierSettingsRecord)==488,"Wrapper stride changed");
 reset(); loadDoesNotWrite();
 expect(cfg.voltageSetV==28 && activeSlotIndex==-1,"Empty flash defaults failed");
 expect(carrierRequestedHz==1000000 && carrierRequestedDeadNs==40,"Empty flash timing defaults failed");

 reset(); auto older=legacyFixture(7,27), newest=legacyFixture(8,29);
 putLegacy(0,older); putLegacy(1,newest); loadDoesNotWrite();
 expect(settingsSequence==8 && std::memcmp(&cfg,&newest,sizeof(cfg))==0,"Legacy calibration migration changed payload");
 expect(carrierRequestedHz==1000000 && carrierRequestedDeadNs==40,"Legacy timing not defaulted");
 expect(activeSlotIndex==1,"Legacy occupancy not mapped onto new stride");
 auto legacyBefore=flashBytes;
 carrierRequestedHz=1500000; carrierRequestedDeadNs=70;
 cfg.calLoadDutyX10[1]=432; cfg.calLoadTargetW[1]=30; settingsDirty=true;
 saveSettingsNow();
 expect(!settingsDirty && settingsSequence==9 && activeSlotIndex==2,"New wrapper append failed");
 expect(erases==0 && programs==122,"Migration erased or wrong record length");
 expect(std::memcmp(flashBytes.data(),legacyBefore.data(),2*LEGACY_SETTINGS_RECORD_BYTES)==0,"Migration overwrote legacy records");
 auto saved=cfg; loadDoesNotWrite();
 expect(std::memcmp(&cfg,&saved,sizeof(cfg))==0 && carrierRequestedHz==1500000 && carrierRequestedDeadNs==70,
  "Calibration and timing did not reboot as a coherent pair");

 reset(); putLegacy(0,legacyFixture(20,26)); putWrapper(2,wrapperFixture(20,31)); loadDoesNotWrite();
 expect(cfg.voltageSetV==31 && carrierRequestedHz==1500000,"Equal sequence did not prefer versioned wrapper");
 putLegacy(1,legacyFixture(21,32)); loadDoesNotWrite();
 expect(cfg.voltageSetV==32 && carrierRequestedHz==1000000 && carrierRequestedDeadNs==40,
  "Newer legacy record did not win with default timing");
 putWrapper(3,wrapperFixture(22,33)); loadDoesNotWrite();
 expect(cfg.voltageSetV==33 && settingsSequence==22,"Newer wrapper not selected");

 // Bad outer integrity must not expose its valid inner legacy payload.
 reset(); putLegacy(0,legacyFixture(1,24)); auto corrupt=wrapperFixture(100,70);
 corrupt.checksum^=1; putWrapper(2,corrupt); loadDoesNotWrite();
 expect(cfg.voltageSetV==24 && settingsSequence==1,"Bad outer checksum fell back to inner legacy payload");
 expect(activeSlotIndex==2,"Corrupt record occupancy ignored");
 reset(); corrupt=wrapperFixture(100,70); corrupt.settings.calLoadDutyX10[0]^=1;
 corrupt.checksum=checksumCarrierRecord(corrupt); putWrapper(0,corrupt); loadDoesNotWrite();
 expect(settingsSequence==0 && cfg.voltageSetV==28,"Bad inner checksum accepted");
 reset(); corrupt=wrapperFixture(100,70,2000000,130); putWrapper(0,corrupt); loadDoesNotWrite();
 expect(settingsSequence==0 && carrierRequestedHz==1000000,"Unrepresentable stored timing accepted");
 reset(); corrupt=wrapperFixture(100,70,499999,40); putWrapper(0,corrupt); loadDoesNotWrite();
 expect(settingsSequence==0,"Out-of-range stored timing accepted");

 // A missing prefix cannot make the remaining programmed words reusable.
 reset(); flashBytes[slotAddress(4)+SETTINGS_RECORD_BYTES-1]=0;
 loadDoesNotWrite(); expect(activeSlotIndex==4,"Torn record tail occupancy ignored");
 saveSettingsNow(); expect(activeSlotIndex==5 && erases==0,"Append did not skip torn prefix block");
 reset(); flashBytes[slotAddress(1)+SETTINGS_RECORD_BYTES-1]=0;
 auto record=wrapperFixture(1,30);
 expect(!eepromWriteBytes(slotAddress(1),(const uint8_t *)&record,sizeof(record)) && programs==0 && erases==0,
  "Writer did not check entire candidate block");

 // Exercise each word-programming failure against the real writer and loader.
 // Previous committed calibration/timing must survive every interrupted append.
 for(int completedWords=0;completedWords<122;++completedWords) {
  reset(); putWrapper(0,wrapperFixture(5,28,1000000,40)); loadDoesNotWrite();
  cfg.voltageSetV=30; carrierRequestedHz=2000000; carrierRequestedDeadNs=120;
  failProgramAfter=completedWords; saveSettingsNow();
  expect(settingsDirty,"Interrupted append reported successful save");
  failProgramAfter=-1; loadDoesNotWrite();
  expect(settingsSequence==5 && cfg.voltageSetV==28 && carrierRequestedHz==1000000 && carrierRequestedDeadNs==40,
   "Torn append replaced committed settings/timing");
 }

 reset(); for(int slot=0;slot<EEPROM_SLOT_COUNT;++slot) putWrapper(slot,wrapperFixture(slot+1,28));
 loadDoesNotWrite(); expect(activeSlotIndex==EEPROM_SLOT_COUNT-1,"Full journal occupancy wrong");
 systemEnabled=true; cfg.voltageSetV=31; expect(!requestSettingsSave("test"),"ON save request reported success");
 expect(settingsDirty && erases==0 && programs==0,"ON save erased full journal");
 expect(activeSlotIndex==EEPROM_SLOT_COUNT-1,"Rejected save request moved journal cursor");
 systemEnabled=false; expect(requestSettingsSave("test"),"OFF wrap request failed");
 expect(!settingsDirty && activeSlotIndex==0 && erases==1,"OFF wrap save did not erase once and write slot zero");
 loadDoesNotWrite(); expect(settingsSequence==EEPROM_SLOT_COUNT+1,"Wrapped wrapper did not reboot");

 // A full legacy journal upgrades by the existing explicit OFF wrap erase.
 reset(); for(unsigned int slot=0;slot<SETTINGS_FLASH_BYTES/LEGACY_SETTINGS_RECORD_BYTES;++slot)
  putLegacy(slot,legacyFixture(slot+1,29));
 loadDoesNotWrite(); expect(activeSlotIndex==EEPROM_SLOT_COUNT-1,"Full legacy journal occupancy wrong");
 carrierRequestedHz=2000000; carrierRequestedDeadNs=120;
 expect(requestSettingsSave("legacy-upgrade"),"Full legacy migration save failed");
 expect(erases==1 && activeSlotIndex==0,"Full legacy upgrade erased outside explicit save or wrong slot");
 loadDoesNotWrite(); expect(cfg.calLoadDutyX10[0]==321 && cfg.calLoadGainWPerPct[0]==1.25f &&
  carrierRequestedHz==2000000 && carrierRequestedDeadNs==120,"Full legacy migration lost calibration/timing");

 reset(); corrupt=wrapperFixture(100,70); corrupt.reserved=0;
 corrupt.checksum=checksumCarrierRecord(corrupt); putWrapper(0,corrupt); loadDoesNotWrite();
 expect(settingsSequence==0,"Noncanonical wrapper reserved byte accepted");

 reset(); settingsStorageReady=false;
 expect(!eepromWriteBytes(0,(const uint8_t *)&record,sizeof(record)) && erases==0,"Unready storage wrote flash");
 settingsStorageReady=true; autoTuneRunning=true;
 expect(!eepromWriteBytes(0,(const uint8_t *)&record,sizeof(record)) && erases==0,"Autotune wrote flash");
 autoTuneRunning=false; webCalibrationRunning=true;
 expect(!eepromWriteBytes(0,(const uint8_t *)&record,sizeof(record)) && erases==0,"Calibration wrote flash");
 webCalibrationRunning=false; startupActive=true;
 expect(!eepromWriteBytes(0,(const uint8_t *)&record,sizeof(record)) && erases==0,"Startup wrote flash");
 std::cout << "PASS: production V2 flash journal; 471-byte legacy payload / 472-byte stride migration, 488-byte timing wrappers, coherent calibration/timing reboot, integrity and range rejection, torn occupancy, all 122 interrupted append word boundaries, OFF-only wrap and flash guards.\n";
}
'''

body = prefix + constants + "\n" + settings_type + region("CARRIER_STORAGE_TYPES") + legacy_stride + region("CARRIER_TIMING_MATH") + state
body += function("checksumSettings") + region("CARRIER_STORAGE_CHECKSUM")
body += function("safeToWriteEepromNow") + function("eepromReadBytes") + function("eepromWriteBytes") + function("slotAddress")
body += region("CARRIER_STORAGE_LOAD") + region("CARRIER_STORAGE_SAVE") + function("markSettingsDirty") + function("requestSettingsSave") + tests
compiler = os.environ.get("CXX") or shutil.which("g++") or shutil.which("clang++")
if not compiler:
    raise SystemExit("A native C++17 compiler (g++ or clang++) is required.")
with tempfile.TemporaryDirectory(prefix="carrier-storage-") as temporary:
    directory = Path(temporary)
    cpp = directory / "storage.cpp"
    cpp.write_text(body, encoding="utf-8")
    executable = directory / ("storage.exe" if os.name == "nt" else "storage")
    subprocess.run([compiler, "-std=c++17", "-Wall", "-Wextra", "-Werror", "-O2", str(cpp), "-o", str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
